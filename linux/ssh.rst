SSH Access
==========

To install ssh::

   $ sudo apt-get install openssh-server


Edit (as root) /etc/ssh/sshd_config. Append the following to it:

     AllowUsers <username>

To set change the upstream origin of a git repos to use ssh::

    git remote set-url origin git@github.com:Zen-CODE/zenprojects.git

To check for ssh keys::

    ls -al ~/.ssh

To generate the ssh key::

    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

To add it to the ssh agent::

    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa

To copy it to the clipboard::

    sudo apt-get install xclip
    xclip -sel clip < ~/.ssh/id_rsa.pub

To check the git repo remote::

   git remote -v

To change to ssh::

    git remote set-url origin git@github.com:USERNAME/REPOSITORY.git

To change to https::

    git remote set-url origin https://github.com/USERNAME/REPOSITORY.git

To  checkout your ssh agent is running::

    eval "$(ssh-agent -s)"

To add the ssh key to the agent, enter the below. Note that the "-K" option is
only required on Apple.::

    ssh-add -K ~/.ssh/id_rsa
