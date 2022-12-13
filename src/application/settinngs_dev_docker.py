from .settings import *
import socket

DEBUG = True
PREFERENCES_CACHE_SETTING = False

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ['127.0.0.1', ]

# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']

# Celery
CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 36000}  # 1 hour.
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'TIMEOUT': 60000
    }
}

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'shop_survey',
        'USER':     'postgres',
        'PASSWORD': 'postgres',
        'HOST':     'db',
        'PORT':     '5432',
    }
}
