from collections import deque
import requests
import time


def regenerate(urls):
    import regenerate_utils as rutils

    urls = deque(urls)

    def regenerate_():
        date_backup = rutils.backup_dates()
        rutils.reset()
        while urls:
            regenerate_from_url(urls.pop())
        rutils.reindex(date_backup)

    def regenerate_from_url(url):
        print("Getting achievements from: ", url)
        try:
            json = requests.get(
                url, timeout=30, headers={"Cache-Control": "no-cache"}
            ).json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return
        achievements = json.get("achievements", [])
        for achievement in achievements:
            row = rutils.new_row(achievement.get("name", "Unknown"))
            for level, level_dat in enumerate(achievement.get("levels", []), start=1):
                trigger_dat = level_dat.get("trigger", {})
                trigger = rutils.new_trigger(
                    trigger_dat.get("name", "achieve.manual_assign"),
                    trigger_dat.get("value", -1),
                )
                rutils.new_achievement(
                    row,
                    level,
                    level_dat.get(
                        "description",
                        achievement.get(
                            "description", "No description provided."
                        ).format(amount=trigger_dat.get("value", -1)),
                    ),
                    level_dat.get(
                        "phrase",
                        achievement.get(
                            "phrase", "No phrase provided."
                        ),
                    ),
                    trigger,
                )
        includes = json.get("include", [])
        for include in includes:
            urls.append(include)

    return regenerate_()


def ensure_django():
    import os

    os.environ["DJANGO_SETTINGS_MODULE"] = "customachivements.settings"
    import django

    django.setup()


if __name__ == "__main__":
    ensure_django()
    regenerate()
