"""Django's command-line utility for administrative tasks."""
import os
import sys
import yaml
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
    if not os.path.exists(settings._DB_PATH):
        execute_from_command_line( [ sys.argv[0], "makemigrations", "achievements" ] )
        execute_from_command_line( [ sys.argv[0], "migrate" ] )
    import regenerate
    regenerate.ensure_django()
    regenerate.regenerate(settings._CONFIG.get("achievement-lists", []))
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
