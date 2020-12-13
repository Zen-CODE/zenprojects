Git
===

To force a re-sync between you branch and origin:

    git fetch origin master
    git reset --hard origin/master

Undo last commit:

    git reset --soft HEAD~1
