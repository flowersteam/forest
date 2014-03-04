from __future__ import print_function, division
import unittest

import env
import forest

class TestFreeze(unittest.TestCase):

    def test_freeze(self):
        tc = forest.Tree()
        tc._branch('a')

        tc._freeze()
        with self.assertRaises(ValueError):
            tc.a.b = 1
        with self.assertRaises(ValueError):
            tc._branch('b')

        tc._unfreeze()
        tc.a.b = 1
        tc._branch('b')

    def test_freeze_struct(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a.b = 1

        tc._freeze_struct()
        with self.assertRaises(ValueError):
            tc.a.c = 1
        tc.a.b = 2
