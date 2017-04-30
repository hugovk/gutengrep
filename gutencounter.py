#!/usr/bin/env python
"""
Print out sentences from a corpus containing each number (in words).
gutencounter.py *.txt --cache >  gutencounter.txt
"""
from __future__ import print_function, unicode_literals
import gutengrep

import re
import inflect
import argparse

try:
    import timing
    assert timing  # Silence warning
except ImportError:
    pass


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def filter_boilerplate(sentences):
    # Filter some boilerplate
    new_sentences = []
    for s in sentences:
        if ("we are now trying to release all our books one" in s.lower() or
                "gutenberg" in s.lower() or
                "value per text" in s.lower() or
                "computer" in s.lower() or
                " etext" in s.lower()):
            continue
        new_sentences.append(s)
    return new_sentences


def find_matching_sentence(regex, sentences, flags=0):
    """Just one sentence"""
    for sentence in sentences:
        # if re.search(r"\b" + re.escape(word) + r"\b", sentence, flags):
        if re.search(regex, sentence, flags):
            # print("-"*80)
            # print_it(sentence)
            return sentence
    return None


def counter(inspec, outfile, sort, cache):

    flags = re.IGNORECASE
    sentences = gutengrep.prepare(inspec, cache)

    sentences = filter_boilerplate(sentences)

    if sort:
        sentences.sort(key=len)

    p = inflect.engine()
    print(1)
    # for i in range(0, 10000+1):
    # for i in range(10001, 50000+1):
    START, END = 30011, 1000000
    i = START - 1
    while(True):

        # Exit while loop?
        if i > END:
            break
        else:
            i += 1

        word = p.number_to_words(i)
        # Don't worry about spaces, commas or hyphens, so instead of:
        # "seven thousand, seven hundred and seventy-five"
        # match
        # "seven[ ]thousand[,] seven[ ]hundred and seventy[-]five"
        flexible_word = word
        # flexible_word = flexible_word.replace(" ", "[ ]?")
        # flexible_word = flexible_word.replace(",", "[,]?")
        # flexible_word = flexible_word.replace("-", "[-]?")
        # flexible_word = flexible_word.replace("[ ]?and[ ]?", " and ")

        regex = r"\b" + flexible_word + r"\b"
        matching_sentence = find_matching_sentence(
            regex, sentences, flags)  # TODO can return just one

        if not matching_sentence:
            continue

            # TODO FIXME don't want to match 123,456 when looking for 123...

            # Match digits ("1,000,000") instead of words ("one million")
            digits = gutengrep.commafy(i)
            # Don't worry about commas:
            # "1,000,000" -> "1[,]000[,]000"
            flexible_word = digits.replace(",", "[,]?")
            regex = r"\b" + flexible_word + r"\b"
            matching_sentence = find_matching_sentence(
                regex, sentences, flags)  # TODO can return just one
            if not matching_sentence:
                # Skip
                continue

        for s in matching_sentence:
            # Just keep the first sentence
            s = matching_sentence
            break

        # TODO remove matches?

        # gutengrep.output(matching_sentences, outfile) TODO append
        print("## " + word)
        print()
        s = s.replace("\r\n", " ")
        # s = s.replace(args.word, "**" + args.word + "**")  TODO
        out = gutengrep.format_text(s) + "\n\n"
        out = out.encode("utf-8")
        print(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Print out sentences from a corpus containing each number "
                    "(in words).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('inspec', nargs=1,
                        help="Input file spec")
    parser.add_argument('-o', '--outfile', default='output.log',
                        help="NOT USED Output filename")
    parser.add_argument('-s', '--sort', action='store_true',
                        help="TODO Also sort sentences by length and save in "
                             "file named like output-sort.log")
#     parser.add_argument('-b', '--bold', action='store_true',
#                         help="Embolden found text TODO")
    parser.add_argument('--cache', action='store_true',
                        help="Load cache. If no cache, save one. Warning: "
                             "the cached is saved based on the initial "
                             "--inspec. Subsequent uses are based on this "
                             "initial cache, effectively ignoring --inspec. ")
    args = parser.parse_args()

    counter(args.inspec[0], args.outfile, args.sort, args.cache)

# End of file
