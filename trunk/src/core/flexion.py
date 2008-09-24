#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the generation of flexed forms.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

import re
from lexicon import Word, Headword
from wordfilter import WordCategoryFilter, WordFilter


__docformat__ = "epytext en"

class Flexion:
	class Transform:
		def __init__(self):
			self.__alternatives = []
			
		def append_alternative(self, item, regexp, repl):
			cre = re.compile(regexp, re.IGNORECASE)
			self.__alternatives.append((item, regexp, cre, repl))
			
		def __call__(self, hw_p):
			for name, r, cre, repl in self.__alternatives:
				if cre.search(hw_p[item]):
					return cre.sub(repl, hw_p[item])
			raise RuntimeError(hw_p)
					
	def __init__(self, lexicon, p_o_s, headword_categories = None):
		self.__lexicon = lexicon
		self.__p_o_s = p_o_s
		self.__headword_categories = headword_categories
		self.__headword_alias = "headword"
		self.__paradigm_def = {}
		self.__transforms = {}

	def rename_headword(self, item):
		self.__headword_alias = item
	
	def define_paradigm(self, item, categories):
		self.__paradigm_def[item] = WordCategoryFilter(self.__p_o_s, self.__headword_categories, categories)

	def paradigm(self, headword):
		ws = self.__lexicon.find_words(WordFilter(Word(None, headword)))
		p = {self.__headword_alias: headword.entry_word}
		for item, wcfilter in self.__paradigm_def.iteritems():
			for w in ws:
				if wcfilter.match(w):
					p[item] = w.form
					break
		return p
		

	def __setitem__(self, categories, transform):
		self.__transforms[tuple(categories.items())] = transform
		
	def __getitem__(self, categories):
		return self.__transforms[tuple(categories.items())]
		
	def __delitem__(self, categories):
		del self.__transforms[tuple(categories.items())]

	def __call__(self, headword):
		def to_dict(cat):
			d = {}
			for k, v in cat: d[k] = v
			return d

		table = {}
		paradigm = self.paradigm(headword)
		for cat, transform in self.__paradigms.iteritems():
			w = Word(transform(paradigm), headword, to_dict(cat))
			table[cat] = w
		return ft



def __test():
	from lexicon import Lexicon
	
	qya = Lexicon()
	telcu = Headword("telcu", 1, "N", None, "jicesi")
	qya.add_word(Word("telco", telcu, {"number":"s", "case":"N"}))
	maama = Headword("roccie", 1, "N", None, "zunbe")
	qya.add_word(Word("roccie", maama, {"number":"s", "case":"N"}))
	f = Flexion(qya, "N")
	f.rename_headword("word-stem")
	f.define_paradigm("base-stem", {"number": "s", "case": "N"})
	
	print qya.find_words(WordFilter(Word("telco", telcu)))
	
	print f.paradigm(telcu)

	tr_o = Flexion.Transform()
	tr_o.append("word-stem", "cu$", "quo") 
	tr_o.append("word-stem", "ie$", "iéo") 
	tr_o.append("word-stem", "[ao]?$", "o") 
	#tr.append_where("base-stem", "i(e)$", "ee", "headword", "t")
	#tr.append("base-stem", "u$", None) #defective
	

	f[{"number": "s", "case": "G"}] = tr_o

	print f(telcu)
	print f(maama)
	#all_niss = f("niss", 1) #flexion table: paradigm = (..), dictionary of generated with none for  defective, iterable over words
	#print all_niss
	#(niss, niis): [niis, nisso, nissen,...]
	
	


if __name__ == "__main__":
	__test()
