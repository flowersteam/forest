from __future__ import print_function, division
import unittest

import env
import forest

class TestCreate(unittest.TestCase):

    def test_create(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a.b = 1

        self.assertEqual(tc.a.b, 1)

    def test_override(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a.b = 1

        with self.assertRaises(ValueError):
            tc._branch('a')

    def test_nestedbranch(self):
        tc = forest.Tree()
        tc._branch('a.b')
        tc.a.b.c = 1
        self.assertEqual(tc.a.b.c, 1)

        tc._branch('a.b.defg.hc.i')
        tc.a.b.defg.hc.i.c = 3
        self.assertEqual(tc.a.b.defg.hc.i.c, 3)
