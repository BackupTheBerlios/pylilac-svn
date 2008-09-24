#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for filters to be used in grammars.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

import utilities
from sys import maxint
from lexicon import Word
from bnf import Literal


class WordFilter(Literal):
	"""
	Regarded parameters: form, headword entry word and ID, word.categories
	"""
	def __init__(self, word):
		if not isinstance(word, Word):
			raise TypeError(word)
		Literal.__init__(self, (word.form, word.headword.entry_word, word.headword.id, None, None, word.categories))

	def __hash__(self):
		def dict_hash(x, i):
			if x is None: 
				return 0
			else:
				return len(x) << i & maxint
		return hash(self.content[:-2]) ^ dict_hash(self.content[4], 2) ^ dict_hash(self.content[5], 4)



	def match(self, word): 
		def test_attr(filter_categories, categories):
			if filter_categories is not None:
				for name, test in filter_categories.iteritems():
					if test is not None and name in categories:
						v = categories[name]
						if v is not None:
							if isinstance(test, CategoryFilter):
								if not test.match(v): return False
							else:
								if test != v: return False
			return True
		def none_or_equal(v, w):
			if v is None: return True
			else: return v == w

		if not none_or_equal(self.content[0], word.form):
			return False
		if not none_or_equal(self.content[1], word.headword.entry_word):
			return False
		if not none_or_equal(self.content[2], word.headword.id):
			return False
		if not none_or_equal(self.content[3], word.headword.p_o_s):
			return False
		if not test_attr(self.content[4], word.headword.categories):
			return False
		if not test_attr(self.content[5], word.categories):
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
	Regarded parameters: headword.p_o_s, headword.categories, word.categories
	"""
	def __init__(self, p_o_s = None, headword_categories = None, categories = None):
		Literal.__init__(self, (None, None, None, p_o_s, headword_categories, categories))

	def __str__(self):
		p_o_s = self.content[3]
		if p_o_s is None:
			return "{*}"
		else:
			return "{%s}" % p_o_s
		

	def __repr__(self):
		p_o_s, headword_categories, categories = self.content[3:6]
		r = []
		r.append("{")
		if p_o_s is None:
			r.append("*")
		else:
			r.append(p_o_s)
		if headword_categories:
			r.append(" ")
			r.append(`headword_categories`)
		elif categories:
			r.append(" {}")
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
	FUNCTIONS["ni"] = (lambda x, parameter: x not in parameter, "^%s")

	def __init__(self, operator, parameter):
		if not self.FUNCTIONS.has_key(operator):
			raise KeyError(operator)
		self.operator = operator
		self.parameter = parameter

	def match(self, value):
		test, rpr = self.FUNCTIONS[self.operator]
		return test(value, self.parameter)	

	def __repr__(self):
		test, rpr = self.FUNCTIONS[self.operator]
		return rpr % repr(self.parameter)

def __test():
	from lexicon import Headword
	lx = WordCategoryFilter("noun")
	lx1 = WordCategoryFilter("noun", {"gender": "m"}, {"number": CategoryFilter("in", ["pl","s"])})
	lx2 = WordCategoryFilter("noun", {"gender": CategoryFilter("ni", ["m"])})
	lx3 = WordFilter(Word("man", Headword("man", 1, "n")))
	w = Word("man", Headword("man", 1, "noun", {"gender": "m"}))
	print `lx1`
	print `lx2`
	print `lx3`

	print lx1.match(w), lx2.match(w), lx3.match(w)

if __name__ == "__main__":
	__test()
