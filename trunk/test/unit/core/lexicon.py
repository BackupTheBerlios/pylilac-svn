#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.lexicon import *

def run():
	lx = Lexicon()
	Lexeme(u"ken", 1, "verb", ("tr",), "kus")
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
	run()
