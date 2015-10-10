# Django settings for hwcentral project.

import os
import sys

from core.routing.urlnames import UrlNames
from core.utils.constants import HWCentralEnv
from hwcentral.exceptions import InvalidHWCentralEnvError

PROD_CONFIG_ROOT = '/etc/hwcentral'

# set environ and debug values
if os.path.isfile(os.path.join(PROD_CONFIG_ROOT, 'prod')):
    ENVIRON = HWCentralEnv.PROD
    DEBUG = False

# check if running on qa
elif os.path.isfile(os.path.join(PROD_CONFIG_ROOT, 'qa')):
    ENVIRON = HWCentralEnv.QA
    DEBUG = False

# check if running on circleCI
elif os.environ.get('CIRCLECI') == 'true':
    ENVIRON = HWCentralEnv.CIRCLECI
    DEBUG = False

else:
    ENVIRON = HWCentralEnv.LOCAL
    DEBUG = True

SLEEP_MODE = os.path.isfile(os.path.join(PROD_CONFIG_ROOT, 'sleep'))
# uncomment the line below to test SLEEP mode locally
# SLEEP_MODE = True

PASSWORD_RESET_TIMEOUT_DAYS=2

SETTINGS_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SETTINGS_ROOT)

VISIBLE_SECRET_KEY = '!x5@#nf^s53jwqx)l%na@=*!(1x+=jr496_yq!%ekh@u0pp1+n'
MAILGUN_HOST = 'smtp.mailgun.org'
MAILGUN_SANDBOX_USER = 'Homework Central Sandbox <postmaster@sandboxab360baee25e495dbb8dd423eab0e2fb.mailgun.org>'
MAILGUN_SANDBOX_PASSWORD = '6ad200251e795d5ed5bbb9d3ad717a6b'

if ENVIRON == HWCentralEnv.PROD:
    with open(os.path.join(PROD_CONFIG_ROOT, 'secret_key.txt'), 'r') as f:
        SECRET_KEY = f.read().strip()
    EMAIL_HOST = MAILGUN_HOST
    EMAIL_HOST_USER = 'Homework Central <postmaster@hwcentral.in>'
    with open(os.path.join(PROD_CONFIG_ROOT, 'mailgun_password.txt'), 'r') as f:
        EMAIL_HOST_PASSWORD = f.read().strip()

    DB_NAME = 'hwcentral_prod'
    with open(os.path.join(PROD_CONFIG_ROOT, 'db_password.txt'), 'r') as f:
        DB_PASSWORD = f.read().strip()
    DB_USER = 'hwcentral'
    DB_HOST = '10.176.7.252'
    DB_PORT = '3306'

elif ENVIRON == HWCentralEnv.QA:
    SECRET_KEY = VISIBLE_SECRET_KEY
    EMAIL_HOST = MAILGUN_HOST
    EMAIL_HOST_USER = MAILGUN_SANDBOX_USER
    EMAIL_HOST_PASSWORD = MAILGUN_SANDBOX_PASSWORD

    DB_NAME = 'hwcentral_dev'
    DB_PASSWORD = 'hwcentral'
    DB_USER = 'root'
    DB_HOST = ''
    DB_PORT = ''

elif ENVIRON == HWCentralEnv.CIRCLECI:
    SECRET_KEY = VISIBLE_SECRET_KEY
    EMAIL_HOST = MAILGUN_HOST
    EMAIL_HOST_USER = MAILGUN_SANDBOX_USER
    EMAIL_HOST_PASSWORD = MAILGUN_SANDBOX_PASSWORD

    DB_NAME = 'circle_test'
    DB_USER = 'ubuntu'
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_PORT = ''

elif ENVIRON == HWCentralEnv.LOCAL:
    SECRET_KEY = VISIBLE_SECRET_KEY
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'hwcentralroot@gmail.com'
    EMAIL_HOST_PASSWORD = 'hwcentral1'

    DB_NAME = 'hwcentral_dev'
    DB_PASSWORD = 'hwcentral'
    DB_USER = 'root'
    DB_HOST = ''
    DB_PORT = ''

else:
    raise InvalidHWCentralEnvError(ENVIRON)

ADMINS = (
    ('HWCentral Exception', 'exception@hwcentral.in'),
)
MANAGERS = (
    ('HWCentral Contact', 'contact@hwcentral.in'),
)

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_TIMEOUT = 20  # seconds
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,

        'OPTIONS': {
            'init_command': 'SET character_set_connection=utf8,collation_connection=utf8_unicode_ci'
        },
    },
}

if ENVIRON == HWCentralEnv.LOCAL:
    SITE_ID = 2  # localhost site
else:
    SITE_ID = 1  # prod site entry

INTERNAL_IPS = ()  # this should be automatically set by debug_toolbar to include localhost

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_root')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    # The following loader will pull in sttic content from dirs specified in STATICFILES_DIRS
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # The following loader will pull in static content from a 'static/' folder in each installed app
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Project-specific location of static files
STATICFILES_DIRS = (
    os.path.join(SETTINGS_ROOT, 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            # Project-specific location of template files
            os.path.join(SETTINGS_ROOT, 'templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MAX_CHARFIELD_LENGTH = 255  # Applying this limit to allow safely marking any CharField as unique. For longer requirement use TextField

# Project-specific location of fixture files
FIXTURE_DIRS = (
    os.path.join(SETTINGS_ROOT, 'fixtures'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hwcentral.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'debug_toolbar',
    'django_extensions',

    # Now HWCentral-specific apps
    'core',
    'cabinet',
    'croupier',
    'grader',
    'concierge',
    'sphinx',
)

SYSLOG_ADDR = '/dev/log'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django': {
            'format': 'django: %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'logging.handlers.SysLogHandler': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'formatter': 'django',
            'address': SYSLOG_ADDR,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'loggly_logs': {
            'handlers': ['logging.handlers.SysLogHandler'],
            'propagate': True,
            'format': 'django: %(message)s',
            'level': 'DEBUG',
        },
    }
}
# Inbuilt Login Configuration
LOGIN_URL = UrlNames.LOGIN.name
LOGIN_REDIRECT_URL = UrlNames.HOME.name  # this is where user is redirected if login view gets no 'next' param

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
if ENVIRON == HWCentralEnv.PROD:
    ALLOWED_HOSTS = [
        '.hwcentral.in',  # Allow FQDN, domain and subdomains
    ]
elif ENVIRON == HWCentralEnv.QA:
    ALLOWED_HOSTS = [
        '128.199.130.205'  # qa server ip address
    ]
elif ENVIRON == HWCentralEnv.CIRCLECI:
    ALLOWED_HOSTS = []


if SLEEP_MODE:
    ROOT_URLCONF = 'hwcentral.urls.sleep_mode'
else:
    if ENVIRON == HWCentralEnv.PROD:
        ROOT_URLCONF = 'hwcentral.urls.prod'
    else:
        ROOT_URLCONF = 'hwcentral.urls.debug'  # qa just uses debug urls for now