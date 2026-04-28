import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================

# On Render, set this in the Environment tab. 
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-development-only-key')

# Set DEBUG to False in Render environment variables
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED HOSTS
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

# Render specific hostname for CSRF
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"]
else:
    CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "https://*.onrender.com"]

# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rosetta',
    'django_recaptcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'whitenoise.runserver_nostatic', 

    # Local apps
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
    'django.middleware.locale.LocaleMiddleware',  # Crucial for i18n_patterns
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
        'DIRS': [BASE_DIR / 'templates'], # For global templates
        'APP_DIRS': True,                 # Looks in core/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.notification_count', 
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =========================
# DATABASE (Dynamic for Render)
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

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise production storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# AUTH & REDIRECTS
# =========================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'feed'  # Redirect here after successful login
LOGOUT_REDIRECT_URL = 'login'

# Allauth specifics (if needed)
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

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

LOCALE_PATHS = [BASE_DIR / 'locale']

# Automatically append slashes to URLs
APPEND_SLASH = True

# =========================
# RECAPTCHA
# =========================

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '6LeiG7QsAAAAAKUF2Yj01yJ4X7CmhmDdXb4X_Z6X')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '6LeiG7QsAAAAAHvODEtyCrJ40ZUqkSMEoXevDStu')

# Standard Django requirement
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'