import json

from channels.generic.websocket import WebsocketConsumer

from django.contrib.auth import get_user_model
from .models import UserProfile, AchievementObsession, Trigger


class StatsStreamConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.accept()

    def disconnect(self, code):
        ...

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
        stat_name = stat_data["stat_name"]
        user = UserProfile.objects.get(user__username=self.username)
        if stat_name not in user.stats:
            user.stats[stat_name] = 1
            user.save()
        else:
            user.stats[stat_name] += 1
            user.save()

        for trigger in Trigger.objects.filter(name=stat_name):
            print(trigger, dir(trigger))
            if not trigger.is_triggered(user):
                continue
            for achievement in trigger.achievement_set.all():
                if user.has_achievement(achievement):
                    continue
                obsession = AchievementObsession.objects.create(achievement=achievement)
                obsession.save()
                user.achievements.add(obsession)
                user.save()
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
