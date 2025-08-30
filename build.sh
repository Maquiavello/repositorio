#!/usr/bin/env bash

# Salir inmediatamente si un comando falla
set -e

# Colectar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate
