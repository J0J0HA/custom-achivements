import os
import shutil
import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

_CONFIG_PATH = BASE_DIR / ".." / "config" / "config.yml"

# if not os.path.exists(_CONFIG_PATH):
#     shutil.copyfile(BASE_DIR / "assets" / "config" / "config.yml", _CONFIG_PATH)

if os.path.exists(_CONFIG_PATH):
    with open(_CONFIG_PATH, "r", encoding="ascii") as file:
        _CONFIG = yaml.load(file, Loader=yaml.Loader)
else:
    _CONFIG = {}

_SETTINGS = _CONFIG.get("settings", {})

_INTERNALS = _CONFIG.get("internals", {})

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = _SETTINGS.get("secret-key", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _SETTINGS.get("debug", False)

if _SETTINGS.get("proxy-ssl", False):
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = _CONFIG.get("trusted-origins", [])
ALLOWED_HOSTS = _CONFIG.get("allowed-hosts", [])

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ()

# Application definition

INSTALLED_APPS = [
    "achievements.apps.AchievementsConfig",
    "daphne",
    "channels",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "customachivements.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "customachivements.wsgi.application"
ASGI_APPLICATION = "customachivements.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if (_DATABASE_TYPE := (_DATABASE := _CONFIG.get("database", {})).get("type", "sqlite3")) == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": (_DB_PATH := BASE_DIR / ".." / "config" / _DATABASE.get("file", "db.sqlite3")),
        }
    }
elif _DATABASE_TYPE == "postgresql":
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _DATABASE.get("ab", "custom_achievements"),
        "USER": _DATABASE.get("user", "custom_achievements_system"),
        "PASSWORD": _DATABASE.get("password", "cas2023"),
        "HOST": _DATABASE.get("host", "db"),
        "PORT": _DATABASE.get("port", 5432),
    }
}
else:
    raise NotImplementedError(f"Database of type {_DATABASE_TYPE} is not supported.")


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
