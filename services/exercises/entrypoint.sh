#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z exercises-db 5432; do
    sleep 0.3
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0
