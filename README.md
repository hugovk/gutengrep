gutengrep
=========

Find whole sentences matching a regex in Project Gutenberg plain text files.

Tip: download the [Project Gutenberg August 2003 CD](http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project) and put all the files in the same directory.

Example commands
----------------

    gutengrep.py "^[^\w]*And then" *.txt --cache -o out\and-then.txt -s --correct

    gutengrep.py "^[^\w]*But why" *.txt --cache -o out\but-why.txt -s --correct

    gutengrep.py -i "whale" moby11.txt -o out\mobydick-whale.txt -s --correct

Example output
--------------

 * [But why?](output/but-why.txt?raw=true)

 * [But why? (sorted)](output/but-why-sorted.txt?raw=true)

 * [But why?](output/and-then.txt?raw=true)

 * [But why? (sorted)](output/and-then-sorted.txt?raw=true)

 * [The whale](output/mobydick-whale.txt?raw=true)

 * [The whale (sorted)](output/mobydick-whale-sort.txt?raw=true)
