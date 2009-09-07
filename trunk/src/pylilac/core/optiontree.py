#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the OptionTree utility class.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"


class OptionTree(object):
	"""
	A container for the explosion of alternative sequences.
	It can be populated recursively.
	The option tree:
		>>>	A B C [DE, D [E1, E2]]

	Can be exploded into the sequences:
		>>> [A, B, C, DE]
		>>> [A, B, C, D, E1]
		>>> [A, B, C, D, E2]

	"""
	def __init__(self, element=None, successors=[]):
		"""
		Create an option tree containing the given element followed by the give successors.
		@param element: The sequence element.
		@type element: object
		@param successors: The following option trees.
		@type successors: list of OptionTree
		"""
		self.element = element
		if not successors:
			self.__successors = []
		else:
			self.__successors = successors

	def append(self, successor):
		"""
		Append a possible successor.

		@param successor: A possible following option tree.
		@type successor: OptionTree
		@return: The same option tree for recursive use.
		@rtype: OptionTree
		"""
		if not isinstance(successor, OptionTree):
			raise TypeError(successor)
		self.__successors.append(successor)
		return successor

	def __repr__(self):
		"""
		Return a string representation of the option tree.
		Blanks separe concatenated elements, while square brackets surround options separated by commas.
		@rtype: str
		"""
		e = []
		if self.element:
			e.append(`self.element`)
		if len(self.__successors) == 0:
			pass
		elif len(self.__successors) == 1:
			e.append(`self.__successors[0]`)
		else:
			e.append(`self.__successors`)
		return " ".join(e)

	def __len__(self):
		"""
		Return the count of possible successors.
		rtype: int
		"""
		return len(self.__successors)

	def __nonzero__(self):
		if self.__successors or self.element:
			return True
		else:
			return False

	def expand(self):
		"""
		Explode an option tree recursively.
		@return: A list of options; each option is a possible sequence of elements.
		@rtype: list of list of object
		"""
		if self.element is None:
			head = []
		else:
			head = [self.element]
		if self.__successors:
			return [head + x for x in reduce(list.__add__, [successor.expand() for successor in self.__successors])]
		else:
			return [head]
