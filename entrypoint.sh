#!/bin/sh

if [ "$POSTGRES_DB" = "hey_store" ]
then
    echo "Ждем postgres..."

    while ! nc -z "db" 5432; do
      sleep 0.5
    done

    echo "PostgreSQL запущен"
fi

python manage.py makemigrations
python manage.py migrate


exec "$@"