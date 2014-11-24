#!/usr/bin/env python
"""
Generate a story by grepping Project Gutenberg.
"""
from __future__ import print_function, unicode_literals
import gutengrep

import re
import argparse

import random


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


def get_em(sentences, regex, flags=0):
    found = gutengrep.find_matching_sentences(regex, sentences, flags)
#     found = gutengrep.correct_those(found)
    print(regex + ":", len(found))

    return found


def make_title(regex, i):
    """Given a regex, make a chapter title"""
    title = 'Chapter ' + str(i+1) + ': ' + markdown_escape(regex)
    print("## " + title)
    print()
    return title


def story(inspec, outfile, sort, cache):

    sentences = gutengrep.prepare(inspec, cache)

#     Double escape regex \s

    # Chapters will begin with "once upon a time"
    flags = re.IGNORECASE
    regex = "once upon a time"
    starters = get_em(sentences, regex, flags)

    # Chapters will end "The end." ...
    flags = re.IGNORECASE
    regex = "the end\\."
    endings = get_em(sentences, regex, flags)

    # ... or "happily ever after"
    flags = re.IGNORECASE
    regex = "happily ever after"
    endings2 = get_em(sentences, regex, flags)

    endings.extend(endings2)
    print("Endings:", len(endings))

    # Let's find a bunch of stuff to fill each chapter
    chapters = []
    regexes = []

    regex = "^[^\\w]*But why"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*And then"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*Why"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*Of course"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*So\\b"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*Therefore"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*Suddenly"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*I\\b"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*We\\b"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*You\\b"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*Presently"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "^[^\\w]*If\\b"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = "year-old"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "princess"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "\\bking"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "\\bwitch"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "violin"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "said"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "asked"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "laughed"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "\\bevil\\b"
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    regex = "(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day"
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = ("January|February|March|April|May|June|July|August|September|"
             "October|November|December")
    chapters.append(get_em(sentences, regex))
    regexes.append(regex)

    regex = ("moonlight")
    chapters.append(get_em(sentences, regex, re.IGNORECASE))
    regexes.append(regex)

    # OK, that'll do, let's build the book!

    # Reset, reuse
    sentences = []
    front_matter = [
        "Title:          Gutenstory, a grepped story\n"
        "CSS:            gutenstory.css\n"
        "HTML Header:    <link rel='stylesheet' type='text/css' href='http://fonts.googleapis.com/css?family=Gentium+Book+Basic:400,700,400italic'>",
        "",
        "# Gutenstory",
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

    for i in range(len(chapters)):

        # Pick a random chapter
        random_chapter = random.randrange(len(chapters))
        print()
        print()

        title = make_title(regexes[random_chapter], i)
        sentences.append("")
        id = 'chapter'+str(i+1)
        sentences.append('## <a id="' + id + '">' + title + '</a>')
        front_matter.append(' * <a href="#' + id + '">' + title + '</a>')

        # Pick a random starter then remove it
        random_tractor = random.randrange(len(starters))
        print(starters[random_tractor])
        sentences.append(markdown_escape(starters[random_tractor]))
        del starters[random_tractor]

        # Print the random chapter
        chapter = chapters[random_chapter]
        # Pick a number of random sentences from this chapter
        chosen = []
        for j in range(75):
            print(random_chapter, len(chapter))
            random_sentence = random.randrange(len(chapter))
            print(chapter[random_sentence])
            chosen.append(markdown_escape(chapter[random_sentence]))
            del chapter[random_sentence]
            print()
        del chapters[random_chapter]
        del regexes[random_chapter]
        if sort:
            chosen.sort(key=len)
        sentences.extend(chosen)

        # Pick a random ending then remove it
        random_tractor = random.randrange(len(endings))
        print(endings[random_tractor])
        sentences.append(markdown_escape(endings[random_tractor]))
        del endings[random_tractor]

    sentences = gutengrep.correct_those(sentences)

    gutengrep.output(front_matter + sentences, outfile,
                     please_format_text=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate a story by grepping Project Gutenberg.",
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('inspec', nargs=1,
                        help="Input file spec")
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

    story(args.inspec[0], args.outfile, args.sort, args.cache)

# End of file
