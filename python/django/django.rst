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

To initialize the models on first use:

    python manage.py makemigrations <app>

To dumpdata from the shell to a json file:

    import sys
    from django.core.management import call_command

    sysout = sys.stdout
    sys.stdout = open('filename.json', 'w')
    call_command('dumpdata', <app_name>)
    sys.stdout = sysout

To un-apply migrations

    python manage.py migrate <app> <migration_no>
