﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the generation of inflected forms.


"""

# General info
__version__ = "0.4"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

import re
from lexicon import Word, Lexicon, CategoryFilter, DEFECTIVE
from utilities import SortedDict

BASED_ON_ENTRY_FORM = 0


class TransformSyntaxError(ValueError):
	pass
class InflectionError(RuntimeError):
	pass

class Inflection:
	class Form:
		def __init__(self, parent_inflection, categories):
			self.__parent = parent_inflection
			self.categories = categories
			self.transforms = []
			
		def create_transform(self, based_on = BASED_ON_ENTRY_FORM, condition = u".", lemma_categories = None):
			c = Transform(self.__parent, based_on , condition, lemma_categories)
			self.transforms.append(c)
			return c

		def append_step(self, search, substitution, mandatory = False):
			for c in self.transforms:
				c.append_step(search, substitution, mandatory)

		def __call__(self, lemma, words):
			for transform in self.transforms:
				s = transform(lemma, words)
				if s is not None:
					return s
			raise InflectionError("Transform cannot apply %s to lemma '%s'" % (`self.categories`, lemma.entry_form))
			
	#Inflection class body
	def __init__(self, p_o_s, condition, lemma_categories):
		self.p_o_s = p_o_s
		if condition == u".":
			condition = None
					
		cco = None
		if condition:
			if not isinstance(condition, unicode):
				raise TypeError("'%s' is not Unicode" % repr(condition))		
			try:
				cco = re.compile(condition, re.IGNORECASE)
			except Exception, e:
				raise TransformSyntaxError("Cannot compile %s: %s" % (`condition`, `e`))
		self.condition = condition
		self.lemma_categories = lemma_categories
		self.__cco = cco
		self.__forms = SortedDict()

	def create_form(self, categories):
		if not isinstance(categories, tuple):
			raise TypeError(categories)
		t =  self.Form(self, categories)
		self.__forms[categories] = t
		return t

	def iter_forms(self):
		return self.__forms.itervalues()

	def do_form(self, lemma, words, categories):
		word = None
		for w in words:
			if CategoryFilter.test(categories, w.categories):
				word = w
				break
		if word is None:
			form = self.__forms[categories]
			word = Word(form(lemma, words), lemma, categories)
		return word
	
	def applies(self, lemma):
		cco = self.__cco
		if self.p_o_s == lemma.p_o_s and (cco is None or cco.search(lemma.entry_form)) and CategoryFilter.test(self.lemma_categories, lemma.categories):
			return True
		else:
			return False

	def __call__(self, lemma, words):
		table = SortedDict()
		for categories in self.__forms.iterkeys():
			word = self.do_form(lemma, words, categories)
			if word.form <> DEFECTIVE:
				table[word.categories] = word
		return table
		
	def __repr__(self):
		s = [self.p_o_s]
		if self.condition:
			s.append(self.condition)
		if self.lemma_categories:
			s.append(`self.lemma_categories`)
		return "/".join(s)
	
class Inflections:
		def __init__(self):
			self.__inflections = []

		def create_inflection(self, p_o_s, condition = None, lemma_categories = None):
			inflection = Inflection(p_o_s, condition, lemma_categories)
			self.__inflections.append(inflection)
			return inflection
		
		def __call__(self, lemma, words):
			for inflection in self.__inflections:
				if inflection.applies(lemma):
					return inflection(lemma, words)
			raise InflectionError("Cannot inflect %s" % `lemma`)
			
class Transform:
	"""
	A transform, a chain of mutation steps.
	
	For example, in Quenya: from the verb stem «I{cava}» the present form «I{cávea}» can be
	seen as applying different mutation steps, one in the middle and one at the end of the stem.
	It can be done by applying three mutation steps to the stem:
		1. alternation (apophony) of the last short vowel «I{-a-}» and «I{-á-}», giving the intermediate form «I{cáva}*»
		2. alternation of the final «I{-a}» and «I{-e}», giving the intermediate form «I{cáve}*»
		3. suffixation of «I{-a}», giving the final form «I{cávea}»

	Mutation steps
	==============
	
	Steps are modeled as tuple:
		>>> (search, substitution, mandatory)
	
	All the occurrences of the C{search} string in the base form are replace with the C{substitution}.
	If C{mandatory} is C{True} and there are no occurrences of the C{search} string the operation will abort.
	See the L{call<__call__>} method for details on execution.
	
	In the example above, the steps from «I{cava}» «I{cávea}» can be seen as follows:
		1. C{u"a(?=[^aeiouáíéóú][yw]?[au]?$)"} S{->} C{u"á"}
		2. C{u"a$"} S{->} C{u"e"}
		3. C{u"$"} S{->} C{u"a"}

	If one of the initial regular expressions is not satisfied and the step is not defined as mandatory, it's neglected and the execution goes on to the next step.
	In this example, the second step might be seen as optional, since stems not ending in «I{-a}» simply go on to the last step : «I{hir}» S{->} «I{híra}» .
	"""
	def __init__(self, parent_inflection, based_on, condition, lemma_categories, steps = None):

		if not isinstance(condition, unicode):
			raise TypeError("'%s' is not Unicode" % repr(condition))		
		self.__parent = parent_inflection

		if BASED_ON_ENTRY_FORM == based_on:
			self.based_on = None
		else:
			self.based_on = based_on
		self.condition = condition
		self.lemma_categories = lemma_categories
		try:
			self.__cco = re.compile(condition, re.IGNORECASE)
		except Exception, e:
			raise TransformSyntaxError("Cannot compile %s: %s" % (`condition`, `e`))
		self.steps = []
		if steps:
			for search, substitution, mandatory in steps:
				self.append_step(search, substitution, mandatory)

	def append_step(self, search, substitution, mandatory = False):
		"""
		Add a step characterized by the string to search, its replacement and a flag stating if the string must be found at least once.
		"""

		if not isinstance(search, unicode):
			raise TypeError("'%s' is not Unicode" % repr(search))
		if not isinstance(substitution, unicode):
			raise TypeError("'%s' is not Unicode" % repr(substitution))

		try:
			cre = re.compile(search, re.IGNORECASE)
		except Exception, e:
			raise TransformSyntaxError("Cannot compile %s for %s: %s" % (`substitution`, `search`, e.message))
		self.steps.append((search, cre, substitution, mandatory))
	
	def __call__(self, lemma, words):
		if not CategoryFilter.test(self.lemma_categories, lemma.categories):
			return None
		if self.based_on is None:
			s = lemma.entry_form
		else:
			s = None
			for w in words:
				if CategoryFilter.test(self.based_on, w.categories):
					s = w.form
					break
			if not s:
				w = self.__parent.do_form(lemma, words, self.based_on)
				s = w.form
		if not s:
			return None
		if DEFECTIVE == s:
			return DEFECTIVE #propagation
		if not self.__cco.search(s):
			return None
		for r, cre, substitution, mandatory in self.steps:
			if cre.search(s):
				try:
					s = cre.sub(substitution, s)
				except:
					raise InflectionError("Invalid form %s for %s" % (`substitution`, `r`))
			elif mandatory:
				return None
		return s

	


def __test():
	from lexicon import Lexeme

	print "QUENYA"
	
	qya = Lexicon()
	telcu = Lexeme(u"telcu", 1, "n", ("0",), "jicesi")
	qya.add_word(Word(u"telco", telcu, ("s","N")))
	maama = Lexeme(u"roccie", 1, "n", (), "zunbe")
	qya.add_word(Word(u"roccie", maama, ("s","N")))
	nis = Lexeme(u"niss", 1, "n", (), "dona")
	qya.add_word(Word(u"nís", nis, ("s","N")))
	z = Inflections()
	f = z.create_inflection("n", None, ("0",))
	
	tr = f.create_form(("s","N")) 
	tr.create_transform(BASED_ON_ENTRY_FORM)
	

	tr_o = f.create_form(("s","G")) 
	c = tr_o.create_transform()
	c.append_step(u"ie$", u"ié")
	c.append_step(u"cu$", u"qu")
	c.append_step(u"[ao]?$", u"o") 
	
	
	tr = f.create_form(("s","D")) 
	c = tr.create_transform(("s","N"), u"[^aeiouáéíóú]$")
	c.append_step(u"$", u"en")
	c = tr.create_transform(("s","N"), u"[aeiouáéíóú]$")
	c.append_step(u"$", u"n")
	
		
	tr = f.create_form(("s","P")) 
	c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[iu]$")
	c.append_step(u"$", u"va")
	c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ss$")
	c.append_step(u"$", u"eva")
	c = tr.create_transform(BASED_ON_ENTRY_FORM, u"c$")
	c.append_step(u"$", u"qua")
	c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[^aeiouáéíóú]$")
	c.append_step(u"$", u"wa")
	c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiouáéíóú]$")
	c.append_step(u"$", u"va")
	


	tr = f.create_form(("s","I")) 
	c = tr.create_transform(("s","D"))
	c.append_step(u"$", u"en")
	
	print f(telcu, qya.retrieve_words(telcu.key()))
	print f(maama, qya.retrieve_words(maama.key()))
	print f(nis, qya.retrieve_words(nis.key()))

	
	
	#all_niss = f(u"niss", 1) #inflection table: paradigm = (..), dictionary of generated with none for defective, iterable over words
	#print all_niss
	#(niss, niis): [niis, nisso, nissen,...]
	
	print "LATIN"
	
	lat = Lexicon()
	rosa = Lexeme(u"rosa", 1, "n", ("f",), "rose")
	lupo = Lexeme(u"luːpo", 1, "n", ("m",), "wolf")
	mar = Lexeme(u"maːr", 1, "n", ("n",), "sea")
	lat.add_word(Word(u"maːre", mar, ("s","N")))
	mar2 = Lexeme(u"maːr", 2, "n", ("m",), "male")
	lat.add_word(Word(u"maːr", mar2, ("s","N")))
	urb = Lexeme(u"urb", 1, "n", ("f",), "town")
	lat.add_word(Word(u"urps", urb, ("s","N")))
	nomin = Lexeme(u"noːmin", 1, "n", ("m",), "name")
	
	decl = Inflections()
	
	decl1 = decl.create_inflection("n", u"a$")
	decl1N = decl1.create_form(("s","N")) 
	decl1N_ = decl1N.create_transform(BASED_ON_ENTRY_FORM)
	
	decl1G = decl1.create_form(("s","G")) 
	decl1G_ = decl1G.create_transform()
	decl1G_.append_step(u"a$", u"ae", True)

	decl2 = decl.create_inflection("n", u"o$")
	decl2N = decl2.create_form(("s","N")) 
	decl2N_ = decl2N.create_transform()
	decl2N_.append_step(u"o$", u"us", True)
	
	decl2G = decl2.create_form(("s","G"))  
	decl2G_ = decl2G.create_transform()
	decl2G_.append_step(u"o$", u"iː", True)
	
	decl3 = decl.create_inflection("n")
	
	decl3N = decl3.create_form(("s","N")) 
	decl3N_ = decl3N.create_transform(BASED_ON_ENTRY_FORM, u"in", ("m",))
	decl3N_.append_step(u"in$", u"en")
	decl3N_ = decl3N.create_transform(BASED_ON_ENTRY_FORM, u"in", ("n",))
	decl3N_.append_step(u"in$", u"o")
	
	decl3G = decl3.create_form(("s","G"))  
	decl3G_ = decl3G.create_transform()
	decl3G_.append_step(u"$", u"iːs", True)
	
	print decl(lupo, lat.retrieve_words(lupo.key()))
	print decl(nomin, lat.retrieve_words(nomin.key()))
	print decl(rosa, lat.retrieve_words(rosa.key()))

if __name__ == "__main__":
	__test()
