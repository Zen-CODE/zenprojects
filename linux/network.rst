Network setup
==============

To list network devices:

   $ cat /proc/net/dev

To set the network address:

   $ ifconfig eth1 10.0.0.11 netmask 255.255.255.0

To add a gateway/route:

    $ route add default gw 10.0.0.1

To setup a static IP, int /etc/network/interfaces, do something like:

    # The loopback network interface
    auto lo
    iface lo inet loopback

    # The primary network interface
    auto eth1
    iface eth1 inet static
    address 10.0.0.11
    netmask 255.255.255.0
    gateway 10.0.0.1
    dns-nameservers 10.0.0.1 8.8.8.8
