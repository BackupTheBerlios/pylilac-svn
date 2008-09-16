#!/usr/bin/python
"""
A module for implementation of token dictionaries.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"


class UnknownTokenException(KeyError):
	pass

class BaseTokenDict:
	"""
	A token dictionary to tokenize a stream.

	"""
	def __init__(self, dict, separator):
		self.__data = {}
		for k, v in dict.iteritems():
			self[k] = v
		self._separator = separator
	def __setitem__(self, key, value):
		if type(value) is not list:
			raise TypeError(value)
		self.__data[key] = value
	def __getitem__(self, key):
		return self.__data[key]
	def __contains__(self, key):
		return key in self.__data
	def __len__(self):
		return len(self.__data)
	def _strip_separator(self, stream, position):
		if self._separator:
			length = len(self._separator)
			while stream[position : position+length] == self._separator:
				position += length
		return position
	def get_token(self, stream, position):
		"""
		Read the next token from the stream, starting from a given position.
		"""
		position = self._strip_separator(stream, position)
		weight = len(stream) - position
		if weight <= 0:
			return []
		while weight > 0:
			key = stream[position : position+weight]
			if key in self:
				return [(v, position+weight) for v in self[key]]
			if self._separator:
				sep = stream.rfind(self._separator, position, position+weight)
				weight = sep - position
			else:
				weight -= 1
		raise UnknownTokenException(stream[position:])
	def __repr__(self):
		return `self.__data`

class TokenDict(BaseTokenDict):
	"""
	A token dictionary to tokenize a stream, returning all matching alternatives.

	@todo: improved algorithm using an FSA.
	"""
	def get_token(self, stream, position):
		possibilities = []
		position = self._strip_separator(stream, position)
		weight = len(stream) - position
		found = weight <= 0
		while weight > 0:
			key = stream[position : position+weight]
			if key in self:
				values = self[key]
				found = True
				for v in values:
					possibilities.append((v, position+weight))
			if self._separator:
				sep = stream.rfind(self._separator, position, position+weight)
				weight = sep - position
			else:
				weight -= 1
		if found:
			return possibilities
		else:
			raise UnknownTokenException(stream[position:])


def __test():
	pass

if __name__ == "__main__":
	__test()
