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
			raise RuntimeError("Transform cannot apply to %s" % `hw_p`)
					
	def __init__(self, lexicon, p_o_s, lemma_categories = None):
		self.__lexicon = lexicon
		self.__p_o_s = p_o_s
		self.__lemma_categories = lemma_categories
		self.__lemma_alias = "lemma"
		self.__paradigm_def = {}
		self.__transforms = []

	def rename_lemma(self, item):
		self.__lemma_alias = item
	
	def define_paradigm(self, item, categories):
		self.__paradigm_def[item] = WordCategoryFilter(self.__p_o_s, self.__lemma_categories, categories)

	def paradigm(self, lemma):
		ws = self.__lexicon.find_words(WordFilter(Word(None, lemma)))
		p = {self.__lemma_alias: lemma.entry_form}
		for item, wcfilter in self.__paradigm_def.iteritems():
			for w in ws:
				if wcfilter.match(w):
					p[item] = w.form
					break
		return p
		

	def create_transform(self, categories):
		t =  self.__Transform()
		self.__transforms.append((categories, t))
		return t
		

	def __call__(self, lemma):
		table = []
		paradigm = self.paradigm(lemma)
		for cat, transform in self.__transforms:
			w = Word(transform(paradigm), lemma, cat)
			table.append((cat, w))
		return table



def __test():
	from lexicon import Lexicon
	
	qya = Lexicon()
	telcu = Lemma("telc", 1, "N", None, "jicesi")
	qya.add_word(Word("telco", telcu, {"number":"s", "case":"N"}))
	maama = Lemma("roccie", 1, "N", None, "zunbe")
	qya.add_word(Word("roccie", maama, {"number":"s", "case":"N"}))
	nis = Lemma("niss", 1, "N", None, "dona")
	qya.add_word(Word("nís", nis, {"number":"s", "case":"N"}))
	f = Flexion(qya, "N")
	f.rename_lemma("stem-form")
	f.define_paradigm("basic-form", {"number": "s", "case": "N"})
	
	print qya.find_words(WordFilter(Word("telco", telcu)))
	
	print f.paradigm(telcu)
	
	tr = f.create_transform({"number": "s", "case": "N"}) 
	tr.create_chain("basic-form")
	

	tr_o = f.create_transform({"number": "s", "case": "G"}) 
	c = tr_o.create_chain("stem-form")
	c.append_step("ie$", "ié", True)
	c.append_step("cu$", "q", True)
	c.append_step("[ao]?$", "o") 
	
	
	tr = f.create_transform({"number": "s", "case": "D"}) 
	c = tr.create_chain("stem-form", "[^aeiouáéíóú]$")
	c.append_step("$", "en")
	c = tr.create_chain("stem-form", "[aeiouáéíóú]$")
	c.append_step("$", "n")
	
		
	tr = f.create_transform({"number": "s", "case": "P"}) 
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
	
	


if __name__ == "__main__":
	__test()
