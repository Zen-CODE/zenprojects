Groups
======

To create a group:

    sudo groupadd <groupname>

To list all the groups of which the current member is a member:

    groups

To list group members:

   getent group groupname

To add a user to a group:

   sudo usermod -a -G groupName userName

To remove a user form a group:

   sudo deluser user group

To change the group owner of file or folder:

   sudo chgrp -R groupname /the/folder
