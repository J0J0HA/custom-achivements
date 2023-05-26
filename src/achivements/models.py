from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Achivement(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    level = models.IntegerField()
    users = models.ManyToManyField(User)
    

    def __str__(self):
        return f"'{self.name}' level {self.level}"
