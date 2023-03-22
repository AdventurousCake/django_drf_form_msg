"""
Django settings for django1 project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from sys import platform

from environs import Env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

env = Env()
env.read_env(path=os.path.join(BASE_DIR, '.env'))

# SYSTEM CHECK; HARDCODED!
RUN_OS = platform
if platform == 'linux':
    IS_SERVER = True
else:
    IS_SERVER = False

# also for drf
# UPD DB AFTER KEY
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_HOSTS.extend(env.list("ALLOWED_HOSTS"))

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")  # in dj 3.x without https

ADMIN_PATH = env.str('ADMIN_PATH') or 'admin'
API_PATH = env.str('API_PATH') or 'api/v1/'

# debug tools ip
INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sorl.thumbnail',
    'rest_framework',
    'corsheaders',
    'django_filters',  # api filters
    'rest_framework.authtoken',
    # "debug_toolbar",  # debug tools
    'social_django',
    # 'request',  # save all requests; also in middleware
    'rest_framework_simplejwt',

    'core',
    'api',
    'FORM_MSG'

]

MIDDLEWARE = [
    # debug tools
    # "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'request.middleware.RequestMiddleware',

]

ROOT_URLCONF = 'django1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'django1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default':
#         {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': 'postgres',
#             'USER': 'postgres',
#             'PASSWORD': 'postgres',
#             'HOST': 'localhost',
#             'PORT': '5432',
#         }
# }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',

    'django.contrib.auth.backends.ModelBackend',  # also SAVE default method! dont delete
)

SOCIAL_AUTH_GITHUB_KEY = env.str('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = env.str('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_JSONFIELD_ENABLED = True  # jsonb field for pgsql

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
# LOGIN_REDIRECT_URL = '/'

from django.urls import reverse_lazy

# check
ABSOLUTE_URL_OVERRIDES = {'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])}
THUMBNAIL_DEBUG = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CART_SESSION_ID = 'cart_1'
# """Это ключ, по которому мы будем хранить данные корзины в сессии.
# Так как сессии Django ассоциируются с конкретным посетителем сайта,
# мы можем использовать один и тот же ключ для разных пользователей.
# Это не приведет к конфликту данных."""

# jwt settings
# SIMPLE_JWT = {} # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
# DEFAULT 5 MIN TOKEN LIFETIME


# rest api
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',

        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',

        # 'rest_framework.throttling.UserRateThrottle',
        # 'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '10000/day',  # лимит для UserRateThrottle
        'anon': '1000/day',  # лимит для AnonRateThrottle
        'low_request': '5/minute',
    },
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

# django request
# REQUEST_BASE_URL = ''