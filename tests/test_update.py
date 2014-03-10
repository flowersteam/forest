from __future__ import print_function, division
import unittest

import env
import forest

class TestUpdate(unittest.TestCase):

    def test_update(self):
        t = forest.Tree()
        t.b = 2
        t._branch('c')
        t.c.d = 5.1
        t._branch('a')

        t2 = forest.Tree()
        t2.b = 3
        t2._branch('c')
        t2.c.d = 5.2
        t2._update(t)

        self.assertEqual(t.a, t2.a)
        self.assertEqual(t2.b, 2)
        self.assertEqual(t2.c.d, 5.1)

        t2.b = 4
        t2.c.d = 5.3
        t2._update(t, overwrite=False)
        self.assertEqual(t2.b, 4)
        self.assertEqual(t2.c.d, 5.3)


    def test_update_frozen(self):
        t = forest.Tree()
        t.b = 2
        t._branch('a')

        t2 = forest.Tree()
        t2.b = 3
        t2._freeze()
        with self.assertRaises(ValueError):
            t2._update(t)


    def test_update_structfrozen(self):
        t = forest.Tree()
        t.b = 2

        t2 = forest.Tree()
        t2.b = 3
        t2._freeze_struct()
        t2._update(t)
        self.assertEqual(t.b, 2)

        t._branch('a')
        with self.assertRaises(ValueError):
            t2._update(t)

    def test_update_dict(self):
        d = {'b'        : 2,
             'abc.cde.d': 3,
             'abc.f'    : 4}
        t = forest.Tree()
        t._update(d, overwrite=True)

        for key, value in d.items():
            self.assertEqual(t[key], value)
        self.assertEqual(t.abc.cde.d, 3)
