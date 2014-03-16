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

    def test_subinstance(self):
        tc = forest.Tree()
        tc._branch('a')
        tc._isinstance('a.b', int)
        tc.a.b = 1
        tc._isinstance('a.c', (int, float))
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

    def test_subvalidate(self):
        tc = forest.Tree()
        tc._branch('a')

        def validate_b(value):
            return 0 <= value <= 256
        tc._validate('a.b', validate_b)

        tc.a.b = 150
        with self.assertRaises(TypeError):
            tc.a.b = -1
        with self.assertRaises(TypeError):
            tc.a.b = 1000

        def validate_c(value):
            assert 0 <= value <= 256
            return True
        tc._validate('a.c', validate_c)

        tc.a.c = 150
        with self.assertRaises(TypeError):
            tc.a.c = -1


    def test_check_tree(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a._isinstance('c', (int, float))
        def validate_b(value):
            return 0 <= value <= 256
        tc.a._validate('b', validate_b)

        t2 = forest.Tree()
        t2._branch('a')
        t2.a.c = 2.0
        t2.a.b = 50
        t2._check(tc)

        t2.a.b = 350
        with self.assertRaises(TypeError):
            t2._check(tc)

        t2.a.b = 250
        t2.a.c = '23'
        with self.assertRaises(TypeError):
            t2._check(tc)

    def test_check_struct(self):
        tc = forest.Tree()
        tc._branch('a')

        t2 = forest.Tree()
        t2._branch('a')
        t2._check(tc, struct=True)

        t2._branch('b')
        with self.assertRaises(TypeError):
            t2._check(tc, struct=True)
        with self.assertRaises(TypeError):
            tc._check(t2, struct=True)
