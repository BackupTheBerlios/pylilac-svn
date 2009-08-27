#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for lexicon management: Word and Lemma.

G{classtree Lemma, Word}

@todo: meaning must be extended to real translation

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.5
"""

__docformat__ = "epytext en"


from sys import maxint
from tokenizer import Tokenizer
from bnf import Literal
from utilities import Utilities


DEFECTIVE = "-"
"""
It abstractly indicates a non existing word form.
It is used in L{inflections<inflection>} to represent a defective form.
Sometimes, it is convenient to use a surrogate form, such as I{"to be able"} for the infiniteive of the English lemma I{"can"}.
"""

class ExistingLemmaError(ValueError):
	"""
	Exception indicating that the lemma already exists.
	"""
	pass

class Lemma(object):
	"""
	A single unit of language, with no functional decoration.
	
	Usually, lemmas or headwords are the I{entry words} in dictionaries.
	
	It is an abstrract class and cannot be instantiated.
	"""
	def __init__(self, entry_form, id, p_o_s, categories = ()):
		"""
		Prepares the base Lemma instance for subclasses.
		It is an abstrract class and cannot be instantiated.
		
		@param entry_form: The canonical form of the lemma.
		@type entry_form: unicode
		@param id: The progressive number to keep colliding canonical forms separated.
		@type id: int
		@param p_o_s: The part of speech of the lemma.
		@type p_o_s: str
		@note: This constructor can not be used, since the class is abstract.
		"""
		if self.__class__ is Lemma: raise TypeError("Lemma is abstract and can not be instantiated.")

		if isinstance(entry_form, unicode):
			self.__entry_form = entry_form
		else:
			raise TypeError("'%s' is not Unicode" % repr(entry_form))	
		self.__id = id
		self.p_o_s = p_o_s
		if not isinstance(categories, tuple):
			raise TypeError(categories)
		self.categories = categories

	def __get_entry_form(self):
		"""
		Get the entry form of a lemma.
		"""
		return self.__entry_form
		
	def __get_id(self):
		"""
		Get the ID of a lemma.
		"""
		return self.__id

	def __readonly(self, value = None):
		raise AttributeError("The attributes 'entry_form' and 'id' are read-only properties.")	

	entry_form = property(__get_entry_form, __readonly, __readonly)
	id = property(__get_id, __readonly, __readonly)

	def key(self):
		"""
		Return the unique key for a Lemma: C{entry_form} and C{ID}.
		@return: A tuple (entry_form, id).
		@rtype: tuple
		"""
		return (self.__entry_form, self.__id)

	def __eq__(self, other):
		"""
		Compares memberwise two lemmas.
		@return: True if entry_form, ID, part of speech and categories are the same.
		@rtype: bool
		@param other: Another lemma.
		@type other: Lemma
		"""
		if isinstance(other, Lemma):
			return self.__entry_form == other.__entry_form and self.__id == other.__id and self.p_o_s == other.p_o_s and self.categories == other.categories
		elif other is None:
			return False
		else:
			return NotImplemented
			
	def __ne__(self, other):
		"""
		Compares memberwise two lemmas for inequality.
		@return: True if entry_form, ID, part of speech or categories are not the same.
		@rtype: bool
		@param other: Another lemma.
		@type other: Lemma
		"""
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__entry_form) ^ (self.__id - 1)

	def __repr__(self):
		"""
		Return an ASCII representation of a lemma.

		@return: An ASCII representation of the entry form followed by the ID.
		@rtype: str
		"""
		return Utilities.unidecode(self.__entry_form)+ "." + str(self.__id)

	def __unicode__(self):
		"""
		Give a concise Unicode representation of a lemma.

		@return: The entry form.
		@rtype: unicode
		"""
		return self.__entry_form


	

class Particle(Lemma):
	"""
	A lect specific particle.
	
	Practically, a L{Lemma} with no precise meaning defined.
	In a dictionary, it can only be described by its use in the lect.

	For example, I{li} in Toki Pona, that indicates the verb in common sentences.
	"""
	def __init__(self, entry_form, id, p_o_s, categories = ()):
		"""
		Create a particle of a specific lect.
		
		@param entry_form: The canonical form of the particle.
		@type entry_form: unicode
		@param id: The progressive number to keep colliding canonical forms separated.
		@type id: int
		@param p_o_s: The part of speech of the particle.
		@type p_o_s: str
		@param categories: The categories to which the particle belongs.
		@type categories: tuple of str
		"""
		Lemma.__init__(self, entry_form, id, p_o_s, categories)


class Lexeme(Lemma):
	"""
	A single language unit, a basic form, with no functional decoration, but with a definable meaning.
	
	A stem is a L{Lemma} with a precise meaning.
	In a dictionary, it can be also be explained by its translations.
	
	"""
	def __init__(self, entry_form, id, p_o_s, categories = (), gloss = None):
		"""
		Create a lexeme of a specific lect.

		Example::
			Lexeme(u"heart", 1, "noun", (), "kawcesi") #heart, the heart organ in English, with no classification.
			Lexeme(u"heart", 2, "noun", (), "kawcijumi") #heart, the heart shape in English.
			Lexeme(u"hɑɹt", 1, "noun", () ,"kawcesi") #/h\u0251\u0279t/, /hɑɹt/, the heart organ phonic representation in General American English
			Lexeme(u"moku", 1, "verb", {"transitive": "n"}, "fucala") #moku, "to eat" in Toki Pona

		@param entry_form: The canonical form of the particle.
		@type entry_form: unicode
		@param id: The progressive number to keep colliding canonical forms separated.
		@type id: int
		@param p_o_s: The part of speech of the particle.
		@type p_o_s: str
		@param categories: The categories to which the particle belongs.
		@type categories: tuple of str
		@param gloss: The meaning and the translation technique, referring to the I{interlingua}.
		@type gloss: str
		"""
		Lemma.__init__(self, entry_form, id, p_o_s, categories)
		self.gloss = gloss


class Word(object):
	"""
	A single unit of language which has meaning and can be expressed.
	"""
	def __init__(self, form, lemma, categories = ()):
		"""
		Create a word with its form, its L{lemma<Lemma>} and its categories.

		Example::
			Word(u"heart", Lexeme("eng", u"heart", 1, "noun", "kawcesi"), ("s"))
			Word(u"hearts", lemmas("eng", u"heart", 1, "noun"), ("pl"))
			Word(u"hɑɹts", hw, ("pl"))
			Word(u"moku", "tko", moku)
	
		@type form: unicode
		@param form: The traditional, standard or neutral form of the word, either graphical or phonical.
		@type lemma:  Lemma
		@param lemma: The lemma of the word.
		@type categories: tuple of str
		@param categories:  The categories of the word. Categories usually indicate word declensions or modifications.
	
		"""
		if not isinstance(categories, tuple):
			raise TypeError(categories)
		if isinstance(form, unicode):
			self.__form = form
		else:
			raise TypeError("'%s' is not Unicode" % repr(form))				
		self.__lemma = lemma
		self.categories = categories

	def __get_form(self):
		"""
		Get the form of the word.
		"""
		return self.__form
		
	def __get_lemma(self):
		"""
		Get the lemma of the word.
		"""
		return self.__lemma

	def __readonly(self, value = None):
		raise AttributeError("The attributes 'form' and 'lemma' are read-only properties.")	

	form = property(__get_form, __readonly, __readonly)
	lemma = property(__get_lemma, __readonly, __readonly)

	def __eq__(self, other):
		"""
		Compares memberwise two words.
		@see: L{Lemma equal operator.<Lemma.__eq__>}
		@return: True if form, lemma and categories are the same.
		@rtype: bool
		@param other: Another word.
		@type other: Word
		"""
		if isinstance(other, Word):
			return self.__form == other.__form and self.__lemma == other.__lemma and self.categories == other.categories
		elif other is None:
			return False		
		else:
			return NotImplemented

	def __ne__(self, other):
		"""
		Compares memberwise two words for inequality.
		@return: True if form, lemma or categories are not the same.
		@rtype: bool
		@param other: Another word.
		@type other: Word
		"""
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__form) ^ hash(self.__lemma)

	def __repr__(self):
		"""
		Give a verbose representation for a word in the format <form>@<lemma><categories>, for example: men@man.1('pl',)"
		
		@rtype: str
		"""
		z =  Utilities.unidecode(self.__form) + "@" + `self.__lemma`
		if len(self.categories) == 0:
			return z
		else:
			return z + `self.categories`

	def __unicode__(self):
		"""
		Give a concise unicode representation for a word.

		@return: The word form.
		@rtype: unicode
		"""
		return self.__form

	def copy(self, lemma = None):
		"""
		Construct a copy of the word, changing the lemma.
		@param lemma: The lemma of the copy to be constructed.
		@type lemma: Lemma
		@rtype: Word
		"""
		if lemma is None:
			lemma = self.__lemma
		return Word(self.__form, lemma, self.categories[:])

	def __nonzero__(self):
		"""
		Check if the word is defective.
		@rtype: bool
		@return: True if the word is not a defective form.
		"""
		return self.__form <> DEFECTIVE


class Lexicon(object):
	"""
	A class to contain and manage lemmas and word.
	"""
	def __init__(self):
		"""
		Create a new empty lexicon.
		"""
		self.__lemmas = {}
		self.__words = {}
		self.__compiled = None
		self.__indexed_words = {}
		self.__valid = False

	def compile(self, properties, force = False):
		"""
		Compile the words of the lexicon into a L{tokenizer<tokenizer.Tokenizer>}.
		The tokenizer is a tool for making expression parsing quick.
		If the C{force} flag is off and the lexicon was already compiled and was not updated, the old result is taken with no recompiling.

		@see: L{Finite State Automaton<fsa.FSA>}
		@param force: Recompile lexicon even if it has already been validated and compiled.
		@type force: bool
		@rtype: tokenizer.Tokenizer
		@raise tokenizer.UnknownTokenException: If an unknown characters is encountered while precompiling..
		@raise fsa.ParseError: If unexpected characters or stops are encountered.		
		"""
		if force or not self.__valid and self.__compiled is None:
			self.__valid = False
			self.__compiled = Tokenizer(self.__words, properties)
			self.__valid = True
		return self.__compiled

	def reset(self):
		"""
		Delete the internal result of the last compiling.
		"""
		del self.__compiled
		self.__compiled = None
		self.__valid = False
		
	def add_word(self, word):
		"""
		Create a word in the lexicon.
		The added word is a copy of the one provided.

		@param word: The word to add.
		@type word: Word
		@return: The word just added.
		@rtype: Word
		@raise ExistingLemmaError: If the lexicon has a lemma having the same key as the given one but is different.
		"""
		if not isinstance(word, Word):
			raise TypeError(word)
		lemma = word.lemma
		key = lemma.key()
		if key in self.__lemmas: #a lemma with that key exists
			existing_lemma = self.__lemmas[key]
			if lemma is not existing_lemma: #a lemma with that key exists but it's another object
				if lemma == existing_lemma: #a lemma with that key exists, it's another object, but it's equivalent
					word = word.copy(existing_lemma)
				else:
					raise ExistingLemmaError(lemma)
		else:
			word = word.copy(self.add_lemma(lemma))
		self.__words.setdefault(word.form, []).append(word)
		self.__indexed_words.setdefault(word.lemma.key(), []).append(word)
		self.__valid = False
		return word
		
	def remove_word(self, word):
		"""
		Remove a word from the lexicon.

		@param word: The word to remove.
		@type word: Word
		"""
		if not isinstance(word, Word):
			raise TypeError(word)
		self.__indexed_words[word.lemma.key()].remove(word)
		self.__words[word.form].remove(word)
		self.__valid = False

	def retrieve_words(self, form = None, lemma_key = None, categories = None):
		"""
		Search the lexicon for words matching the given conditions.
		If some fields are irrelevant they must be left C{None}.
		
		@param form: The form of the words to retrieve.
		@type form: unicode
		@param lemma_key: The key of the lemma of the words to retrieve.
		@type lemma_key: tuple (entry form, ID)
		@param categories: The categories of words to retrieve.
		@type categories: tuple of str/CategoryFilter
		@return: The list of the words matching the conditions.
		@rtype: list of Word
		"""
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
		"""
		Add a lemma to the lexicon.

		@param lemma: The lemma to add.
		@type lemma: Lemma
		@return: The added lemma.
		@rtype: Lemma
		@raise ExistingLemmaError: If the lemma already exists in the lexicon.
		"""
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
		"""
		Remove the lemma having the given key from the lexicon.
		Also its words are removed.

		@param lemma_key: The key of the lemma to remove.
		@type lemma_key: tuple (entry word, ID)
		"""
		for w in self.__indexed_words[lemma_key]:
			self.__words[w.form].remove(w)
		del self.__indexed_words[lemma_key]
		del self.__lemmas[lemma_key]
		self.__valid = False

	def get_lemma_by_key(self, lemma_key):
		"""
		Retrieve the lemma having the given key.

		@param lemma_key: The key of the lemma to retrieve.
		@type lemma_key: tuple (entry word, ID)
		"""
		return self.__lemmas.get(lemma_key)
		
	def iter_lemmas(self):
		"""
		Return an iterator to lemmas.
		@rtype: iterator of Lemma
		"""
		return self.__lemmas.itervalues()
		
	def iter_words(self):
		"""
		Return an iterator to words.
		@rtype: iterator of Word
		"""
		for lw in self.__indexed_words.itervalues():
			for w in lw:
				yield w

	def retrieve_lemmas(self, entry_form, id = None, p_o_s = None, lemma_categories = None):
		"""
		Search the lexicon for lemmas matching the given conditions.
		If some fields are irrelevant they must be left C{None}.
		
		@param entry_form: The entry form of the lemmas to retrieve.
		@type entry_form: unicode
		@param id: The ID of the lemmas to retrieve.
		@type id: int
		@param lemma_categories: The lemma categories of the lemmas to retrieve.
		@type lemma_categories: tuple of str/CategoryFilter
		@param p_o_s: The part of speech of the lemmas to retrieve.
		@type p_o_s: str
		@return: The list of the lemmas matching the conditions.
		@rtype: list of Lemma
		"""
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

	def __str__(self):
		"""
		Return a short string with lexicon statistics.
		@rtype: str
		"""
		return "[[%d lemmas, %d words]]" % (len(self.__lemmas), len(self.__words))
		
	def check(self, lect, corrective_p_o_s = None):
		"""
		Run a diagnostic on the lexicon.
		These anomalies are detected:
			- unknown parts of speech (they can be fixed)
			- wrong number of categories for lemmas and words
		
		@param corrective_p_o_s:
			The part of speech to overwrite unknown parts of speech.
			If no correction is required, leave C{None}.
		@type corrective_p_o_s: str
		@return: The anomaluos words and lemmas.
		@rtype: set of Word/Lemma
		"""
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
	A class to match and process words during parsing.
	
	The regarded fields, when not null, are:
		- word form
		- lemma entry form
		- lemma ID
		- word categories
	"""
	def __init__(self, word):
		"""
		Create a word filter.
		Irrelevant members can be left null.
		@param word: The word containing the conditions to include.
		@type word: Word
		"""
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

	def match(self, word):
		"""
		Verify that a word can be processed.
		If the internal values are C{None} or equal to those of the instantiation, equivalence is proven.
		
		@param word: The word to check.
		@type word: lexicon.Word
		@rtype: bool
		@return: True if the contents is equal to the parameter.
		"""
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
		"""
		Process the word and return it for tagging.
		
		@param word: The object to process.
		@type word: lexicon.Word
		@rtype: lexicon.Word
		@return: The word itself.
		@todo: Word tagging
		"""
		return word

	def __str__(self):
		"""
		Return a short string representation.
		@rtype: str
		"""
		return "'%s'" % self.content[0]

	def __repr__(self):
		"""
		Return a verbose string representation.
		@rtype: str
		"""
		r = []
		r.append("{'%s'(%s%d)" % self.content[0:3])
		if self.content[5]:
			r.append(" ")
			r.append(`self.content[5]`)
		r.append("}")
		return "".join(r)

	def insert_transitions(self, grammar, fsa, initial, final, tag = None, max_levels = 40):
		"""
		Insert a sub-FSA in a L{FSA<fsa.FSA>} according to the rules in a L{grammar<grammar.Grammar>}.

		@type grammar: Grammar
		@param grammar: The grammar providing the rules and options to build the sub-FSA.
		@type fsa: FSA
		@param fsa: The Finite-state Automaton in which the sub-graph must be inserted.
		@type initial: FSA node
		@param initial: The state from which the sub-graph departs.
		@type final: FSA node
		@param final: The state in which the sub-graph ends.
		@type tag: FSA tag
		@param tag: The initial tag for the arcs.
		@type max_levels: int
		@param max_levels: The maximum number of levels of recursion to accept.
		@todo: Word tagging.
			Instead of C{fsa.add_transition(initial, self, final, tag + (None,))}, it may be useful storing more than 'word' field
		"""
		fsa.add_transition(initial, self, final, tag + (self.content[0],))


class WordCategoryFilter(WordFilter):
	"""
	A class to match and process words during parsing.

	The regarded fields, when not null, are:
		- lemma part of speech
		- lemma categories
		- word categories	
	"""
	def __init__(self, p_o_s = None, lemma_categories = None, categories = None):
		"""
		Create a word category filter.
		Irrelevant fields can be left null.
		
		@param p_o_s: The part of speech to match.
		@type p_o_s: str
		@param lemma_categories: The lemma category to match.
		@type lemma_categories: tuple of str/CategoryFilter
		@param categories: The word category to match.
		@type categories: tuple of str/CategoryFilter
		"""
		if lemma_categories is not None and not isinstance(lemma_categories, tuple):
			raise TypeError(lemma_categories)
		if categories is not None and not isinstance(categories, tuple):
			raise TypeError(categories)
		Literal.__init__(self, (None, None, None, p_o_s, lemma_categories, categories))

	def __str__(self):
		"""
		Return a short string representation.
		@rtype: str
		"""
		p_o_s = self.content[3]
		if p_o_s is None:
			return "{*}"
		else:
			return "{%s}" % p_o_s
		

	def __repr__(self):
		"""
		Return a verbose string representation.
		@rtype: str
		"""
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
		"""
		Insert a sub-FSA in a L{FSA<fsa.FSA>} according to the rules in a L{grammar<grammar.Grammar>}.

		@type grammar: Grammar
		@param grammar: The grammar providing the rules and options to build the sub-FSA.
		@type fsa: FSA
		@param fsa: The Finite-state Automaton in which the sub-graph must be inserted.
		@type initial: FSA node
		@param initial: The state from which the sub-graph departs.
		@type final: FSA node
		@param final: The state in which the sub-graph ends.
		@type tag: FSA tag
		@param tag: The initial tag for the arcs.
		@type max_levels: int
		@param max_levels: The maximum number of levels of recursion to accept.
		@todo: Word tagging.
			Instead of C{fsa.add_transition(initial, self, final, tag + (None,))}, it may be useful storing more than 'word' field
		"""
		fsa.add_transition(initial, self, final, tag + (self.content[3],))

class CategoryFilter(object):
	"""
	A class to match categories of words and lemmas.
	"""
	FUNCTIONS = {}
	FUNCTIONS["in"] = (lambda x, parameter: x in parameter, "%s")
	FUNCTIONS["ni"] = (lambda x, parameter: x not in parameter, "¬%s")

	@staticmethod
	def test(filter_categories, categories):
		"""
		Compare filters and values.
		
		@param filter_categories: The filters to match.
		@type filter_categories: tuple of str/CategoryFilter
		@param categories: The values to check.
		@type categories: tuple of str/CategoryFilter
		@return: true if all filters are verified.
		@rtype: bool
		"""	
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
		"""
		Create an instance of category filter.

		@param operator: The operator to apply.
			Supported operators are:
				- C{in} ("in"), to test inclusion in a set of possible values
				- C{ni} ("not in"), to test not inclusion in a set of possible values
		@type operator: str
		@param parameter: The values to match.
		@type parameter: sequence of str
		"""
		if operator not in self.FUNCTIONS:
			raise KeyError(operator)
		self.operator = operator
		self.parameter = frozenset(parameter)

	def match(self, value):
		"""
		Verify the category filter against a category.
		@param value: The value to verify
		@type value: str
		@rtype: bool
		@return: True if the value matches the filter.
		"""
		test, r = self.FUNCTIONS[self.operator]
		return test(value, self.parameter)	

	def __repr__(self):
		"""
		Return a string representation of the category filter.
		@rtype: str
		"""
		t, rpr = self.FUNCTIONS[self.operator]
		return rpr % repr(tuple(self.parameter))
		

def __test():

	lx = Lexicon()
	r = Lexeme(u"ken", 1, "verb", ("tr",), "kus")
	lx.add_word(Word(u"mi", Lexeme(u"mi", 1, "pronoun", (), "bavi")))
	lx.add_word(Word(u"sina", Lexeme(u"sina", 1, "pronoun", (), "zavi")))
	lx.add_word(Word(u"suli", Lexeme(u"suli", 1, "adjective", (), "kemo")))
	lx.add_word(Word(u"suna", Lexeme(u"suna", 1, "noun", (), "Lakitisi")))
	lx.add_word(Word(u"telo", Lexeme(u"telo", 1, "noun", (), "bocivi")))
	lx.add_word(Word(u"moku", Lexeme(u"moku", 1, "verb", ("intr",), "fucala")))
	lx.add_word(Word(u"moku", Lexeme(u"moku", 2, "verb", ("tr",), "fucalinza")))
	lx.add_word(Word(u"jan", Lexeme(u"jan", 1, "noun", (), "becami")))
	lx.add_word(Word(u"li", Particle(u"li", 1, "sep")))
	print lx
	tk = lx.compile({"separator": " "})
	print tk(u"jan li moku")

	lx = WordCategoryFilter("noun")
	lx1 = WordCategoryFilter("noun", ("m", CategoryFilter("in", ["pl","s"])))
	lx2 = WordCategoryFilter("noun", (CategoryFilter("ni", ["m"]), None))
	lx3 = WordFilter(Word(u"man", Lexeme(u"man", 1, "n", (), "None")))
	w = Word(u"man", Lexeme(u"man", 1, "noun", ("m",), "Uomo"))
	print `lx1`
	print `lx2`
	print `lx3`
	print lx1.match(w), lx2.match(w), lx3.match(w)
	

	cf = CategoryFilter("in", ("A","B"))
	cf2 = CategoryFilter("ni", ("A","B"))
	print `cf`
	print "Yes", cf.match("A"), CategoryFilter.test((cf2,), ("C",))
	print "No", cf.match("C"), CategoryFilter.test((cf2,), ("A",))
	
	homo = Lexeme(u"man", 1, "noun", ("m",), "Uomo")
	print homo.entry_form.__doc__
	try:
		homo.entry_form = u"maen"
	except AttributeError, a:
		print a
	try:
		del homo.entry_form 
	except AttributeError, a:
		print a
	
	
if __name__ == "__main__":
	__test()
