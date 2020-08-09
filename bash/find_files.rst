To find files containing text:

    $ find ./ -type f -iname "*.txt" -exec grep -l "text to find" {} \;
