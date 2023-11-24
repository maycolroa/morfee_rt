"""
Django settings for morfee_rt_dev project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from os import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PRODUCT_STATUS = getenv("PRODUCT_STATUS", "False") == "True"
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b%xb#)n%)i)*qgeim!3929=7c#ipw#_h8q*cdp7vq&0$9iuc4@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '10.244.8.31', 'famisanar.morfee.com.co', 'dolphin-app-scewd.ondigitalocean.app', 'https://dolphin-app-scewd.ondigitalocean.app']

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'channels',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'morfee_rt_dev',
    'consulta',
    'autorizaciones',
    'contratos',
    'facturas',
    'incapacidades',
    'pagos',
    'proyecciones',
    'triangulos',
    'users',
    'lab',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'morfee_rt_dev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ASGI_APPLICATION = 'morfee_rt_dev.asgi.application'
# CHANNEL_LAYERS = {
#     'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}
# }

WSGI_APPLICATION = 'morfee_rt_dev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if PRODUCT_STATUS == False:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_morfee_rt',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_morfee_rt',
            'USER': 'doadmin',
            'PASSWORD': 'zcnkr6zdz2depana',
            'HOST': 'db-mysql-nyc3-80737-do-user-7990340-0.b.db.ondigitalocean.com',
            'PORT': '25060',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# CUSTOM_URI_MONGO = 'mongodb://localhost:27017/'
CUSTOM_URI_MONGO = 'mongodb+srv://carvi:ac2502412@sgsss.yv4ar.gcp.mongodb.net/morfeeweb?authSource=admin'
CUSTOM_DB_MONGO = 'morfee_lobster'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTH_USER_MODEL = 'users.UserMorfee'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

MODELS = BASE_DIR / 'modelos'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

if PRODUCT_STATUS == False:
    STATIC_URL = 'static/'
    STATICFILES_DIRS = [BASE_DIR / "static",]
    STATIC_ROOT = "/staticfiles/"
else:
    #Version actualizada
    AWS_ACCESS_KEY_ID = 'VDPJXJOCWLN4YLB7WLVG'
    AWS_SECRET_ACCESS_KEY = 'oCXyf0QEppqysauxt3mdRV03G4Cs3OSrkQLnPZeMuZk'
    AWS_STORAGE_BUCKET_NAME = 'almacenmorfee'
    AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', 'ACL': 'public-read'}
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = 'https://almacenmorfee.nyc3.digitaloceanspaces.com/'
    # AWS_LOCATION = 'reservas/static'
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/reservas/static/"

    STATICFILES_FOLDER = "reservas/static"
    MEDIAFILES_FOLDER = "reservas/media"

    STATICFILES_STORAGE = 'custom_storages.StaticFileStorage'
    DEFAULT_FILE_STORAGE = "custom_storages.MediaFileStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
