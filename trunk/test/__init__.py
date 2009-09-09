#!/usr/bin/python
import unittest
from os import chdir
from sys import path

chdir("../..")
path.append("trunk/src")
import test_cases
suite = unittest.TestLoader().loadTestsFromTestCase(test_cases.TestCases)
unittest.TextTestRunner(verbosity=4).run(suite)

