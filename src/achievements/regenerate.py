from collections import deque
import requests


def regenerate(urls):
    from .import regenerate_utils as rutils

    urls = deque(urls)

    def regenerate_():
        rutils.reset()
        while urls:
            regenerate_from_url(urls.pop())
        rutils.reindex()

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
            for level, level_dat in enumerate(achievement["levels"], start=1):
                trigger_dat = level_dat.get("trigger", {})
                trigger = rutils.new_trigger(
                    trigger_dat.get("name", "achieve.manual_assign"),
                    trigger_dat.get("value", -1),
                )
                name = level_dat.get("name", achievement["name"] + " " + str(level))
                level = level_dat.get("level", level)
                description = level_dat.get("description", achievement["description"].format(amount=trigger.value))
                phrase = level_dat.get("phrase", achievement["phrase"])
                image = level_dat.get("image", achievement["image"])
                
                rutils.new_achievement(
                    name=name,
                    level=level,
                    description=description,
                    phrase=phrase,
                    image=image,
                    trigger=trigger
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
