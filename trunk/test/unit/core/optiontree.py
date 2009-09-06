#!/usr/bin/python

"""
A module for testing the OptionTree utility class.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.optiontree import *




def run():
	_iam = OptionTree(None)
	_the = _iam.append(OptionTree("the"))
	_queen = _the.append(OptionTree("queen"))
	_queen.append(OptionTree("of",[OptionTree("hearts"), OptionTree("hearts-2")]))
	_qoh = _the.append(OptionTree("queen of hearts"))
	print _iam
	print "\n"
	print _iam.expand()
	print not not _iam

if __name__ == "__main__":
	run
