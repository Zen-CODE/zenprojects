Aliases
=======

Bash has the handy concept of creating "aliases", which are simply shorthad
for issueing a more complex command. To create an alias, you add a line
to the end of your *.bashrc* file, something like:

    $ alias revenv='rm -rf venv && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

When you type "revenv", it will remove any "venv" folder and recreate it using
the requirements file in the current folder.