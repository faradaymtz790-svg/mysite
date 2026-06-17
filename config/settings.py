import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# SECURITY
# -------------------------
# -------------------------
# SECURITY
# -------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')

DEBUG = os.environ.get("DEBUG", "True") == "True"

# Base production domains
ALLOWED_HOSTS = [
    'www.zeed.social', 
    'zeed.social', 
    'mysite-0v87.onrender.com'
]

# Automatically append local hosts only when running locally (DEBUG = True)
if DEBUG:
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']



CSRF_TRUSTED_ORIGINS = [
    "https://www.zeed.social",
    "https://zeed.social",
    "https://mysite-1-jhw2.onrender.com"
    "https://mysite-0v87.onrender.com"
]
# -------------------------
# APPS
# -------------------------
INSTALLED_APPS = [
    # Cloudinary (keep installed but safe)
    'cloudinary_storage',
    'cloudinary',

    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rosetta',
    'whitenoise.runserver_nostatic',

    # Your app
    'core',
]

# -------------------------
# MIDDLEWARE
# -------------------------
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

# -------------------------
# TEMPLATES
# -------------------------
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

# -------------------------
# DATABASE
# -------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# -------------------------
# AUTH
# -------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ACCOUNT_ADAPTER = 'core.adapters.ZeedAccountAdapter'

SITE_ID = 1

# Remove the old ACCOUNT_EMAIL_REQUIRED line entirely!

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# config/settings.py

LOGOUT_REDIRECT_URL = 'login'
# config/settings.py
LOGIN_REDIRECT_URL = 'feed'
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

# The email* notation here already tells Allauth that email is required
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# -------------------------
# STATIC FILES
# -------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



if DEBUG:
    # LOCAL DEVELOPMENT
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    # PRODUCTION (RENDER + CLOUDINARY)
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
        "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
        "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
        "SECURE": True,
    }

    # 🌟 OVERRIDE MEDIA_URL IN PRODUCTION SO DJANGO PULLS FROM THE CLOUD
    # Replace 'dwccyjh8z' with your cloud name if it differs from your settings dump
    MEDIA_URL = f"https://res.cloudinary.com/dwccyjh8z/image/upload/"
# -------------------------
# INTERNATIONALIZATION
# -------------------------
LANGUAGE_CODE = 'en'
USE_I18N = True
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

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale/')]

# -------------------------
# SESSIONS (FIX FOR LOCAL)
# -------------------------
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True

# Security cookies only in production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
else:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# config/settings.py

# config/settings.py

# 1. Use Django's native SMTP backend engine
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# 2. Resend SMTP Connection parameters
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# 3. Security credentials 
EMAIL_HOST_USER = 'resend'
EMAIL_HOST_PASSWORD = 're_H5RVLsgF_9ekUxpXCP4BwyBLSEsmt3F4P'

# 4. Your live domain identity
DEFAULT_FROM_EMAIL = 'Zeed App <no-reply@zeed.social>'

# 5. Your custom Allauth email template
ACCOUNT_HTML_EMAIL_TEMPLATE = 'email_verify.html'