Git
===

To force a re-sync between you branch and origin:

    git fetch origin master
    git reset --hard origin/master

Undo last commit:

    git reset --soft HEAD~1

To pip install from a branch

    pip install git+ssh://git@github.com/<username>/<repo>.git@<branch_name>

To squash merges:

   git reset --soft HEAD~3
   git commit -m <commit_msg>

To prevent the `git branch` command from being interactive:

   git config --global pager.branch false
