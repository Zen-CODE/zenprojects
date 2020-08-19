To find files containing text:

    $ find ./ -type f -iname "*.txt" -exec grep -l "text to find" {} \;

Or you can use grep directly:

    grep -rnw 'folder/' -e 'your text'

For adding a prefix to a file or a group of files:

    for f in *.mp3 ; do mv -- "$f" "my_prefix$f" ; done