#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to create Quenya language file.
"""

from core.lect import Lect
from core.bnf import Reference, POSITIVE_CLOSURE, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from core.lexicon import Lexicon, Particle, Word, Lemma
from core.flexion import BASED_ON_LEMMA
import re

def run():
	def show(s):
		print
		print s
		for i, x in enumerate(l.read(s)):
			print u"%d. " % i, x



	def build_lexicon(l, f):
		for h in nouns():
			lemma = Lemma(h[0], 1, h[2], (), h[3])
			l.add_lemma(lemma)
			word = Word(h[1], lemma, (u"s",u"Nom",u"0"))
			l.add_word(word)
			ft = f(lemma, (word,))
			for w in ft.itervalues():
				l.add_word(w)

	def correct_word(l, old, new):
		for v in l.iter_words():
			if re.search(old, v.form, re.I):
				v2 = Word(re.sub(old, new, v.form, re.I), v.lemma, v.categories)
				l.remove_word(v)
				l.add_word(v2)

	def build_flexions(fl):
		f = fl.create_flexion(u"n",())

		tr = f.create_transform((u"s", u"Gen", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[aeiou]?°", u"", True)
		c.append_step(u"ie$", u"ié", True)
		c.append_step(u"cu$", u"qu", True)
		c.append_step(u"l[rns]$", u"ll", True)
		c.append_step(u"[ao]?$", u"o") 
		
		tr = f.create_transform((u"s", u"Poss", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"[^q]ui[^aeiouáéíóú][aeiou]$")
		c.append_step(u"$", u"va")
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou][^aeiouáéíóú][aeiou]$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"a$", u"áva", True)
		c.append_step(u"e$", u"éva", True)
		c.append_step(u"i$", u"íva", True)
		c.append_step(u"o$", u"óva", True)
		c.append_step(u"u$", u"úva", True)
		c = tr.create_chain(BASED_ON_LEMMA, u"ss$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"eva")
		c = tr.create_chain(BASED_ON_LEMMA, u"c$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"c$", u"qua")
		c = tr.create_chain(BASED_ON_LEMMA, u"v$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"wa")
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"va")
		c = tr.create_chain(BASED_ON_LEMMA, u"$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"wa")

		tr = f.create_transform((u"s", u"Dat", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"n")
		c = tr.create_chain(BASED_ON_LEMMA, u"$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"en")
		
		tr = f.create_transform((u"s", u"Abl", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou][lrns]$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"[lrns]$", u"llo")
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"llo")
		c = tr.create_chain(BASED_ON_LEMMA, u"$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"ello")
		
		tr = f.create_transform((u"s", u"All", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou]l$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"da")
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou]n$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"na")
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"nna")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"enna")
		
		tr = f.create_transform((u"s", u"Loc", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou][ln]$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"de")
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou]t$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"se")
		c = tr.create_chain(BASED_ON_LEMMA, u"s$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"s?s$", u"sse")
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"sse")
		c = tr.create_chain(BASED_ON_LEMMA, u"$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"asse")
		
		tr = f.create_transform((u"s", u"Instr", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou][pct]$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"([pct])$", u"n\\1en")

		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou]l$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"den")
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóúmlrn]$)|([aeiouáéíóúmlnr]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"nen")
		c = tr.create_chain(BASED_ON_LEMMA, u"$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"enen")


		tr = f.create_transform((u"s", u"Resp", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"s")
		c = tr.create_chain(BASED_ON_LEMMA, u"$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"es")





		#Nominative non singular

		tr = f.create_transform((u"pl", u"Nom", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aiouáíéóú]$)|([aiouáíéóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"r") 
		c = tr.create_chain(BASED_ON_LEMMA, u"(ie$)|(ie°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"r") 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"e?$", u"i") 

		tr = f.create_transform((u"d", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"u$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"t")
		c = tr.create_chain(BASED_ON_LEMMA, u"ie$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"t")
		c = tr.create_chain(BASED_ON_LEMMA, u"^°")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"u") 
		c = tr.create_chain(BASED_ON_LEMMA, u"[dt].{0,3}$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"[aou]?$", u"u") 
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiouáéíóú]$|[aeiouáéíóú]°$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"t")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"et")

		tr = f.create_transform((u"part", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"li")
		c = tr.create_chain(BASED_ON_LEMMA, u"rsn$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"([aeiouáéíóú])t?[rsn]$", u"\\1lli", True)
		c = tr.create_chain(BASED_ON_LEMMA, u"t$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"eli", True)
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"ili", True)

		#Indirect plural

		tr = f.create_transform((u"pl", u"Gen", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"(ie$)|(ie°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"e$", u"éron") 
		c = tr.create_chain((u"pl", u"Nom", u"0"))
		c.append_step(u"$", u"on") 

		tr = f.create_transform((u"pl",u"Poss", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"i$|e$|(ie)$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"i$|e$|(ie)$", u"íva") 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"iva")

		tr = f.create_transform((u"pl",u"Dat", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"i$|e$|(ie)$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"i$|e$|(ie)$", u"ín") 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"cu$", u"qu", True)
		c.append_step(u"$", u"in")

		tr = f.create_transform((u"pl",u"Abl", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"llon") 
		c = tr.create_chain(BASED_ON_LEMMA, u"(l$)|(l°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"l?l$", u"llon")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"illon")

		tr = f.create_transform((u"pl",u"All", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"nnar") 
		c = tr.create_chain(BASED_ON_LEMMA, u"(n$)|(n°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"n?n$", u"nnar")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"innar")

		tr = f.create_transform((u"pl",u"Loc", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"ssen")
		c = tr.create_chain(BASED_ON_LEMMA, u"t(s$)|(s°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"en")
		c = tr.create_chain(BASED_ON_LEMMA, u"(s$)|(s°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"s?s$", u"ssen")
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiouáéíóú]c$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"c$", u"xen")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"issen")


		tr = f.create_transform((u"pl",u"Instr", u"0"))
		c = tr.create_chain((u"pl",u"Dat", u"0"))
		tr.append_step(u"$", u"en")

		tr = f.create_transform((u"pl",u"Resp", u"0"))
		c = tr.create_chain((u"pl",u"Dat", u"0"))
		tr.append_step(u"n$", u"s")





		#Indirect dual

		tr = f.create_transform((u"d", u"Gen", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"u$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"to")
		c = tr.create_chain(BASED_ON_LEMMA, u"ie$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"e$", u"éto")
		c = tr.create_chain(BASED_ON_LEMMA, u"^°")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"uo") 
		c = tr.create_chain(BASED_ON_LEMMA, u"[dt].{0,3}$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"[aou]?$", u"uo") 
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiouáéíóú][rlsn]$")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"to") 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiouáéíóú]$)|([aeiouáéíóú]°$)")
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"to")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"", True)
		c.append_step(u"$", u"eto")

		tr = f.create_transform((u"d", u"Poss", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"uva", True)
		tr.append_step(u"t$", u"twa", True)

		tr = f.create_transform((u"d", u"Dat", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"un", True)
		tr.append_step(u"t$", u"nt", True)

		tr = f.create_transform((u"d", u"Abl", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"ullo", True)
		tr.append_step(u"t$", u"lto", True)

		tr = f.create_transform((u"d", u"All", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"unna", True)
		tr.append_step(u"t$", u"nta", True)

		tr = f.create_transform((u"d", u"Loc", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"usse", True)
		tr.append_step(u"t$", u"tse", True)

		tr = f.create_transform((u"d", u"Instr", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"unen", True)
		tr.append_step(u"t$", u"nten", True)

		tr = f.create_transform((u"d", u"Resp", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"us", True)
		tr.append_step(u"t$", u"tes", True)


		#Indirect partitive
		tr = f.create_transform((u"part", u"Gen", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"on")

		tr = f.create_transform((u"part", u"Poss", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"([^l])li$", u"\\1lí", True)
		tr.append_step(u"lli$", u"\\1li", True)
		tr.append_step(u"$", u"va")

		tr = f.create_transform((u"part", u"Dat", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"n")

		tr = f.create_transform((u"part", u"Abl", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"llon")

		tr = f.create_transform((u"part", u"All", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"nnar")

		tr = f.create_transform((u"part", u"Loc", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"ssen")

		tr = f.create_transform((u"part", u"Instr", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"([^l])li$", u"\\1lí", True)
		tr.append_step(u"lli$", u"\\1li", True)
		tr.append_step(u"$", u"nen")

		tr = f.create_transform((u"part", u"Resp", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"s")

		#Personal forms

		POSS = {"1s":"nya", u"2":"lya", u"3s":"rya", u"1+2+3": "lva", u"1+3": "lma", u"1d": "mma", u"3pl":"nta"}
		def add_personal(number, case, person):
			x = f.create_transform((number, case, person)) 
			z = x.create_chain(BASED_ON_LEMMA)
			z.append_step(u"[^aeiou]?°", u"", True)
			v = u"e"
			if number == u"pl" or number == u"part" or person == "1":
				v = u"i"
			elif number == u"d":
				v = u"u"
			initial = POSS[person][0]
			z.append_step(u"([^aiouáíéóú"+initial+u"])$", u"\\1"+v, True)
			z.append_step(initial + u"$", u"", True)
			z.append_step(u"$", POSS[person])
			return z

		for p in POSS.iterkeys():
			c = add_personal(u"s", u"Nom", p)

			c = add_personal(u"s", u"Gen", p)
			c.append_step(u"a$", u"o")

			#f.create_transform((u"s", u"Gen", p))
			#c = tr.create_chain((u"s", u"Nom", p))
			#c.append_step(u"a$", u"o")

			c = add_personal(u"s", u"Poss", p)
			c.append_step(u"$", u"va")
			c = add_personal(u"s", u"Dat", p)
			c.append_step(u"$", u"n")
			c = add_personal(u"s", u"Abl", p)
			c.append_step(u"$", u"llo")
			c = add_personal(u"s", u"All", p)
			c.append_step(u"$", u"nna")
			c = add_personal(u"s", u"Loc", p)
			c.append_step(u"$", u"sse")
			c = add_personal(u"s", u"Instr", p)
			c.append_step(u"$", u"nen")
			c = add_personal(u"s", u"Resp", p)
			c.append_step(u"$", u"s")

			c = add_personal(u"pl", u"Nom", p)
			c.append_step(u"$", u"r")
			c = add_personal(u"pl", u"Gen", p)
			c.append_step(u"$", u"ron")
			c = add_personal(u"pl", u"Poss", p)
			c.append_step(u"$", u"iva")
			c = add_personal(u"pl", u"Dat", p)
			c.append_step(u"$", u"in")
			c = add_personal(u"pl", u"Abl", p)
			c.append_step(u"$", u"llon")
			c = add_personal(u"pl", u"All", p)
			c.append_step(u"$", u"nnar")
			c = add_personal(u"pl", u"Loc", p)
			c.append_step(u"$", u"ssen")
			c = add_personal(u"pl", u"Instr", p)
			c.append_step(u"$", u"inen")
			c = add_personal(u"pl", u"Resp", p)
			c.append_step(u"$", u"is")

			c = add_personal(u"d", u"Nom", p)
			c.append_step(u"$", u"t")
			c = add_personal(u"d", u"Gen", p)
			c.append_step(u"$", u"to")
			c = add_personal(u"d", u"Poss", p)
			c.append_step(u"$", u"twa")
			c = add_personal(u"d", u"Dat", p)
			c.append_step(u"$", u"nt")
			c = add_personal(u"d", u"Abl", p)
			c.append_step(u"$", u"lto")
			c = add_personal(u"d", u"All", p)
			c.append_step(u"$", u"nta")
			c = add_personal(u"d", u"Loc", p)
			c.append_step(u"$", u"tse")
			c = add_personal(u"d", u"Instr", p)
			c.append_step(u"$", u"nten")
			c = add_personal(u"d", u"Resp", p)
			c.append_step(u"$", u"tes")

			c = add_personal(u"part", u"Nom", p)
			c.append_step(u"$", u"li")
			c = add_personal(u"part", u"Gen", p)
			c.append_step(u"$", u"lion")
			c = add_personal(u"part", u"Poss", p)
			c.append_step(u"$", u"líva")
			c = add_personal(u"part", u"Dat", p)
			c.append_step(u"$", u"lin")
			c = add_personal(u"part", u"Abl", p)
			c.append_step(u"$", u"lillon")
			c = add_personal(u"part", u"All", p)
			c.append_step(u"$", u"linnar")
			c = add_personal(u"part", u"Loc", p)
			c.append_step(u"$", u"lisse")
			c = add_personal(u"part", u"Instr", p)
			c.append_step(u"$", u"línen")
			c = add_personal(u"part", u"Resp", p)
			c.append_step(u"$", u"lis")


	def nouns():
		d = []
		d.append(  (u"niss", u"nís", u"n", u"woman") )
		d.append(  (u"toro°n", u"toron", u"n", u"brother") )
		d.append(  (u"lómi", u"lóme", u"n", u"night") )
		d.append(  (u"ner", u"nér", u"n", u"man") )
		d.append(  (u"henets°", u"henet", u"n", u"window") )
		d.append(  (u"alda", u"alda", u"n", u"tree") )
		d.append(  (u"amill°", u"amil", u"n", u"mother") )
		d.append(  (u"elen", u"elen", u"n", u"star") )
		d.append(  (u"filic", u"filit", u"n", u"little bird") )
		d.append(  (u"sele°r", u"seler", u"n", u"sister") )
		d.append(  (u"atar", u"atar", u"n", u"father") )
		d.append(  (u"tie", u"tie", u"n", u"path") )
		d.append(  (u"híni", u"hína", u"n", u"child") )
		d.append(  (u"malle", u"malle", u"n", u"street") )
		d.append(  (u"máqua", u"máqua", u"n", u"hand") )
		d.append(  (u"tala°", u"tál", u"n", u"foot") )
		d.append(  (u"tollo°", u"tol", u"n", u"island") )
		d.append(  (u"samb", u"san", u"n", u"chamber") )
		d.append(  (u"olor", u"olos", u"n", u"dream") )
		d.append(  (u"ráv", u"rá", u"n", u"lion") )
		d.append(  (u"cas", u"cár", u"n", u"head") )
		d.append(  (u"cos", u"cor", u"n", u"war") )
		d.append(  (u"mas", u"cor", u"n", u"home") )
		d.append(  (u"nelc", u"nelet", u"n", u"tooth") )
		d.append(  (u"hend", u"hen", u"n", u"eye") )
		d.append(  (u"°pé", u"pé", u"n", u"lip") )
		d.append(  (u"°lar", u"lár", u"n", u"ear") )
		d.append(  (u"rancu", u"ranco", u"n", u"arm") )
		d.append(  (u"telcu", u"telco", u"n", u"leg") )
		return d



	l = Lect(u"qya")
	l.name = u"Quuenya"
	l.english_name = u"Quenya"
	l.append_p_o_s(u"v", (u"transitiveness",), (u"tense", u"person", u"object person"))
	l.append_p_o_s(u"n", (), (u"number", u"case", u"person"))
	l.append_p_o_s(u"adj", (u"transitiveness",), (u"number", u"case", u"person"))
	l.append_p_o_s(u"adv", (), ())
	l.append_p_o_s(u"prep", (u"structure",), (u"object person",))

	build_flexions(l.flexions)
	build_lexicon(l.lexicon, l.flexions)
	correct_word(l.lexicon, u"^malli$", u"maller")
	correct_word(l.lexicon, u"^hínir$", u"híni")
	correct_word(l.lexicon, u"^híninya", u"hínya")
	v, w = "aeiou", u"áéíóú"
	for i in (0,1,2,3,4):
		correct_word(l.lexicon, w[i]+u"ll", v[i]+u"ll")
		correct_word(l.lexicon, w[i]+u"nn", v[i]+u"nn")
		correct_word(l.lexicon, w[i]+u"ss",  v[i]+u"ss")
		correct_word(l.lexicon, w[i]+u"lv",  v[i]+u"lv")
		correct_word(l.lexicon, w[i]+u"mm",  v[i]+u"mm")
		correct_word(l.lexicon, w[i]+u"lm",  v[i]+u"lm")
		correct_word(l.lexicon, w[i]+u"lt",  v[i]+u"lt")
	correct_word(l.lexicon, u"°péo", u"péo")
	correct_word(l.lexicon, u"°laro", u"laro")
	#build_grammar(l.grammar)
	l.properties[u"capitalization"] = 2 #lexical
	l.save(u"test/qya.lct")


if __name__ == "__main__":
	run()

