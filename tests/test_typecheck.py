from __future__ import print_function, division
import unittest

import env
import forest

class TestTypeCheck(unittest.TestCase):

    def test_simple(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a._isinstance('b', int)
        tc.a.b = 1

        with self.assertRaises(TypeError):
            tc.a.b = 'abc'

        with self.assertRaises(TypeError):
            tc.a.b = 1.0