from django.db.models import Q
import json
import datetime
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from .models import UserProfile, AchievementObsession, Trigger


class StatsStreamConsumer(WebsocketConsumer):
    def connect(self):
        username = self.scope["url_route"]["kwargs"]["username"]
        self.accept()

        try:
            self.user = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            self.send(
                text_data=json.dumps(
                    {
                        "type": "error_report",
                        "error": "unknown_user",
                        "description": f"The user {username} is unknown.",
                    }
                )
            )
            self.disconnect()

        if username == "admin":
            self.send(json.dumps({"type": "notice_superuser"}))

    def disconnect(self, code):
        ...

    def user_inecrease_stat(self, stat_name, meta, value):
        if stat_name not in self.user.stats:
            self.user.stats[stat_name] = [meta for _ in range(value)]
            self.user.save()
        else:
            self.user.stats[stat_name] += [meta for _ in range(value)]
            self.user.save()

    def receive(self, text_data):
        stat_data = json.loads(text_data)
        msg_type = stat_data["type"]
        if msg_type != "stats_update":
            self.send(
                text_data=json.dumps(
                    {
                        "type": "error_report",
                        "error": "unknown_type",
                        "description": f"The type {msg_type} is unknown.",
                    }
                )
            )
            return
        stat_name = stat_data["name"]
        value = stat_data["count"]
        meta = stat_data["meta"]
        if "timestamp" not in meta:
            self.send(
                text_data=json.dumps(
                    {
                        "type": "error_report",
                        "error": "missing_timestamp",
                        "description": f"The 'timestamp' filed in 'meta' is missing.",
                    }
                )
            )
            return

        filter_query = Q()
        parts = stat_name.split(".")
        for part in range(len(parts)):
            pat = ".".join(parts[: part + 1])
            self.user_inecrease_stat(pat, meta, value)
            filter_query |= Q(name=pat)

        for trigger in Trigger.objects.filter(filter_query):
            if not trigger.is_triggered(self.user):
                continue
            for achievement in trigger.achievement_set.all():
                if self.user.has_achievement(achievement):
                    continue
                obsession = AchievementObsession.objects.create(date = trigger.get_date(self.user), achievement=achievement)
                obsession.save()
                self.user.achievements.add(obsession)
                self.user.save()
                self.send(
                    text_data=json.dumps(
                        {
                            "type": "new_achievement",
                            "name": achievement.row.name,
                            "level": achievement.level,
                            "description": achievement.description,
                            "image_url": "https://picsum.photos/200",
                        }
                    )
                )
        # achievements_changed = Achievement.objects.filter(trigger=stat, trigger_value__lte=user.stats[stat_name])
        # for achievement in achievements_changed:
        #     if achievement in [a.achievement for a in user.achievements.all()]:
        #         continue
        #     obsession = AchievementObsession.objects.create(achievement=achievement)
        #     obsession.save()
        #     user.achievements.add(obsession)
        #     self.send(
        #         text_data=json.dumps(
        #             {
        #                 "type": "new_achievement",
        #                 "name": achievement.row.name,
        #                 "level": achievement.level,
        #                 "description": achievement.description,
        #                 "image_url": "https://picsum.photos/200",
        #             }
        #         )
        #     )
