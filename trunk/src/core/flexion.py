#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the generation of flexed forms.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

import re
from lexicon import Word, Lemma
from wordfilter import WordCategoryFilter, WordFilter


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

			
		def __init__(self):
			self.__chains = []
			
		def create_chain(self, item, condition = "."):
			c = self.__Chain(item, condition)
			self.__chains.append(c)
			return c
			
		def __call__(self, hw_p):
			for c in self.__chains:
				s = c(hw_p)
				if s is not None:
					return s
			raise ValueError("Transform cannot apply to lemma '%s'" % `hw_p`)
					
	def __init__(self, lexicon, p_o_s, lemma_categories = None):
		self.__lexicon = lexicon
		self.__p_o_s = p_o_s
		self.__lemma_categories = lemma_categories
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
		self.__paradigm_def[item] = WordCategoryFilter(self.__p_o_s, self.__lemma_categories, categories)


	def paradigm(self, lemma):
		ws = self.__lexicon.find_words((lemma.entry_form, lemma.id))
		p = {self.__lemma_alias: lemma.entry_form}
		for item, wcfilter in self.__paradigm_def.iteritems():
			for w in ws:
				if wcfilter.match(w):
					p[item] = w.form
					break
		return p
		

	def create_transform(self, categories):
		if type(categories) is not tuple:
			raise TypeError(categories)
		t =  self.__Transform()
		self.__transforms[categories] = t
		return t
	def get_transforms(self):
		return self.__transforms
		

	def __call__(self, lemma):
		table = _SortedDict()
		paradigm = self.paradigm(lemma)
		for cat, transform in self.__transforms.iteritems():
			w = Word(transform(paradigm), lemma, cat)
			table[cat] = w
		return table



def __test():
	from lexicon import Lexicon
	
	qya = Lexicon()
	telcu = Lemma("telcu", 1, "N", None, "jicesi")
	qya.add_word(Word("telco", telcu, ("s","N")))
	maama = Lemma("roccie", 1, "N", None, "zunbe")
	qya.add_word(Word("roccie", maama, ("s","N")))
	nis = Lemma("niss", 1, "N", None, "dona")
	qya.add_word(Word("nís", nis, ("s","N")))
	f = Flexion(qya, "N")
	f.rename_lemma("stem-form")
	f.define_paradigm("basic-form", ("s","N"))
	
	print f.paradigm(telcu)
	print f.paradigm(nis)
	
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
	
	
	print f(telcu)
	print f(maama)
	print f(nis)
	#all_niss = f("niss", 1) #flexion table: paradigm = (..), dictionary of generated with none for  defective, iterable over words
	#print all_niss
	#(niss, niis): [niis, nisso, nissen,...]
	import pickle
	pickle.dump(f, "n.fln")
	


if __name__ == "__main__":
	__test()
