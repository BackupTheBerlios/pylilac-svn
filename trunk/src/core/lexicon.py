#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for lexicon management: Word and Lemma.

G{classtree Lemma, Word}

@todo: meaning must be extended to real translation

"""

# General info
__version__ = "0.1"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"


from sys import maxint
from tokenizer import Tokenizer
from bnf import Literal
from utilities import Utilities


DEFECTIVE = -3

class ExistingLemmaError(ValueError):
	pass

class Lemma:
	"""
	A single unit of language, with no functional decoration.
	
	Usually, lemmas or headwords are the I{entry words} in dictionaries.
	"""
	def __init__(self, entry_form, id, p_o_s, categories = ()):
		"""
		It cannot be used publicly, since the class is abstract.
		"""

		if self.__class__ is Lemma: raise TypeError("Lemma is abstract and cannot be instantiated.")
		self.__entry_form = Utilities.unicode(entry_form)
		self.__id = id
		self.p_o_s = p_o_s
		if not isinstance(categories, tuple):
			raise TypeError(categories)
		self.categories = categories


	@property
	def entry_form(self):
		"""
		Get the entry form of a lemma.
		"""
		return self.__entry_form

	@property
	def id(self):
		return self.__id

	def key(self):
		return (self.__entry_form, self.__id)

	def __eq__(self, other):
		"""
		Compares memberwise two particles.
		"""
		if isinstance(other, Lemma):
			return self.__entry_form == other.__entry_form and self.__id == other.__id and self.p_o_s == other.p_o_s and self.categories == other.categories
		else:
			return NotImplemented
			
	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__entry_form) ^ (self.__id - 1)

	def __repr__(self):
		return `self.__entry_form`+ "." + str(self.__id)

	def __unicode__(self):
		"""
		Give a concise representation for a word.

		@return: The word's form.
		"""
		return self.__entry_form


	

class Particle(Lemma):
	"""
	A language specific particle.
	
	Practically, a L{Lemma} with no precise meaning defined.
	In a dictionary, it can only be described by its use in the lect.

	For example, I{li} in Toki Pona, that indicates the verb in common sentences.
	"""
	def __init__(self, entry_form, id, p_o_s, categories = ()):
		Lemma.__init__(self, entry_form, id, p_o_s, categories)


class Stem(Lemma):
	"""
	A single unit of language, a basic form, with no functional decoration, but with a definable meaning.
	
	A stem is a L{Lemma} with a precise meaning.
	In a dictionary, it can be also be explained by its translations.
	
	"""
	def __init__(self, entry_form, id, p_o_s, categories = (), gloss = None):
		"""
		Create a stem in a specific language for the I{entry form} specified.

		Example::
			Stem(u"heart", 1, "noun", (), "kawcesi") #heart, the heart organ in English, with no classification.
			Stem(u"heart", 2, "noun", (), "kawcijumi") #heart, the heart shape in English.
			Stem(u"hɑɹt", 1, "noun", () ,"kawcesi") #/h\u0251\u0279t/, /hɑɹt/, the heart organ phonic representation in General American English
			Stem(u"moku", 1, "verb", {"transitive": "n"}, "fucala") #moku, "to eat" in Toki Pona

		@type entry_form: unicode
		@param entry_form: 
		    A U{Unicode<http://www.unicode.org>} representation of the entry word, either graphical or phonical.

		    The representation of a word can be its written form or its spoken form, refer to Unicode conventions for the proper encoding.

		    For phonetic/phonical representations, the alphabet of the U{IPA<http://www.arts.gla.ac.uk/IPA>} (Internationa Phonetic Association) is the standard, though some kind of extension could be advisable; the representation should be a phonetic transcription.
		@type id: number
		@param id:  A unique id to distinguish different lemmas having identical representation in a given language.

		    Major meanings in dictionaries are usually associated to different id's.
		@type p_o_s: str
		@param p_o_s: A string which indicates the I{part of speech} to which the lemma belongs to in the specific language.

		    The I{part of speech} is the general classification of the word: usually it distinguish nouns from verbs &c..
		@type categories: tuple (srt)
		@param categories: The categories of the lemma.

		    Categories can specify better the features of a particular I{part of speech}.
		@type gloss: str
		@param gloss: The meaning and the translation technique, referring to the I{interlingua}.

		    For the interlingua to use, Latejami or its successors are recommended.

		"""
		Lemma.__init__(self, entry_form, id, p_o_s, categories)
		self.gloss = gloss


class Word:
	"""
	A single unit of language which has meaning and can be expressed.
	"""
	def __init__(self, form, lemma, categories = ()):
		"""
		Create a word with its form, its L{lemma<Lemma>} and its categories.

		Example::
			Word(u"heart", Stem("eng", u"heart", 1, "noun", None, "kawcesi"))
			Word(u"hearts", lemmas["eng", u"heart", 1], ("pl"))
			Word(u"hɑɹts", hw, ("pl"))
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
		if not isinstance(categories, tuple):
			raise TypeError(categories)
		self.__form = Utilities.unicode(form)
		self.__lemma = lemma
		self.categories = categories

	@property
	def form(self):
		return self.__form
	
	@property
	def lemma(self):
		return self.__lemma

	def __eq__(self, other):
		"""
		Compares two words: form, lemma and categories.
		"""
		if isinstance(other, Word):
			return self.__form == other.__form and self.__lemma == other.__lemma and self.categories == other.categories
		else:
			return NotImplemented

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__form) ^ hash(self.__lemma)

	def __repr__(self):
		"""
		Give a verbose representation for a word in the format <form>@<lemma><categories>, for example: 'men'@'man'.1('pl')"
		"""
		z =  `self.__form` + "@" + `self.__lemma`
		if len(self.categories) == 0:
			return z
		else:
			return z + `self.categories`

	def __unicode__(self):
		"""
		Give a concise representation for a word.

		@return: The word's form.
		"""
		return self.__form

	def copy(self, lemma = None):
		if lemma is None:
			lemma = self.__lemma
		return Word(self.__form, lemma, self.categories[:])

	def __nonzero__(self):
		return self.__form <> DEFECTIVE


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
		if not isinstance(word, Word):
			raise TypeError(word)
		lemma = word.lemma
		if lemma:
			key = lemma.key()
			if key in self.__lemmas:
				if lemma != self.__lemmas[key]:
					raise ExistingLemmaError(lemma)
				else:
					word = word.copy(self.__lemmas[key])
			else:
				word = word.copy(self.add_lemma(lemma))
		self.__words.setdefault(word.form, []).append(word)
		self.__indexed_words.setdefault(word.lemma.key(), []).append(word)
		self.__valid = False
		return word
		
	def remove_word(self, word):
		if not isinstance(word, Word):
			raise TypeError(word)
		self.__indexed_words[word.lemma.key()].remove(word)
		self.__words[word.form].remove(word)
		self.__valid = False

	def retrieve_words(self, form = None, lemma_key = None, categories = None):
		ws = []
		if lemma_key is not None:
			for w in self.__indexed_words[lemma_key]:
				if form is not None and form != w.form:
					continue
				if not CategoryFilter.test(categories, w.categories):
					continue
				ws.append(w)
		else:
			for w in self.__words.get(form, []):
				if CategoryFilter.test(categories, w.categories):
					ws.append(w)
		return ws
	
	def add_lemma(self, lemma):
		if not isinstance(lemma, Lemma):
			raise TypeError(lemma)
		k = lemma.key()
		if k in self.__lemmas:
			raise ExistingLemmaError(self.__lemmas[k])
		else:
			self.__lemmas[k] = lemma
		self.__valid = False
		return lemma
		
	def remove_lemma_by_key(self, lemma_key):
		for w in self.__indexed_words[lemma_key]:
			self.__words[w.form].remove(w)
		del self.__indexed_words[lemma_key]
		del self.__lemmas[lemma_key]
		self.__valid = False

	def get_lemma_by_key(self, lemma_key):
		return self.__lemmas.get(lemma_key)
		
	def iter_lemmas(self):
		return self.__lemmas.itervalues()
		
	def iter_words(self):
		for lw in self.__indexed_words.itervalues():
			for w in lw:
				yield w

	def retrieve_lemmas(self, entry_form, id = None, p_o_s = None, lemma_categories = None):
		f = []
		for i in self.__lemmas.itervalues():
			if entry_form is not None and entry_form != i.entry_form:
				continue
			if id is not None and id != i.id:
				continue
			if p_o_s is not None and p_o_s != i.p_o_s:
				continue
			if not CategoryFilter.test(lemma_categories, i.categories):
				continue
			f.append(j)
		return f

	def __repr__(self):
		return "[[%d entries, %d forms]]" % (len(self.__lemmas), len(self.__words))
		
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
			d[p] = lect.get_categories(p)
		for hw in self.__lemmas.itervalues():
			if hw.p_o_s not in d:
				err.add(hw)
				if corrective_p_o_s:
					hw.p_o_s = corrective_p_o_s
			if hw.p_o_s in d:
				check_length(hw, len(d[hw.p_o_s][0]), err, corrective_p_o_s)
		for wz in self.__words.itervalues():
			for w in wz:
				p_o_s = w.lemma.p_o_s
				if p_o_s in d:
					check_length(w, len(d[p_o_s][1]), err, corrective_p_o_s)
		self.__valid = False
		return err

class WordFilter(Literal):
	"""
	Regarded parameters: form, lemma entry word and ID, word.categories
	"""
	def __init__(self, word):
		if not isinstance(word, Word):
			raise TypeError(word)
		Literal.__init__(self, (word.form, word.lemma.entry_form, word.lemma.id, None, None, word.categories))

	def __hash__(self):
		def dict_hash(x, i):
			if x is None: 
				return 0
			else:
				return len(x) << i & maxint
		return hash(self.content[:-2]) ^ dict_hash(self.content[4], 2) ^ dict_hash(self.content[5], 4)

	def __eq__(self, other):
		"""
		Compare a terminal to another.
		Two terminals are equal if their contents are the same.
		"""
		if isinstance(other, WordFilter):
			return self.content == other.content
		elif other is None:
			return False
		else:
		    raise TypeError(other.__class__)


	def match(self, word):
		def none_or_equal(v, w):
			if v is None: return True
			else: return v == w

		if not none_or_equal(self.content[0], word.form):
			return False
		if not none_or_equal(self.content[1], word.lemma.entry_form):
			return False
		if not none_or_equal(self.content[2], word.lemma.id):
			return False
		if not none_or_equal(self.content[3], word.lemma.p_o_s):
			return False
		if not CategoryFilter.test(self.content[4], word.lemma.categories):
			return False
		if not CategoryFilter.test(self.content[5], word.categories):
			return False
		return True

	def process(self, word):
		#TODO word tagging
		return word

	def __str__(self):
		return "'%s'" % self.content[0]

	def __repr__(self):
		r = []
		r.append("{'%s'(%s%d)" % self.content[0:3])
		if self.content[5]:
			r.append(" ")
			r.append(`self.content[5]`)
		r.append("}")
		return "".join(r)

	def insert_transitions(self, grammar, fsa, initial, final, tag = None, max_levels = 40):
		#instead of fsa.add_transition(initial, self, final, tag + (None,))
		#may be useful storing more than 'word' field
		fsa.add_transition(initial, self, final, tag + (self.content[0],))


class WordCategoryFilter(WordFilter):
	"""
	Regarded parameters: lemma.p_o_s, lemma.categories, word.categories
	"""
	def __init__(self, p_o_s = None, lemma_categories = None, categories = None):
		if lemma_categories is not None and not isinstance(lemma_categories, tuple):
			raise TypeError(lemma_categories)
		if categories is not None and not isinstance(categories, tuple):
			raise TypeError(categories)
		Literal.__init__(self, (None, None, None, p_o_s, lemma_categories, categories))

	def __str__(self):
		p_o_s = self.content[3]
		if p_o_s is None:
			return "{*}"
		else:
			return "{%s}" % p_o_s
		

	def __repr__(self):
		p_o_s, lemma_categories, categories = self.content[3:6]
		r = []
		r.append("{")
		if p_o_s is None:
			r.append("*")
		else:
			r.append(p_o_s)
		if lemma_categories:
			r.append(" ")
			r.append(`lemma_categories`)
		elif categories:
			r.append(" ()")
		if categories:
			r.append(`categories`)
		r.append("}")
		return "".join(r)

	def insert_transitions(self, grammar, fsa, initial, final, tag = None, max_levels = 40):
		#instead of fsa.add_transition(initial, self, final, tag + (None,))
		#may be useful storing more than 'word' field
		fsa.add_transition(initial, self, final, tag + (self.content[3],))

class CategoryFilter:

	FUNCTIONS = {}
	FUNCTIONS["in"] = (lambda x, parameter: x in parameter, "%s")
	FUNCTIONS["ni"] = (lambda x, parameter: x not in parameter, "¬%s")

	@staticmethod
	def test(filter_categories, categories):
		if filter_categories is not None:
			for i, test in enumerate(filter_categories):
				if test is not None and i < len(categories):
					v = categories[i]
					if v is not None:
						if not isinstance(test, CategoryFilter):
							if test != v: return False
						else:
							if not test.match(v): return False
		return True


	def __init__(self, operator, parameter):
		if operator not in self.FUNCTIONS:
			raise KeyError(operator)
		self.operator = operator
		self.parameter = tuple(parameter)

	def match(self, value):
		test, rpr = self.FUNCTIONS[self.operator]
		return test(value, self.parameter)	

	def __repr__(self):
		test, rpr = self.FUNCTIONS[self.operator]
		return rpr % `self.parameter`
		

def __test():

	lx = Lexicon()
	r = Stem(u"ken", 1, "verb", ("tr",), "kus")
	lx.add_word(Word(u"mi", Stem(u"mi", 1, "pronoun", (), "bavi")))
	lx.add_word(Word(u"sina", Stem(u"sina", 1, "pronoun", (), "zavi")))
	lx.add_word(Word(u"suli", Stem(u"suli", 1, "adjective", (), "kemo")))
	lx.add_word(Word(u"suna", Stem(u"suna", 1, "noun", (), "Lakitisi")))
	lx.add_word(Word(u"telo", Stem(u"telo", 1, "noun", (), "bocivi")))
	lx.add_word(Word(u"moku", Stem(u"moku", 1, "verb", ("intr",), "fucala")))
	lx.add_word(Word(u"moku", Stem(u"moku", 2, "verb", ("tr",), "fucalinza")))
	lx.add_word(Word(u"jan", Stem(u"jan", 1, "noun", (), "becami")))
	lx.add_word(Word(u"li", Particle(u"li", 1, "sep")))
	print lx
	tk = lx.compile({"separator": " "})
	print tk(u"jan li moku")

	lx = WordCategoryFilter("noun")
	lx1 = WordCategoryFilter("noun", ("m", CategoryFilter("in", ["pl","s"])))
	lx2 = WordCategoryFilter("noun", (CategoryFilter("ni", ["m"]), None))
	lx3 = WordFilter(Word("man", Stem("man", 1, "n", (), "None")))
	w = Word("man", Stem("man", 1, "noun", ("m",), "Uomo"))
	print `lx1`
	print `lx2`
	print `lx3`
	print lx1.match(w), lx2.match(w), lx3.match(w)
	

	cf = CategoryFilter("in", ("A","B"))
	cf2 = CategoryFilter("ni", ("A","B"))
	print `cf`
	print "Yes", cf.match("A"), CategoryFilter.test((cf2,), ("C",))
	print "No", cf.match("C"), CategoryFilter.test((cf2,), ("A",))
	
if __name__ == "__main__":
	__test()
