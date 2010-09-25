#!/usr/bin/python

import unittest
import unit

class AutomaticTest(unittest.TestCase):
    def test_automatic(self):
        unit.run()

    def test_smoke_test(self):
        from pylilac.core.lect import Lect
        l = Lect("abc")
        self.assertTrue(l is not None, "Instantiation faile")


if __name__ == '__main__':
    from os import chdir
    from sys import path
    chdir("../..")
    path.append("trunk/src")
    #TODO: this above doesn't work!
    unittest.main()

