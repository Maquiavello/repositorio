#!/usr/bin/env bash
# Salir inmediatamente si un comando falla
set -e
# Instalar dependencias del proyecto
pip install -r requirements.txt
# Colectar archivos estáticos
python manage.py collectstatic --noinput
# Ejecutar migraciones
python manage.py migrate
# Ejecutar el comando de gestión para crear las salas
python manage.py create_rooms
