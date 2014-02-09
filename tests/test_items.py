from __future__ import print_function, division
import unittest

import env
import treecfg

class TestItem(unittest.TestCase):

    def test_item(self):
        tc = treecfg.TreeCfg()
        tc._newnode = 'a'

        tc.a['b'] = 1
        self.assertEqual(tc.a.b, 1)
        self.assertEqual(tc.a['b'], 1)

        tc.a.b = 2
        self.assertEqual(tc.a.b, 2)
        self.assertEqual(tc.a['b'], 2)

    def test_del(self):
        tc = treecfg.TreeCfg()
        tc._newnode = 'a'

        tc.a.b = 2
        del tc.a['b']
        with self.assertRaises(KeyError):
            tc.a.b

        tc.a.c = 2
        del tc.a.c
        with self.assertRaises(KeyError):
            tc.a.c


class TestNestedItem(unittest.TestCase):

    def test_nestitem(self):
        tc = treecfg.TreeCfg()

        with self.assertRaises(KeyError):
            tc['a.b'] = 1

        tc._newnode = 'a'
        tc['a.b'] = 1

        self.assertEqual(tc.a.b, 1)
