"""
Django settings for decider_backend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from ConfigParser import NoOptionError, NoSectionError, RawConfigParser
import urlparse
from django.core.urlresolvers import reverse, reverse_lazy
import os
PROJECT_NAME = 'decider'
APP_NAME = 'decider_app'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(BASE_DIR, APP_NAME)


# Config
def get_config_opt(_config, section, option, default=None):
    try:
        return _config.get(section, option)
    except NoOptionError:
        if not default:
            raise NoOptionError
        return default
    except NoSectionError:
        if not default:
            raise NoSectionError
        return default

config = RawConfigParser()
config.read(os.path.join("conf", PROJECT_NAME + ".conf"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_config_opt(config, 'django', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DEBUG_TOOLBAR_PATCH_SETTINGS = False

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
    'corsheaders',
    'social.apps.django_app.default',
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

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

ROOT_URLCONF = 'decider_backend.urls'

WSGI_APPLICATION = 'decider_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_config_opt(config, 'db', 'ENGINE'),
        'NAME': get_config_opt(config, 'db', 'NAME'),
        'USER': get_config_opt(config, 'db', 'USER'),
        'PASSWORD': get_config_opt(config, 'db', 'PASSWORD'),
        'HOST': get_config_opt(config, 'db', 'HOST'),
        'PORT': get_config_opt(config, 'db', 'PORT')
    }
}

AUTH_USER_MODEL = 'decider_app.User'
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.vk.VKOAuth2'
)

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

OAUTH_CLIENT_ID = get_config_opt(config, 'oauth', 'CLIENT_ID')
OAUTH_CLIENT_SECRET = get_config_opt(config, 'oauth', 'CLIENT_SECRET')

SOCIAL_AUTH_URL_NAMESPACE = 'api:social'

SOCIAL_AUTH_USER_MODEL = 'decider_app.User'

SOCIAL_AUTH_VK_OAUTH2_KEY = get_config_opt(config, 'vk', 'VK_APP_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = get_config_opt(config, 'vk', 'VK_APP_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = []

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details'
)