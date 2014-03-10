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

    def test_settree(self):
        tc = forest.Tree()
        tc.a = forest.Tree()
        tc.a.b = 1

    def test_nestedbranch(self):
        tc = forest.Tree()
        tc._branch('a.b')
        tc.a.b.c = 1
        self.assertEqual(tc.a.b.c, 1)

        tc._branch('a.b.defg.hc.i')
        tc.a.b.defg.hc.i.c = 3
        self.assertEqual(tc.a.b.defg.hc.i.c, 3)
        self.assertEqual(tc.a.b.c, 1)

    def test_setitem(self):
        tc = forest.Tree()
        tc['a.b.c'] = 1
        self.assertEqual(tc.a.b.c, 1)

    def test_init(self):
        t = forest.Tree({'a': 1, 'b.c':2})

        self.assertEqual(t.a, 1)
        self.assertEqual(t.b.c, 2)

    def test_copy(self):
        tc = forest.Tree()
        tc._branch('a.b')
        tc.a.b.c = 1
        tc['a.b.defg.hc.i'] = 3

        t2 = tc._copy()
        self.assertEqual(tc, t2)

        t3 = tc._copy(deep=True)
        self.assertEqual(tc, t3)

    def test_get(self):
        tc = forest.Tree()
        tc._branch('a.b')
        tc.a.b.c = 1

        self.assertEqual(tc._get('a.b.c', 2), 1)
        self.assertEqual(tc._get('a.b.d', 2), 2)

    def test_setdefault(self):
        tc = forest.Tree()
        tc._branch('a.b')
        tc.a.b.c = 1
        tc.a._setdefault('b.c', 2)
        tc.a._setdefault('e.c', 4)

        self.assertEqual(tc.a.b.c, 1)
        self.assertEqual(tc.a.e.c, 4)



    def test_in(self):
        tc = forest.Tree()
        tc._branch('a.b')
        tc.a.b.c = 1

        self.assertTrue('a.b.c' in tc)
        self.assertTrue(not 'a.b.d' in tc)

