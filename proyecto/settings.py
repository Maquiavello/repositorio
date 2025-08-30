import os
from pathlib import Path
from decouple import config
import dj_database_url

# --------------------------------------------------------------------------------------
# Configuración Base
# --------------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Usamos una variable de entorno de Render para ALLOWED_HOSTS
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] # Para desarrollo local
CORS_ALLOWED_ORIGINS = [
    "https://tu-sitio-netlify.netlify.app",  # ← REEMPLAZA CON TU URL DE NETLIFY
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://tu-sitio-netlify.netlify.app",  # ← MISMA URL QUE ARRIBA
    "https://mi-app-1-2wv9.onrender.com",
]
# --------------------------------------------------------------------------------------
# Aplicaciones y Middleware
# --------------------------------------------------------------------------------------
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'daphne',
    'channels',
    'corsheaders',  # ← AGREGAR ESTA APP (arriba de django apps)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mi_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← DEBE IR PRIMERO
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Agregamos una ruta para tus templates
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

# --------------------------------------------------------------------------------------
# Configuración de URLs, WSGI y ASGI
# --------------------------------------------------------------------------------------
WSGI_APPLICATION = 'proyecto.wsgi.application'
ASGI_APPLICATION = 'proyecto.asgi.application'

# --------------------------------------------------------------------------------------
# Configuración de Django Channels y Redis
# --------------------------------------------------------------------------------------
# Usamos os.environ.get() que maneja mejor los valores por defecto de la URL de Redis
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# --------------------------------------------------------------------------------------
# Configuración de Base de Datos
# --------------------------------------------------------------------------------------
# Usamos dj_database_url para parsear la URL de la base de datos de Render
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# --------------------------------------------------------------------------------------
# Validadores de Contraseña
# --------------------------------------------------------------------------------------
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

# --------------------------------------------------------------------------------------
# Configuración de Archivos Estáticos
# --------------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------------------------------------------------------------------
# Configuraciones de Seguridad para Producción
# --------------------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
# --------------------------------------------------------------------------------------
# Otras Configuraciones
# --------------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'