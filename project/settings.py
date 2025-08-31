from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Se usa 'os.environ.get()' para leer la clave secreta de una variable de entorno en Render.
# Si no está definida (entorno local), usa una clave de respaldo.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-xc)k0o7*zzzk7=9!pu#iq7b0j9rj$fmpb%$43z62&&txzf+o^r')

# SECURITY WARNING: don't run with debug turned on in production!
# 'DEBUG' se activa solo si la variable de entorno 'RENDER' no existe,
# lo que indica que estás en un entorno local.
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
# Se configura el host permitido dinámicamente.
# Si estás en Render (DEBUG es False), permite la URL de Render.
# En desarrollo (DEBUG es True), permite localhost y 127.0.0.1.
if not DEBUG:
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
        CSRF_TRUSTED_ORIGINS = ['https://' + RENDER_EXTERNAL_HOSTNAME]
else:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1', '127.00.1:8000']
    
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


# Configuración CORS
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    # Configurar CORS de forma más restrictiva en producción
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CORS_ORIGIN', ''),
    ]
    CORS_ALLOW_CREDENTIALS = True


# Database
# Se usará la configuración local solo cuando DEBUG sea True.
if not DEBUG:
    DATABASES = {
        'default': dj_database_url.config(
            default='sqlite:///db.sqlite3',
            conn_max_age=600
        )
    }
else:
    # Esta es tu configuración original para desarrollo local.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'app_db': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'app.db',
        }
    }


# Database router configuration
DATABASE_ROUTERS = ['mi_app.routers.AppRouter'] 

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