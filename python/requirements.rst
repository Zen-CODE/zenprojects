Capturing Python Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    $ pip freeze > requirements.txt

will capture all your installations dependencies in the text file. To capture
only those used::

    $ pip install pipreqs

    $ pipreqs /path/to/project
