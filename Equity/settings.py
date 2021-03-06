"""
Django settings for Equity project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('', ''),
)

MANAGERS = ADMINS

# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'equity',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$^ynby2*+w$(8@xmctv2sj18$gcj=*=x$c!fpz)b&xi)t5em6o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATE_INPUT_FORMATS = (
    '%d/%m/%Y',
)

DATETIME_FORMAT = 'N j, Y, P'

# Application definition
INSTALLED_APPS = (
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_countries',
    'widget_tweaks',
    'bootstrap3',
    'inmuebles',
    'noticias',
    'mathfilters',
    'easy_pdf',
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

ROOT_URLCONF = 'equity.urls'

WSGI_APPLICATION = 'equity.wsgi.application'

LOGIN_URL = '/admin/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Directorio de los templates
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

MEDIA_URL = '/uploads/'

# For Sidebar Menu (List of apps and models) (RECOMMENDED)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'inmuebles.context_processor.context_busqueda',
)

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, '../static/fixtures'),
)

# Configuracion de envio de correos
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'equity_mail'
EMAIL_HOST_PASSWORD = 'G*7j5$8'
DEFAULT_FROM_EMAIL = 'contacto@equity-international.com'
SERVER_EMAIL = 'contacto@equity-international.com'
