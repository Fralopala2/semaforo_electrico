import os
from pathlib import Path
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') # Ahora se obtiene de .env
# print(f"DEBUG: DJANGO_SECRET_KEY leída: '{SECRET_KEY}'") # Línea de depuración - Desactivada para producción

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users', # Tu aplicación de usuarios para la autenticación
    'electricity_prices', # ¡NUEVA APLICACIÓN!
    'rest_framework', # Para la FASE 1 y la API de precios
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'semaforo_electrico_project.urls' # Asegúrate de que esto coincida con el nombre de tu proyecto

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Usa Pathlib para el directorio de plantillas
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

WSGI_APPLICATION = 'semaforo_electrico_project.wsgi.application' # Asegúrate de que esto coincida con el nombre de tu proyecto

# Configuración de la base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'localhost', # IMPORTANTE: Cambiado a 'localhost' para Windows
        'PORT': '5432',
        'OPTIONS': {'client_encoding': 'UTF8'}, # ¡NUEVA LÍNEA!
    }
}
# print(f"DEBUG: POSTGRES_DB leída: '{os.getenv('POSTGRES_DB')}'") # Línea de depuración - Desactivada
# print(f"DEBUG: POSTGRES_USER leída: '{os.getenv('POSTGRES_USER')}'") # Línea de depuración - Desactivada
# print(f"DEBUG: POSTGRES_PASSWORD leída: '{os.getenv('POSTGRES_PASSWORD')}'") # Línea de depuración - Desactivada

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

LANGUAGE_CODE = 'es-es' # Configura el idioma a español

TIME_ZONE = 'Europe/Madrid' # Configura la zona horaria a Madrid

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static', # Usa Pathlib para el directorio de estáticos
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLs de redirección para autenticación
LOGIN_REDIRECT_URL = 'home' # Redirige a la página 'home' después de iniciar sesión
LOGOUT_REDIRECT_URL = 'login' # Redirige a la página 'login' después de cerrar sesión
LOGIN_URL = 'login' # URL para el login (importante para las redirecciones)

# Configuración para el envío de correos (necesario para restablecimiento de contraseña)
# Para desarrollo, puedes usar la consola para ver los correos.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Si quieres usar un servidor SMTP real, descomenta y configura (para producción):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu_email@example.com'
# EMAIL_HOST_PASSWORD = 'tu_password_de_email'