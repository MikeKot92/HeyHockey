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
python manage.py collectstatic --noinput

if [ -f "mysite_data.json" ]; then
    echo "Загружаем фикстуры из mysite_data.json..."
    python manage.py loaddata mysite_data.json
else
    echo "Файл mysite_data.json не найден, пропускаем загрузку фикстур."
fi

exec "$@"