#!/usr/bin/env bash

python manage.py migrate
python manage.py collectstatic  --noinput
gunicorn randomizer.wsgi --bind 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000
