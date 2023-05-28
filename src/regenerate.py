import regenerate_utils as rutils


def regenerate():
    date_backup = rutils.backup_dates()

    rutils.reset()

    rutils.achievements_from_list_templated(
        rutils.new_row("Python Pro"),
        [10, 50, 100, 200, 500, 1000],
        "You have opened %s Python files.",
        "file.python.open",
    )

    rutils.achievements_from_list_templated(
        rutils.new_row("VSCode Fan"),
        [10, 50, 100, 200, 500, 1000],
        "You have opened VSCode %s times.",
        "vscode.open",
    )

    # rutils.achievements_from_list_templated(
    #     rutils.new_row("HyperTyper"),
    #     [10, 50, 100, 200, 500, 1000],
    #     "You smashed the buttons on your keyboard %s times.",
    #     "type",
    # )

    rutils.reindex(date_backup)

if __name__ == "__main__":
    import os
    os.environ["DJANGO_SETTINGS_MODULE"] = "customachivements.settings"
    import django
    django.setup()
    regenerate()
