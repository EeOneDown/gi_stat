#!/bin/sh

while ! nc -z gi_stat_app_db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# docker exec -it gi-stat-app /bin/sh
# python manage.py createsuperuser
# python manage.py clear_data
# python manage.py populate_data
