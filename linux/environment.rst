Environment variables
======================

To list your current environment variables::

    $ printenv

To set an environment variable::

    $ export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/

To erase::

    # unset JAVA_HOME

To launch an binary with a environment configured via env file:

    sh -ac ' . ./.env.template; python manage.py test'

