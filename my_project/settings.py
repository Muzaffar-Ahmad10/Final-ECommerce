from pathlib import Path
import os
import json
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG = json.loads(open(str(BASE_DIR) + "/config.json", "r").read())

SECRET_KEY = CONFIG["SECRET_KEY"]

STRIPE_SECRET_KEY = 'sk_test_51PG3XeEFP8WxWAAHztB4r0ERiRAJjqHS7vjb2Q0xHwSQTBi1FNrrhArW3JuHdp0fVf48vQuX5VVNJoIf3CUmPQOR00OrHPFWRf'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51PG3XeEFP8WxWAAHk1Ln1cwqnWTdQmGqUAInKu2Xfk4YbBK9puyEYvNsXNffHUpYT2HwRHBXr8yiXJgaB0HVlXIz00ZrSZVmhf'

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'corsheaders',
    'cart',
    'products',
    'mainapp',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

CORS_ALLOW_ALL_ORIGINS = True

WSGI_APPLICATION = 'my_project.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(CONFIG['DATABASE'])
}

CSRF_TRUSTED_ORIGINS = [
    'https://8000-muzaffarahm-finalecomme-3hax6bdglm6.ws-eu114.gitpod.io',
    'https://*.gitpod.io',  # This allows all subdomains of gitpod.io
    'https://*.herokuapp.com'
]

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
