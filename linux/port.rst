Ports
=====

To find out which process is listending on a port:

   $ lsof -i :5432

To list all used ports:

   $ netstat -anvp tcp | awk 'NR<3 || /LISTEN/'

`