from __future__ import print_function, division
import unittest

import env
import forest


class TestIterators(unittest.TestCase):

    def test_kvi(self):
        tc = forest.Tree()
        tc._branch('a')

        tc.a['b'] = 1
        tc.color = 'blue'

        self.assertEqual({'a.b', 'color'}, set(tc._keys()))
        self.assertEqual({1, 'blue'}, set(tc._values()))
        self.assertEqual({('a.b', 1), ('color', 'blue')}, set(tc._items()))

if __name__ == '__main__':
    unittest.main()