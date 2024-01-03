import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import UserProfile
from .regenerate import regenerate as regenach
from . import settings

User = get_user_model()


achievement_orders = {
    "trigger__timestamp": (
        "-trigger__timestamp",
        "achievement__name",
        "achievement__level",
    ),
    "name": (
        "achievement__name",
        "achievement__level",
        "trigger__timestamp",
    ),
    "level": (
        "achievement__level",
        "trigger__timestamp",
        "achievement__name",
    ),
    "-trigger__timestamp": (
        "trigger__timestamp",
        "achievement__name",
        "achievement__level",
    ),
    "-name": (
        "-achievement__name",
        "achievement__level",
        "trigger__timestamp",
    ),
    "-level": (
        "-achievement__level",
        "trigger__timestamp",
        "achievement__name",
    ),
}


def get_stats(request, username, self):
    requested_order = request.GET.get("order", "trigger__timestamp")
    selected_order = achievement_orders.get(requested_order, "trigger__timestamp")
    profile = get_object_or_404(UserProfile, user__username=username)
    achievements = profile.achievements.all().order_by(*selected_order)
    statistics = {}
    if self:
        for entry in profile.statistics.all():
            if not entry.name in statistics:
                statistics[entry.name] = []
            statistics[entry.name].append(entry.timestamp.timestamp())
    else:
        for entry in profile.statistics.all():
            if not entry.name in statistics:
                statistics[entry.name] = 0
            statistics[entry.name] += 1
    return achievements, statistics


def render_stats(request, username, self):
    achievements, stats = get_stats(request, username, self)
    return render(
        request,
        "achievement/index.html",
        {"username": username, "achievements": achievements, "stats": stats},
    )


def json_stats(request, username, self):
    achievements, stats = get_stats(request, username, self)

    return HttpResponse(
        json.dumps(
            {
                "username": username,
                "achievements": [
                    {
                        "name": achievement.achievement.name,
                        "level": achievement.achievement.level,
                        "description": achievement.achievement.description,
                        "phrase": achievement.get_phrase(),
                        "user_count": achievement.achievement.achievementobsession_set.count(),
                    }
                    for achievement in achievements
                ],
                "stats": stats,
            }
        ),
        content_type="application/json",
    )


@login_required(login_url="/login")
def index(request):
    return render_stats(request, request.user.username, True)


@login_required(login_url="/login")
def index_api(request):
    return json_stats(request, request.user.username, True)


@login_required(login_url="/login")
def regenerate(request):
    regenach(settings._CONFIG.get("achievement-lists", []))
    return HttpResponse("Done")


def user(request, username):
    return render_stats(request, username, False)


def user_api(request, username):
    return json_stats(request, username, False)
