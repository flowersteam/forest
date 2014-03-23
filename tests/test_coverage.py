from __future__ import print_function, division
import unittest

import env
import forest

class TestCoverage(unittest.TestCase):

    def test_coverage(self):
        tc = forest.Tree()
        tc._branch('a')
        with self.assertRaises(KeyError):
            tc._coverage('a.b')
        tc.a.b = 1
        self.assertEqual(tc._coverage('a.b'), 0)
        tc.a.b
        self.assertEqual(tc._coverage('a.b'), 1)

    def test_history(self):
        tc = forest.Tree()
        tc._branch('a')
        with self.assertRaises(KeyError):
            tc._history('a.b')
        tc.a.b = 1
        self.assertEqual(tc._history('a.b'), [1])
        tc.a.b = '2'
        self.assertEqual(tc._history('a.b'), [1, '2'])

if __name__ == '__main__':
    unittest.main()
