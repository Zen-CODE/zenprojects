zerofree
^^^^^^^^

zerofree is used to write null bytes to your disk, so that virtualbox can 
properly compact your *vdi* disk image.

Firstly, install zerofree::

    $ sudo apt-get install zerofree

Then empty you trash, remove all unused files, possibly by using a tool 
such as bleachbit.

Next, boot into recovery mode by pressing escape as the system boots.

Use the root root option and select "maintenance". Then run::

    $ systemctl stop systemd-journald.socket && systemctl stop systemd-journald.service && sudo swapoff -a && mount -n -o remount,ro -t ext2 /dev/sda1 / && zerofree /dev/sda1
    # shutdown now

You may need to run the command above a few times until it works. Then, on
your host, run:

    $ vboxmanage list hdds

to find your list of attached disks. Then, finally, run::

    $ VBoxManage.exe modifymedium disk "C:\path\to\disk.vdi" --compact

Where the path is replaced by the listed path to the *vdi* your wish to
compact.