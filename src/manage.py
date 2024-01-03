#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import shutil
import sys
from customachivements import settings

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customachivements.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) > 1 and sys.argv[1] == "cas":
        match sys.argv[2]:
            case "init":
                if not os.path.exists("/config"):
                    os.mkdir("/config")
                print("Resetting config...")
                shutil.copyfile("/src/assets/config/config.yml", "/config/config.yml")
                print("Done")
            case "migrate":
                print("Migrating DB...")
                execute_from_command_line([ *sys.argv, "migrate" ])
                print("Done")
            case "createprofile":
                if len(sys.argv) > 3:
                    username = sys.argv[3]
                else:
                    username = input("Username: ")
                
                from achievements import regenerate
                regenerate.ensure_django()
                from achievements.models import User, UserProfile
                
                if not User.objects.filter(username=username).exists():
                    print("This user does not exist. Creating...")
                    password = input("Password: ")
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                else:
                    user = User.objects.get(username=username)
                UserProfile.objects.create(user=user).save()
                print("Profile created.")
            case "pull":
                print("Starting...")
                from achievements import regenerate
                regenerate.ensure_django()
                regenerate.regenerate(settings._CONFIG.get("achievement-lists", []))
                print("Finished.")
            case _:
                execute_from_command_line(sys.argv)
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
