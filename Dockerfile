FROM python:3
EXPOSE 8055
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY config /config
VOLUME /config
COPY src /src
WORKDIR /src
RUN python manage.py migrate
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
RUN python manage.py createsuperuser --noinput
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8055"]
