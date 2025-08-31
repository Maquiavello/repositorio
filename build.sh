#!/usr/bin/env bash

# Salir inmediatamente si un comando falla
set -e

# Instalar dependencias del proyecto desde requirements.txt
pip install -r requirements.txt

# Colectar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate