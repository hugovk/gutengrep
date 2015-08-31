#!/usr/bin/env python
"""
Find whole sentences matching a regex in Project Gutenberg plain text files.
"""
from __future__ import print_function, unicode_literals
import re
import os
import sys
import glob
import codecs
import argparse
import textwrap
import nltk.data

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    import timing
except ImportError:
    pass

SENTENCES_CACHE = "sentences_cache.pkl"
TOKENIZER = None


def load_cache(filename):
    data = None
    if os.path.isfile(filename):
        print("Open cache...")
        with open(filename, 'rb') as fp:
            data = pickle.load(fp)
    return data


def save_cache(filename, data):
    with open(filename, 'wb') as fp:
        pickle.dump(data, fp, -1)


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


# Add thousands commas
def commafy(value):
    return "{:,}".format(value)


def format_text(text, indent=0, width=70):
    return textwrap.fill(text, width=width, initial_indent=" "*indent,
                         subsequent_indent=" "*indent)


def find_sentences_in_text(filename):
    """Read text from file and return a list of sentences"""
    global TOKENIZER
    print("Open " + filename + "...")
    try:
        with codecs.open(filename, encoding='cp1252') as fp:
            text = fp.read()

        print("Tokenize...")
        if TOKENIZER is None:
            TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = TOKENIZER.tokenize(text)
        print(commafy(len(sentences)), "sentences found")

        return sentences
    except UnicodeDecodeError:
        return []


def load_sentences_from_files(files, regex=None, flags=0):
    all_sentences = []

    for i, filename in enumerate(files):
        print(i+1, "/", len(files))
        sentences = find_sentences_in_text(filename)

        all_sentences.extend(sentences)

    print(commafy(len(all_sentences)), "total sentences found")
    return all_sentences


def find_matching_sentences(regex, sentences, flags=0, andnext=False,
                            language=None):
    total_sentences = len(sentences)
    matching_sentences = []

    for i, sentence in enumerate(sentences):
        # if re.search(r"\b" + re.escape(word) + r"\b", sentence, flags):
        if re.search(regex, sentence, flags):
            # print("-"*80)
            # print_it(sentence)

            if language:
                if detect(sentence) != language:
                    continue

            if andnext and i+2 <= total_sentences:
                matching_sentences.append(sentence + " " + sentences[i+1])
            else:
                matching_sentences.append(sentence)
    return matching_sentences


def output(sentences, filename, please_format_text=True):
    with open(filename, "w") as fp:
        for s in sentences:
            out = s.replace("\r\n", " ")
            # out = s.replace(args.word, "**" + args.word + "**")  TODO
            if please_format_text:
                out = format_text(out)
            out = (out + "\n\n").encode("utf-8")
            print(out)
            fp.write(out)
            # print("-"*80)


def insert_thing_into_filename(thing, filename):
    """Insert thing before the filename's extension"""
    root, ext = os.path.splitext(filename)
    filename = root + thing + ext
    return filename


def correct_quotes(text, quote):
    """
    Are quotes (probably) imbalanced?
    OK:
        "Hello!"
        He said: "Hello!"
        Not ok:
        "Hello!
    """
    count = text.count(quote)
    if not (count % 2 == 0):  # odd
        if text.startswith(quote) and not text.endswith(quote):
            text = text + quote
        if not text.startswith(quote) and text.endswith(quote):
            text = quote + text
    return text


def correct_those(sentences):

    for i, sentence in enumerate(sentences):
        # Remove initial quote-space, often a dangling end quote from the
        # previous sentence
        sentence = sentence.lstrip("' ").lstrip('" ')

        # Remove leading close-brackets
        sentence = sentence.lstrip("]").lstrip(")")

        # Strip whitespace
        sentence = sentence.strip()

        # Remove duplicate whitespace
        sentence = " ".join(sentence.split())

        # Balance quotes
        sentence = correct_quotes(sentence, '"')
        sentence = correct_quotes(sentence, '"')

        # Update
        sentences[i] = sentence

    return sentences


def prepare(inspec, cache):

    if not inspec and not cache:
        sys.exit("Error: inspec and/or cache arguments needed")

    if inspec:
        files = glob.glob(inspec)
        if not files:
            sys.exit("No input files found matching " + inspec)

    sentences = None
    # Open
    if cache:
        sentences = load_cache(SENTENCES_CACHE)

    if not sentences:
        sentences = load_sentences_from_files(files)
        if cache:
            save_cache(SENTENCES_CACHE, sentences)

    print(commafy(len(sentences)), "sentences found")
    return sentences


def gutengrep(regex, inspec, outfile, ignore_case, sort, cache, correct,
              andnext=False, language=None):

    if ignore_case:
        flags = re.IGNORECASE
    else:
        flags = 0

    sentences = prepare(inspec, cache)

    # Filter
    sentences = find_matching_sentences(regex, sentences, flags, andnext,
                                        language)

    if args.correct:
        sentences = correct_those(sentences)

    output(sentences, outfile)

    if sort:
        sentences.sort(key=len)
        print("*"*80)
        outfile = insert_thing_into_filename("-sort", outfile)
        output(sentences, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Find whole sentences matching a regex in "
                    "Project Gutenberg plain text files.",
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('regex', nargs=1,
                        help='Input regular expression e.g. "\\bword\\b"')
    parser.add_argument('inspec', nargs='?',
                        help="Input file spec")
    parser.add_argument('-o', '--outfile', default='output.log',
                        help="Output filename")
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help="Ignore case distinctions")
    parser.add_argument('-s', '--sort', action='store_true',
                        help="Also sort sentences by length and save in "
                             "file named like output-sort.log")
    # parser.add_argument('-b', '--bold', action='store_true',
    #                     help="Embolden found text TODO")
    parser.add_argument('--cache', action='store_true',
                        help="Load cache. If no cache, save one. Warning: "
                             "the cache is saved based on the initial "
                             "inspec. Subsequent uses are based on this "
                             "initial cache, effectively ignoring inspec. ")
    parser.add_argument('--correct', action='store_true',
                        help="Make little corrections to sentences: "
                             "stripping whitespace, balancing quotes")
    parser.add_argument('--andnext', action='store_true',
                        help="Also output the next sentence")
    parser.add_argument('-l', '--language',
                        help="Only this language sentences. Use language code,"
                             "like en or es.")
    args = parser.parse_args()

    if args.language:
        from langdetect import detect

    gutengrep(args.regex[0], args.inspec, args.outfile, args.ignore_case,
              args.sort, args.cache, args.correct, args.andnext, args.language)

# End of file
