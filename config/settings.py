import os
from pathlib import Path
import dj_database_url

# BASE_DIR should point to the root (where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True' #was true here

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://mysite-1-jhw2.onrender.com"
]

INSTALLED_APPS = [
    'cloudinary_storage', # Must be at the top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary', # Required for Cloudinary storage to work
    'django.contrib.staticfiles',
    
    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rosetta',
    'whitenoise.runserver_nostatic',
    
    # Your Apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required before Locale
    'django.middleware.locale.LocaleMiddleware',            # <--- ADD THIS HERE
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

# DATABASE
# DATABASE
# This will automatically use the Postgres URL on Render
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}
# AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = 'feed'
LOGOUT_REDIRECT_URL = 'login'

# STATIC & MEDIA
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use WhiteNoise for production static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'SECURE': True,  # <--- Add this line here
}

# Ensure this is also set to tell Django to use Cloudinary for media
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'




# LANGUAGES
LANGUAGE_CODE = 'en'
USE_I18N = False
USE_L10N = True
USE_TZ = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('sw', _('Swahili')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('pt', _('Portuguese')),
    ('ar', _('Arabic')),
    ('hi', _('Hindi')),
    ('ko', _('Korean')),
    ('ru', _('Russian')),
    ('ja', _('Japanese')),
    ('th', _('Thai')),
    ('de', _('German')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# settings.py

LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 31536000  # 1 year in seconds
LANGUAGE_COOKIE_PATH = '/'      # Makes it available across the whole site
LANGUAGE_COOKIE_SAMESITE = 'Lax'


# --- Scroll to the bottom of settings.py ---

# Authentication Settings (django-allauth)
SITE_ID = 1

# Update these lines to remove the deprecation warnings:
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# Keep your other existing allauth settings here
ACCOUNT_EMAIL_VERIFICATION = 'none' 
# ... etc


# ==============================================================================
# COOKIE & SESSION MANAGEMENT
# ==============================================================================

# Keeps the user logged in even after they close their browser window
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# The duration a session remains valid (in seconds). 
# 1209600 seconds is exactly 2 weeks.
SESSION_COOKIE_AGE = 1209600

# Save the session to the database on every single request 
# (this refreshes the expiration timer so active users never get kicked out)
SESSION_SAVE_EVERY_REQUEST = True
