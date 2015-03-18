"""
Django settings for decider_backend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
APP_NAME = 'decider_app'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(BASE_DIR, APP_NAME)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#c!29ow1anf+n&&78ec%haxm^ha986+jw&5yod)trakuhcuxi!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'decider_app',
    'oauth2_provider',
    'corsheaders'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
)

ROOT_URLCONF = 'decider_backend.urls'

WSGI_APPLICATION = 'decider_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'decider_db',
        'USER': 'decider_db_user',
        'PASSWORD': 'decider_db_pass',
        'HOST': 'localhost',
        'PORT': ''
    }
}

AUTH_USER_MODEL = 'decider_app.User'
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = os.path.join(APP_DIR, '/static/')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

CORS_ORIGIN_ALLOW_ALL = True if DEBUG else False

LOGIN_URL = "/login/"

HOST_SCHEMA = "http"
HOST_ADDRESS = "0.0.0.0"
HOST_PORT = "8000"

OAUTH_CLIENT_ID = 'qKUIA4ddXuPgTjjZNAR-KaRhJ3CfQHrFiZElo.yA'
OAUTH_CLIENT_SECRET = 'YiQ;_kk.LJsu6ue1S2PYT@obImiqeVYZ=VtTwwGwZJXiFBdvzVm2Y=2lLF7pZ:.C-vx;4p_fZrog_fF9qal-_S9GSh061.6NfyY=FP03D=BLV2YtGlp=473V2YxGdk1V'