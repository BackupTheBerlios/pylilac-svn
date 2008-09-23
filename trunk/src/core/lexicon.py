#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for lexicon management: Word and Headword.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""
#TODO: meaning must be extended to real translation

__docformat__ = "epytext en"

from utilities import Utilities
from tokenizer import Tokenizer

class ExistingHeadwordError(ValueError):
	pass

class Headword:
	"""
	A single unit of language, with no functional decoration.
	
	Usually, headword are the I{entry words} in dictionaries and encyclopediae.
	"""
	def __init__(self, entry_word, id, p_o_s, categories = None, gloss = None):
		"""
		Create a headword in a specific language for the I{entry word} specified.

		Example::
			Headword(u"heart", 1, "noun", None, "kawcesi") #heart, the heart organ in English, with no classification.
			Headword(u"heart", 2, "noun", None, "kawcijumi") #heart, the heart shape in English.
			Headword(u"hɑɹt", 1, "noun", None ,"kawcesi") #/h\u0251\u0279t/, /hɑɹt/, the heart organ phonic representation in General American English
			Headword(u"moku", 1, "verb", {"transitive": "n"}, "fucala") #moku, "to eat" in Toki Pona

		@type entry_word: unicode
		@param entry_word: 
		    A U{Unicode<http://www.unicode.org>} representation of the entry word, either graphical or phonical.

		    The representation of a word can be its written form or its spoken form, refer to Unicode conventions for the proper encoding.

		    For phonical representations, the alphabet of the U{IPA<http://www.arts.gla.ac.uk/IPA>} (Internationa Phonetic Association) is the standard, though some kind of extension could be advisable; the representation should be a phonetic transcription.
		@type id: number
		@param id: 
		    A unique id to distinguish different headwords having identical representation in a given language.

		    Major meanings in dictionaries are usually associated to different id's.
		@type p_o_s: str
		@param p_o_s:
		    A string which indicates the I{part of speech} to which the headword belongs to in the specific language.

		    The I{part of speech} is the general classification of the word: usually it distinguish nouns from verbs &c..
		@type categories: dict (srt, str)
		@param categories:
		    The categories of the headword; default is the empty dictionary.

		    categories can specify better the features of a particular I{part of speech}.
		@type gloss: str
		@param gloss:
		    The meaning and the translation technique, referring to the I{interlingua}.

		    For the interlingua to use, Latejami or its successors are recommended.

		"""
		self.entry_word = entry_word
		self.id = Utilities.nvl(id, 1)
		self.p_o_s = p_o_s
		self.categories = Utilities.nvl(categories, {})
		self.gloss = gloss

	def __eq__(self, other):
		"""
		Compares memberwise two headwords.
		"""
		if isinstance(other, Headword):
			return self.entry_word == other.entry_word and self.id == other.id and self.p_o_s == other.p_o_s and self.categories == other.categories
		else:
			return False
	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.entry_word) ^ self.id

	def __repr__(self):
		"""
		Give a verbose representation for a headword.
		"""
		return "%s%d~%s" % (self.entry_word, self.id, self.gloss)

	def __str__(self):
		"""
		Give a concise representation for a headword.

		@return: the entry word.
		"""
		return "%s%d" % (self.entry_word, self.id)

class Word:
	"""
	A single unit of language which has meaning and can be expressed.
	"""
	def __init__(self, form, headword, categories = None):
		"""
		Create a word with its form, its L{headword<Headword>} and its categories.

		Example::
			Word(u"heart", Headword("eng", u"heart", 1, "noun", None, "kawcesi"))
			Word(u"hearts", headwords["eng", u"heart", 1], {"number": "pl"})
			Word(u"hɑɹts", hw, {"number": "pl"})
			Word(u"moku", "tko", moku)
	
		@type form: unicode
		@param form:
		    The traditional, standard or neutral form of the word, either graphical or phonical.
		@type headword:  Headword
		@param headword:
		    A headword
		@type categories: dict (srt, str)
		@param categories: 
		    The categories of the word; default is the empty dictionary.

		    Categories can indicate word declensions or modifications.
	
		"""
		self.form = form
		self.headword = headword
		self.categories = Utilities.nvl(categories, {})

	def __eq__(self, other):
		"""
		Compares two words: form, headword and categories.
		"""
		if isinstance(other, Word):
			return self.form == other.form and self.headword == other.headword and self.categories == other.categories
		else:
			return False
	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.form) ^ hash(self.headword)

	def __repr__(self):
		"""
		Give a verbose representation for a word.
		"""
		return "%s(%s)" % (self.form, self.headword)

	def __str__(self):
		"""
		Give a concise representation for a word.
		"""
		return self.form


class Particle(Word):
	"""
	A language specific particle.

	For example, I{li} in Toki Pona.
	"""
	def __init__(self, form, id, p_o_s):
		Word.__init__(self, form, Headword(form, id, p_o_s))
	def __repr__(self):
		return self.form


class Lexicon:
	def __init__(self):
		self.__headwords = {}
		self.__words = {}
		self.__compiled = None
		self.__valid = False
		
	def compile(self, properties = None, force = False):
		if properties is None:
			properties = {}
		if force or not self.__valid and self.__compiled is None:
			self.__valid = False
			self.__compiled = Tokenizer(self.__words, properties)
			self.__valid = True
		return self.__compiled
		
	def reset(self):
		del self.__compiled
		self.__compiled = None
		self.__valid = False
		
	def add_word(self, word):
		headword = word.headword
		if headword:
			word.headword = self.add_headword(headword)
		self.__words.setdefault(word.form, []).append(word)
		return word
		
	def remove_word(self, word):
		ws = self.__words[word.form]
		if word in ws:
			ws.remove(word)
			
	def get_word(self, form):
		ws = self.__words.get(form, [])
		return ws
		
	def add_headword(self, headword):
		k = (headword.entry_word, headword.id)
		if k in self.__headwords:
			if self.__headwords[k] != headword:
				raise ExistingHeadwordError(headword)
			else:
				headword = self.__headwords[k]
		else:
			self.__headwords[k] = headword
		return headword
		
	def remove_headword(self, headword):
		k = (headword.entry_word, headword.id)
		if k in self.__headwords:
			del self.__headwords[k]
			
	def get_headword(self, headword):
		return self.__headwords.get((headword.entry_word, headword.id))
		
	def find_words(self, filter):
		f = []
		for i in self.__words.itervalues():
			for j in i:
				if filter.match(j):
					f.append(j)
		return f
	
	def __repr__(self):
		return `self.__words`

def __test():

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
	print lx
	print lx.compile({"separator":" "})
	

if __name__ == "__main__":
	__test()
