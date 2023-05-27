from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class AchievementRow(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Trigger(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField(default=0)

    def is_triggered(self, user):
        return user.stats.get(self.name, 0) >= self.value

    def __str__(self):
        return f"{self.name} >= {self.value}"


class Achievement(models.Model):
    row = models.ForeignKey(AchievementRow, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    level = models.IntegerField(default=1)
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.row.name} {self.level}"


class AchievementObsession(models.Model):
    date = models.DateTimeField(default=datetime.now)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"[{self.date}] {self.achievement.row}"
        )


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stats = models.JSONField(null=True, blank=True, default=dict)
    achievements = models.ManyToManyField(AchievementObsession, blank=True)

    def has_achievement(self, achievement):
        return achievement in [x.achievement for x in self.achievements.all()]

    def __str__(self):
        return f"{self.user.username}'s Profile"
