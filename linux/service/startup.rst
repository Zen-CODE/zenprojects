SystedD Startup
===============

SystedD service units are scripts which live in '/etc/systemd/system/'. In order
to create one::

    * Create a shell script you want to run at startup. e.g.
      'touch-dev-permisssions.sh'

    * Place a unit file in '/etc/systemd/system/' that runs this script.
      'touch-dev-permisssions.service' in one example of how this file should
      look.

    * Make the script executable e.g.

        # chmod 744 touch-dev-permisssions.sh

    * Install the service unit and make it executable.

        # sudo chmod 664 /etc/systemd/system/touch-dev-permisssions.service
        # sudo systemctl daemon-reload
        # sudo systemctl enable touch-dev-permisssions.service

To start your service::

    # systemctl start touch-dev-permisssions.service

To stop your service::

    # systemctl stop touch-dev-permisssions.service

To remove your service::

    # systemctl stop touch-dev-permisssions.service

For more::

    https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux