from __future__ import print_function, division
import unittest
import pickle

import env
import forest

import os
import tempfile
from contextlib import contextmanager

def tempname():
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    return temp.name

class TestFiles(unittest.TestCase):

    def test_lines(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a.b = 1
        tc.a.d = [1, 2, 3]

        self.assertTrue(tc.__str__() in ['a.b=1\na.d=[1, 2, 3]', 'a.d=[1, 2, 3]\na.b=1'])

    def test_save(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a.b = '1'
        tc.a.d = [1, 2, 3]

        filename = tempname()
        tc._to_file(filename)

        with open(filename, 'r') as f:
            s = f.read()

        print(s)
        self.assertTrue(s in ["a.b='1'\na.d=[1, 2, 3]", "a.d=[1, 2, 3]\na.b='1'"])
        os.unlink(filename)

    def test_load(self):
        filename = tempname()
        with open(filename, 'w') as f:
            s = f.write('a.b=1\na.d=[1, 2, 3]')
        tc = forest.Tree._from_file(filename)

        self.assertTrue(tc.__str__() in ['a.b=1\na.d=[1, 2, 3]', 'a.d=[1, 2, 3]\na.b=1'])

        os.unlink(filename)

    def test_both(self):
        tc = forest.Tree()
        tc._branch('a')
        tc.a.b = 1
        tc.a.d = [1, 2, 3]

        filename = tempname()
        tc._to_file(filename)
        t2 = forest.Tree._from_file(filename)

        self.assertEqual(tc, t2)

class TestPickle(unittest.TestCase):

    def test_pickle(self):
        t = forest.Tree()
        t.a = forest.Tree()
        t.a.b = 1
        t.a.c = '2'
        t.a._branch('efg')
        t.a.efg.h = [2, 3, 4]
        t['b.farm'] = None

        s = pickle.dumps(t)
        t2 = pickle.loads(s)
        self.assertEqual(t, t2)

        filename = tempname()
        with open(filename, 'wb') as f:
            pickle.dump(t, f)

        with open(filename, 'rb') as f:
            t2 = pickle.load(f)

        self.assertEqual(t, t2)

if __name__ == '__main__':
    unittest.main()
