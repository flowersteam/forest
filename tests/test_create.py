import unittest

import env
import treecfg

class TestCreate(unittest.TestCase):

    def test_create(self):
        tc = treecfg.TreeCfg()
        tc._node('a')
        tc.a.b = 1

        self.assertEqual(tc.a.b, 1)

    def test_newnode(self):
        tc = treecfg.TreeCfg()
        tc._newnode = 'a'
        tc.a.b = 1

        self.assertEqual(tc.a.b, 1)

    def test_override(self):
        tc = treecfg.TreeCfg()
        tc._node('a')
        tc.a.b = 1

        tc._node('a', override=True)

        with self.assertRaises(KeyError):
            tc.a.b

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
