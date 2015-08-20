"""
Django settings for TorrentBox project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# We use celery for background task processing
import djcelery
djcelery.setup_loader()
BROKER_URL = "amqp://guest@127.0.0.1:5672//"

# Torrent Download Directory
DOWNLOAD_DIR = os.path.join(BASE_DIR, "static", "TorrentStorage")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8(gg%tztpz!!8ss*z$ete_ha-@4a74a#&crtdg9bv7dq3p_6c8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = False

# This is for test, you have to edit this!
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djcelery',
    'core',
    'account',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TorrentBox.urls'

WSGI_APPLICATION = 'TorrentBox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASE_OPTIONS = {'charset': 'utf8'}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/account/sign_in/'
LOGOUT_URL = '/account/sign_out/'

# FIXED ISSUE: 404 Not Found error when Debug set to False (https://github.com/L34p/TorrentBOX/issues/2)
if DEBUG:
	STATIC_ROOT = os.path.join(BASE_DIR, '/static', 'static')
else:
	STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static')

# Template location
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "static", "templates"),
)

STATICFILES_DIRS = os.path.join(BASE_DIR, "static", "static"),

