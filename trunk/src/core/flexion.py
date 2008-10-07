#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the generation of flexed forms.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

import re
from lexicon import Word, Lemma


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

class Flexion:
	class __Transform:
		class __Chain:
			def __init__(self, item, condition = "."):
				self.item = item
				self.condition = condition
				self.__cco = re.compile(condition, re.IGNORECASE)
				self.steps = []
				
			def append_step(self, regexp, repl, optional = False):
				cre = re.compile(regexp, re.IGNORECASE)
				self.steps.append((regexp, cre, repl, optional))
			
			def __call__(self, hw_p):
				s = hw_p[self.item]
				if not self.__cco.search(s):
					return None
				for r, cre, repl, optional in self.steps:
					if cre.search(s):
						s = cre.sub(repl, s)
					elif not optional:
						return None
				return s

			def copy(self):
				c = self.__class__(self.item, self.condition)
				c.steps = self.steps[:]
				return c

			
		def __init__(self):
			self.chains = []
			
		def create_chain(self, item, condition = "."):
			c = self.__Chain(item, condition)
			self.chains.append(c)
			return c
		
		def copy(self):
			c = self.__class__()
			c.chains = [x.copy() for x in self.chains]
			return c

		def append_step(self, regexp, repl, optional = False):
			for c in self.chains:
				c.append_step(regexp, repl, optional)

		def __call__(self, hw_p):
			for c in self.chains:
				s = c(hw_p)
				if s is not None:
					return s
			raise ValueError("Transform cannot apply to lemma '%s'" % `hw_p`)
					
	def __init__(self):
		self.__lemma_alias = "lemma"
		self.__paradigm_def = {}
		self.__transforms = _SortedDict()

	def rename_lemma(self, item):
		if self.__paradigm_def.has_key(item):
			raise ValueError("%s is already in use" % item)
		self.__lemma_alias = item
	
	def define_paradigm(self, item, categories):
		if item == self.__lemma_alias:
			raise ValueError("%s is reserved for the lemma entry form" % item)
		self.__paradigm_def[item] = categories


	def paradigm(self, lemma, words):
		p = {self.__lemma_alias: lemma.entry_form}
		for item, wcfilter in self.__paradigm_def.iteritems():
			for w in words:
				if w.categories == wcfilter:
					p[item] = w.form
					break
		return p
		

	def create_transform(self, categories, template = None):
		if type(categories) is not tuple:
			raise TypeError(categories)
		if template is None:
			t =  self.__Transform()
		else:
			if type(template) is not tuple:
				raise TypeError(template)
			t = self.__transforms[template].copy()
		self.__transforms[categories] = t
		return t

	def get_transforms(self):
		return self.__transforms

	def copy(self):
		clone = self.__class__()
		clone.__lemma_alias = self.__lemma_alias
		clone.__paradigm_def = self.__paradigm_def.copy()
		tr = _SortedDict()
		for k, v in self.__transforms.iteritems():
			tr[k] = v.copy()
		clone.__transforms = tr	
		return clone

	def __call__(self, lemma, words):
		table = _SortedDict()
		paradigm = self.paradigm(lemma, words)
		for cat, transform in self.__transforms.iteritems():
			w = Word(transform(paradigm), lemma, cat)
			table[cat] = w
		return table

class Flexions():
        def __init__(self):
                self.__flexions = {}
        def create_flexion(self, p_o_s, lemma_categories):
                f = Flexion()
                self.__flexions[(p_o_s, lemma_categories)] = f
                return f
        def clone_flexion(self, p_o_s, lemma_categories, lemma_categories_2):
		cl =  self.__flexions[(p_o_s, lemma_categories)].copy()
                self.__flexions[(p_o_s, lemma_categories_2)] = cl
		return cl
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
	f.rename_lemma("stem-form")
	f.define_paradigm("basic-form", ("s","N"))
	
	print f.paradigm(telcu, qya.find_words(telcu.key()))
	print f.paradigm(nis, qya.find_words(nis.key()))
	
	tr = f.create_transform(("s","N")) 
	tr.create_chain("basic-form")
	

	tr_o = f.create_transform(("s","G")) 
	c = tr_o.create_chain("stem-form")
	c.append_step("ie$", "ié", True)
	c.append_step("cu$", "qu", True)
	c.append_step("[ao]?$", "o") 
	
	
	tr = f.create_transform(("s","D")) 
	c = tr.create_chain("stem-form", "[^aeiouáéíóú]$")
	c.append_step("$", "en")
	c = tr.create_chain("stem-form", "[aeiouáéíóú]$")
	c.append_step("$", "n")
	
		
	tr = f.create_transform(("s","P")) 
	c = tr.create_chain("stem-form", "[iu]$")
	c.append_step("$", "va")
	c = tr.create_chain("stem-form", "ss$")
	c.append_step("$", "eva")
	c = tr.create_chain("stem-form", "c$")
	c.append_step("$", "qua")
	c = tr.create_chain("basic-form", "[^aeiouáéíóú]$")
	c.append_step("$", "wa")
	c = tr.create_chain("basic-form", "[aeiouáéíóú]$")
	c.append_step("$", "va")
	
	
	print f(telcu, qya.find_words(telcu.key()))
	print f(maama, qya.find_words(maama.key()))
	print f(nis, qya.find_words(nis.key()))

	z.clone_flexion("n", ("0",), ("1",))
	z(telcu, qya.find_words(telcu.key()))
	
	#all_niss = f("niss", 1) #flexion table: paradigm = (..), dictionary of generated with none for defective, iterable over words
	#print all_niss
	#(niss, niis): [niis, nisso, nissen,...]
	


if __name__ == "__main__":
	__test()
