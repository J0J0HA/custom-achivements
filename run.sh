echo "Setting up..."
cd src
python manage.py makemigrations achievements
python manage.py migrate
echo "Starting..."
python manage.py runserver 8055
