To find files containing text:

    $ find ./ -type f -iname "*.txt" -exec grep -l "text to find" {} \;

Or you can use grep directly:

    grep -rnw 'folder/' -e 'your text'

