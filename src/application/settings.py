"""
Django settings for application project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*&4v3$o4ykt-x5zm+er0^am3qky+wgt!n((_j5k+%sd_lvju7x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
API_HOSTS = ['api.shop-survey.ru', 'localhost:8000', ]
MAPS_HOSTS = ['map.shop-survey.ru', ]


# Application definition

INSTALLED_APPS = [

    'compressor',
    'dal',
    'dal_select2',
    'import_export',
    'django_admin_multiple_choice_list_filter',

    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',

    'cache_model',
    'preferences',
    'public_model',
    'sort_model',

    'application.survey',
    'application.solar_staff',
    'application.solar_staff_accounts',
    'application.telegram',
    'application.profi',
    'application.users',
    'application.agent',
    'application.inspector',
    'application.dump',
    'application.loyalty',
    'application.archive',
    'application.mobile',
    'application.iceman',
    'application.ai',
    'application.supervisor',
    'application.iceman_imports',

    'rest_framework',
    'rest_framework.authtoken'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'application.survey.middleware.MultipleDomainMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',                
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'shop_survey',
        'USER':     'postgres',
        'PASSWORD': 'postgres',
        'HOST':     'localhost',
        'PORT':     '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = False
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

#if not DEBUG:
#MEDIA_ROOT = '/mnt/HC_Volume_6378924/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

# else:
#     MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
DOWNLOAD_PATH = os.path.join(MEDIA_ROOT, 'downloads')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'


# Admin tools settings
ADMIN_TOOLS_INDEX_DASHBOARD = 'application.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_MENU = 'application.menu.CustomMenu'
ADMIN_TOOLS_THEMING_CSS = 'admin/css/theming_v4.css'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 36000}  # 1 hour.
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# User
AUTH_USER_MODEL = 'users.User'
AUTH_USER_DEVELOPER = 'mail@engine2.ru'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'TIMEOUT': 60000
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_PAGINATION_CLASS': 'application.survey.pagination.StandardResultsSetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}


DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'shop-survey-bot@yandex.ru'
EMAIL_HOST_PASSWORD = '9k23nhsd793kmd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_FROM = 'shop-survey-bot@yandex.ru'

ADMIN_USERS = (
    'mail@engine2.ru', 'luknitskiy@yahoo.com',
)
SOLAR_STAFF_USERS = (
    'mail@engine2.ru', 'luknitskiy@yahoo.com',
)
TAXPAYERS_STAFF_USERS = (
    'mail@engine2.ru', 'luknitskiy@yahoo.com', '9623465666@mail.ru', '9849966@mail.ru', 'val7622@yandex.ru',
)
ADD_TASK_USERS = (
    'kurashevmichael@gmail.com', 'andrew@mail.ru'
)
PROMO_CODES_USERS = (
    'mail@engine2.ru', 'luknitskiy@yahoo.com', 'm.golodnyh@icecream-chl.ru',
)

SALES_PATH = '/var/survey/shop-survey/media/sales/'

# Compress
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_OUTPUT_DIR = 'cached'
COMPRESS_ROOT = STATIC_ROOT

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 мегабайт

# Application
APPLICATIONS = (
    ('iceman', 'Айсмен'),
    ('promotion', 'ГО Айсмен'),
    ('classic_logistic', 'Классик логистика'),
    ('classic_logistic_2', '2 Классик логистика'),
    ('logistic_msk', 'Логистика МСК'),
    ('nefco', 'Нэфис Косметикс'),
    ('samberu', 'Самберу'),
    ('smoroza', 'Смороза Биз'),
    ('shop_survey', 'Сюрвеер'),
    ('logistic_msk_2', 'Сюрвеер СВ'),
    ('bp_operators', 'Сюрвеер Ш'),
)

# Tinkoff
TINKOFF_TERMINALS = (
    ('1639142013666', 'm0l2avpxji3yeszf'),
    ('1645173777967', 'c4kqh9lxt6v0g0bb'),
    ('1647442881878', 'a0g1yru1p09zpncp'),
)