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
		f = open(filename, "wb")
		pickle.dump(self.__tuple(), f, 2)
		f.flush()
		f.close()

	def load(self, filename = None):
		if filename is None:
			filename = "%s.lg" % self.code
		f = open(filename, "rb")
		tuple = pickle.load(f)
		self.code, self.name, self.english_name, self.properties, self.p_o_s, self.categories, self.grammar, self.lexicon = tuple
		f.close()

	def read(self, stream):
		tokenizer = self.lexicon.compile(self.properties)
		fsa = self.grammar.compile()
		er = ExpressionReader(tokenizer, fsa)
		return er(stream)
			



def _test():
	from bnf import Reference, Literal, EPSILON_SYMBOL
	from lexicon import Word, Headword, Lexicon, Particle
	from wordfilter import WordCategoryFilter, WordFilter, AttributeFilter

	if True:
		g = Grammar("Toki pona")
		g["sentence"] = Reference("subject") + Reference("predicate")
		g["predicate"] = Reference("transitive-verb*") + Reference("object") 
		g["predicate"] = Reference("intransitive-verb*") 
		g["predicate"] = Reference("pn")
		g["subject"] = Reference("pronoun*") | Reference("noun*") + WordFilter(Particle("li", 1))
		g["object"] = Reference("noun*")
		g["pronoun*"] = WordCategoryFilter("pronoun")
		g["transitive-verb*"] = WordCategoryFilter("verb", {"transitive": "y"})
		g["intransitive-verb*"] = WordCategoryFilter("verb", {"transitive": AttributeFilter("ni", ["y"])})
		g["noun*"] = WordCategoryFilter("noun")
		g["noun**"] = WordCategoryFilter("noun")
		g["pn"] = WordCategoryFilter("adjective")
	
		lx = Lexicon()
		lx.add_word(Word("mi", Headword("mi", 1, "pronoun", None, "bavi")))
		lx.add_word(Word("sina", Headword("sina", 1, "pronoun", None, "zavi")))
		lx.add_word(Word("suli", Headword("suli", 1, "adjective", None, "kemo")))
		lx.add_word(Word("suna", Headword("suna", 1, "noun", None, "Lakitisi")))
		lx.add_word(Word("telo", Headword("telo", 1, "noun", None, "bocivi")))
		lx.add_word(Word("moku", Headword("moku", 1, "verb", {"transitive": "n"}, "fucala")))
		lx.add_word(Word("moku", Headword("moku", 2, "verb", {"transitive": "y"}, "fucalinza")))
		lx.add_word(Word("jan", Headword("jan", 1, "noun", None, "becami")))
		lx.add_word(Particle("li",1))
		#import pdb
		#pdb.set_trace()
	
		l = Language("tko")
		l.name = "Toki Pona"
		l.grammar = g
		l.lexicon = lx
		l.save()
		del l

	from bnf import OPTIONAL_CLOSURE
	
	tko = Language("tko")
	tko.load()
	print tko.grammar.compile()
	print tko.read("mi moku telo")
	print tko.read("mi moku")
	print tko.read("suna li suli")
	
	aa = Language("aa")
	aa.grammar["sentence"] = Reference("pre") * OPTIONAL_CLOSURE + Reference("main") + Reference("post") * OPTIONAL_CLOSURE
	aa.grammar["pre"] = WordFilter(Particle("e",1)) | WordFilter(Particle("u",1))
	aa.grammar["post"] = aa.grammar["pre"]
	aa.grammar["main"] = WordFilter(Particle("e",1)) | WordFilter(Particle("o",1))
	# "e can only be a main"
	# "e e can be pre main or main post"
	aa.lexicon.add_word(Particle("e",1))
	aa.lexicon.add_word(Particle("o",1))
	aa.lexicon.add_word(Particle("u",1))
	print aa.grammar
	print aa.grammar.compile()
	print aa.read("e e")
	print aa.read("e")
#	print aa.read("o o")
#	print aa.read("u")
	
	

if __name__ == "__main__":
	_test()

