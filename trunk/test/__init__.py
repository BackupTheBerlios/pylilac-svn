#!/usr/bin/python

"""
Run tests.
"""

from sys import path
from optparse import OptionParser
path.insert(0, '../src')
import use_cases
import unit
import pylilac

def run(subset = 255):
	print "***********************************************"
	print "*********  R U N N I N G   T E S T S  *********"
	print "***********************************************"
	print ""
	if subset & 1:
		print "Unit tests...."
		unit.run()
	if subset & 2:
		print "Unit use cases...."
		use_cases.run()
	if subset & 4:
		print "Language Architect...."
		pylilac.run_la()
	print "Succesfully completed testing routine."


if __name__ == "__main__":
	parser = OptionParser("usage: %prog [1 = unit | 2 = use cases | 4 = LA]")

	_, args = parser.parse_args()

	if len(args)>1:
		parser.print_help()
		sys.exit(0)	

	subset = 3
	if len(args)>0:
		subset = int(args[0])
	run(subset)

