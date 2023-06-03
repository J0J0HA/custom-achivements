import json
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import UserProfile, AchievementObsession, Trigger
from .settings import PROTOCOL_VERSIONS_COMPATIBLE


class StatsStreamConsumer(AsyncWebsocketConsumer):
    user: None | User
    profile: None | UserProfile
    connection_accepted: bool = False

    async def connect(self):
        print(self.scope["headers_dict"])

        await self.accept()

        if (
            self.scope["headers_dict"].get("protocol-version")
            not in PROTOCOL_VERSIONS_COMPATIBLE
        ):
            print(self.scope["headers_dict"].get("protocol-version"), PROTOCOL_VERSIONS_COMPATIBLE)
            await self.close(4101)
            return

        if "auth-password" not in self.scope["headers_dict"]:
            await self.close(4201)
            return

        username = self.scope["url_route"]["kwargs"]["username"]
        self.user = await database_sync_to_async(authenticate)(
            username=username, password=self.scope["headers_dict"].get("auth-password")
        )

        if self.user is None:
            await self.close(4202)
            return

        if self.user.is_anonymous:
            await self.close(4202)
            return

        try:
            self.profile = await UserProfile.objects.aget(user__username=username)
        except UserProfile.DoesNotExist:
            await self.close(4401)
            return


        self.connection_accepted = True
        
        await self.send(
                text_data=json.dumps(
                    {
                        "type": "accept_connection"
                    }
                )
            )

        if self.user.is_superuser:
            await self.send(json.dumps({"type": "notice", "topic": "superuser"}))
            
    
    async def disconnect(self, code):
        print("Disconnect", code)
        return code

    async def user_inecrease_stat(self, stat_name, meta, value):
        if stat_name not in self.profile.stats:
            self.profile.stats[stat_name] = [meta for _ in range(value)]
        else:
            self.profile.stats[stat_name] += [meta for _ in range(value)]
        await database_sync_to_async(self.profile.save)()

    async def receive(self, text_data):
        print(text_data, self.connection_accepted)
        if not self.connection_accepted:
            await self.close(4103)
        
        stat_data = json.loads(text_data)
        msg_type = stat_data["type"]
        if msg_type != "stats_update":
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
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
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error_report",
                        "error": "missing_timestamp",
                        "description": "The 'timestamp' filed in 'meta' is missing.",
                    }
                )
            )

        filter_query = Q()
        parts = stat_name.split(".")
        for part in range(len(parts)):
            pat = ".".join(parts[: part + 1])
            await self.user_inecrease_stat(pat, meta, value)
            filter_query |= Q(name=pat)

        async for trigger in Trigger.objects.filter(filter_query):
            if not trigger.is_triggered(self.profile):
                continue
            async for achievement in trigger.achievement_set.all():
                if await database_sync_to_async(self.profile.has_achievement)(
                    achievement
                ):
                    continue
                obsession = await AchievementObsession.objects.acreate(
                    date=trigger.get_date(self.profile), achievement=achievement
                )
                await obsession.asave()
                await self.profile.achievements.aadd(obsession)
                await self.profile.asave()
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "new_achievement",
                            "name": (
                                await database_sync_to_async(
                                    lambda achievement: achievement.row
                                )(achievement)
                            ).name,
                            "level": achievement.level,
                            "description": achievement.description,
                            "image_url": "https://picsum.photos/200",
                        }
                    )
                )
