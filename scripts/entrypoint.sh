#!/bin/sh

set -e
# start Container
echo "Contenedor iniciado"
echo "$(date): Ejecutando proceso"



# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver 0.0.0.0:$PORT


gunicorn api.wsgi:application --bind 0.0.0.0:$PORT --certfile ./fullchain.pem --keyfile ./privkey.pem
# gunicorn api.wsgi:application --bind 0.0.0.0:8000 --certfile ./fullchain.pem --keyfile ./privkey.pem
