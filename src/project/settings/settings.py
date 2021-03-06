"""
Django settings for webAutomateTesting project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('APP_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'visual-browser-test.com',
    'localhost',
    '127.0.0.1',
    '165.227.76.119'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',

    'src.project.apps.clarifaiApi',
    'src.project.apps.screenshot',
    'src.project.apps.accounts',
    'src.project.apps.automatetest'
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

ROOT_URLCONF = 'src.project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'project/templates')
        ],
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

WSGI_APPLICATION = 'src.project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('WEB_AUTO_TEST_DB_NAME'),
        'USER': config('WEB_AUTO_TEST_DB_USER'),
        'PASSWORD': config('WEB_AUTO_TEST_DB_PASS'),
        'HOST':config('WEB_AUTO_TEST_DB_HOST'),
        'PORT': config('WEB_AUTO_TEST_DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'project/media/upload/')
# MEDIA_URL = '/media/'

AWS_S3_USER = config('AWS_S3_USER')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'project/static'),

]

# Static AWS S3
AWS_STATIC_LOCATION = 'static'

STATIC_URL = 'https://{0}/{1}/'.format(AWS_S3_DOMAIN, AWS_STATIC_LOCATION)
STATICFILES_STORAGE = 'src.project.settings.storage_backend.StaticStorage'

AWS_MEDIA_LOCATION = 'media'
MEDIA_URL = 'https://{0}/{1}/'.format(AWS_S3_DOMAIN, AWS_MEDIA_LOCATION)
DEFAULT_FILE_STORAGE = 'src.project.settings.storage_backend.MediaStorage'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

BS_API_USER = config('BS_API_USER')
BS_API_KEY = config('BS_API_KEY')
BS_API_HUB_URL = 'http://{0}:{1}@hub.browserstack.com:80/wd/hub'.format(BS_API_USER, BS_API_KEY)

GALEN_REPORT_DIR = os.path.join(BASE_DIR, 'project/reports/')
AWS_GALEN_REPORT_LOCATION = 'reports'
REPORT_BASE_URL = 'https://{0}/{1}/'.format(AWS_S3_DOMAIN, AWS_GALEN_REPORT_LOCATION)

SPEC_FILE_LOCATION = 'specfiles'
SPEC_FILE_URL = 'https://{0}/{1}/'.format(AWS_S3_DOMAIN, SPEC_FILE_LOCATION)
