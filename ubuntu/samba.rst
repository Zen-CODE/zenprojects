Samba
^^^^^

The samba file is in /etc/samba/smb.conf

To set the password::

    sudo smbpasswd -a <username>

To set the linux uset password ::

    sudo passwd <username>

To restart

    sudo /etc/init.d/samba restart

