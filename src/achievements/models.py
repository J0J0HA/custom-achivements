from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class AchievementRow(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Trigger(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField(default=0)

    def is_triggered(self, user):
        return len(user.stats.get(self.name, [])) >= self.value

    def get_date(self, user):
        timestamp = user.stats.get(self.name, [])[self.value - 1].get("timestamp", 0)
        return datetime.utcfromtimestamp(timestamp / 1000)

    def __str__(self):
        return f"{self.name} >= {self.value}"


class Achievement(models.Model):
    row = models.ForeignKey(AchievementRow, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    phrase = models.CharField(max_length=500)
    level = models.IntegerField(default=1)
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.row.name} {self.level}"


class AchievementObsession(models.Model):
    date = models.DateTimeField(default=timezone.now)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    def get_phrase(self):
        return self.achievement.phrase.format(
            username=self.userprofile_set.first().user.username,
            amount=self.achievement.trigger.value,
        )

    def __str__(self):
        return f"[{self.date}] {self.achievement.row}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stats = models.JSONField(null=True, blank=True, default=dict)
    achievements = models.ManyToManyField(AchievementObsession, blank=True)

    def has_achievement(self, achievement):
        return achievement in [x.achievement for x in self.achievements.all()]

    def __str__(self):
        return f"{self.user.username}'s Profile"
