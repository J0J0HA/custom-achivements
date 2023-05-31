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


def reindex():
    for achievement in Achievement.objects.all():
        for user in UserProfile.objects.all():
            if not achievement.trigger.is_triggered(user):
                continue
            print(f"Adding Achievement '{achievement}' to {user}...")
            date = achievement.trigger.get_date(user)
            obsession = AchievementObsession.objects.create(
                date=date,
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


def new_achievement(row, level, description, phrase, trigger):
    print("Adding Achievement", row, level, description, phrase, trigger)
    achievement = Achievement.objects.create(
        row=row, level=level, description=description, phrase=phrase, trigger=trigger
    )
    achievement.save()
    return achievement


# def achievements_from_list_manual(row, map):
#     for index, item in enumerate(map):
#         new_achievement(row=row, level=index, description=map[0], trigger=map[1])


# def achievements_from_list_templated(row, nums, description, trigger_name):
#     for index, num in enumerate(nums):
#         new_achievement(
#             row=row,
#             level=index + 1,
#             description=description % num,
#             trigger=new_trigger(trigger_name, num),
#         )
