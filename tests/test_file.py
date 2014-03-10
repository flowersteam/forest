from __future__ import print_function, division
import unittest

import env
import forest

class TestFiles(unittest.TestCase):

    def test_lines(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a.b = 1
        tc.a.d = [1, 2, 3]

        self.assertEqual(tc.__str__(), 'a.b=1\na.d=[1, 2, 3]')
