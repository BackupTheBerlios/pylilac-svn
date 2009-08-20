#!/usr/bin/python
"""
A module for language variety serialization.

"""

# General info
__version__ = "0.1"
__author__ = "Paolo Olmino"
__url__ = "http://pylilac.berlios.de/"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

import utilities
from grammar import Grammar
from lexicon import Lexicon
from flexion import Flexions
from expression import ExpressionReader
import pickle

class Lect:
	def __init__(self, code = "zxx"):
		"""
		Create a lect object.
		A I{lect} is a variety of a language; it can either be either a spoken or a written form, and colloquial, mediatic or standard form, and so on.
		
		It encapsulate serialization and high-level functionalities.

		@type code: str
		@param code:
		    A language code according to U{ISO<http://www.iso.org>} standard.

		    For the language codes, refer to 639-3 specifications.
		    
		    A country/variant code and a representation system might be added: C{eng-US}, C{esp:ERG}, C{por-BR:IPA}
		"""
		self.code = code
		self.name = u""
		self.english_name = ""
		self.__p_o_s = ()
		self.__lemma_categories = {}
		self.__categories = {}
		self.grammar = Grammar(code)
		self.lexicon = Lexicon()
		self.flexions = Flexions()
		self.properties = {"separator" : " ", "capitalization" : "3"} #Lexical and Initials

	def __tuple(self):
		return (self.code, self.name, self.english_name, self.__p_o_s, self.__lemma_categories, self.__categories, self.grammar, self.lexicon, self.properties)

	def save(self, filename, compact = False):
		"""
		Save the lect on the file system.
		"""
		f = utilities.ZipFile(filename, "wb", 6)
		if compact:
			self.lexicon.reset()
			self.grammar.reset()
		pickle.dump(self.__tuple(), f, 2)
		f.flush()
		f.close()

	def load(self, filename):
		"""
		Load the lect from the file system.
		"""
		f = utilities.ZipFile(filename, "rb")
		tuple = pickle.load(f)
		self.code, self.name, self.english_name, self.__p_o_s, self.__lemma_categories, self.__categories, self.grammar, self.lexicon, self.properties = tuple
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
		tokenizer = self.lexicon.compile(self.properties)
		parser = self.grammar.compile()
		er = ExpressionReader(tokenizer, parser)
		return er(utilities.Utilities.unicode(expression))
	
	def compile(self, force = False):
		self.lexicon.compile(self.properties, force)
		self.grammar.compile(force)
			



def _test():
	pass
	
	

if __name__ == "__main__":
	_test()

