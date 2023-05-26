clear
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
python -m pip install -r requirements.txt
python manage.py migrate
echo "Please create a Superuser:"
python manage.py createsuperuser
echo "python manage.py runserver 0.0.0.0:8055" > "run.sh"
