Django
======

To run the django server:

    python3 manage.py runserver

To create a superuser:

    python3 manage.py createsuperuser --username=admin --email=zenkey.zencode@gmail.com

To reset the password:

    python3 manage.py changepassword <user_name>

To create/synchronize the database:

    python manage.py makemigrations
    python manage.py migrate

