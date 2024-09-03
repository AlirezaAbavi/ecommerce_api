from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'z16g)!3_zx1ol9(%2!q0y_1iaq@%wmj6q(kotda&0mkjh+24c#'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*'
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # Add your front-end URL or any other URLs you want to allow
]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# JWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
}

SITE_ID = 1
REST_USE_JWT = True
REST_SESSION_LOGIN = False
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

ORDER_EXPIRY_TIME = 86400  # 24 hours
