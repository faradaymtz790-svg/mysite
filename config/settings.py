import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ✅ BASE_DIR points to the root (where manage.py lives)
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'a-safe-fallback-for-local-only')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"]
else:
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:8000",
        "https://*.onrender.com",
    ]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'cloudinary_storage',  
    'whitenoise.runserver_nostatic',          
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 

    'cloudinary',
    'rosetta',
    'django_recaptcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'core', 
]

SITE_ID = 1

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# =========================
# DATABASE
# =========================
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# =========================
# STATIC & MEDIA FILES
# =========================


# =========================
# STATIC & MEDIA FILES
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Keep the modern way for Django 6.0
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage", 
    },
}

# ✅ THE CRITICAL FIX: Direct assignment for third-party package compatibility
# This MUST be a top-level variable in settings.py
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# =========================
# CLOUDINARY CONFIG
# =========================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'dwccyjh8z'), 
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'RESOURCE_TYPES': ['image', 'video', 'raw'], 
}

# =========================
# AUTH & REDIRECTS
# =========================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'feed'
LOGOUT_REDIRECT_URL = 'login'

ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
    ('fr', 'French'),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
APPEND_SLASH = True

# =========================
# RECAPTCHA
# =========================
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '6LeiG7QsAAAAAKUF2Yj01yJ4X7CmhmDdXb4X_Z6X')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '6LeiG7QsAAAAAHvODEtyCrJ40ZUqkSMEoXevDStu')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# LOGGING
# =========================
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
        'level': 'DEBUG',
    },
}