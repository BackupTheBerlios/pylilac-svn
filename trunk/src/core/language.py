#!/usr/bin/python
"""
A module for language serialization.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

import utilities
from grammar import Grammar
from lexicon import Lexicon
from expression import ExpressionReader
from gzip import GzipFile
import pickle

class Language:
	def __init__(self, code):
		"""
                Create a language object.
		It encapsulate serialization and high-leven functionality.

                @type code: str
		@param code:
		    A language code according to U{ISO<http://www.iso.org>} standard.

		    For the language codes, refer to 639-3 specifications.
		"""
		self.code = code
		self.name = unicode(code)
		self.english_name = None
		self.properties = {"separator": " "}
		self.p_o_s = []
		self.categories = {}
		self.grammar = Grammar(code)
		self.lexicon = Lexicon()


	def __tuple(self):
		return (self.code, self.name, self.english_name, self.properties, self.p_o_s, self.categories, self.grammar, self.lexicon)

	def save(self, filename = None):
		if filename is None:
			filename = "%s.lg" % self.code
		f = GzipFile(filename, "wb")
		pickle.dump(self.__tuple(), f, 2)
		f.flush()
		f.close()

	def load(self, filename = None):
		if filename is None:
			filename = "%s.lg" % self.code
		f = GzipFile(filename, "rb")
		tuple = pickle.load(f)
		self.code, self.name, self.english_name, self.properties, self.p_o_s, self.categories, self.grammar, self.lexicon = tuple
		f.close()

	def read(self, stream):
		lexical_fsa = self.lexicon.compile(self.properties)
		grammatical_fsa = self.grammar.compile()
		er = ExpressionReader(lexical_fsa, grammatical_fsa)
		return er(stream)
			



def _test():
	pass
	
	

if __name__ == "__main__":
	_test()

