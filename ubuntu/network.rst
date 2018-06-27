Network setup
==============

To list network devices:

   $ cat /proc/net/dev

To set the network address:

   $ ifconfig eth1 10.0.0.11 netmask 255.255.255.0

To add a gateway/route:

    $ route add default gw 10.0.0.1