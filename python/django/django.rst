Django
======

To run the django server:

    python3 manage.py runserver

To create a superuser:

    python3 manage.py createsuperuser --username=joe --email=joe@example.com

To reset the password:

    python3 manage.py changepassword <user_name>

To create/synchronize the database:

    python manage.py makemigrations
    python manage.py migrate

