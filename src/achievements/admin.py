from django.contrib import admin

from .models import Achievement, AchievementRow, Trigger, AchievementObsession, UserProfile


admin.site.register(AchievementObsession)
admin.site.register(Trigger)
admin.site.register(Achievement)
admin.site.register(AchievementRow)
admin.site.register(UserProfile)
