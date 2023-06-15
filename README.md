# custom-achievements-server

[![Docker Image CI](https://github.com/J0J0HA/custom-achievements-server/actions/workflows/docker-image.yml/badge.svg?branch=master)](https://github.com/J0J0HA/custom-achievements-server/actions/workflows/docker-image.yml)
[![CodeQL](https://github.com/J0J0HA/custom-achievements-server/actions/workflows/codeql.yml/badge.svg)](https://github.com/J0J0HA/custom-achievements-server/actions/workflows/codeql.yml)

Readmes are overrated, at least if you know how the program works.

## Install

You need to clone the repo first.

### Manual

#### Linux

Install:

```bash
pip install -r requirements.txt
```

Run:
```bash
python src/manage.py runserver 0.0.0.0:8055
```

#### Windows

Install:

```bash
pip install -r requirements.txt
```

Run:
```bash
python src\manage.py runserver 0.0.0.0:8055
```

### Docker

#### Image

Download with:

```bash
docker pull jojojux/custom-achievements-server:latest
```

Install with:

```bash
docker run -d -p 8055:8055 --name achievement-server jojojux/custom-achievements-server
```

#### Compose

Run with:
```bash
docker compose up
```

Own compose example:
```bash
version: '3'
services:
  server:
    image: jojojux/custom-achievements-server:latest
    networks:
      - server
    ports:
      - "8055:80"
    volumes:
      - config:/config
    environment:
      DJANGO_SUPERUSER_USERNAME: admin
      DJANGO_SUPERUSER_PASSWORD: admin
      DJANGO_SUPERUSER_EMAIL: admin@example.com

networks:
  server:
    driver: bridge
```
