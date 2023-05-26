from django.contrib import admin

from .models import Achievement, AchievementRow, AchievementObsession


admin.site.register(Achievement)
admin.site.register(AchievementRow)
admin.site.register(AchievementObsession)
