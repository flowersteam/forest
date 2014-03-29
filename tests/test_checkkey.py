from __future__ import print_function, division
import unittest

import env
import forest

class TestCheckKey(unittest.TestCase):

    def test_leaf(self):
        forest.Tree._check_key('abcde', leaf=True)
        forest.Tree._check_key('Abcde', leaf=True)

        with self.assertRaises(ValueError):
            forest.Tree._check_key('abc de', leaf=True)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('1bc de', leaf=True)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('1bc\de', leaf=True)

        with self.assertRaises(ValueError):
            forest.Tree._check_key('_abcde', leaf=True)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('_', leaf=True)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('__flag', leaf=True)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('_1toad', leaf=True)

    def test_key(self):
        forest.Tree._check_key('abc.de', leaf=False)
        forest.Tree._check_key('Abcde', leaf=False)

        with self.assertRaises(ValueError):
            forest.Tree._check_key('abc de', leaf=False)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('1bc de', leaf=False)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('1bc\de', leaf=False)

        with self.assertRaises(ValueError):
            forest.Tree._check_key('_abcde', leaf=False)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('_', leaf=False)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('__flag', leaf=False)
        with self.assertRaises(ValueError):
            forest.Tree._check_key('_1toad', leaf=False)


    
if __name__ == '__main__':
    unittest.main()
