Webcam
^^^^^^

If you get an error that the webcm is in use:

    $ fuser /dev/video0
    /dev/video0: 1871m
    $ ps axl | grep 1871
    $ kill -9 1871
