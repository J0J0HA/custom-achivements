FROM python:3.11-slim-bullseye
EXPOSE 80
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
VOLUME /config
COPY src /src
WORKDIR /src
RUN chmod +x bin/pull && chmod +x bin/init && chmod +x bin/manage && chmod +x bin/createprofile && chmod +x bin/migrate && chmod +x bin/createsuperuser
ENV PATH="/src/bin:$PATH"
CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]
