"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
import environ

env = environ.Env()
root = environ.Path(BASE_DIR, 'secrets')


DEBUG = True
if DEBUG:
    env.read_env(root('.env.dev'))
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    env.read_env(root('.env.prod'))
    DATABASES = {
        'default': {
            'ENGINE': env.str('DB_ENGINE'),
            'NAME': env.str('DB_NAME'),
            'USER': env.str('DB_USER'),
            'PASSWORD': env.str('DB_PASSWORD'),
            'HOST': env.str('DB_HOST'),
            'PORT': env.str('DB_PORT'),
        }

    }

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
SECRET_KEY = env.str('DJANGO_SECRET_KEY') 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'blog.apps.BlogConfig',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # whitenoise設定
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


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases




# Heroku用のデータベース設定をインポートし、DATABASESを上書き
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# ----- static 設定項目 -----
STATICFILES_DIRS = [    # staticフォルダのパス（各アプリにstaticフォルダを作成した場合、リスト形式で全てのパスを記載）
    os.path.join(BASE_DIR, 'static'),   
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')     # collectstaticをした時の、まとめ先

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # whitenoise設定

MEDIA_URL = '/media/'   # サービス内でmediaフォルダのURLパスを設定
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')   # アップロードファイルなどを読み込む際のフォルダの場所を記載

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/login/'

# ------ message tab with bootstrap alert class -----
from django.contrib import messages
MESSAGE_TAGS = {        # templatesでクラス名として使用↓
    messages.ERROR: 'rounded-0 alert alert-danger',
    messages.WARNING: 'rounded-0 alert alert-warning',
    messages.SUCCESS: 'rounded-0 alert alert-success',
    messages.INFO: 'rounded-0 alert alert-info',
    messages.DEBUG: 'rounded-0 alert alert-secondary',
}

AUTH_USER_MODEL = 'account.User'

GRECAPTCHA_SECRETKEY = env.str('GRECAPTCHA_SECRETKEY')
GRECAPTCHA_SITEKEY = env.str('GRECAPTCHA_SITEKEY')

DEFAULT_EMAIL_FROM = env.str('DEFAULT_EMAIL_FROM')

if not DEBUG:
    # Heroku用に設定を適用
    import django_heroku
    django_heroku.settings(locals())