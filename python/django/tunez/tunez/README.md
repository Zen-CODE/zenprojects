# Tunez

## Overview

This folder houses the Djnago backend for the Tunez React frontend. This
frontend offers a UI to:
* control the currently active MPRIS2 Player (audacious)
* access the music library (as stored in Zen structure)

In order the run the app:
```
python manage.py runserver 0.0.0.0:8000
```
## React Application

This app can be installed by going into the "../../../react/zentunez" folder
and running the *deploy.sh* script. Please refer to the React Application 
documentation for further details.

## Configuration

Secrets are stored in a *.env* file this folder. Get the file from Zen's Google
drive. PostgreSQL certificates are also stored on this drive, and should be
copied into the *.postgresql* folder on the host.
