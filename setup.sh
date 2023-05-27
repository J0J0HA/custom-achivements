export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
python -m pip install -r requirements.txt
python src/manage.py makemigrations achievements
python manage.py migrate
python src/regenerate.py
echo "Please create a Superuser:"
python manage.py createsuperuser
