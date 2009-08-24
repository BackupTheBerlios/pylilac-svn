#!/usr/bin/python

"""
A module for the OptionTree utility class.
"""

# General info
__version__ = "0.4"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

from utilities import Utilities

class OptionTree:
	"""
	A container for the possible expansions of a sequence.
	It can be populated recursively.
	"""
	def __init__(self, element = None, successors = []):
		self.element = element
		if not successors:
			self.__successors = []
		else:
			self.__successors = successors

	def append(self, successor):
		if not isinstance(successor, OptionTree):
			raise TypeError(successor)
		self.__successors.append(successor)
		return successor

	def __repr__(self):
		if self.element:
			e = `self.element`
		else:
			e = ""
	
		if len(self.__successors)==0:
			c = ""
		elif len(self.__successors)==1:
			if len(e) > 0: e += " "
			c = repr(self.__successors[0])
		else:
			if len(e) > 0: e += " "
			c = `self.__successors`
		return e + c

	def __len__(self):
		return len(self.__successors)

	def __nonzero__(self):
		if self.__successors or self.element:
			return True
		else:
			return False

	def expand(self):
		if self.element is None:
			head = []
		else:
			head = [self.element]
		if self.__successors:
			return [head + x for x in reduce(list.__add__, [successor.expand() for successor in self.__successors])]
		else:
			return [head]


def _test():
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
	_test()
