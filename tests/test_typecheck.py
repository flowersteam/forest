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

        with self.assertRaises(TypeError):
            tc.a.b = 'abc'

        with self.assertRaises(TypeError):
            tc.a.b = 1.0

    def test_validate(self):
        tc = forest.Tree()
        tc._branch('a')
        def validate_a(value):
            return 0 <= value <= 256
        tc.a._validate('b', validate_a)

        tc.a.b = 150
        with self.assertRaises(TypeError):
            tc.a.b = -1
        with self.assertRaises(TypeError):
            tc.a.b = 1000
