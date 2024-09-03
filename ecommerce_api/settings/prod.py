from decouple import config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: Change this in production!
ALLOWED_HOSTS = config('ALLOWED_HOSTS')

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS')

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS')


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# run 'pip install mysqlclient'
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}

# JWT

# Uncomment for custom token lifetime
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
# }

SITE_ID = 1
REST_USE_JWT = True
REST_SESSION_LOGIN = False
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

# Orders expire time

ORDER_EXPIRY_TIME = 86400  # 24 hours
