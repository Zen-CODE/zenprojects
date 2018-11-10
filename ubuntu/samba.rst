Samba
^^^^^

The samba file is in /etc/samba/smb.conf

To set the password::

    sudo smbpasswd -a <username>

To set the linux uset password ::

    sudo passwd <username>

Don't forget to give the user the appropriate file permissions. For reading:

    sudo chmod +r -R <folder>

OR for writing:

    sudo chmod +rw -R <folder>

To restart

    sudo systemctl restart smbd

To mount the share. You may need to install cifs-utils.

    sudo mount -t cifs -o username=<user>,ro,password=<pwd> //myServerIpAdress/sharename /mnt/myFolder/
