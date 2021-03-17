Processes Using Ports
=====================

To kill and processes using port 8000:

    sudo lsof -t -i tcp:8000 | xargs kill -9
