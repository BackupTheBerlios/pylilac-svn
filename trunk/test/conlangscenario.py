#!/usr/bin/python

import unittest

import cases.quenya as qya
import cases.latejami as ltq
import cases.tokipona as tko

class ConLangScenario(unittest.TestCase):
	def setUp(self):
		self.subset = 7

	def test_latejami(self):
		if self.subset & 1:
			ltq.run()

	def test_quenya(self):
		if self.subset & 2:
			qya.run()

	def test_tokipona(self):
		if self.subset & 4:
			tko.run()

if __name__ == '__main__':
	unittest.main()

