"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from decouple import config, Csv
from google.oauth2 import service_account

from dj_database_url import parse as dburl
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default='django-insecure-0h49uhk#u)-laod!&4mg%%@%%um9hi9gg%ask42i7giw+v*29$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

BASE_URL = config("BASE_URL", default='http://127.0.0.1:8000')

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default='*', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'blog.core',
    'blog.posts',
    'blog.pages',
    'blog.accounts',
    'blog.comments',
    'blog.categories',
    
    'dbbackup',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    'django_filters',
    'anymail',
    'import_export',
    'tinymce',
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

ROOT_URLCONF = 'blog.urls'

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
                'blog.core.context_processors.global_configurations',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
# LOGIN_REDIRECT_URL = 'dashboard:dashboard'

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'blog.core.utils.CsrfExemptSessionAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        'rest_framework.permissions.IsAuthenticated',
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 15,
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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default="http://0.0.0.0", cast=Csv())

ADMIN_URL = config('ADMIN_URL', default='admin/')

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='mail@mail.com.br')

ANYMAIL = {
    "MAILGUN_API_KEY": config("MAILGUN_API_KEY", default=""),
    "MAILGUN_SENDER_DOMAIN": config("MAILGUN_SENDER_DOMAIN", default="")
}

sentry_sdk.init(
    dsn=config("SENTRY_DSN", default=""),
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.1,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


GS_DATA = {
    "type": "service_account",
    "project_id": config("GS_PROJECT_ID", default="GS_PROJECT_ID"),
    "private_key_id": config("GS_PRIVATE_KEY_ID", default="GS_PRIVATE_KEY_ID"),
    "client_email": config("GS_CLIENT_EMAIL", default="GS_CLIENT_EMAIL"),
    "private_key": config("GS_PRIVATE_KEY", default="GS_PRIVATE_KEY").replace("\\n", "\n"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": config('CLIENT_x509_CERT_URL', default='')
}


if not DEBUG:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(GS_DATA)
    GS_BUCKET_NAME=config('GS_BUCKET_NAME', default='GS_BUCKET_NAME')
    
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    
DBBACKUP_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
DBBACKUP_STORAGE_OPTIONS = {
    "bucket_name": config('GS_BACKUPS_BUCKET_NAME', default='GS_BACKUPS_BUCKET_NAME'),
    "project_id": config("GS_PROJECT_ID", default="GS_PROJECT_ID"),
    'location': 'blog/',
    "blob_chunk_size": 1024 * 1024
}

IMPORT_EXPORT_USE_TRANSACTIONS = True

# PARA A INTERFACE PERSONALIZADA DO ADMIN
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

TINYMCE_JS_URL = "https://cdnjs.cloudflare.com/ajax/libs/tinymce/5.3.0/tinymce.min.js"

DOMAIN_URL = BASE_URL if 'http' in BASE_URL else 'https://' + BASE_URL

TINYMCE_DEFAULT_CONFIG = {
    'toolbar': 'undo redo | bold italic underline strikethrough superscript subscript | fontsizeselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | charmap | image media | tiny_mce_wiris_formulaEditor | nonbreaking | preview | fullscreen | code',
    
    'plugins': ['link  table charmap hr pagebreak nonbreaking anchor toc insertdatetime lists wordcount image textpattern noneditable help  charmap quickbars autoresize powerpaste code imagetools media', 'searchreplace visualblocks code fullscreen'],
    'nonbreaking_force_tab': True,
    'menubar': False,
    'statusbar': False,
    'toolbar_mode': 'wrap',
    'image_caption': True,
    'autoresize_bottom_margin': 0,
    'autoresize_on_init': True, 
    'schema': "html5",
    'cleanup_on_startup': True,
    'entity_encoding': 'raw', 
    'language': 'pt_BR',
    'language_url': f'{BASE_URL}/static/js/tinymce/langs/pt.js',
    # 'external_plugins': {
    #     'powerpaste': f'{BASE_URL}/static/js/tinymce/powerpaste.js',    
    # },
    'images_upload_url': '/tiny/upload-image/',
    'paste_data_images': True,
    'automatic_uploads': True,
    'smart_paste': False,
    'powerpaste_allow_local_images': True,
    'powerpaste_html_import': 'clean',
    'powerpaste_word_import': 'clean',
    'powerpaste_googledocs_import': 'clean',
    'paste_merge_formats': True,
    'content_style': "body {font-size: 12pt;}",
    'fontsize_formats': "8pt 10pt 12pt 14pt 18pt",
    'indentation' : '40pt'
}

MULTIBLOGS = config("MULTIBLOGS", default=True, cast=bool)