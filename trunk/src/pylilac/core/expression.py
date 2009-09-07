#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for expression management: reading (comprehension), translating, writing (composition).

The module offers the high-level interfaces to internal structures.

@summary: A module for expression management.
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

from fsa import ParseError, Parser
from utilities import SortedDict, Utilities


class ExpressionParseError(StandardError):
	"""
	An exception thrown when no syntax tree could be built.
	"""
	def __init__(self):
		"""
		Create a new instance of ExpressionParseError.
		"""
		self.parse_error = None
		self.__cardinality = 0

	def __len__(self):
		"""
		Return the length of the longest end-point encountered.
		@rtype: int
		"""
		if self.parse_error is None:
			return 0
		else:
			return len(self.parse_error)

	def include(self, parse_error):
		"""
		Append a parse exceptions to internal collection.

		@param parse_error: The parse error to include
		@type parse_error: L{ParseError<fsa.ParseError>}
		@see: L{ParseError<parser.ParseError>}
		"""
		if len(self) == len(parse_error):
			self.__cardinality += 1
		elif len(self) < len(parse_error):
			self.parse_error = parse_error
			self.__cardinality = 1

	def __str__(self):
		"""
		Return a string representation of the parse exceptions encountered while parsing the different tokenized interpretations.

		@return: The longest end-point (I{culdesacs}) and the count of end-points where the parsing of expressions interrupted.
		@rtype: str
		"""
		return str(self.parse_error) + "*" + str(self.__cardinality)

class ExpressionReader(object):
	"""
	An expression reader, combining a L{tokenizer<tokenizer.Tokenizer>} and a L{parser<fsa.Parser>}.
	"""
	def __init__(self, tokenizer, parser):
		"""
		Construct a new expression reader, coordinating the given L{tokenizer<tokenizer.Tokenizer>} and L{parser<fsa.Parser>}.

		@param tokenizer: The tokenizer (or scanner) to use.
		@type tokenizer: tokenizer.Tokenizer
		@param parser: The parser to use.
		@type parser: fsa.Parser
		"""
		self.__parser = parser
		self.__tokenizer = tokenizer

	def __call__(self, stream):
		"""
		Transform a stream into a list of syntax trees.

		The tokenizer forms streams into token sequences, then the parser forms them into syntax trees.

		@param stream: The stream to read, usually a string.
		@type stream: C{str}
		@raise ExpressionParseError: If no syntax tree could be constructed.
		@return: The list of possible interpretations.
		@rtype: list of ParseTree
		"""
		token_tree = self.__tokenizer(stream)
		results = []
		errors = ExpressionParseError()
		for expansion in token_tree.expand():
			try:
				rot = self.__parser(expansion)
				for recognition in rot.expand():
					pt = ParseTree()
					pt.add_recognition(recognition)
					results.append(pt)
			except ParseError, pe:
				errors.include(pe)
		if len(results)==0 and len(errors)>0:
			raise errors
		return results

class ParseTree(object):
	"""
	A parse tree to model an expression parsing.

	It is returned by the L{read<lect.Lect.read>} method of class C{Lect}.
	"""
	def __init__(self):
		"""
		Instantiate an empty tree.
		"""
		self.__contents = None
		self.__elements = SortedDict()

	def add_recognition(self, recognition):
		"""
		Add a list of expression parsings to the tree, calling the L{add} method.

		@param recognition: A list of expression parsings.
		@type recognition: list of C{(item, path)} tuples
		"""
		for item, path in recognition:
			self.add(item, path)

	def iter_children(self, path):
		"""
		Return an iterator to the subtrees below a given position.

		@param path: A tree path.
		@type path: list of str

		@return: The child trees below a given position.
		@rtype: iterator of ParseTree
		"""
		return self.__elements.iteritems()

	def subtree(self, path):
		"""
		Return the subtree at a given position.

		@param path: A tree path.
		@type path: list of str

		@return: The child tree at given position.
		@rtype: ParseTree
		"""
		st = self
		for segm in path:
			st = st.__elements[segm]
		return st

	def iter_items(self):
		"""
		Return an iterator to the items.

		@rtype: iterator of items
		"""
		for i in self.__contents:
			yield i

	def add(self, item, path):
		"""
		Add an expression parsing to the tree.

		If another item exists at the given position, the new item is appended, otherwise the new position is created with the item only.

		@param item: An expression parsing.
		@type item: C{(item, path)} tuples
		@param path: A tree path.
		@type path: list of str
		"""
		if len(path) == 0:
			return
		st = self
		for segm in path:
			if segm in st.__elements:
				st = st.__elements[segm]
			else:
				nst = ParseTree()
				st.__elements[segm] = nst
				st = nst
		if st.__contents is None:
			st.__contents = [item]
		else:
			st.__contents.append(item)

	def __repr__(self):
		"""
		Compute a representation for the parse tree.

		@rtype: str
		"""
		s = []
		if self.__elements:
			s.append(Utilities.dict_str(self.__elements))
		if self.__contents:
			s.append(str(self.__contents))
		return " = ".join(s)
