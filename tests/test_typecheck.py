from __future__ import print_function, division
import unittest

import env
import forest

class TestTypeCheck(unittest.TestCase):

    def test_instance(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a._isinstance('b', int)
        tc.a.b = 1
        tc.a._isinstance('c', (int, float))
        tc.a.c = 1
        tc.a.c = 1.5

        with self.assertRaises(TypeError):
            tc.a.b = 'abc'

        with self.assertRaises(TypeError):
            tc.a.b = 1.0

    def test_validate(self):
        tc = forest.Tree()
        tc._branch('a')

        def validate_b(value):
            return 0 <= value <= 256
        tc.a._validate('b', validate_b)

        tc.a.b = 150
        with self.assertRaises(TypeError):
            tc.a.b = -1
        with self.assertRaises(TypeError):
            tc.a.b = 1000

        def validate_c(value):
            assert 0 <= value <= 256
            return True
        tc.a._validate('c', validate_c)

        tc.a.c = 150
        with self.assertRaises(TypeError):
            tc.a.c = -1
