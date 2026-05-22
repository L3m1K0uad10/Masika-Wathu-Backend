import environ

from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ENVIRONMENT VARIABLES SETTINGS
env = environ.Env()
environ.Env.read_env(env_file = BASE_DIR / '.env')


# SECURITY SETTINGS
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default = False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default = [])


# APPLICATIONS SETTINGS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # local apps
    'apps.users',
    'apps.merchants',
    'apps.marketplace',
    'apps.payments'
]


# MIDDLEWARE SETTINGS
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


# URLS / WSGI SETTINGS
ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'


# TEMPLATES SETTINGS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


# DATABASE SETTINGS
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# AUTH USER MODEL SETTINGS
AUTH_USER_MODEL = 'users.User'


# PASSWORD VALIDATION SETTINGS
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


# INTERNATIONALIZATION SETTINGS
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# STATIC FILES SETTINGS
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


# MEDIA FILES SETTINGS
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

PRIVATE_MEDIA_ROOT = BASE_DIR / 'private_media'


# DJANGO REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },  

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# CORS HEADERS SETTINGS
# Only allow our Malawi-based frontend domain
CORS_ALLOWED_ORIGINS = [
    "https://masikawathu.mw",
    "http://localhost:3000", # i will keep as i am still developing
]


# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# PAYCHANGU SETTINGS
PAYCHANGU_BASE_URL = env('PAYCHANGU_BASE_URL', default = 'https://api.paychangu.com/v1')
PAYCHANGU_SECRET_KEY = env('PAYCHANGU_SECRET_KEY')
PAYCHANGU_PUBLIC_KEY = env('PAYCHANGU_PUBLIC_KEY')
PAYCHANGU_WEBHOOK_SECRET = env('PAYCHANGU_WEBHOOK_SECRET')
BACKEND_BASE_URL = env("BACKEND_BASE_URL")