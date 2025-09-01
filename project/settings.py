from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Manejo de ALLOWED_HOSTS de forma dinámica y segura.
# En producción (DEBUG=False), se lee la URL desde las variables de entorno de Render.
# En desarrollo (DEBUG=True), se permite localhost y 127.0.0.1.
if not DEBUG:
    # Lee la lista de hosts permitidos de la variable de entorno,
    # que debe ser una cadena de texto separada por comas.
    ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = ['maquiavellichat.onrender.com']

# Configuración de CORS y CSRF para producción
# Esta configuración se aplicará tanto en desarrollo como en producción
# para simplificar la lógica y evitar errores.
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
CORS_ALLOWED_ORIGINS = [
    'https://*.onrender.com'
]
CORS_ALLOW_CREDENTIALS = True

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'corsheaders',
    'mi_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Agregado para servir archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración para Channels
ASGI_APPLICATION = 'project.asgi.application'

# Se agrega la configuración de la URL de Redis en un solo lugar
REDIS_URL = os.environ.get('REDIS_URL')

if not DEBUG:
    # Usar Redis para la capa de canales en producción
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
else:
    # Usar capa en memoria para desarrollo local
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

# Database
# Se usa dj_database_url.config() para parsear la URL completa de la base de datos
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = 'static/'
# La ruta donde 'collectstatic' reunirá todos los archivos estáticos en producción.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Habilitar WhiteNoise para servir archivos estáticos comprimidos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'