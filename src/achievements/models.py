from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Trigger(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField(default=0)

    def is_triggered(self, user):
        return user.statistics.filter(name=self.name).count() >= self.value

    def get_trigger(self):
        return StatisticEntry.get_nth_of(self.name, self.value)

    def __str__(self):
        return f"{self.name} >= {self.value}"


class Achievement(models.Model):
    description = models.CharField(max_length=500)
    phrase = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE)
    image = models.URLField(default="https://picsum.photos/200")

    def __str__(self):
        return f"{self.name} {self.level}"


class StatisticEntry(models.Model):
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    def get_nth_of(name, n):
        return StatisticEntry.objects.filter(name=name).order_by("timestamp")[n]

    def __str__(self):
        return f"{self.timestamp}"


class AchievementObsession(models.Model):
    trigger = models.ForeignKey(StatisticEntry, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    def get_phrase(self):
        return self.achievement.phrase.format(
            username=self.userprofile_set.first().user.username,
            amount=self.achievement.trigger.value,
        )

    def __str__(self):
        return f"{self.userprofile_set.first().user.username} {self.achievement.name} {self.achievement.level}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    statistics = models.ManyToManyField(StatisticEntry, blank=True)
    achievements = models.ManyToManyField(AchievementObsession, blank=True)

    def has_achievement(self, achievement: Achievement) -> bool:
        return self.achievements.filter(achievement=achievement).exists()

    def reindex_achievements(self, filter_query: models.Q = None):
        new_achievements = []
        for trigger in Trigger.objects.filter(*(f for f in (filter_query,) if f)):
            if not trigger.is_triggered(self):
                continue
            achievement = trigger.achievement_set.first()
            if self.has_achievement(achievement):
                continue
            obsession = AchievementObsession.objects.create(
                trigger=trigger.get_trigger(), achievement=achievement
            )

            obsession.save()
            self.achievements.add(obsession)
            self.save()
            new_achievements.append(achievement)
        return new_achievements

    def __str__(self):
        return f"{self.user.username}'s Profile"
