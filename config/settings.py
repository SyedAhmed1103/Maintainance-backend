from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================
# SECURITY
# ======================================================

SECRET_KEY = "django-insecure-ovgu4w-wvao4l(ihsdp*l1)%@vx+-@_=#$ky@(4u5uv^d3+&b)" \
""

DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

FRONTEND_URL = "https://your-frontend-domain.com"

# ======================================================
# INSTALLED APPS
# ======================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",

    # Local Apps
    "apps.building",
    "apps.wing",
    "apps.flats",
    "apps.users",
    "apps.maintenance",
    "apps.income",
    "apps.expense",
    "apps.complaint",
    "apps.notice",
    "apps.media_manager",
]

# ======================================================
# MIDDLEWARE
# ======================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ======================================================
# TEMPLATES
# ======================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ======================================================
# DATABASE
# ======================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres.tgsafgcdtuehrgrkwqaj",
        "PASSWORD": "Django@2026#Supabase",
        "HOST": "aws-1-ap-southeast-2.pooler.supabase.com",
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# ======================================================
# AUTH USER
# ======================================================

AUTH_USER_MODEL = "users.User"

# ======================================================
# PASSWORD VALIDATORS
# ======================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ======================================================
# INTERNATIONALIZATION
# ======================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

# ======================================================
# STATIC
# ======================================================

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ======================================================
# MEDIA
# ======================================================

MEDIA_URL = "/assets/"
MEDIA_ROOT = BASE_DIR / "assets"

# ======================================================
# DEFAULT PK
# ======================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ======================================================
# DRF
# ======================================================

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# ======================================================
# JWT
# ======================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# ======================================================
# SWAGGER
# ======================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Society Management API",
    "DESCRIPTION": "Society Management Backend",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ======================================================
# EMAIL
# ======================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.hostinger.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = "inquiry@itdax.in'"
EMAIL_HOST_PASSWORD = "5x!rddk8S~"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ======================================================
# CORS
# ======================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True