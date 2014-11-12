gutengrep
=========

Find whole sentences matching a regex in Project Gutenberg plain text files.

Examples:

    gutengrep.py "^[^\w]*And then" *.txt --cache -o out\and-then.txt -s --correct

    gutengrep.py "^[^\w]*But why" *.txt --cache -o out\but-why.txt -s --correct

    gutengrep.py -i "whale" moby11.txt -o out\mobydick-whale.txt -s --correct
