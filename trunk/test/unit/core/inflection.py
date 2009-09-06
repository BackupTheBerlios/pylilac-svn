#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.inflection import *
from lexicon import Lexeme


def run():

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
	
	f.create_transform(("s","N"), BASED_ON_ENTRY_FORM)
	
	c = f.create_transform(("s","G"))
	c.append_step(u"ie$", u"ié")
	c.append_step(u"cu$", u"qu")
	c.append_step(u"[ao]?$", u"o") 
	
	c = f.create_transform(("s","D"), ("s","N"), u"[^aeiouáéíóú]$")
	c.append_step(u"$", u"en")
	c = f.create_transform(("s","D"), ("s","N"), u"[aeiouáéíóú]$")
	c.append_step(u"$", u"n")
	
		
	c = f.create_transform(("s","P"), BASED_ON_ENTRY_FORM, u"[iu]$")
	c.append_step(u"$", u"va")
	c = f.create_transform(("s","P"),BASED_ON_ENTRY_FORM, u"ss$")
	c.append_step(u"$", u"eva")
	c = f.create_transform(("s","P"),BASED_ON_ENTRY_FORM, u"c$")
	c.append_step(u"$", u"qua")
	c = f.create_transform(("s","P"),BASED_ON_ENTRY_FORM, u"[^aeiouáéíóú]$")
	c.append_step(u"$", u"wa")
	c = f.create_transform(("s","P"),BASED_ON_ENTRY_FORM, u"[aeiouáéíóú]$")
	c.append_step(u"$", u"va")
	


	c = f.create_transform(("s","I"), ("s","D"))
	c.append_step(u"$", u"en")
	
	print f(telcu, [w for w in qya.find_words(telcu.key())])
	print f(maama, [w for w in qya.find_words(maama.key())])
	print f(nis, [w for w in qya.find_words(nis.key())])

	
	
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
	decl1.create_transform(("s","N"), BASED_ON_ENTRY_FORM)

	decl1G = decl1.create_transform(("s","G"))
	decl1G.append_step(u"a$", u"ae", True)

	decl2 = decl.create_inflection("n", u"o$")
	decl2N = decl2.create_transform(("s","N"))
	decl2N.append_step(u"o$", u"us", True)
	
	decl2G = decl2.create_transform(("s","G"))
	decl2G.append_step(u"o$", u"iː", True)
	
	decl3 = decl.create_inflection("n")
	
	decl3N = decl3.create_transform(("s","N"), BASED_ON_ENTRY_FORM, u"in", ("m",))
	decl3N.append_step(u"in$", u"en")
	decl3N = decl3.create_transform(("s","N"), BASED_ON_ENTRY_FORM, u"in", ("n",))
	decl3N.append_step(u"in$", u"o")
	 
	decl3G = decl3.create_transform(("s","G"))
	decl3G.append_step(u"$", u"iːs", True)
	
	print decl(lupo, [w for w in lat.find_words(lupo.key())])
	print decl(nomin,  [w for w in lat.find_words(nomin.key())])
	print decl(rosa,  [w for w in lat.find_words(rosa.key())])

if __name__ == "__main__":
	run()
