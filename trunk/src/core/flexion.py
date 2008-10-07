#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the generation of flexed forms.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

import re
from lexicon import Word, Lemma, Lexicon

__docformat__ = "epytext en"

class _SortedDict(dict):
	def __init__(self):
		dict.__init__(self)
		self.__sort = []
	def __setitem__(self, key, value):
		dict.__setitem__(self, key, value)
		self.__sort.append(key)
	def iterkeys(self):
		for key in self.__sort:
			yield key
	def itervalues(self):
		for key in self.__sort:
			yield self[key]
	def iteritems(self):
		for key in self.__sort:
			yield (key, self[key])
	def __repr__(self):
		s = ""
		for key in self.__sort:
			if s == "":
				s = "{["
			else:
				s += ", "
			s += `key` + " : " + `self[key]`
		s += "]}"
		return s

BASED_ON_LEMMA = "LEMMA"

class Flexion:
	class __Transform:
		class __Chain:
			def __init__(self, parent_flexion, based_on, condition):
				self.__parent = parent_flexion
				if BASED_ON_LEMMA == based_on:
					self.based_on = None
				else:
					self.based_on = based_on
				self.condition = condition
				self.__cco = re.compile(condition, re.IGNORECASE)
				self.steps = []
				
			def append_step(self, regexp, repl, optional = False):
				cre = re.compile(regexp, re.IGNORECASE)
				self.steps.append((regexp, cre, repl, optional))
			
			def __call__(self, lemma, words):
				if self.based_on is None:
					s = lemma.entry_form
				else:
					s = None
					for w in words:
						if Lexicon.test_categories(self.based_on, w.categories):
							s = w.form
							break
					if not s:
						w = self.__parent.do_transform(lemma, words, self.based_on)
						s = w.form
				if not s:
					return None
				if not self.__cco.search(s):
					return None
				for r, cre, repl, optional in self.steps:
					if cre.search(s):
						s = cre.sub(repl, s)
					elif not optional:
						return None
				return s

			
		def __init__(self, parent_flexion, categories):
			self.__parent = parent_flexion
			self.categories = categories
			self.chains = []
			
		def create_chain(self, based_on = BASED_ON_LEMMA, condition = "."):
			c = self.__Chain(self.__parent, based_on , condition)
			self.chains.append(c)
			return c
		

		def append_step(self, regexp, repl, optional = False):
			for c in self.chains:
				c.append_step(regexp, repl, optional)

		def __call__(self, lemma, words):
			for chain in self.chains:
				s = chain(lemma, words)
				if s is not None:
					return s
			raise ValueError("Transform cannot apply to lemma '%s'" % `lemma`)
			
	def __init__(self):
		self.__transforms = _SortedDict()

	def create_transform(self, categories):
		if type(categories) is not tuple:
			raise TypeError(categories)
		t =  self.__Transform(self, categories)
		self.__transforms[categories] = t
		return t

	def iter_transforms(self):
		return self.__transforms.itervalues()

	def do_transform(self, lemma, words, categories):
		word = None
		for w in words:
			if Lexicon.test_categories(categories, w.categories):
				word = w
				break
		if word is None:
			transform = self.__transforms[categories]
			word = Word(transform(lemma, words), lemma, categories)
		return word



	def __call__(self, lemma, words):
		table = _SortedDict()
		for categories in self.__transforms.iterkeys():		
			word = self.do_transform(lemma, words, categories)	
			table[word.categories] = word
		return table

class Flexions():
        def __init__(self):
                self.__flexions = {}
        def create_flexion(self, p_o_s, lemma_categories):
                f = Flexion()
                self.__flexions[(p_o_s, lemma_categories)] = f
                return f
        def __call__(self, lemma, words):
                f = self.__flexions[(lemma.p_o_s, lemma.categories)]
                return f(lemma, words)

def __test():
	from lexicon import Lexicon
	
	qya = Lexicon()
	telcu = Lemma("telcu", 1, "n", ("0",), "jicesi")
	qya.add_word(Word("telco", telcu, ("s","N")))
	maama = Lemma("roccie", 1, "n", None, "zunbe")
	qya.add_word(Word("roccie", maama, ("s","N")))
	nis = Lemma("niss", 1, "n", None, "dona")
	qya.add_word(Word("nís", nis, ("s","N")))
	z = Flexions()
	f = z.create_flexion("n", ("0",))
	
	tr = f.create_transform(("s","N")) 
	tr.create_chain(BASED_ON_LEMMA)
	

	tr_o = f.create_transform(("s","G")) 
	c = tr_o.create_chain()
	c.append_step("ie$", "ié", True)
	c.append_step("cu$", "qu", True)
	c.append_step("[ao]?$", "o") 
	
	
	tr = f.create_transform(("s","D")) 
	c = tr.create_chain(("s","N"), "[^aeiouáéíóú]$")
	c.append_step("$", "en")
	c = tr.create_chain(("s","N"), "[aeiouáéíóú]$")
	c.append_step("$", "n")
	
		
	tr = f.create_transform(("s","P")) 
	c = tr.create_chain(BASED_ON_LEMMA, "[iu]$")
	c.append_step("$", "va")
	c = tr.create_chain(BASED_ON_LEMMA, "ss$")
	c.append_step("$", "eva")
	c = tr.create_chain(BASED_ON_LEMMA, "c$")
	c.append_step("$", "qua")
	c = tr.create_chain(BASED_ON_LEMMA, "[^aeiouáéíóú]$")
	c.append_step("$", "wa")
	c = tr.create_chain(BASED_ON_LEMMA, "[aeiouáéíóú]$")
	c.append_step("$", "va")
	


	tr = f.create_transform(("s","I")) 
	c = tr.create_chain(("s","D"))
	c.append_step("$", "en")
	
	print f(telcu, qya.retrieve_words(telcu.key()))
	print f(maama, qya.retrieve_words(maama.key()))
	print f(nis, qya.retrieve_words(nis.key()))

	
	
	#all_niss = f(u"niss", 1) #flexion table: paradigm = (..), dictionary of generated with none for defective, iterable over words
	#print all_niss
	#(niss, niis): [niis, nisso, nissen,...]
	


if __name__ == "__main__":
	__test()
