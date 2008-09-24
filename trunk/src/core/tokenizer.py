#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A specialized parser for expressions.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

from fsa import FSA, Parser, ParseError
from optiontree import OptionTree

class UnknownTokenException(KeyError): 
	pass

class Tokenizer(Parser):
	def __init__(self, dict, properties = None):
		if properties is None:
			properties = {}
		self._separator = properties.get("separator", " ")
		fsa = self.__create_key_fsa(dict)
		Parser.__init__(self, fsa)
		self.__dict = dict

	def __create_key_fsa(self, dict):
		def add(fsa, key):
			s = key + self._separator
			for i, c in enumerate(s):
				if i == len(s) - 1:
					fsa.add_transition(s[:i], c, fsa.get_initial(), key)
					break
				else:
					fsa.add_transition(s[:i], c, s[:i+1])
		fsa = FSA()
		fsa.add_state("")
		fsa.set_initial("")
		fsa.set_final("")
		for k, v in dict.iteritems():
			if type(v) is not list:
				raise TypeError(v)
			add(fsa, k)
		return fsa

	def __call__(self, stream):
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
			raise UnknownTokenException(stream[len(pe) - 1 :])
		ot = OptionTree()
		for u in p.expand():
			ot.append(explode_list(self.__dict, [y[1] for y in u if y[1] is not None], 0))
		return ot

def __test():
	t = Tokenizer({"a": ["1"], "b": ["2"]})
	c = t("a a b b a a")
	print c
	t2 = Tokenizer({"ala": ["ALA"], "mi": ["MI"], "pona": ["PONA","BENE"], "mi ala": ["MIALA"]})
	print t2("mi ala pona")
	print t2("mi kontento")


if __name__ == "__main__":
	__test()
