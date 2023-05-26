echo "Setting up..."
cd src
python manage.py migrate
clear
echo "Starting..."
python manage.py runserver 8055
