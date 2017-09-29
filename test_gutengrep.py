#!/usr/bin/env python
# encoding: utf-8
"""
Unit tests for gutengrep.py
"""
from __future__ import print_function, unicode_literals
import unittest

import gutengrep


class TestIt(unittest.TestCase):

    def test_correct_quotes(self):
        input = ["' I looked."]
        expected = ["I looked."]

        input = gutengrep.correct_those(input)

        self.assertEqual(input, expected)


if __name__ == '__main__':
    unittest.main()

# End of file
