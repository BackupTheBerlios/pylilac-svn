#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A specialized parser for expressions.
"""

# General info
__version__ = "0.4"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

from fsa import FSA, Parser, ParseError
from optiontree import OptionTree

class UnknownTokenException(KeyError): 
	pass

class Tokenizer(Parser):
	def __init__(self, dict, properties):
		self._separator = properties["separator"]
		fsa = self.__create_key_fsa(dict)
		Parser.__init__(self, fsa)
		self.__dict = dict
		
	def process(self, label, token):
		"""
		No processing required for tokenizing.
		"""
		return None		

	def __create_key_fsa(self, dict):
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
					end = s[:i+1]
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
			rgt = max(stream.rfind(self._separator, 0, dead_end-1)+1,0)
			lft = stream.find(self._separator, dead_end+1)
			if lft<>-1:
				ell = u"..."
			else:
				ell = u""
			raise UnknownTokenException(stream[rgt:lft]+ell)
		ot = OptionTree()
		for u in p.expand():
			ot.append(explode_list(self.__dict, [y[1] for y in u if y[1] is not None], 0))
		return ot

def __test():
	t = Tokenizer({"a": ["1"], "b": ["2"]}, {"separator": " "})
	c = t("a a b b a a")
	print c
	t2 = Tokenizer({"ala": ["ALA"], "mi": ["MI"], "pona": ["PONA","BENE"], "mi ala": ["MIALA"]}, {"separator": " "})
	print t2("mi ala pona")
	t3 = Tokenizer({"a": ["1"], "bb": ["2"]}, {"separator": ""})
	c3 = t3("abba")
	print c3



if __name__ == "__main__":
	__test()
