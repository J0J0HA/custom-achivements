import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import UserProfile


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
    profile = get_object_or_404(UserProfile, user__username=username)
    achievements = profile.achievements.order_by(*selected_order)
    return achievements, profile.stats


def render_stats(request, username):
    achievements, stats = get_stats(request, username)
    return render(
        request,
        "achievement/index.html",
        {"username": username, "achievements": achievements, "stats": stats},
    )


def json_stats(request, username):
    achievements, stats = get_stats(request, username)
    return HttpResponse(
        json.dumps(
            {
                "username": username,
                "achievements": [
                    {
                        "name": achievement.achievement.row.name,
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


def index(request):
    if User.objects.all().count() == 0:
        superuser = User.objects.create_superuser(username="admin", password="admin")
        UserProfile.objects.create(user=superuser).save()
        return HttpResponse(
            "<h1>First user!</h1><p>You can now login as 'admin' with password 'admin'.<br>Please consider to change your password!</p><a href='?'>Reload to start.</a>"
        )

    @login_required(login_url="/login")
    def index_handler(request):
        return render_stats(request, request.user.username)

    return index_handler(request)


@login_required(login_url="/login")
def index_api(request):
    return json_stats(request, request.user.username)


def user(request, username):
    return render_stats(request, username)


def user_api(request, username):
    return json_stats(request, username)
