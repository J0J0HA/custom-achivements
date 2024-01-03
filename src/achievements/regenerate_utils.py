from achievements.models import (
    Achievement,
    AchievementObsession,
    Trigger,
    UserProfile
)


def reset():
    Trigger.objects.all().delete()
    Achievement.objects.all().delete()
    AchievementObsession.objects.all().delete()


def reindex():
    for user in UserProfile.objects.all():
        user.reindex_achievements()


def new_trigger(name, value):
    print("Adding Trigger", name, value)
    trigger = Trigger.objects.create(name=name, value=value)
    trigger.save()
    return trigger

def new_achievement(name, level, description, phrase, image, trigger):
    print("Adding Achievement", name, description, phrase, trigger)
    achievement = Achievement.objects.create(
        name=name, level=level, description=description, phrase=phrase, trigger=trigger, image=image
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
