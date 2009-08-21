#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the generation of flexed forms.


"""

# General info
__version__ = "0.1"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

import re
from lexicon import Word, Lexicon, CategoryFilter, DEFECTIVE
from utilities import SortedDict

BASED_ON_LEMMA = 0


class MutationStepError(ValueError):
	pass
class FlexionError(RuntimeError):
	pass

class Flexion:
	class __Transform:
		class __Chain:
			"""
			A chain of mutation steps.
			
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
			def __init__(self, parent_flexion, based_on, condition, lemma_categories, steps = None):
				self.__parent = parent_flexion
				if BASED_ON_LEMMA == based_on:
					self.based_on = None
				else:
					self.based_on = based_on
				self.condition = condition
				self.lemma_categories = lemma_categories
				try:
					self.__cco = re.compile(condition, re.IGNORECASE)
				except Exception, e:
					raise MutationStepError("Cannot compile %s: %s" % (`condition`, e.message))
				self.steps = []
				if steps:
					for search, substitution, mandatory in steps:
					    self.append_step(search, substitution, mandatory)

			def append_step(self, search, substitution, mandatory = False):
				"""
				Add a mutation step characterized by the string to search, its replacement and a flag stating if the string must be found at least once.
				"""
				try:
					cre = re.compile(search, re.IGNORECASE)
				except Exception, e:
					raise MutationStepError("Cannot compile %s for %s: %s" % (`substitution`, `search`, e.message))
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
						w = self.__parent.do_transform(lemma, words, self.based_on)
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
							raise FlexionError("Invalid transform %s for %s" % (`substitution`, `r`))
					elif mandatory:
						return None
				return s

			
		def __init__(self, parent_flexion, categories):
			self.__parent = parent_flexion
			self.categories = categories
			self.chains = []
			
		def create_chain(self, based_on = BASED_ON_LEMMA, condition = u".", lemma_categories = None):
			c = self.__Chain(self.__parent, based_on , condition, lemma_categories)
			self.chains.append(c)
			return c

		def append_step(self, regexp, substitution, mandatory = False):
			for c in self.chains:
				c.append_step(regexp, substitution, mandatory)

		def __call__(self, lemma, words):
			for chain in self.chains:
				s = chain(lemma, words)
				if s is not None:
					return s
			raise FlexionError("Transform cannot apply %s to lemma '%s'" % (`self.categories`, lemma.entry_form))
			
	def __init__(self):
		self.p_o_s = p_o_s
		self.
		self.__transforms = SortedDict()

	def create_transform(self, categories):
		if not isinstance(categories, tuple):
			raise TypeError(categories)
		t =  self.__Transform(self, categories)
		self.__transforms[categories] = t
		return t

	def iter_transforms(self):
		return self.__transforms.itervalues()

	def do_transform(self, lemma, words, categories):
		word = None
		for w in words:
			if CategoryFilter.test(categories, w.categories):
				word = w
				break
		if word is None:
			transform = self.__transforms[categories]
			word = Word(transform(lemma, words), lemma, categories)
		return word

	def __call__(self, lemma, words):
		table = SortedDict()
		for categories in self.__transforms.iterkeys():	
			word = self.do_transform(lemma, words, categories)
			if word.form <> DEFECTIVE:
				table[word.categories] = word
		return table

class Flexions:
		def __init__(self):
			self.__flexions = []
		def create_flexion(self, p_o_s, condition = None, lemma_categories = None):
			flexion = Flexion()
			if condition == u".":
			    condition = None
			cco = None
			if condition:
				try:
					cco = re.compile(condition, re.IGNORECASE)
				except Exception, e:
					raise MutationStepError("Cannot compile %s: %s" % (`condition`, e.message))
			self.__flexions.append((p_o_s, condition,  cco, lemma_categories, flexion))
			return flexion
		
		def __call__(self, lemma, words):
			for p_o_s, c,  cco, lemma_categories, f in self.__flexions:
				if p_o_s == lemma.p_o_s and (cco is None or cco.search(lemma.entry_form)) and CategoryFilter.test(lemma_categories, lemma.categories):
					return f(lemma, words)
			return None

def __test():
	from lexicon import Stem


	
	qya = Lexicon()
	telcu = Stem(u"telcu", 1, "n", ("0",), "jicesi")
	qya.add_word(Word(u"telco", telcu, ("s","N")))
	maama = Stem(u"roccie", 1, "n", (), "zunbe")
	qya.add_word(Word(u"roccie", maama, ("s","N")))
	nis = Stem(u"niss", 1, "n", (), "dona")
	qya.add_word(Word(u"nís", nis, ("s","N")))
	z = Flexions()
	f = z.create_flexion("n", ("0",))
	
	tr = f.create_transform(("s","N")) 
	tr.create_chain(BASED_ON_LEMMA)
	

	tr_o = f.create_transform(("s","G")) 
	c = tr_o.create_chain()
	c.append_step(u"ie$", u"ié")
	c.append_step(u"cu$", u"qu")
	c.append_step(u"[ao]?$", u"o") 
	
	
	tr = f.create_transform(("s","D")) 
	c = tr.create_chain(("s","N"), u"[^aeiouáéíóú]$")
	c.append_step(u"$", u"en")
	c = tr.create_chain(("s","N"), u"[aeiouáéíóú]$")
	c.append_step(u"$", u"n")
	
		
	tr = f.create_transform(("s","P")) 
	c = tr.create_chain(BASED_ON_LEMMA, u"[iu]$")
	c.append_step(u"$", u"va")
	c = tr.create_chain(BASED_ON_LEMMA, u"ss$")
	c.append_step(u"$", u"eva")
	c = tr.create_chain(BASED_ON_LEMMA, u"c$")
	c.append_step(u"$", u"qua")
	c = tr.create_chain(BASED_ON_LEMMA, u"[^aeiouáéíóú]$")
	c.append_step(u"$", u"wa")
	c = tr.create_chain(BASED_ON_LEMMA, u"[aeiouáéíóú]$")
	c.append_step(u"$", u"va")
	


	tr = f.create_transform(("s","I")) 
	c = tr.create_chain(("s","D"))
	c.append_step(u"$", u"en")
	
	print f(telcu, qya.retrieve_words(telcu.key()))
	print f(maama, qya.retrieve_words(maama.key()))
	print f(nis, qya.retrieve_words(nis.key()))

	
	
	#all_niss = f(u"niss", 1) #flexion table: paradigm = (..), dictionary of generated with none for defective, iterable over words
	#print all_niss
	#(niss, niis): [niis, nisso, nissen,...]
	


if __name__ == "__main__":
	__test()
