#! /bin/bash
source ./venv/bin/activate
python manage.py runserver 0.0.0.0:8000 2>&1 > /dev/null &
