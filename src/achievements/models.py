from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AchievementRow(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"


class Achievement(models.Model):
    row = models.ForeignKey(AchievementRow, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    level = models.IntegerField()

    def __str__(self):
        return f"{self.row.name} lvl {self.level}"


class AchievementObsession(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user.username}'s {self.achievement}"
