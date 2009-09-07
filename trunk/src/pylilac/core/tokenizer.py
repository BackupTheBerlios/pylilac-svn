#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A specialized parser for expressions.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

from fsa import FSA
from fsa import ParseError
from fsa import Parser
from optiontree import OptionTree

class UnknownTokenException(KeyError):
	"""
	Exception to indicate that a token was not expected.
	"""
	pass

class Tokenizer(Parser):
	"""
	A parser specialized for tokenizing strings.
	"""
	def __init__(self, map, options):
		"""
		Create a Tokenizer from a map.
		@param map: A map associating tokens to their possible recognitions.
		@type map: dict (unicode -> list of object)
		@param options: The options to use.
			Required information is:
				- A separator
		@type options: dict
		"""
		self._separator = options["separator"]
		fsa = self.__create_key_fsa(map)
		Parser.__init__(self, fsa)
		self.__dict = map

	def process(self, label, token):
		"""
		Override the generic behavior of a Parser.
		No processing required for tokenizing.
		@return: C{None}
		"""
		return None

	def __create_key_fsa(self, dict):
		"""
		Create an FSA from the keys in a map.
		"""
		def add_key(fsa, key):
			def add_new_transition(fsa, start, label, end, tag):
				for x in fsa.transitions_from(start):
					if x == (label, end, tag):
						return False
				fsa.add_transition(start, label, end, tag)

			for j in range(len(key), -1, -1):
				if j > 0 and fsa.has_state(key[:j]):
					break
			s = key + self._separator
			for i in range(j, len(s)):
				c = s[i]
				if i == len(s) - 1: #last step
					end = fsa.get_initial()
					tag = key
				else:
					end = s[:i + 1]
					tag = None
				add_new_transition(fsa, s[:i], c, end, tag)
		fsa = FSA()
		fsa.add_state("")
		fsa.set_initial("")
		fsa.set_final("")
		for k, v in dict.iteritems():
			if not isinstance(v, list):
				raise TypeError(v)
			add_key(fsa, k)
		return fsa

	def __call__(self, stream):
		"""
		Tokenize a character stream.
		@param stream: A character stream.
		@param stream: unicode
		@return: The result of the parsing.
		@rtype: OptionTree

		@raise tokenizer.UnknownTokenException: If an unexpected token is encountered.
		"""
		def explode_list(dct, lst, pos):
			t = OptionTree()
			if pos < len(lst):
				for obj in dct[lst[pos]]:
					c = explode_list(dct, lst, pos + 1)
					c.element = obj
					t.append(c)
			return t

		terminated = stream + self._separator
		try:
			p = Parser.__call__(self, terminated)
		except ParseError, pe:
			dead_end = len(pe) - 1
			rgt = max(stream.rfind(self._separator, 0, dead_end-1) + 1, 0)
			lft = stream.find(self._separator, dead_end + 1)
			if lft <> -1:
				ell = u"..."
			else:
				ell = u""
			raise UnknownTokenException(stream[rgt:lft] + ell)
		ot = OptionTree()
		for u in p.expand():
			ot.append(explode_list(self.__dict, [y[1] for y in u if y[1] is not None], 0))
		return ot
