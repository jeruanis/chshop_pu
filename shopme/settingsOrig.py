
import os
from pathlib import Path
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
ROOT_URLCONF = f'{config("PROJECT_NAME")}.urls'
WSGI_APPLICATION = f'{config("PROJECT_NAME")}.wsgi.application'
ASGI_APPLICATION = f'{config("PROJECT_NAME")}.routing.application'
#PREPEND_WWW = True

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
    'django.contrib.humanize',
    'admin_honeypot',
    'currencies',
    'django_filters',
    'storages',
    'chatapp',
    'customer',
    'notification',
    'templatetags',
    'rest_framework',
    'rest_framework.authtoken',
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

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = config('HSTS')
SECURE_HSTS_PRELOAD =True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [

    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True, #remove this because app_dirs must be set error is raised upn adding the loaders=(django.template.loaders.app_directories.Loader) :similar
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
                'currencies.context_processors.currencies',
                'carts.context_processors.country_cur',

            ],
            'loaders':[
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    ]),
            ],
            'libraries': {
                'filter_tags': 'templatetags.filter_tags',
           }
        },
    },
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

ASGI_THREADS = 20

AUTH_USER_MODEL = 'accounts.Account'

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

# CACHES = {
#    'default': {
#       'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#       'LOCATION': 'my_cache_table',
#    }
# }

CACHE_MIDDLEWARE_ALIAS = 'memory'
CACHE_MIDDLEWARE_SECONDS = 5 * 60 #1min caching
CACHE_MIDDLEWARE_KEY_PREFIX = ' '


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
DEFAULT_FILE_STORAGE = f'{config("PROJECT_NAME")}.media_storages.MediaStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    }
}


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = config('AWS_LOCATION')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

EMAIL_HOST =  config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        # 'file':{
        #     'class': 'logging.FileHandler',
        #     'filename': config('jvlog'),
        #     'level': 'DEBUG',
        # },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        # '': {
        #     'level': 'DEBUG',
        #     'handlers':['file'],
        #     'propagate': True,
        # },
    }
}

#MANAGERS AND ADMINS MUST FOLLOW LOGGING
ADMINS = [
    ('error_note', config('EMAIL_HOST_USER')),
]
MANAGERS = [
    ('error_note', config('EMAIL_HOST_USER')),
]


BASE_URL = "https://my-web.com"
TEMP = os.path.join(BASE_DIR, 'temp')
