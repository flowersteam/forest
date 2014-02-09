from __future__ import print_function, division
import unittest

import env
import trees

class TestCreate(unittest.TestCase):

    def test_create(self):
        tc = trees.Tree()
        tc._node('a')
        tc.a.b = 1

        self.assertEqual(tc.a.b, 1)

    def test_override(self):
        tc = trees.Tree()
        tc._node('a')
        tc.a.b = 1

        tc._node('a', overwrite=True)

        with self.assertRaises(KeyError):
            tc.a.b

    def test_newnode(self):
        tc = trees.Tree()
        tc._newnode = 'a'
        tc.a.b = 1

        self.assertEqual(tc.a.b, 1)

    def test_nestednewnode(self):
        tc = trees.Tree()
        tc._newnode = 'a.b'
        tc.a.b.c = 1
        self.assertEqual(tc.a.b.c, 1)

        tc._newnode = 'a.b.defg.hc.i'
        tc.a.b.defg.hc.i.c = 3
        self.assertEqual(tc.a.b.defg.hc.i.c, 3)
