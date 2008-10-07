#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for lexicon management: Word and Lemma.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""
#TODO: meaning must be extended to real translation

__docformat__ = "epytext en"

from utilities import Utilities
from tokenizer import Tokenizer

class ExistingLemmaError(ValueError):
	pass

class Lemma:
	"""
	A single unit of language, with no functional decoration.
	
	Usually, lemmas or headwords are the I{entry words} in dictionaries and encyclopediae.
	"""
	def __init__(self, entry_form, id, p_o_s, categories, gloss):
		"""
		Create a lemma in a specific language for the I{entry word} specified.

		Example::
			Lemma(u"heart", 1, "noun", None, "kawcesi") #heart, the heart organ in English, with no classification.
			Lemma(u"heart", 2, "noun", None, "kawcijumi") #heart, the heart shape in English.
			Lemma(u"h??t", 1, "noun", None ,"kawcesi") #/h\u0251\u0279t/, /h??t/, the heart organ phonic representation in General American English
			Lemma(u"moku", 1, "verb", {"transitive": "n"}, "fucala") #moku, "to eat" in Toki Pona

		@type entry_form: unicode
		@param entry_form: 
		    A U{Unicode<http://www.unicode.org>} representation of the entry word, either graphical or phonical.

		    The representation of a word can be its written form or its spoken form, refer to Unicode conventions for the proper encoding.

		    For phonetic/phonical representations, the alphabet of the U{IPA<http://www.arts.gla.ac.uk/IPA>} (Internationa Phonetic Association) is the standard, though some kind of extension could be advisable; the representation should be a phonetic transcription.
		@type id: number
		@param id: 
		    A unique id to distinguish different lemmas having identical representation in a given language.

		    Major meanings in dictionaries are usually associated to different id's.
		@type p_o_s: str
		@param p_o_s:
		    A string which indicates the I{part of speech} to which the lemma belongs to in the specific language.

		    The I{part of speech} is the general classification of the word: usually it distinguish nouns from verbs &c..
		@type categories: tuple (srt)
		@param categories:
		    The categories of the lemma.

		    Categories can specify better the features of a particular I{part of speech}.
		@type gloss: str
		@param gloss:
		    The meaning and the translation technique, referring to the I{interlingua}.

		    For the interlingua to use, Latejami or its successors are recommended.

		"""
		self.entry_form = entry_form
		self.id = Utilities.nvl(id, 1)
		self.p_o_s = p_o_s
		self.categories = Utilities.nvl(categories, ())
		self.gloss = gloss

	def key(self):
		return (self.entry_form, self.id)

	def __eq__(self, other):
		"""
		Compares memberwise two lemmas.
		"""
		if isinstance(other, Lemma):
			return self.entry_form == other.entry_form and self.id == other.id and self.p_o_s == other.p_o_s and self.categories == other.categories
		else:
			return False
	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.entry_form) ^ self.id

	def __repr__(self):
		return "%s.%d" % (self.entry_form, self.id)

class Word:
	"""
	A single unit of language which has meaning and can be expressed.
	"""
	def __init__(self, form, lemma, categories = ()):
		"""
		Create a word with its form, its L{lemma<Lemma>} and its categories.

		Example::
			Word(u"heart", Lemma("eng", u"heart", 1, "noun", None, "kawcesi"))
			Word(u"hearts", lemmas["eng", u"heart", 1], ("pl"))
			Word(u"h??ts", hw, ("pl"))
			Word(u"moku", "tko", moku)
	
		@type form: unicode
		@param form:
		    The traditional, standard or neutral form of the word, either graphical or phonical.
		@type lemma:  Lemma
		@param lemma:
		    The lemma of the word.
		@type categories: dict (srt, str)
		@param categories: 
		    The categories of the word; default is the empty tuple.

		    Categories can indicate word declensions or modifications.
	
		"""
		self.form = form
		self.lemma = lemma
		self.categories = categories

	def __eq__(self, other):
		"""
		Compares two words: form, lemma and categories.
		"""
		if isinstance(other, Word):
			return self.form == other.form and self.lemma == other.lemma and self.categories == other.categories
		else:
			return False
	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.form) ^ hash(self.lemma)

	def __repr__(self):
		"""
		Give a verbose representation for a word in the format <form>(<lemma>)
		"""
		return "%s(%s)" % (self.form, self.lemma)

	def __str__(self):
		"""
		Give a concise representation for a word.

		@return: The word's form.
		"""
		return self.form


class Particle(Word):
	"""
	A language specific particle.

	For example, I{li} in Toki Pona.
	"""
	def __init__(self, form, id, p_o_s):
		Word.__init__(self, form, Lemma(form, id, p_o_s))
	def __repr__(self):
		return self.form


class Lexicon:
	def __init__(self):
		self.__lemmas = {}
		self.__words = {}
		self.__compiled = None
		self.__indexed_words = {}
		self.__valid = False
		
	def compile(self, properties, force = False):
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
		lemma = word.lemma
		if lemma:
			word.lemma = self.add_lemma(lemma)
		self.__words.setdefault(word.form, []).append(word)
		self.__indexed_words.setdefault(word.lemma.key(), []).append(word)
		self.__valid = False
		return word
		
	def remove_word(self, word):
		self.__indexed_words[word.lemma.key()].remove(word)
		self.__words[word.form].remove(word)
		self.__valid = False

	def get_words(self, word_form):
		ws = self.__words.get(word_form, [])
		return ws
			
		
	def add_lemma(self, lemma):
		k = lemma.key()
		if k in self.__lemmas:
			if self.__lemmas[k] != lemma:
				raise ExistingLemmaError(lemma)
			else:
				lemma = self.__lemmas[k]
		else:
			self.__lemmas[k] = lemma
		self.__valid = False
		return lemma
		
	def remove_lemma(self, lemma_key):
		for w in self.__indexed_words[lemma_key]:
			self.__words[w.form].remove(w)
		del self.__indexed_words[lemma_key]
		del self.__lemmas[lemma_key]
		self.__valid = False

	def get_lemma(self, lemma_key):
		return self.__lemmas.get(lemma_key)
		
	def iter_lemmas(self):
		return self.__lemmas.iterkeys()
		
	def iter_words(self):
		for lw in self.__indexed_words.itervalues():
			for w in lw:
				yield w

	def find_lemmas(self, entry_form, id = None, p_o_s = None, lemma_categories = None):
		def test_attr(filter_categories, categories):
			if filter_categories is not None:
				for i, test in enumerate(filter_categories):
					if test is not None and i < len(categories):
						v = categories[i]
						if v is not None:
							if isinstance(test, CategoryFilter):
								if not test.match(v): return False
							else:
								if test != v: return False
			return True
		f = []
		for i in self.__lemmas.itervalues():
			if entry_form is not None and entry_form != i.entry_form:
				continue
			if id is not None and id != i.id:
				continue
			if p_o_s is not None and p_o_s != i.p_o_s:
				continue
			if not test_attr(lemma_categories, i.categories):
				continue
			f.append(j)
		return f


	def find_words(self, lemma_key):
		return self.__indexed_words[lemma_key]

	def __repr__(self):
		return "[[%d lemmas, %d words]]" % (len(self.__lemmas), len(self.__words))
		
	def check(self, lect, corrective_p_o_s = None):
		def check_length(w, l, err, corr):
			if len(w.categories) < l:
				err.add(w)
				if corr:
					w.categories += ("0",)*(l - len(hw.categories))
			if len(w.categories) > len(d[hw.p_o_s][0]):
				err.add(w)
				if corr:
					w.categories = w.categories[0:l]		
		err = set()
		d = {}
		for p in lect.get_p_o_s_names():
			d[p] = lect.get_p_o_s(p)
		for hw in self.__lemmas.itervalues():
			if not d.has_key(hw.p_o_s):
				err.add(hw)
				if corrective_p_o_s:
					hw.p_o_s = corrective_p_o_s
			if d.has_key(hw.p_o_s):
				check_length(hw, len(d[hw.p_o_s][0]), err, corrective_p_o_s)
		for wz in self.__words.itervalues():
			for w in wz:
				p_o_s = w.lemma.p_o_s
				if d.has_key(p_o_s):
					check_length(w, len(d[p_o_s][1]), err, corrective_p_o_s)
		self.__valid = False
		return err
		
		

def __test():

	lx = Lexicon()
	lx.add_word(Word("mi", Lemma("mi", 1, "pronoun", None, "bavi")))
	lx.add_word(Word("sina", Lemma("sina", 1, "pronoun", None, "zavi")))
	lx.add_word(Word("suli", Lemma("suli", 1, "adjective", None, "kemo")))
	lx.add_word(Word("suna", Lemma("suna", 1, "noun", None, "Lakitisi")))
	lx.add_word(Word("telo", Lemma("telo", 1, "noun", None, "bocivi")))
	lx.add_word(Word("moku", Lemma("moku", 1, "verb", ("intr"), "fucala")))
	lx.add_word(Word("moku", Lemma("moku", 2, "verb", ("tr"), "fucalinza")))
	lx.add_word(Word("jan", Lemma("jan", 1, "noun", None, "becami")))
	lx.add_word(Particle("li",1,"sep"))
	print lx
	tk = lx.compile()
	print tk("jan li moku")
	

if __name__ == "__main__":
	__test()
