import unittest
import pylilac
import unit
import use_cases.quenya as qya
import use_cases.latejami as ltq
import use_cases.tokipona as tko

class TestCases(unittest.TestCase):
	def setUp(self):
		self.subset = 7

	def test_units(self):
		if self.subset & 1:
			unit.run()

	def test_latejami(self):
		if self.subset & 2:
			ltq.run()

	def test_quenya(self):
		if self.subset & 2:
			qya.run()

	def test_tokipona(self):
		if self.subset & 2:
			tko.run()

		print "Succesfully completed testing routine."

if __name__ == '__main__':
    unittest.main()
