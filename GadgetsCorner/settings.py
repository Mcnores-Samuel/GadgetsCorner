"""
Django settings for GadgetsCorner project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
ICON_LINK = os.environ.get('ICON_LINK')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (bool(int(os.environ.get('DEBUG', 1))))

SERVER_DOMAIN1 = os.environ.get('SERVER_DOMAIN', default=".vercel.app")
SERVER_DOMAIN2 = os.environ.get('SERVER_DOMAIN2', default=".railway.app")
OTHER_DOMAIN = os.environ.get('OTHER_DOMAIN')
ALLOWED_HOSTS = [SERVER_DOMAIN1, SERVER_DOMAIN2, OTHER_DOMAIN]
CRSF_COOKIE_SECURE = True
CRSF_TRUSTED_ORIGINS = [SERVER_DOMAIN1, SERVER_DOMAIN2, OTHER_DOMAIN]

SESSION_COOKIE_SECURE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gadgetsCorner.apps.SystemCore1Config',
    'django_filters',
    'django_email_verification',
    'storages',
    'django_bootstrap5',
    'webpush',
]

WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": "BCbSiJmN3xQ07a5mZPb_nQGtRPX-GCPWkEOGbhslH96GjeFFbw6PxFPb87laYYjYWmTnGJvc_YSUnze3b7haR3I",
   "VAPID_PRIVATE_KEY": "tC_NbpUtELaPc_mcP_h2w1CKIwUHzkSTdnUeGKgu2pI",
   "VAPID_ADMIN_EMAIL": "samuelmcnores1@gmail.com"
}

FILTERS_EMPTY_CHOICE_LABEL = 'All'
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'gadgetsCorner.middleware.RedirectAuthenticatedUsersMiddleware',
]

X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'GadgetsCorner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'GadgetsCorner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'gadgetsCorner.UserProfile'

def verified_callback(user):
    user.is_active = True

EMAIL_MAIL_CALLBACK = verified_callback

EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_FROM_ADDRESS = os.environ.get('EMAIL_FROM_ADDRESS')
EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'authentication/activation_email.html'
EMAIL_MAIL_PLAIN = 'authentication/activation_email.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60
EMAIL_MAIL_PAGE_TEMPLATE = 'comfirm_template.html'
EMAIL_PAGE_DOMAIN = os.environ.get('EMAIL_PAGE_DOMAIN')
EMAIL_MULTI_USER = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


PASSWORD_RESET_TIMEOUT_DAYS = 1
PASSWORD_RESET_EMAIL_SUBJECT = 'registration/reset_email_subject.txt'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'LOCATION': os.path.join(BASE_DIR, 'media'),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'django': {
        'handlers': ['console'],
        'level': 'ERROR',
        'propagate': True,
    },
}
