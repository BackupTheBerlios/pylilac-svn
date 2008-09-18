#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A tokenizer to split a stream into tokens.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

from optiontree import OptionTree
from tokendict import TokenDict

class Tokenizer:
	def __init__(self, dict, properties = None):
		if properties is None:
			properties = {}
		separator = properties.get("separator", " ")
		alternative = properties.get("alternative", "Y")
		if alternative == "Y":
			self.__tokendict = TokenDict(dict, separator)
		else:
			self.__tokendict = BaseTokenDict(dict, separator)
	def _get_token(self, stream, position):
		return self.__tokendict.get_token(stream, position)
	def __call__(self, stream, position = 0):
		node = OptionTree()
		for token, new_pos in self._get_token(stream, position):
			successor = self(stream, new_pos)
			successor.element = token
			node.append(successor)
		return node

def __test():
	t = Tokenizer({"a": ["1"], "b": ["2"]})
	c = t("a a b b a a")
	print c
	t2 = Tokenizer({"ala": ["ALA"], "mi": ["MI"], "pona": ["PONA"], "mi ala": ["MIALA"]})
	print t2("mi ala pona")


if __name__ == "__main__":
	__test()
