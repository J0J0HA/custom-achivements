@echo off
setx PYTHONDONTWRITEBYTECODE 1
setx PYTHONUNBUFFERED 1
python -m pip install -r requirements.txt
python src\manage.py makemigrations achievements
python src\manage.py migrate
python src\regenerate.py
echo Please create a Superuser:
python src\manage.py createsuperuser
