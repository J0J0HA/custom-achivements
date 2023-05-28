FROM python:3
EXPOSE 80
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
VOLUME /config
COPY src /src
WORKDIR /src
CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]
