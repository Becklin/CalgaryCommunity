import dj_database_url
from pathlib import Path
import environ
import os

# Initialize environment variables
env = environ.Env()

ENV_FILE = ".env.prod" if os.getenv("DJANGO_ENV") == "production" else ".env.dev"
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, ENV_FILE))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env.read_env(os.path.join(BASE_DIR, ".env"))


SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

import os, platform

# GDAL / GEOS libraries: only needed locally on Windows/Mac
GDAL_LIBRARY_PATH = os.getenv("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.getenv("GEOS_LIBRARY_PATH")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    # 3rd part apps
    "django_cleanup.apps.CleanupConfig",
    "rest_framework",
    "rest_framework_gis",
    "clearcache",
    # Local apps
    "backend.apps.BackendConfig",  # in apps.py
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
print("DEBUG = ", DEBUG)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS = ["*"]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://calgary-community-frontend-lin-becks-projects.vercel.app",
        "http://localhost:3000",
    ]
    ALLOWED_HOSTS = ["calcommunity.onrender.com"]

ROOT_URLCONF = "calCrimes.urls"

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

WSGI_APPLICATION = "calCrimes.wsgi.application"


if os.getenv("DJANGO_ENV") == "production":
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600, default=os.getenv("DATABASE_URL")
        )
    }
else:
    DATABASES = {
        "default": {
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_URL = "/static/"
if os.getenv("DJANGO_ENV") == "development":
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    ## python manage.py collectstatic
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
