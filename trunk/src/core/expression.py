﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for expression management: reading (comprehension), translating, writing (composition).

The module offers the high-level interfaces to internal structures.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}

"""

__docformat__ = "epytext en" 

from fsa import ParseError
from utilities import SortedDict


class ExpressionParseError(StandardError):
	"""
	An exception thrown when no syntax tree could be built.

	"""
	def __init__(self):
		self.parse_error = None
		self.potence = 0

	def __len__(self):
		if self.parse_error is None:
			return 0
		else:
			return len(self.parse_error)
		
	def include(self, parse_error):
		if len(self) == len(parse_error):
			self.potence += 1
		elif len(self) < len(parse_error):
			self.parse_error = parse_error
			self.potence = 1
			
	def __str__(self):
		"""
		Return a synthesis of the parse exceptions encountered while parsing the different tokenized interpretations.

		@return: A list of the main end-points (I{culdesacs}) where the parsing of expressions interrupted.
		@rtype: C{str}
		@see: L{ParseError<parser.ParseError>}
		"""
		return str(self.parse_error) + "*" + str(self.potence)
		
class ExpressionReader:
	"""
	An expression reader, combining a L{tokenizer<tokenizer.Tokenizer>} and a L{parser<fsa.Parser>}.

	"""
	def __init__(self, tokenizer, parser):
		"""
		Construct a new expression reader, coordinating the given L{tokenizer<tokenizer.Tokenizer>} and L{parser<fsa.Parser>}.

		@param tokenizer: The tokenizer (or scanner) to use.
		@type tokenizer: tokenizer.Tokenizer
		@param parser: The parser to use.
		@type parser: parser.Parser

		"""
		self.__parser = parser
		self.__tokenizer = tokenizer

	def __call__(self, stream):
		"""
		Transform a stream into a list of syntax trees.

		The tokenizer transforms streams into token sequences, then the parser transforms them into syntax trees.

		@param stream: The stream to read, usually a string.
		@type stream: C{str}
		@raise ExpressionParseError: If no syntax tree could be constructed.
		@return: A list of syntax trees
		@rtype: C{list} of C{OptionTree}
		"""
		token_tree = self.__tokenizer(stream)
		results = []
		errors = ExpressionParseError()
		for expansion in token_tree.expand():
			try:
				rot = self.__parser(expansion)
				for recognition in rot.expand():
					results.append(ParseTree(recognition))
			except ParseError, pe:
				errors.include(pe)
		if len(results)==0 and len(errors)>0:
			raise errors
		return results

class ParseTree:
	def __init__(self, recognition = None):
		self.__content = None
		self.__elements = SortedDict()
		if recognition:
			self.add_recognition(recognition)

	def add_recognition(self, recognition):
		for item, path in recognition:
			self.add(item, path)

	def get(self, path):
		st = self
		for segm in path:
			st = st.__elements[segm]
		return st.__content
		
	def add(self, item, path):
		st = self
		for segm in path:
			if st.__elements.has_key(segm):
				st = st.__elements[segm]
			else:
				nst = ParseTree()
				st.__elements[segm] = nst
				st = nst
		st.__content = item

	def __repr__(self):
		s = []
		if self.__content:
			s.append(str(self.__content))
		else:
			s.append("(")
			c = False
			for k, v in self.__elements.iteritems():
				if c:
					s.append(", ")
				else:
					c = True
				s.append(k+" : "+str(v))
			s.append(")")
		return "".join(s)
		

def __test():
	pass

if __name__ == "__main__":
	__test()
