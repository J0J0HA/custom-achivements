import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import AchievementObsession


User = get_user_model()


achievement_orders = {
    "date": (
        "-date",
        "achievement__row__name",
        "achievement__level",
    ),
    "name": (
        "achievement__row__name",
        "achievement__level",
        "date",
    ),
    "level": (
        "achievement__level",
        "date",
        "achievement__row__name",
    ),
    "-date": (
        "date",
        "achievement__row__name",
        "achievement__level",
    ),
    "-name": (
        "-achievement__row__name",
        "achievement__level",
        "date",
    ),
    "-level": (
        "-achievement__level",
        "date",
        "achievement__row__name",
    ),
}

def get_stats(request, username):
    requested_order = request.GET.get("order", "date")
    selected_order = achievement_orders.get(requested_order, "date")
    achievements = AchievementObsession.objects.filter(
        user__exact=get_object_or_404(User, username=username)
    ).order_by(*selected_order)
    return achievements

def render_stats(request, username):
    achievements = get_stats(request, username)
    return render(
        request,
        "achievement/index.html",
        {"username": username, "achievements": achievements},
    )
    
def json_stats(request, username):
    achievements = get_stats(request, username)
    return HttpResponse(json.dumps({
        "username": username,
        "achievements": [
            {
                "name": achievement.achievement.row.name,
                "level": achievement.achievement.level,
                "description": achievement.achievement.description,
                "user_count": achievement.achievement.achievementobsession_set.count(),
            } for achievement in achievements
        ]
    }), content_type="application/json")

@login_required(login_url="/login")
def index(request):
    return render_stats(request, request.user.username)


def user(request, username):
    return render_stats(request, username)


def user_api(request, username):
    return json_stats(request, username)
