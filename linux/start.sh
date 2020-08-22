#!/bin/bash
echo "Launching firefox"
firefox &
echo "Launching Double Commander"
cd /home/fruitbat/Apps/doublecmd/
sh doublecmd.sh &
echo "Launching Jupyter notebook"
cd /home/fruitbat/Repos/zenpersonal/jupyter/
. venv/bin/activate
jupyter notebook --ip=0.0.0.0 &
echo "Launching ZenPlayer"
cd /home/fruitbat/Repos/zenplayer/
sh run_in_env.sh &

