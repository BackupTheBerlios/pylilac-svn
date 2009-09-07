#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for serialization and management of a language variety.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"


import utilities
from grammar import Grammar
from lexicon import Lexicon
from inflection import Inflections
from expression import ExpressionReader
import pickle

class Lect(object):
	def __init__(self, code = "zxx"):
		"""
		Create a lect object.
		A I{lect} is language variety; it can either be a spoken or a written form, and a colloquial, mediatic or standard form, and so on.

		It wraps serialization and high-level features.

		It contains three independent internal members:
			- L{lexicon<lexicon>}
			- L{grammar<grammar>}
			- L{inflections<inflection>}

		@type code: str
		@param code:
			A language code according to U{ISO<http://www.iso.org>} standard.

			For the language codes, refer to 639-3 specifications.

			A country/variety code and a representation system might be added: C{eng-US}, C{esp:ERG}, C{por-BR:IPA}
		"""
		self.code = code
		self.name = u""
		self.english_name = ""
		self.__p_o_s = ()
		self.__lemma_categories = {}
		self.__categories = {}
		self.grammar = Grammar(code)
		self.lexicon = Lexicon()
		self.inflections = Inflections()
		self.properties = {"separator" : " ", "capitalization" : "3"} #Lexical and Initials

	#[Properties

	def __get_grammar(self):
		return self.__grammar
	def __get_lexicon(self):
		return self.__lexicon
	def __get_inflections(self):
		return self.__inflections

	def __tuple(self):
		return (self.code, self.name, self.english_name, self.properties, self.__p_o_s, self.__lemma_categories, self.__categories, self.grammar, self.lexicon, self.inflections)

	def save(self, filename, reset = False):
		"""
		Save the lect on the file system.
		The format is a Python I{pickle} file compressed using the GZip algorithm at a medium compression.

		@param reset: If True, resets the lect, stripping out the compilation result of lexicon and grammar.
			In particular, resetting before saving can be beneficial for lects with large lexica.
			The default value is False and the lect is saved in its current status.
		@type reset: bool
		@param filename: The name of the file to generate.
		@type filename: str
		"""
		f = utilities.ZipFile(filename, "wb", 5)
		if reset:
			self.reset()
		pickle.dump(self.__tuple(), f, 2)
		f.flush()
		f.close()

	def load(self, filename):
		"""
		Load the lect from the file system.
		The format is a Python I{pickle} file compressed using the GZip algorithm.

		@param filename: The name of the file to load.
		@type filename: str
		"""
		f = utilities.ZipFile(filename, "rb")
		tuple = pickle.load(f)
		self.code, self.name, self.english_name, self.properties, self.__p_o_s, self.__lemma_categories, self.__categories, self.grammar, self.lexicon, self.inflections = tuple
		f.close()

	def append_p_o_s(self, name, lemma_categories = (), categories = ()):
		"""
		Append a part of speech, defined by its name and the categories of lemmas and words belonging to it.

		@param name: The name of the part of speech.
		@type name: str
		@param lemma_categories: The categories of lemmas belonging to the part of speech. Optional.
		@type lemma_categories: tuple of str
		@param categories: The categories of words belonging to the part of speech. Optional.
		@type categories: tuple of str
		"""
		if name in self.__p_o_s:
			raise KeyError("P.o.s. %s already exists" % name)
		self.__p_o_s += (name,)
		self.__lemma_categories[name] = tuple(lemma_categories)
		self.__categories[name] = tuple(categories)

	def get_p_o_s_names(self):
		"""
		Return the names of the parts of speech.

		@rtype: tuple of str
		"""
		return self.__p_o_s

	def get_categories(self, name):
		"""
		Return the lemma and word categories of a part of speech.

		@param name: The name of the part of speech.
		@type name: str

		@rtype: tuple of tuple of str
		@return: A tuple where the first element is a tuple containing the lemma categories and the second contains the word categories.
		"""
		if name not in self.__p_o_s:
			raise KeyError(name)
		return (self.__lemma_categories[name], self.__categories[name])

	def read(self, expression):
		"""
		Interprete an expression.

		@param expression: The expression to read.
		@type expression: C{str}

		@raise fsa.ParseError: If the grammar can not parse the expression.
		@raise expression.ExpressionParseError: If no syntax tree could be constructed.
		@raise tokenizer.UnknownTokenException: If an unexpected token is encountered.

		@return: The list of possible interpretations.
		@rtype: list of ParseTree
		"""

		if not isinstance(expression, unicode):
			raise TypeError("%s is not Unicode" % repr(expression))

		tokenizer = self.lexicon.compile(self.properties, False)
		parser = self.grammar.compile(False)
		er = ExpressionReader(tokenizer, parser)
		return er(expression)

	def compile(self, force = False):
		"""
		Compile the lexicon and the grammar.
		@param force: Recompile even if the result of a previous compilation was in memory.
		@type force: bool
		@raise grammar.GrammarError: If anomalies are encountered while precompiling the grammar.
		@raise tokenizer.UnknownTokenException: If an unknown character is encountered while precompiling the lexicon.
		@raise fsa.ParseError: If unexpected tokens or stops are encountered.
		"""
		self.lexicon.compile(self.properties, force)
		self.grammar.compile(force)

	def reset(self):
		"""
		Delete the internal results of the last compiling.
		"""
		self.lexicon.reset()
		self.grammar.reset()
