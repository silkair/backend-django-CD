from pathlib import Path
import os
import environ
import pymysql
import logging
from logging.handlers import RotatingFileHandler
from elasticsearch import Elasticsearch

pymysql.install_as_MySQLdb()
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env()
SECRET_KEY = env('SECRET_KEY')
OPENAI_API_KEY = env('OPENAI_API_KEY')

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'backend',]
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'user',
    'storages',
    'image',
    'background',
    'recreated_background',
    'banner',
    'django_redis',
    'image_resizing',
    'django_celery_results',  # Celery 결과 백엔드 추가
    'django_prometheus',      # 모니터링 할 때 추가
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware', #(모니터링 할 때 추가)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware', #(모니터링 할 때 추가)
]
ROOT_URLCONF = 'backend.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'bootcamp',
            'in': 'header'
        }
    },
}

WSGI_APPLICATION = 'backend.wsgi.application'
# Database
# <https://docs.djangoproject.com/en/4.2/ref/settings/#databases>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': '3306',
        'CONN_MAX_AGE': 0,  # 매 쿼리마다 새로운 커넥션을 생성
    }
}
# Password validation
# <https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators>
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
# <https://docs.djangoproject.com/en/4.2/topics/i18n/>
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# <https://docs.djangoproject.com/en/4.2/howto/static-files/>
STATIC_URL = 'static/'
# Default primary key field type
# <https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field>
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ORIGIN_ALLOW_ALL = True

# AWS S3 연결
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_QUERYSTRING_AUTH = False

# 파일 저장 시 S3 를 디폴드 값으로 설정
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DRF 설정
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
}

OPENAI_API_KEY = env('OPENAI_API_KEY')

DRAPHART_API_KEY = env('DRAPHART_API_KEY')
DRAPHART_USER_NAME = env('DRAPHART_USER_NAME')
DRAPHART_MULTIBLOD_SOD= env('DRAPHART_MULTIBLOD_SOD')
DRAPHART_BD_COLOR_HEX_CODE= env('DRAPHART_BD_COLOR_HEX_CODE')

#Redis를 쓰고 싶다면!
#CELERY_BROKER_URL = 'redis://redis:6379/0'
#CELERY_RESULT_BACKEND = 'django-cache'

#RabbiMQ를 쓰고싶다면!!
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//' #여기서 guest:guest 는 아이디:비밀번호
CELERY_RESULT_BACKEND = 'django-db'  # 작업 결과를 Django 데이터베이스에 저장
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_CACHE_BACKEND = 'default'
CELERY_WORKER_HIJACK_ROOT_LOGGER = False  # Celery가 root logger를 hijack하지 않도록 설정

CELERYD_TASK_TIME_LIMIT = 300  # 작업 제한 시간 설정 (초)
CELERYD_TASK_SOFT_TIME_LIMIT = 270  # 소프트 제한 시간 설정 (초)

# Redis settings for Django cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',  # Redis 서버 위치
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 커스텀 Elasticsearch 핸들러 정의
class ElasticsearchHandler(logging.Handler):
    def __init__(self, hosts=None, index='django-logs'):
        logging.Handler.__init__(self)
        self.es = Elasticsearch(hosts=hosts)
        self.index = index

    def emit(self, record):
        log_entry = self.format(record)
        self.es.index(index=self.index, document={'message': log_entry})

#LOGGING설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/debug.log',
            'formatter': 'verbose',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,  # 백업 파일 수
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}