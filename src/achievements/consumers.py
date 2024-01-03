import json
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import UserProfile, AchievementObsession, Trigger, StatisticEntry
from .settings import PROTOCOL_VERSIONS_COMPATIBLE
from datetime import datetime

class StatsStreamConsumer(AsyncWebsocketConsumer):
    user: None | User
    profile: None | UserProfile
    connection_accepted: bool = False

    async def connect(self):
        await self.accept()
        
        if (
            self.scope["headers_dict"].get("protocol-version")
            not in PROTOCOL_VERSIONS_COMPATIBLE
        ):
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

        await self.send(text_data=json.dumps({"type": "accept_connection"}))

        if self.user.is_superuser:
            await self.send(json.dumps({"type": "notice", "topic": "superuser"}))

    async def disconnect(self, code):
        print("Disconnect", code)
        return code

    async def user_increase_stat(self, stat_name, timestamp, value):
        for _ in range(value):
            stat_entry = await StatisticEntry.objects.acreate(
                name = stat_name,
                timestamp = datetime.fromtimestamp(timestamp/1000),
            )
            await stat_entry.asave()
            await self.profile.statistics.aadd(
                stat_entry
            )
        await self.profile.asave()

    async def receive(self, text_data):
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
            await self.user_increase_stat(pat, meta["timestamp"], value)
            filter_query |= Q(name=pat)

        new_achievements = await database_sync_to_async(self.profile.reindex_achievements)(filter_query)
        for achievement in new_achievements:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "new_achievement",
                        "name": achievement.name,
                        "level": achievement.level,
                        "description": achievement.description,
                        "image_url": achievement.image,
                    }
                )
            )
