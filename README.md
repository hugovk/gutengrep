gutengrep
=========

Find whole sentences matching a regex in Project Gutenberg plain text files.

Example commands
----------------

    gutengrep.py "^[^\w]*And then" "*.txt" --cache --sort --correct -o output/and-then.txt

    gutengrep.py "^[^\w]*But why" "*.txt" --cache --sort --correct -o output/but-why.txt

    gutengrep.py -i "whale" moby11.txt --sort --correct -o out\mobydick-whale.txt

Example output
--------------

|                       Name                      |                        Sorted                        |       Regex      |     Input    | Word count |
|:-----------------------------------------------:|:----------------------------------------------------:|:----------------:|:------------:|:----------:|
|     [But why?](output/but-why.txt?raw=true)     |     [But why?](output/but-why-sort.txt?raw=true)     | `^[^\w]*But why` |    `*.txt`   |    7,572   |
|    [And then!](output/and-then.txt?raw=true)    |    [And then!](output/and-then-sort.txt?raw=true)    | `[^\w]*And then` |    `*.txt`   |   85,014   |
| [The whale](output/mobydick-whale.txt?raw=true) | [The whale](output/mobydick-whale-sort.txt?raw=true) |      `whale`     | `moby11.txt` |   50,913   |
|    [Why](output/why.txt?raw=true)    |    [Why](output/why-sort.txt?raw=true)    | `[^\w]*Why` |    `*.txt`   |   184,832   |
|    [Once upon a time](output/once-upon-a-time.txt?raw=true)    |    [Why](output/once-upon-a-time-sort.txt?raw=true)    | `-i` `once upon a time` |    `*.txt`   |   6,195   |

Tips
----

Download the [Project Gutenberg August 2003 CD](http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project) and put all the files in the same directory.

When working on the whole corpus, use `--cache` to cut down on file operations. The first time it will build a cache file of all tokenised sentences. This first pass takes about 5 minutes on my MBP to go through the 597 books of the Project Gutenberg CD and extract its 3,583,390 sentences. Subsequent runs using the cache take about 50 seconds.

If searching just a single file, or a subset of files, make sure not to use `--cache` because it will use the cache file generated on the initial file spec.

