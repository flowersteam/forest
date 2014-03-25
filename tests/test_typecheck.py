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

    def test_docstring(self):
        tc = forest.Tree()
        tc._branch('a')
        tc._docstring('a.b', 'a nice descriptive docstring')
        tc._docstring('a.c', """Another one""")

        self.assertEqual(tc._docstring('a.b'), 'a nice descriptive docstring')
        self.assertEqual(tc._docstring('a.c'), 'Another one')
        self.assertEqual(tc._docstring('a.f'), None)

    def test_describe(self):
        tc = forest.Tree()
        tc._branch('a')
        tc._describe('a.b', 'a nice descriptive docstring', int)
        tc._describe('c.b', 'can describe things on non existing branches', int)
        with self.assertRaises(TypeError):
            tc.a.b = 1.0
        tc.a.b = 1

        def validate_ac(value):
            return 0 <= value <= 256
        tc._describe('a.c', """Another one""", instanceof=int, validate=validate_ac)

        self.assertEqual(tc._docstring('a.b'), 'a nice descriptive docstring')
        self.assertEqual(tc._docstring('a.c'), 'Another one')
        with self.assertRaises(TypeError):
            tc.a.c = 1.0

        tc._describe('a.c', """A different one""", float, validate=validate_ac)
        self.assertEqual(tc._docstring('a.c'), 'A different one')
        tc.a.c = 1.0
        with self.assertRaises(TypeError):
            tc.a.c = -50.0

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

    def test_check_struct(self):
        t = forest.Tree()
        t._strict()

        t._isinstance('a', int)
        t.a = 1
        with self.assertRaises(TypeError):
            t.b = 1

        def validate_b(value):
            return 0 <= value <= 256
        t._validate('b', validate_b)
        t.b = 1

    def test_collision(self):
        t = forest.Tree()
        t._isinstance('a', int)
        with self.assertRaises(ValueError):
            t._isinstance('a.b', int)

    def test_complete(self):
        t = forest.Tree()

        t._isinstance('f', int)
        self.assertEqual(t._complete(), set(('f')))

        t._docstring('a.b', int)
        self.assertEqual(t._complete(), set(('f', 'a.b')))

        def validate_c(value):
            return 0 <= value <= 256
        t._validate('a.e.c', validate_c)
        self.assertEqual(t._complete(), set(('f', 'a.b', 'a.e.c')))

        t._describe('c.b', docstring='can describe things on non existing branches', instanceof=int)
        self.assertEqual(t._complete(), set(('f', 'a.b', 'a.e.c', 'c.b')))

        t.a.b = 2
        self.assertEqual(t._complete(), set(('f', 'a.e.c', 'c.b')))
        t.f = 42
        self.assertEqual(t._complete(), set(('a.e.c', 'c.b')))

    def test_update(self):
        t = forest.Tree()
        t._isinstance('f', int)
        t2 = forest.Tree(strict=True)
        with self.assertRaises(TypeError):
            t2.f = 2
        t2._update(t, descriptions=False)
        with self.assertRaises(TypeError):
            t2.f = 2
        t2._update(t)
        t2.f = 2

if __name__ == '__main__':
    unittest.main()