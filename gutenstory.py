#!/usr/bin/env python
"""
Generate a story by grepping Project Gutenberg.
"""
from __future__ import print_function, unicode_literals
import gutengrep

import argparse
import random
import re

try:
    import timing
except ImportError:
    pass


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def markdown_escape(text):
    chars = "\`*_{}[]()>#+-.!$"
    for c in chars:
        if c in text:
            text = text.replace(c, "\\" + c)
    return text


def get_em(sentences, regex, flags=0, filter=True, sort=False):
    found = gutengrep.find_matching_sentences(regex, sentences, flags)
#     found = gutengrep.correct_those(found)
    print(regex + ":", len(found))

    if not filter:
        chosen = found
    else:
        # Keep a number of random sentences
        chosen = []
        for j in range(70):
            random_tractor = random.randrange(len(found))
#             print(found[random_tractor])
            chosen.append(markdown_escape(found[random_tractor]))
            del found[random_tractor]
#             print()

    print(regex + ":", len(chosen))
    if sort:
        chosen.sort(key=len)

    return chosen


def make_title(regex, i):
    """Make a chapter title"""
    title = 'Chapter ' + str(i+1)  # + ': ' + markdown_escape(regex)
    print("## " + title)
    print()
    return title


def make_appendix_entry(regex, i):
    """Show which regex each chapter used"""
    text = 'Chapter ' + str(i+1) + ': ' + markdown_escape(regex)
    print(" * " + text)
    print()
    return text


def story(inspec, outfile, sort, cache, story_title):

    sentences = gutengrep.prepare(inspec, cache)

    # Double escape regex \s

    # Chapters will begin with "once upon a time"
    flags = re.IGNORECASE
    regex = "once upon a time"
    starters = get_em(sentences, regex, flags, filter=False)

    # Chapters will end "The end." ...
    flags = re.IGNORECASE
    regex = "the end\\."
    endings = get_em(sentences, regex, flags, filter=False)

    # ... or "happily ever after"
    flags = re.IGNORECASE
    regex = "happily ever after"
    endings2 = get_em(sentences, regex, flags, filter=False)

    endings.extend(endings2)
    print("Endings:", len(endings))

    # Let's find a bunch of stuff to fill each chapter
    chapters = []
    regexes = []

    regex = "^[^\\w]*But why"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*And then"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*Why"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*Of course"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*So\\b"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*Therefore"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*Suddenly"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*I\\b"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*We\\b"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*You\\b"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*Presently"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "^[^\\w]*If\\b"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = "year-old"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "princess"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "\\bking"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "\\bwitch"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "violin"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "said"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "asked"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "laughed"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "\\bevil\\b"
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = "(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day"
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = ("January|February|March|April|May|June|July|August|September|"
             "October|November|December")
    chapters.append(get_em(sentences, regex, sort=sort))
    regexes.append(regex)

    regex = ("moonlight")
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    regex = ("\\benchant")
    chapters.append(get_em(sentences, regex, re.IGNORECASE, sort=sort))
    regexes.append(regex)

    # OK, that'll do, let's build the book!

    # Reset, reuse
    sentences = []
    front_matter = [
        "Title:          " + story_title + ", a grepped story\n"
        "CSS:            gutenstory.css\n"
        "HTML Header:    <link rel='stylesheet' type='text/css' href='https://fonts.googleapis.com/css?family=Gentium+Book+Basic:400,700,400italic'>",
        "",
        "# " + story_title,
        "",
        "# A grepped story",
        "",
        '<p class="author">gutenstory.py</p>',
        "",
        '<p class="auth-desc">for NaNoGenMo 2014</p>',
        "",
        '<p class="source">source code at https://github.com/hugovk/gutengrep</p>',
        "",
        "## Contents",
        ]
    end_matter = ['## <a id="appendix">Appendix</a>',
                  "Regular expressions used for each chapter.",
                  ""]

    for i in range(len(chapters)):

        # Pick a random chapter
        random_chapter = random.randrange(len(chapters))
        print()
        print()

        title = make_title(regexes[random_chapter], i)
        entry = make_appendix_entry(regexes[random_chapter], i)
        sentences.append("")
        id = 'chapter'+str(i+1)
        sentences.append('## <a id="' + id + '">' + title + '</a>')
        front_matter.append(' * <a href="#' + id + '">' + title + '</a>')
        end_matter.append(entry)

        # Pick a random starter then remove it
        random_tractor = random.randrange(len(starters))
        print(starters[random_tractor])
        sentences.append(markdown_escape(starters[random_tractor]))
        del starters[random_tractor]

        # Print the random chapter
        chapter = chapters[random_chapter]
        sentences.extend(chapter)
        del chapters[random_chapter]
        del regexes[random_chapter]

        # Pick a random ending then remove it
        random_tractor = random.randrange(len(endings))
        print(endings[random_tractor])
        sentences.append(markdown_escape(endings[random_tractor]))
        del endings[random_tractor]

    front_matter.append(' * <a href="#appendix">Appendix</a>')
    sentences = gutengrep.correct_those(sentences)

    gutengrep.output(front_matter + sentences + end_matter, outfile,
                     please_format_text=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate a story by grepping Project Gutenberg.",
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('inspec', nargs=1,
                        help="Input file spec")
    parser.add_argument('-t', '--title', default='Gutenstory',
                        help="Story title")
    parser.add_argument('-o', '--outfile', default='gutenstory.md',
                        help="Output filename")
    parser.add_argument('-s', '--sort', action='store_true',
                        help="Sort sentences by length")
#     parser.add_argument('-b', '--bold', action='store_true',
#                         help="Embolden found text TODO")
    parser.add_argument('--cache', action='store_true',
                        help="Load cache. If no cache, save one. Warning: "
                             "the cached is saved based on the initial "
                             "--inspec. Subsequent uses are based on this "
                             "initial cache, effectively ignoring --inspec. ")
    args = parser.parse_args()

    story(args.inspec[0], args.outfile, args.sort, args.cache, args.title)

# End of file
