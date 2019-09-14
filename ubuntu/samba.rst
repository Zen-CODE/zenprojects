Samba
^^^^^

The samba file is in /etc/samba/smb.conf

To set the password::

    sudo smbpasswd -a <username>

To set the linux user password ::

    sudo passwd <username>

To add and remove linux uisers (on ubuntu):

    sudo adduser <user>
    sudo userdel -r <user>

Don't forget to give the user the appropriate file permissions. For reading:

    sudo chmod a+r -R <folder>

OR for writing:

    sudo chmod a+rwx -R <folder>

To restart

    sudo systemctl restart smbd

To mount the share. You may need to install cifs-utils.

    sudo mount -t cifs -o username=<user>,ro,password=<pwd> //myServerIpAdress/sharename /mnt/myFolder/
