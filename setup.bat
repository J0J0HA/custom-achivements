@echo off
cls
setx PYTHONDONTWRITEBYTECODE 1
setx PYTHONUNBUFFERED 1
python -m pip install -r requirements.txt
python src\manage.py migrate
cls
echo Please create a Superuser:
python src\manage.py createsuperuser

echo python src\manage.py runserver 0.0.0.0:8055 > "run.bat"
