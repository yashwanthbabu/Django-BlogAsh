"""
Django settings for sampleblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'sampleblog.settings')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'abcdefghijklmnop'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

FEEDBACK_ADMIN_EMAIL = 'yashwanth@agiliq.com'

TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

ALLOWED_HOSTS = ['blogging-application.herokuapp.com']

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'blog/templates/blog'),
    # Putstringshere,like"/home/html/django_templates"r"C:/www/django/templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')

STATIC_ROOT = 'staticfiles'

STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/')

SOUTH_TESTS_MIGRATE = False

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}


# Application definition

INSTALLED_APPS = (
    'suit',
    # 'django_admin_bootstrapped.bootstrap3',
    # 'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.comments',
    # 'django.contrib.sites',
    # 'ad_rotator',
    'analytical',
    'twitter_tag',
    # 'south',
    'blog',
    'taggit',
    # 'social_auth',
    # 'password_reset',
    # 'registration',
    'django_extensions',
    'django-session-idle-timeout',
)

# One-week activation window; you may, of course, use a different value.
ACCOUNT_ACTIVATION_DAYS = 7

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django-session-idle-timeout.middleware.SessionIdleTimeout',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'social_auth.backends.pipeline.misc.save_status_to_session',
)

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-56497829-1'

GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True

GOOGLE_ANALYTICS_SITE_SPEED = True

GOOGLE_ANALYTICS_ANONYMIZE_IP = True

SESSION_IDLE_TIMEOUT = 600

SOCIAL_AUTH_EMABLED_BACKENDS = ('twitter', 'facebook', 'google',)

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('google_client_id')

GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('google_client_secret')

FACEBOOK_APP_ID = os.environ.get('facebook_id')

FACEBOOK_API_SECRET = os.environ.get('facebook_secret')

TWITTER_CONSUMER_KEY = os.environ.get('twitter_id')

TWITTER_CONSUMER_SECRET = os.environ.get('twitter_secret')

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'publish_actions']

# Your access token: Access token
TWITTER_OAUTH_TOKEN = '181107703-NIS0AQbOMpmQbaRSwYoI7oX2QYyfQbOHKPWuSR7m'
# Your access token: Access token secret
TWITTER_OAUTH_SECRET = 'nv1lqg5tjxOGZSYQSNJNfScFZnG6vj1jrJ9uJZ7NaV0Rb'
# OAuth settings: Consumer key
TWITTER_CONSUMER_KEY = 'KkJwCnVX6rrvSSljPqi5tezq3'
# OAuth settings: Consumer secret
TWITTER_CONSUMER_SECRET = 'j5HHkDer21cTfq3Yzl5nWypebpv20Y0Kn5SyzXHBgzna0Q2ftW'

LOGIN_URL = 'django.contrib.auth.views.login'
LOGIN_REDIRECT_URL = '/blog/'
LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/blog/'
SOCIAL_AUTH_INACTIVE_USER_URL = '...'

FACEBOOK_EXTENDED_PERMISSIONS = ['email']

ROOT_URLCONF = 'sampleblog.urls'

WSGI_APPLICATION = 'sampleblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pyme',
        'PASSWORD': 'giant1pass',
        'USER': 'awsuser',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = "/static/"

BLOG_NUMBER_OF_ENTRIES_PER_PAGE = 3

STATIC_URL = '/static/'

BLOG_NUMBER_OF_ENTRIES_PER_PAGE = 3

BLOG_NUMBER_OF_RECENT_ENTRIES_PER_PAGE = 5

ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_SETTINGS_REDIRECT_URL = 'home'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('emailhost')
EMAIL_HOST_USER = os.environ.get('hostuser')
EMAIL_HOST_PASSWORD = os.environ.get('hostpswd')
EMAIL_USE_TLS = True
EMAIL_PORT = 587

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
