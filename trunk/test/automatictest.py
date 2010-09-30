#!/usr/bin/python

import unittest

class AutomaticTest(unittest.TestCase):
    def test_automatic(self):
        pass

    def test_smoke_test(self):
        from pylilac.core.lect import Lect
        l = Lect("abc")
        self.assertTrue(l is not None, "Instantiation failed")


if __name__ == '__main__':
    unittest.main()
