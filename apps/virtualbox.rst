Virtual Box
===========

To enable USB debugging, you need to add the use to the vboxusers group:

   sudo adduser $USER vboxusers

Then login and lagout again.

To compact a vdi:

    vboxmanage modifymedium --compact /path/to/thedisk.vdi

To clone a disk:

    vboxmanage clonehd <old> <new> --format VDI

