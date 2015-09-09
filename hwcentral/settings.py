# Django settings for hwcentral project.

import os

from core.routing.urlnames import UrlNames

PROD_CONFIG_ROOT = '/etc/hwcentral'

if os.path.isfile(os.path.join(PROD_CONFIG_ROOT, 'prod')):
    DEBUG = False
    CIRCLECI = False
# check if running on circleCI
elif os.environ.get('CIRCLECI') == 'true':
    DEBUG = False
    CIRCLECI = True
else:
    DEBUG = True
    CIRCLECI = False

PASSWORD_RESET_TIMEOUT_DAYS=1

SETTINGS_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SETTINGS_ROOT)
ASSIGNMENTS_ROOT = os.path.join(PROJECT_ROOT, 'core', 'assignments')
SUBMISSIONS_ROOT = os.path.join(PROJECT_ROOT, 'core', 'submissions')
QUESTIONS_ROOT = os.path.join(PROJECT_ROOT, 'core', 'questions')


MAILGUN_PASSWORD = '59cc8c52f2fa20a465d5c3d4c9a0f33c'
MAILGUN_ID = 'postmaster@hwcentral.in'
GMAIL_ID ='hwcentralroot@gmail.com'
GMAIL_PASSWORD ='hwcentral1'

ADMINS = (
    ('HWCentral Exception', 'exception@hwcentral.in'),
)
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_TIMEOUT = 20  # seconds

if (DEBUG or CIRCLECI):
    SECRET_KEY = '!x5@#nf^s53jwqx)l%na@=*!(1x+=jr496_yq!%ekh@u0pp1+n'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = GMAIL_ID
    EMAIL_HOST_PASSWORD = GMAIL_PASSWORD


else:
    # prod secret key should only be on prod server
    with open(os.path.join(PROD_CONFIG_ROOT, 'secret_key.txt'), 'r') as f:
        SECRET_KEY = f.read().strip()
    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_HOST_USER = MAILGUN_ID
    EMAIL_HOST_PASSWORD = MAILGUN_PASSWORD

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

MANAGERS = ADMINS

if CIRCLECI:
    DB_NAME = 'circle_test'
    DB_USER = 'ubuntu'
    DB_PASSWORD = ''
else:
    if DEBUG:
        DB_NAME = 'hwcentral-dev'
        DB_PASSWORD = 'hwcentral'
    else:
        DB_NAME = 'hwcentral-qa'
        with open(os.path.join(PROD_CONFIG_ROOT, 'db_password.txt'), 'r') as f:
            DB_PASSWORD = f.read().strip()
    DB_USER = 'root'

# signifies localhost
DB_HOST = ''
DB_PORT = ''

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

if DEBUG:
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

ROOT_URLCONF = 'hwcentral.urls'


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
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
# Inbuilt Login Configuration
LOGIN_URL = UrlNames.LOGIN.name
LOGIN_REDIRECT_URL = UrlNames.HOME.name  # this is where user is redirected if login view gets no 'next' param

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
if not DEBUG:
    ALLOWED_HOSTS = [
        '.hwcentral.in',  # Allow FQDN, domain and subdomains
    ]

    # uncomment the 2 lines below to simulate DEBUG=False on local machine
    # DEBUG = False
    # ALLOWED_HOSTS = ['localhost']
