"""
Django settings for aizo_backend project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import json
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# secret_file = os.path.join(BASE_DIR, 'secrets.json')
#
# with open(secret_file) as f:
#     secrets = json.loads(f.read())
#
#
# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = "Set the {} environment variable".format(setting)
#         raise ImproperlyConfigured(error_msg)


SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'account',
    'login',
    'storage',
    'media'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aizo_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'aizo_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# DB_INFO = secrets.get('DB')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STORAGE_INFO = secrets.get('STORAGE')
STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY')
STORAGE_AZURE_CONTAINER = os.getenv('STORAGE_AZURE_CONTAINER')
STORAGE_CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_CUSTOM_DOMAIN = f'{STORAGE_ACCOUNT_NAME}.blob.core.windows.net'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STORAGE_AZURE_CONTAINER}/'

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = False

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

REST_USE_JWT = True
