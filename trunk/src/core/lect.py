#!/usr/bin/python
"""
A module for language variety serialization.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

import utilities
from grammar import Grammar
from lexicon import Lexicon
from flexion import Flexions
from expression import ExpressionReader
from gzip import GzipFile
import pickle

class Lect:
	def __init__(self, code = "zxx"):
		"""
                Create a language object.
		It encapsulate serialization and high-leven functionality.

                @type code: str
		@param code:
		    A language code according to U{ISO<http://www.iso.org>} standard.

		    For the language codes, refer to 639-3 specifications.
		    
		    A country/variant code and a representation system might be added: C{eng-US}, C{esp:ERG}, C{por-BR:IPA}
		"""
		self.code = code
		self.name = u""
		self.english_name = u""
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
		if filename is None:
			filename = "%s.lct" % self.code
		f = GzipFile(filename, "wb", 6)
		if compact:
			self.lexicon.reset()
			self.grammar.reset()
		pickle.dump(self.__tuple(), f, 2)
		f.flush()
		f.close()

	def load(self, filename):
		if filename is None:
			filename = "%s.lct" % self.code
		f = GzipFile(filename, "rb")
		tuple = pickle.load(f)
		self.code, self.name, self.english_name, self.__p_o_s, self.__lemma_categories, self.__categories, self.grammar, self.lexicon, self.properties = tuple
		f.close()

 	def append_p_o_s(self, name, lemma_categories = (), categories = ()):
 		if name in self.__p_o_s:
 			raise KeyError("P.o.s. %s already exists" % name)
 		self.__p_o_s += (name,)
 		self.__lemma_categories[name] = tuple(lemma_categories)
 		self.__categories[name] = tuple(categories)

	def get_p_o_s_names(self):
 		return self.__p_o_s
 		
	def get_categories(self, name):
 		if name not in self.__p_o_s:
 			raise KeyError(name)
 		return (self.__lemma_categories[name], self.__categories[name])
 		
	def read(self, expression):
		tokenizer = self.lexicon.compile(self.properties)
		parser = self.grammar.compile()
		er = ExpressionReader(tokenizer, parser)
		return er(expression)
	
	def compile(self, force = False):
		self.lexicon.compile(self.properties, force)
		self.grammar.compile(force)
			



def _test():
	pass
	
	

if __name__ == "__main__":
	_test()

