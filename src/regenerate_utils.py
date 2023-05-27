import os, django, manage, json

os.environ["DJANGO_SETTINGS_MODULE"] = "customachivements.settings"

django.setup()

from achievements.models import (
    AchievementRow,
    Achievement,
    Trigger,
    UserProfile,
    AchievementObsession,
)


def reset():
    AchievementRow.objects.all().delete()
    Achievement.objects.all().delete()
    Trigger.objects.all().delete()


def backup_dates():
    date_backup = {}
    for user in UserProfile.objects.all():
        for achievement in user.achievements.all():
            date_backup[
                user.user.username
                + "$"
                + achievement.achievement.row.name
                + "$"
                + str(achievement.achievement.level)
            ] = achievement.date
    return date_backup


def reindex(date_backup):
    for achievement in Achievement.objects.all():
        for user in UserProfile.objects.all():
            if not achievement.trigger.is_triggered(user):
                continue
            print(f"Adding Achievement '{achievement}' to {user}...")
            print(date_backup.get(
                user.user.username
                + "$"
                + achievement.row.name
                + "$"
                + str(achievement.level),
                0,
            ))
            obsession = AchievementObsession.objects.create(
                date=date_backup.get(
                    user.user.username
                    + "$"
                    + achievement.row.name
                    + "$"
                    + str(achievement.level),
                    0,
                ),
                achievement=achievement,
            )
            obsession.save()
            user.achievements.add(obsession)
            user.save()


def new_trigger(name, value):
    print("Adding Trigger", name, value)
    trigger = Trigger.objects.create(name=name, value=value)
    trigger.save()
    return trigger


def new_row(name):
    print("Adding Row", name)
    row = AchievementRow.objects.create(name=name)
    row.save()
    return row


def new_achievement(row, level, description, trigger):
    print("Adding Achievement", row, level, description, trigger)
    achievement = Achievement.objects.create(
        row=row, level=level, description=description, trigger=trigger
    )
    achievement.save()
    return achievement


def achievements_from_list_manual(row, map):
    for index, item in enumerate(map):
        new_achievement(row=row, level=index, description=map[0], trigger=map[1])


def achievements_from_list_templated(row, nums, description, trigger_name):
    for index, num in enumerate(nums):
        new_achievement(
            row=row,
            level=index + 1,
            description=description % num,
            trigger=new_trigger(trigger_name, num),
        )