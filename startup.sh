#!/bin/bash

# Este archivo inicia la aplicación Flask usando Gunicorn
# Configura el puerto para Azure App Service
export PORT=8000

# Inicia la aplicación
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 --workers 4 --threads 2 main:app
