#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to create Quenya language file.
"""

from core.lect import Lect
from core.bnf import Reference, POSITIVE_CLOSURE, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from core.lexicon import Lexicon, Particle, Word, Lemma, CategoryFilter
from core.flexion import BASED_ON_LEMMA
import re

def run():
	def show(s):
		print
		print s
		for i, x in enumerate(l.read(s)):
			print u"%d. " % i, x



	def build_lexicon(l, f):
		def correct_table(table):
			correct_word(table, u"^híninya", u"hínya")
			correct_word(table, u"^húa", u"hua")
			v, w = u"aeiou", u"áéíóú"
			for i in (0,1,2,3,4):
				correct_word(table, w[i]+u"ll", v[i]+u"ll")
				correct_word(table, w[i]+u"nn", v[i]+u"nn")
				correct_word(table, w[i]+u"ss",  v[i]+u"ss")
				correct_word(table, w[i]+u"lv",  v[i]+u"lv")
				correct_word(table, w[i]+u"mm",  v[i]+u"mm")
				correct_word(table, w[i]+u"lm",  v[i]+u"lm")
				correct_word(table, w[i]+u"lt",  v[i]+u"lt")
				correct_word(table, w[i]+u"nt",  v[i]+u"nt")
				correct_word(table, w[i]+u"([^lnhcgr])y",  v[i]+u"\\1y")
				correct_word(table, w[i]+u"([^lnhgr])w",  v[i]+u"\\1w")		

		for h in nouns():
			if len(h)>4:
				id = h[4]
			else:
				id = 1
			lemma = Lemma(h[0], id, u"n", (), h[2])
			word = Word(h[1], lemma, (u"s",u"Nom",u"0"))
			words = [word]
			if len(h)>3:
				for j in h[3]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			correct_table(ft)
			l.add_lemma(lemma)
			for w in ft.itervalues():
				l.add_word(w)
				
		for h in verbs():
			if len(h)>4:
				id = h[4]
			else:
				id = 1
			lemma = Lemma(h[0], id, u"v", (h[1],), h[2])
			words = []
			if len(h)>3:
				for j in h[3]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			if lemma.entry_form == u"na":
				lemma.entry_form = u"ná"
				ft[(u"aor", u"s", u"0")]=Word(u"ná", lemma, (u"aor", u"s", u"0"))
				ft[(u"past", u"s", u"0")]=Word(u"né", lemma, (u"past", u"s", u"0"))

			correct_table(ft)			
			l.add_lemma(lemma)
			for w in ft.itervalues():
				l.add_word(w)
		

	def correct_word(table, old, new):
		for k, v in table.iteritems():
			if re.search(old, v.form, re.I):
				v2 = Word(re.sub(old, new, v.form, re.I), v.lemma, v.categories)
				table[k] = v2

	def build_flexions(fl):
		f = fl.create_flexion(u"n",())

		tr = f.create_transform((u"s", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"°", u"") 

		tr = f.create_transform((u"s", u"Gen", u"0")) #no V°
		c = tr.create_chain(BASED_ON_LEMMA, u"ie$") 
		c.append_step(u"[aeiou]?°", u"") 
		c.append_step(u"e$", u"éo")
		c = tr.create_chain(BASED_ON_LEMMA, u"cu$") 
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"cu$", u"quo")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"[ao]?$", u"o")
		
		tr = f.create_transform((u"s", u"Poss", u"0")) #no C°
		c = tr.create_chain(BASED_ON_LEMMA, u"[^q]ui[^aeiouáéíóú][aeiou]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"va")
		c = tr.create_chain(BASED_ON_LEMMA, u"[^aeiouáéíóú]?[aeiou]([^aeiouáéíóú]y?|qu)[aeiou]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"a$", u"áva")
		c.append_step(u"e$", u"éva")
		c.append_step(u"i$", u"íva")
		c.append_step(u"o$", u"óva")
		c.append_step(u"u$", u"úva")
		c = tr.create_chain(BASED_ON_LEMMA, u"ss$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"eva")
		c = tr.create_chain(BASED_ON_LEMMA, u"c$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"c$", u"qua")
		c = tr.create_chain(BASED_ON_LEMMA, u"(v$)|(v°$)")
		c.append_step(u"[^aeiouv]?°", u"")
		c.append_step(u"$", u"a")
		c = tr.create_chain(BASED_ON_LEMMA, u"[nl][dt]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"[dt]$", u"wa")
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiouáéíóú]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"va")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"wa")

		tr = f.create_transform((u"s", u"Dat", u"0"))  #no V°
		c = tr.create_chain(BASED_ON_LEMMA) 
		c.append_step(u"[aeiou]?°", u"") 
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"n")
		
		tr = f.create_transform((u"s", u"Abl", u"0")) #no C°
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"([aeiouáéíóú])[lnrs]$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"llo")
		
		tr = f.create_transform((u"s", u"All", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiou]l$)|(ll°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"da")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"([aeiouáéíóú])n$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"nna")
		
		tr = f.create_transform((u"s", u"Loc", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiou][ln]$)|(ll°$)|(nn°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"de")
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiou]t$)|(ts$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"s?$", u"se")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"([aeiouáéíóú])s$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"sse")
		
		tr = f.create_transform((u"s", u"Instr", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou][pct]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"([pct])$", u"n\\1en")

		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiou]l$)|(ll°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"den")
		c = tr.create_chain(BASED_ON_LEMMA, u"([aeiou][mrn]$)|(rr°$)|(nn°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"nen")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"nen")


		tr = f.create_transform((u"s", u"Resp", u"0")) 
		c = tr.create_chain((u"s", u"Dat", u"0"))
		c.append_step(u"n$", u"s")





		#Nominative non singular

		tr = f.create_transform((u"pl", u"Nom", u"0")) #no V°
		c = tr.create_chain(BASED_ON_LEMMA, u"[^aeiouáéíóú]cu$") 
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"cu$", u"qui")
		c = tr.create_chain(BASED_ON_LEMMA, u"[aiouáéíóú]$|ie$") 
		c.append_step(u"[aeiou]?°", u"") 
		c.append_step(u"$", u"r")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"e?$", u"i")

		tr = f.create_transform((u"d", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"u$|ie$")
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"$", u"t")
		c = tr.create_chain(BASED_ON_LEMMA, u"[dt].{0,4}$")
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"[aou]?$", u"u")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"t")

		tr = f.create_transform((u"part", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"cu$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"cu$", u"quili")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"([aeiouáéíóú])[nrs]$", u"\\1l")
		c.append_step(u"ll$", u"l")
		c.append_step(u"([^aeiouáéíóúl])$", u"\\1e")
		c.append_step(u"$", u"li")

		#Indirect plural

		tr = f.create_transform((u"pl", u"Gen", u"0")) 
		c = tr.create_chain((u"pl", u"Nom", u"0"))
		c.append_step(u"ier$", u"iér") 
		c.append_step(u"$", u"on") 

		tr = f.create_transform((u"pl",u"Poss", u"0"))
		c = tr.create_chain((u"pl",u"Dat", u"0"))
		tr.append_step(u"n$", u"va")

		tr = f.create_transform((u"pl",u"Dat", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"i$|e$|(ie)$")
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"i$|e$|(ie)$", u"ín") 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"cu$", u"qu")
		c.append_step(u"$", u"in")

		tr = f.create_transform((u"pl",u"Abl", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"([aeiouáéíóú])l$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"llon")

		tr = f.create_transform((u"pl",u"All", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"([aeiouáéíóú])n$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"nnar")

		tr = f.create_transform((u"pl",u"Loc", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, "ts$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"en")
		c = tr.create_chain(BASED_ON_LEMMA, "c$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"c$", u"xen")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"s$", u"")
		c.append_step(u"([aeiouáéíóú])s$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"ssen")


		tr = f.create_transform((u"pl",u"Instr", u"0"))
		c = tr.create_chain((u"pl",u"Dat", u"0"))
		tr.append_step(u"$", u"en")

		tr = f.create_transform((u"pl",u"Resp", u"0"))
		c = tr.create_chain((u"pl",u"Dat", u"0"))
		tr.append_step(u"n$", u"s")





		#Indirect dual

		tr = f.create_transform((u"d", u"Gen", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"([aeiouáéíóú][lnrs])et$", u"\\1t")
		tr.append_step(u"iet$", u"iét")
		c.append_step(u"$", u"o")

		tr = f.create_transform((u"d", u"Poss", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"uva")
		tr.append_step(u"t$", u"twa")

		tr = f.create_transform((u"d", u"Dat", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"un")
		tr.append_step(u"t$", u"nt")

		tr = f.create_transform((u"d", u"Abl", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"ullo")
		tr.append_step(u"t$", u"lto")

		tr = f.create_transform((u"d", u"All", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"unna")
		tr.append_step(u"t$", u"nta")

		tr = f.create_transform((u"d", u"Loc", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"usse")
		tr.append_step(u"t$", u"tse")

		tr = f.create_transform((u"d", u"Instr", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"unen")
		tr.append_step(u"t$", u"nten")

		tr = f.create_transform((u"d", u"Resp", u"0"))
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"u$", u"us")
		tr.append_step(u"t$", u"tes")


		#Indirect partitive
		tr = f.create_transform((u"part", u"Gen", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"on")

		tr = f.create_transform((u"part", u"Poss", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"([^l])li$", u"\\1lí")
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
		tr.append_step(u"([^l])li$", u"\\1lí")
		tr.append_step(u"$", u"nen")

		tr = f.create_transform((u"part", u"Resp", u"0"))
		c = tr.create_chain((u"part", u"Nom", u"0"))
		tr.append_step(u"$", u"s")

		#Personal forms

		POSS = {u"1s":u"nya", u"2":u"lya", u"3s":"rya", u"1+2+3": u"lva", u"1+3": u"lma", u"1d": u"mma", u"3pl":u"nta"}
		def add_personal(number, case, person):
			x = f.create_transform((number, case, person)) 
			z = x.create_chain(BASED_ON_LEMMA)
			z.append_step(u"[^aeiou]?°", u"")
			v = u"e"
			if number == u"pl" or number == u"part" or person == "1":
				v = u"i"
			elif number == u"d":
				v = u"u"
			initial = POSS[person][0]
			z.append_step(u"([^aeiouáíéóú"+initial+u"])$", u"\\1"+v)
			z.append_step(initial + u"$", u"")
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


		#verbs
		def add_verb_flexion(args, transitive):
			f = fl.create_flexion(u"v", (args,))

			tr = f.create_transform((u"aor", u"s", u"0")) 
			c = tr.create_chain(BASED_ON_LEMMA, "a$")
			c = tr.create_chain(BASED_ON_LEMMA, "u$")
			c.append_step(u"u$", u"o")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"$", u"e")
			tr = f.create_transform((u"aor", u"pl", u"0")) 
			c = tr.create_chain(BASED_ON_LEMMA, "[au]$")
			c.append_step(u"$", u"r")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"$", u"ir")

			tr = f.create_transform((u"pres", u"s", u"0")) 
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"a([^aeiouáíéóú][yw]?[au]?)$", u"á\\1")
			c.append_step(u"a(qu[au]?)$", u"á\\1")
			c.append_step(u"e([^aeiouáíéóú][yw]?[au]?)$", u"é\\1")
			c.append_step(u"e(qu[au]?)$", u"é\\1")
			c.append_step(u"o([^aeiouáíéóú][yw]?[au]?)$", u"ó\\1")
			c.append_step(u"o(qu[au]?)$", u"ó\\1")
			c.append_step(u"([^aeiouáíéóú])i([^aeiouáíéóú][yw]?[au]?)$", u"\\1í\\2")
			c.append_step(u"([^aeiouáíéóú])i(qu[au]?)$", u"\\1í\\2")
			c.append_step(u"([^aeiouáíéóú])u([^aeiouáíéóú][yw]?[au]?)$", u"\\1ú\\2")
			c.append_step(u"([^aeiouáíéóú])u(qu[au]?)$", u"\\1ú\\2")
			c.append_step(u"a$", u"e")
			c.append_step(u"$", u"a")
			tr = f.create_transform((u"pres", u"pl", u"0")) 
			c = tr.create_chain((u"pres", u"s", u"0"))
			c.append_step(u"$", u"r")


			tr = f.create_transform((u"past", u"s", u"0")) 
			c = tr.create_chain(BASED_ON_LEMMA, u"ha$")
			c.append_step(u"$", u"ne")
			c = tr.create_chain(BASED_ON_LEMMA, u"wa$")
			c.append_step(u"wa$", u"ngwe")
			
			if transitive:
				c = tr.create_chain(BASED_ON_LEMMA, u"ya$")
				c.append_step(u"$", u"ne")
			else:
				c = tr.create_chain(BASED_ON_LEMMA, u"[rnm]ya$")
				c.append_step(u"ya$", u"ne")
				c = tr.create_chain(BASED_ON_LEMMA, u"tya$")
				c.append_step(u"tya$", u"nte")
				c = tr.create_chain(BASED_ON_LEMMA, u"pya$")
				c.append_step(u"pya$", u"mpe")
				c = tr.create_chain(BASED_ON_LEMMA, u"lya$")
				c.append_step(u"lya$", u"lle")
				c = tr.create_chain(BASED_ON_LEMMA, u"[sv]ya$")
				c.append_step(u"a([sv]ya)$", u"á\\1")
				c.append_step(u"e([sv]ya)$", u"é\\1")
				c.append_step(u"o([sv]ya)$", u"ó\\1")
				c.append_step(u"([^aeiouáíéóú])i([sv]ya)$", u"\\1í\\2")
				c.append_step(u"([^aeiouáíéóú])u([sv]ya)$", u"\\1ú\\2")
				c.append_step(u"$", u"e")
				c = tr.create_chain(BASED_ON_LEMMA, u"ya$")
				c.append_step(u"ya$", u"ne")
				
			c = tr.create_chain(BASED_ON_LEMMA, u"[rnm]$")
			c.append_step(u"$", u"ne")
			c = tr.create_chain(BASED_ON_LEMMA, u"([tc]$)|(qu$)")
			c.append_step(u"([tc]$)|(qu$)", u"n\\1e")
			c = tr.create_chain(BASED_ON_LEMMA, u"t[au]$")
			c.append_step(u"t[au]$", u"nte")
			c = tr.create_chain(BASED_ON_LEMMA, u"p[au]?$")
			c.append_step(u"p[au]?$", u"mpe")
			c = tr.create_chain(BASED_ON_LEMMA, u"l[au]?$")
			c.append_step(u"l[au]?$", u"lle")
			c = tr.create_chain(BASED_ON_LEMMA, u"[sv]$")
			c.append_step(u"a([sv]$)", u"á\\1")
			c.append_step(u"e([sv]$)", u"é\\1")
			c.append_step(u"o([sv]$)", u"ó\\1")
			c.append_step(u"([^aeiouáíéóú])i([sv])$", u"\\1í\\2")
			c.append_step(u"([^aeiouáíéóú])u([sv])$", u"\\1ú\\2")
			c.append_step(u"$", u"e")
			c = tr.create_chain(BASED_ON_LEMMA, u"[^aeiouáíéóú]qu[au]$")
			c.append_step(u"$", u"ne") 
			c = tr.create_chain(BASED_ON_LEMMA, u"x[au]$")
			c.append_step(u"$", u"ne")
			c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou][ui][^aeiouáíéóú][au]$")
			c.append_step(u"$", u"ne")
			c = tr.create_chain(BASED_ON_LEMMA, u"[^aeiou][^aeiouáíéóú][au]$")
			c.append_step(u"$", u"ne")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"$", u"ne") 
			tr = f.create_transform((u"past", u"pl", u"0")) 
			c = tr.create_chain((u"past", u"s", u"0"))
			c.append_step(u"$", u"r")



			tr = f.create_transform((u"perf", u"s", u"0"))
			c = tr.create_chain(BASED_ON_LEMMA,u"^[aeiouáíéóú]")
			c.append_step(u"y*[au]?$", u"ie")
			c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou]{2}([^aeiouáíéóú]|qu)y*[au]?$")
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)([aeiou])([aeiou])([^aeiouáíéóú]|qu)$", u"\\2\\1\\2\\3\\4")
			c.append_step(u"$", u"ie")
			c = tr.create_chain(BASED_ON_LEMMA, u"[aeiouáíéóú]([^aeiouáíéóú]|qu)y*[au]?$")
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)[aá]([^aeiouáíéóú]|qu)$", u"a\\1á\\2")
			c.append_step(u"^(.*)[eé]([^aeiouáíéóú]|qu)$", u"e\\1é\\2")
			c.append_step(u"^(.*)[ií]([^aeiouáíéóú]|qu)$", u"i\\1í\\2")
			c.append_step(u"^(.*)[oó]([^aeiouáíéóú]|qu)$", u"o\\1ó\\2")
			c.append_step(u"^(.*)[uú]([^aeiouáíéóú]|qu)$", u"u\\1ú\\2")
			c.append_step(u"$", u"ie")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)a", u"a\\1a")
			c.append_step(u"^(.*)e", u"e\\1e")
			c.append_step(u"^(.*)i", u"i\\1i")
			c.append_step(u"^(.*)o", u"o\\1o")
			c.append_step(u"^(.*)u", u"u\\1u")
			c.append_step(u"$", u"ie")
			tr = f.create_transform((u"perf", u"pl", u"0")) 
			c = tr.create_chain((u"perf", u"s", u"0"))
			c.append_step(u"$", u"r")

			tr = f.create_transform((u"fut", u"s", u"0")) 
			c = tr.create_chain(BASED_ON_LEMMA, "u$")
			c.append_step(u"u$", u"úva")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"a?$", u"uva")
			tr = f.create_transform((u"fut", u"pl", u"0")) 
			c = tr.create_chain((u"fut", u"s", u"0"))
			c.append_step(u"$", u"r")

			TENSE = [u"aor",u"pres",u"past",u"perf",u"fut"]
			SUBJ = {u"1s":[u"nye",u"n"], u"2":[u"lye",u"l"], u"3s":["rye","s"], u"1+2+3": [u"lve"], u"1+3": [u"lme"], u"1d": [u"mme"], u"3pl":[u"nte"]}
			OBJ = {u"1s":u"n", u"2":u"l", u"3s":"s", u"3pl":u"t"}
			for t in TENSE:
				for k,v in SUBJ.iteritems():
					tr = f.create_transform((t, k, u"0"))
					c = tr.create_chain((t, u"s", u"0"))
					if len(v)==1:
						c.append_step(u"$", v[0])
					else:
						c.append_step(u"$", v[1])
					if transitive:
						for k1, v1 in OBJ.iteritems():
							tr = f.create_transform((t, k, k1))
							c = tr.create_chain((t, u"s", u"0"))
							c.append_step(u"$", v[0]+v1)
		
		add_verb_flexion( CategoryFilter("in", (u"Acc", u"Acc+Dat")), True)
		add_verb_flexion( CategoryFilter("ni", (u"Acc", u"Acc+Dat")), False)
		

	def nouns():
		d = []
		d.append(  (u"niss", u"nís", u"woman") )
		d.append(  (u"toro°n", u"toron", u"brother") )
		d.append(  (u"lómi", u"lóme", u"night") )
		d.append(  (u"ner", u"nér", u"man") )
		d.append(  (u"henets", u"henet", u"window", [(u"henetwa", (u"s",u"Poss",u"0"))] ) )
		d.append(  (u"alda", u"alda", u"tree") )
		d.append(  (u"amill°", u"amil", u"mother") )
		d.append(  (u"elen", u"elen", u"star") )
		d.append(  (u"filic", u"filit", u"little bird") )
		d.append(  (u"sell", u"seler", u"sister", [(u"selerwa", (u"s",u"Poss",u"0")), (u"selernen", (u"s",u"Instr",u"0"))] ) )
		d.append(  (u"atar", u"atar", u"father") )
		d.append(  (u"tie", u"tie", u"path") )
		d.append(  (u"híni", u"hína", u"child", [(u"híni", (u"pl",u"Nom",u"0"))] ) )
		d.append(  (u"malle", u"malle", u"street", [(u"maller", (u"pl",u"Nom",u"0"))]))
		d.append(  (u"máqua", u"máqua", u"hand") )
		d.append(  (u"tal", u"tál", u"foot", [(u"talan", (u"s",u"Dat",u"0")) , (u"talain", (u"pl",u"Dat",u"0"))] ))
		d.append(  (u"toll°", u"tol", u"island", [(u"tollon", (u"s",u"Dat",u"0")), (u"tolloin", (u"pl",u"Dat",u"0"))] ) )
		d.append(  (u"samb", u"san", u"chamber") )
		d.append(  (u"húa°n", u"huan", u"hound") )
		d.append(  (u"olor", u"olos", u"dream") )
		d.append(  (u"ráv", u"rá", u"lion") )
		d.append(  (u"cas", u"cár", u"head") )
		d.append(  (u"cos", u"cor", u"war") )
		d.append(  (u"coa", u"coa", u"house", [(u"coavo", (u"s",u"Gen",u"0")),(u"coava", (u"s",u"Poss",u"0"))] ) )
		d.append(  (u"mas", u"mar", u"home") )
		d.append(  (u"nelc", u"nelet", u"tooth", [(u"neletse", (u"s",u"Loc",u"0"))] ) )
		d.append(  (u"ilim", u"ilin", u"milk") )
		d.append(  (u"hend", u"hen", u"eye") )
		d.append(  (u"pé", u"pé", u"lip", [(u"péu", (u"d",u"Nom",u"0")), (u"pein", (u"pl",u"Dat",u"0"))]) )
		d.append(  (u"lar", u"lár", u"ear", [(u"laru", (u"d",u"Nom",u"0"))]) ) 
		d.append(  (u"rancu", u"ranco", u"arm") )
		d.append(  (u"telcu", u"telco", u"leg") )
		d.append(  (u"fiond", u"fion", u"hawk") )
		d.append(  (u"ré", u"ré", u"day", [(u"rein", (u"pl",u"Dat",u"0"))]) ) 
		d.append(  (u"pí", u"pí", u"insect", [(u"pín", (u"pl",u"Dat",u"0"))]) ) 
		return d


	def verbs():
		d = []
		d.append(  (u"na", u"Nom", u"be", [(u"ne", (u"past",u"s",u"0"))]) ) 
		d.append(  (u"ea", u"0", u"be", [(u"ea", (u"pres",u"s",u"0")), (u"engie", (u"perf",u"s",u"0")), (u"enge", (u"past",u"s",u"0"))]) ) 
		d.append(  (u"cen", u"Acc", u"see") ) 
		d.append(  (u"mel", u"Acc", u"love") ) 
		d.append(  (u"mat", u"Acc", u"eat") )
		d.append(  (u"suc", u"Acc", u"drink") )
		d.append(  (u"anta", u"Acc+Dat", u"give", [(u"áne", (u"past",u"s",u"0"))]) ) 
		d.append(  (u"ista", u"Acc", u"know", [(u"sinte", (u"past",u"s",u"0"))]) ) 
		d.append(  (u"lelya", u"0", u"go", [(u"lende", (u"past",u"s",u"0"))]) )  
		d.append(  (u"ulya", u"Acc", u"pour", [], 1) )  
		d.append(  (u"ulya", u"0", u"pour", [], 2) )  
		d.append(  (u"mar", u"0", u"dwell", [(u"ambárie", (u"perf",u"s",u"0"))]) ) 
		return d


	l = Lect(u"qya")
	l.name = u"Quenya"
	l.english_name = u"Quenya"
	l.append_p_o_s(u"v", (u"arguments",), (u"tense", u"person", u"object person"))
	l.append_p_o_s(u"n", (), (u"number", u"case", u"person"))
	l.append_p_o_s(u"adj", (u"transitiveness",), (u"number", u"case", u"person"))
	l.append_p_o_s(u"adv", (), ())
	l.append_p_o_s(u"prep", (u"argument",), (u"object person",))
	build_flexions(l.flexions)
	build_lexicon(l.lexicon, l.flexions)
	print l.lexicon
	#build_grammar(l.grammar)
	l.properties[u"capitalization"] = 2 #lexical
	l.save(u"test/qya.lct")


if __name__ == "__main__":
	run()

