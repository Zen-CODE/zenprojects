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

To specify an SSH key for git commands:

   GIT_SSH_COMMAND='ssh -i ~/.ssh/zen-code/id_rsa -o IdentitiesOnly=yes' git pull

To stop tracking changed file that are commited:

    git update-index --skip-worktree <file>

Resume tracking files with the following command:

    git update-index --no-skip-worktree <file>
