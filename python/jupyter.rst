Jupyter notebook
================

If you have Python 3 installed (which is recommended):

    $ python3 -m pip install --upgrade pip
    $ python3 -m pip install jupyter

If you have Python 2 installed:

    $ python -m pip install --upgrade pip
    $ python -m pip install jupyter

Congratulations, you have installed Jupyter Notebook! To run the notebook, run
the following command at the Terminal (Mac/Linux) or Command Prompt (Windows):

    $ jupyter notebook

To enable non-local access, you first need to generate a config file (if you do
not already have one).

    $ jupyter notebook --generate-config

Then enable the password option in the config file and restart juypter. It will
then prompt you for the password.:

    c.NotebookApp.password_required = True

Or set the password

    $ jupyter notebook password

To ernable access from other IP's:

    c.NotebookApp.ip = '10.0.0.3'


