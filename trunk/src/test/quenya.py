#!/bin/python
# -*- coding: utf-8 -*-

"""
A module to create Quenya language file.
"""

from core.lect import Lect
from core.bnf import Reference, POSITIVE_CLOSURE, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from core.lexicon import Lexicon, Particle, Word, Lemma, CategoryFilter
from core.flexion import BASED_ON_LEMMA, DEFECTIVE
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
				correct_word(table, w[i]+u"ts",  v[i]+u"ts")
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
			if ord(h[0][0])<91:
				if h[0] not in (u"Mumba",u"Sanga"):
					proper = 1
				else:
					proper = 2
			else:
				proper = 0
			for w in ft.itervalues():
				if proper == 0 or (proper == 1 and w.categories[0] == u"s" and w.categories[2] == u"0")or (proper == 2 and w.categories[0] == u"pl" and w.categories[2] == u"0"):
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
				
		for h in adjs():
			if len(h)>2:
				id = h[4]
			else:
				id = 1
			lemma = Lemma(h[0], id, u"adj", (), h[1])
			words = []
			if len(h)>3:
				for j in h[3]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
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
		c = tr.create_chain(BASED_ON_LEMMA, u"[^aeiouáéíóú]?[aeiou](?:[^aeiouáéíóú]y?|qu)[aeiou]$")
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
		c = tr.create_chain(BASED_ON_LEMMA, u"[nlrm][dtpb]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"[dtpb]$", u"wa")
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiouáéíóú]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"va")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"wa")

		tr = f.create_transform((u"s", u"Dat", u"0"))  #no V°
		c = tr.create_chain(BASED_ON_LEMMA) 
		c.append_step(u"[aeiou]?°", u"") 
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"n")

		tr = f.create_transform((u"s", u"Abl", u"0")) #no C°
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"(?<=[aeiouáéíóú])[lnrs]$", u"")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"llo")

		tr = f.create_transform((u"s", u"All", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"(?:[aeiou]l$)|(?:ll°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"da")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"(?<=[aeiouáéíóú])n$", u"")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"nna")

		tr = f.create_transform((u"s", u"Loc", u"0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"(?:[aeiou][ln]$)|(?:ll°$)|(?:nn°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"de")
		c = tr.create_chain(BASED_ON_LEMMA, u"(?:[aeiou]t$)|(?:ts$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"s?$", u"se")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"(?<=[aeiouáéíóú])s$", u"")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"sse")

		tr = f.create_transform((u"s", u"Instr", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"[aeiou][pct]$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"([pct])$", u"n\\1en")

		c = tr.create_chain(BASED_ON_LEMMA, u"(?:[aeiou]l$)|(?:ll°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"den")
		c = tr.create_chain(BASED_ON_LEMMA, u"(?:[aeiou][mrn]$)|(?:rr°$)|(?:nn°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"nen")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"nen")


		tr = f.create_transform((u"s", u"Resp", u"0")) 
		c = tr.create_chain((u"s", u"Dat", u"0"))
		c.append_step(u"n$", u"s")





		#Nominative non singular

		tr = f.create_transform((u"pl", u"Nom", u"0")) #no V°
		c = tr.create_chain(BASED_ON_LEMMA, u"[^aeiouáéíóú][cgh]u$") 
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"gu$", u"gwi")
		c.append_step(u"hu$", u"hwi")
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
		c = tr.create_chain(BASED_ON_LEMMA, u"[cgh]u$")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"cu$", u"quili")
		c.append_step(u"gu$", u"gwili")
		c.append_step(u"hu$", u"hwili")
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
		tr.append_step(u"eu$", u"et")
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
			c.append_step(u"a(?=[^aeiouáíéóú][yw]?[au]?$)", u"á")
			c.append_step(u"a(?=qu[au]?$)", u"á")
			c.append_step(u"e(?=[^aeiouáíéóú][yw]?[au]?$)", u"é")
			c.append_step(u"e(?=qu[au]?$)", u"é")
			c.append_step(u"o(?=[^aeiouáíéóú][yw]?[au]?$)", u"ó")
			c.append_step(u"o(?=qu[au]?)$", u"ó")
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


			tr = f.create_transform((u"inf", u"0", u"0")) 
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


			tr = f.create_transform((u"act-part", u"0", u"0")) 
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
			c.append_step(u"(?<=[^au])$", u"a")
			c.append_step(u"$", u"la")
			
			tr = f.create_transform((u"pass-part", u"0", u"0")) 
			c = tr.create_chain(BASED_ON_LEMMA, u"qu$")
			c.append_step(u"a(?=qu)$", u"á")
			c.append_step(u"e(?=qu)$", u"é")
			c.append_step(u"o(?=qu)$", u"ó")
			c.append_step(u"(?<=[^aeiou])i(?=qu)$", u"í")
			c.append_step(u"(?<=[^aeiouá])u(?=qu)$", u"ú")
			c.append_step(u"$", u"ina")
			c = tr.create_chain(BASED_ON_LEMMA, u"[au]$")
			c.append_step(u"$", u"na")	
			c = tr.create_chain(BASED_ON_LEMMA, u"l$")
			c.append_step(u"$", u"da")	
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"a(?=[^aeiouáíéóú][yw]?)$", u"á")
			c.append_step(u"e(?=[^aeiouáíéóú][yw]?)$", u"é")
			c.append_step(u"o(?=[^aeiouáíéóú][yw]?)$", u"ó")
			c.append_step(u"(?<=[^aeiou])i(?=[^aeiouáíéóú][yw]?)$", u"í")
			c.append_step(u"(?<=[^aeiou])u(?=[^aeiouáíéóú][yw]?)$", u"ú")
			c.append_step(u"(?<=[^rmn])$", u"i")
			c.append_step(u"$", u"na")	

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
						if t==u"aor":
							c.append_step(u"e$", u"i")
						c.append_step(u"$", v[1])
					if transitive:
						for k1, v1 in OBJ.iteritems():
							tr = f.create_transform((t, k, k1))
							c = tr.create_chain((t, u"s", u"0"))
							c.append_step(u"$", v[0]+v1)

			if transitive:
				for k1, v1 in OBJ.iteritems():
					tr = f.create_transform((u"inf", u"0", k1))
					c = tr.create_chain(BASED_ON_LEMMA)
					c.append_step(u"(?<=[^au])$", u"i")
					c.append_step(u"$", u"ta"+v1)

		add_verb_flexion( CategoryFilter("in", (u"Acc", u"Acc+Dat")), True)
		add_verb_flexion( CategoryFilter("ni", (u"Acc", u"Acc+Dat")), False)
		
		f = fl.create_flexion(u"adj",())

		tr = f.create_transform((u"s", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA)

		tr = f.create_transform((u"s", u"Gen", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"o")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"io")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"do")
		tr = f.create_transform((u"s", u"Poss", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"ava")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"iva")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"wa")
		tr = f.create_transform((u"s", u"Dat", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"$", u"n")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"in")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"den")
		tr = f.create_transform((u"s", u"Abl", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"Dat", u"0"))
		c.append_step(u"n$", u"llo")
		tr = f.create_transform((u"s", u"All", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"Dat", u"0"))
		c.append_step(u"n$", u"nna")
		tr = f.create_transform((u"s", u"Loc", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"Dat", u"0"))
		c.append_step(u"n$", u"sse")
		tr = f.create_transform((u"s", u"Instr", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"Dat", u"0"))
		c.append_step(u"$", u"en")
		tr = f.create_transform((u"s", u"Resp", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"Dat", u"0"))
		c.append_step(u"n$", u"s")


		tr = f.create_transform((u"pl", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"e")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"i")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"di")
		tr = f.create_transform((u"pl", u"Gen", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"pl", u"Nom", u"0"))
		c.append_step(u"$", u"on")
		tr = f.create_transform((u"pl", u"Poss", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"pl", u"Dat", u"0"))
		c.append_step(u"n$", u"va")
		tr = f.create_transform((u"pl", u"Dat", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"ain")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"ín")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"din")
		tr = f.create_transform((u"pl", u"Abl", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"Abl", u"0"))
		c.append_step(u"$", u"n")
		tr = f.create_transform((u"pl", u"All", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"All", u"0"))
		c.append_step(u"$", u"r")
		tr = f.create_transform((u"pl", u"Loc", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"s", u"Loc", u"0"))
		c.append_step(u"$", u"n")
		tr = f.create_transform((u"pl", u"Instr", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"pl", u"Dat", u"0"))
		c.append_step(u"$", u"en")
		tr = f.create_transform((u"pl", u"Resp", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"pl", u"Dat", u"0"))
		c.append_step(u"n$", u"s")

		tr = f.create_transform((u"d", u"Nom", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"at")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"it")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"det")

		tr = f.create_transform((u"d", u"Gen", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		c.append_step(u"t$", u"to")

		tr = f.create_transform((u"d", u"Poss", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"t$", u"twa")

		tr = f.create_transform((u"d", u"Dat", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"t$", u"nt")

		tr = f.create_transform((u"d", u"Abl", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"t$", u"lto")

		tr = f.create_transform((u"d", u"All", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"t$", u"nta")

		tr = f.create_transform((u"d", u"Loc", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"t$", u"tse")

		tr = f.create_transform((u"d", u"Instr", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"t$", u"nten")

		tr = f.create_transform((u"d", u"Resp", u"0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain((u"d", u"Nom", u"0"))
		tr.append_step(u"t$", u"tes")


		tr = f.create_transform((u"s", u"Nom", u"abs"))
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"alda")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"ilda")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"[ie]n$", u"ilda")

		tr = f.create_transform((u"s", u"Gen", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"a$", u"o")
		tr = f.create_transform((u"s", u"Poss", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"va")
		tr = f.create_transform((u"s", u"Dat", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"n")
		tr = f.create_transform((u"s", u"Abl", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"llo")
		tr = f.create_transform((u"s", u"All", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"nna")
		tr = f.create_transform((u"s", u"Loc", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"sse")
		tr = f.create_transform((u"s", u"Instr", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"nen")
		tr = f.create_transform((u"s", u"Resp", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"s")

		tr = f.create_transform((u"pl", u"Nom", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"a$", u"e")
		tr = f.create_transform((u"pl", u"Gen", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"a$", u"eon")
		tr = f.create_transform((u"pl", u"Poss", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"iva")
		tr = f.create_transform((u"pl", u"Dat", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"in")
		tr = f.create_transform((u"pl", u"Abl", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"llon")
		tr = f.create_transform((u"pl", u"All", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"llar")
		tr = f.create_transform((u"pl", u"Loc", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"ssen")
		tr = f.create_transform((u"pl", u"Instr", u"abs"))
		c = tr.create_chain((u"pl", u"Dat", u"abs"))
		c.append_step(u"$", u"en")
		tr = f.create_transform((u"pl", u"Resp", u"abs"))
		c = tr.create_chain((u"pl", u"Dat", u"abs"))
		c.append_step(u"n$", u"s")

		tr = f.create_transform((u"d", u"Nom", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"t")

		tr = f.create_transform((u"d", u"Gen", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"to")

		tr = f.create_transform((u"d", u"Poss", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"twa")

		tr = f.create_transform((u"d", u"Dat", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"nt")

		tr = f.create_transform((u"d", u"Abl", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"lto")

		tr = f.create_transform((u"d", u"All", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"nta")

		tr = f.create_transform((u"d", u"Loc", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"tse")

		tr = f.create_transform((u"d", u"Instr", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$",u"nten")

		tr = f.create_transform((u"d", u"Resp", u"abs"))
		c = tr.create_chain((u"s", u"Nom", u"abs"))
		c.append_step(u"$", u"tes")



	def nouns():
		d = []
		d.append(  (u"cas", u"cár", u"cesi") ) #head
		d.append(  (u"cumbo", u"cumbo", u"fucesi") ) #belly
		d.append(  (u"hon", u"hón", u"kawcesi") ) #heart
		d.append(  (u"esse", u"esse", u"tedapemi", [(u"essi", (u"pl",u"Nom",u"0"))] ) ) #name
		d.append(  (u"sambe", u"sambe", u"depi") ) #room
		d.append(  (u"card", u"car", u"byekigi") ) #building
		d.append(  (u"telme", u"telme", u"bidetavi") ) #blanket
		d.append(  (u"limpe", u"limpe", u"zoyfupi") ) #spirits
		d.append(  (u"síra", u"0", u"bape-tovay") ) #today
		d.append(  (u"sovasamb", u"sovasan", u"bodepi") ) #restroom
		d.append(  (u"lindale", u"lindale", u"dinjami") ) #music
		d.append(  (u"colla", u"colla", u"byetavi") ) #garment
		d.append(  (u"tecil", u"tecil", u"bofifusi") ) #pen
		d.append(  (u"hríve", u"hríve", u"cayfemi") ) #winter
		d.append(  (u"laire", u"laire", u"fefemi") ) #summer
		d.append(  (u"henets", u"henet", u"kifigi", [(u"henetwa", (u"s",u"Poss",u"0"))] ) ) #window
		d.append(  (u"rancu", u"ranco", u"twecesi") ) #arm
		d.append(  (u"nonwa", u"nonwa", u"kobisi") ) #computer
		d.append(  (u"palancen", u"palancen", u"kifabisi") ) #television
		d.append(  (u"asta", u"asta", u"ketovi") ) #month
		d.append(  (u"nolyasse", u"nolyasse", u"kokigi") ) #school
		d.append(  (u"ner", u"nér", u"loybegi") ) #man
		d.append(  (u"niss", u"nís", u"lawbegi") ) #woman
		d.append(  (u"híni", u"hína", u"fobegi", [(u"híni", (u"pl",u"Nom",u"0"))] ) )#child
		d.append(  (u"huo", u"huo", u"zovi") ) #dog
		d.append(  (u"yaule", u"yaule/meoi?", u"kwizovi") ) #cat
		d.append(  (u"aiwe", u"aiwe", u"byedami") ) #bird
		d.append(  (u"lingwi", u"lingwe", u"byebomi") ) #fish
		d.append(  (u"mas", u"mar", u"kigi") ) #house
		d.append(  (u"yaxe", u"yaxe", u"lawfutigi") ) #cow
		d.append(  (u"ilim", u"ilin", u"bazopi") ) #milk
		d.append(  (u"massa", u"massa", u"josi") ) #bread
		d.append(  (u"norolle", u"norolle", u"timi") ) #car
		d.append(  (u"ori", u"ore", u"cindonfupi") ) #rice-grain
		d.append(  (u"vinya", u"vinya", u"dawkemo") ) #new
		d.append(  (u"orva", u"orva", u"zobemi") ) #apple
		d.append(  (u"apsa", u"apsa", u"fayzopi") ) #meat
		d.append(  (u"celva", u"celva", u"byefasi") ) #animal
		d.append(  (u"quen", u"quén", u"begi") ) #person
		d.append(  (u"hanta", u"hanta", u"xentegemu") ) #thank you
		d.append(  (u"nen", u"nén", u"bocivi") ) #water
		d.append(  (u"telcu", u"telco", u"jicesi") ) #leg
		d.append(  (u"polca", u"polca", u"jotigi") ) #pig
		d.append(  (u"meldo", u"meldo", u"zoyzevi") ) #friend
		d.append(  (u"aure", u"aure", u"tovi") ) #day
		d.append(  (u"ear", u"ear", u"kebivi") ) #sea
		d.append(  (u"malle", u"malle", u"zegi", [(u"maller", (u"pl",u"Nom",u"0"))]))#road
		d.append(  (u"caima", u"caima", u"kunjisi") ) #bed
		d.append(  (u"telpe", u"telpe", u"jafimi") ) #money
		d.append(  (u"ando", u"ando", u"tifigi") ) #door
		d.append(  (u"tyurd", u"tyur", u"caybafupi") ) #cheese
		d.append(  (u"palallon", u"palallon", u"tebisi") ) #telphone
		d.append(  (u"lómi", u"lóme", u"kunfemi") ) #night
		d.append(  (u"miriand", u"mirian", u"cayjafimi") ) #coin
		d.append(  (u"toro°n", u"toron", u"zutasaw") ) #brother
		d.append(  (u"alda", u"alda", u"jigi") ) #tree
		d.append(  (u"amill°", u"amil", u"ditasaw") ) #mother
		d.append(  (u"elen", u"elen", u"kitisi") ) #star
		d.append(  (u"filic", u"filit", u"byedami") ) #bird (little)
		d.append(  (u"sell", u"seler", u"zitasaw", [(u"selerwa", (u"s",u"Poss",u"0")), (u"selernen", (u"s",u"Instr",u"0"))] ) )
		d.append(  (u"atar", u"atar", u"dutasaw") ) #father
		d.append(  (u"tie", u"tie", u"zuzegi") ) #path
		d.append(  (u"máqua", u"máqua", u"zicesi") ) #hand
		d.append(  (u"tal", u"tál", u"cucesi", [(u"talan", (u"s",u"Dat",u"0")) , (u"talain", (u"pl",u"Dat",u"0"))] ))#foot
		d.append(  (u"toll°", u"tol", u"ketisi", [(u"tollon", (u"s",u"Dat",u"0")), (u"tolloin", (u"pl",u"Dat",u"0"))] ) )#island
		d.append(  (u"ráv", u"rá", u"xozovi") ) #lion
		d.append(  (u"raine", u"raine", u"baxasoni") ) #peace
		d.append(  (u"cos", u"cor", u"bizozugi") ) #war
		d.append(  (u"coa", u"coa", u"kigi", [(u"coavo", (u"s",u"Gen",u"0")),(u"coava", (u"s",u"Poss",u"0"))] ) )#house
		d.append(  (u"mas", u"mar", u"kwicalaymi") ) #home
		d.append(  (u"nelc", u"nelet", u"futevi", [(u"neletse", (u"s",u"Loc",u"0"))] ) ) #tooth
		d.append(  (u"hend", u"hen", u"kicesi") ) #eye
		d.append(  (u"pé", u"pé", u"teduncesi", [(u"péu", (u"d",u"Nom",u"0")), (u"pein", (u"pl",u"Dat",u"0"))]) ) #lip
		d.append(  (u"lar", u"lár", u"foycesi", [(u"laru", (u"d",u"Nom",u"0"))]) ) #ear
		d.append(  (u"fiond", u"fion", u"bedami") ) #hawk
		d.append(  (u"ré", u"ré", u"tovi", [(u"rein", (u"pl",u"Dat",u"0"))]) ) #24hours
		d.append(  (u"pí", u"pí", u"byekagi", [(u"pín", (u"pl",u"Dat",u"0"))]) ) #insect
		d.append(  (u"oxi", u"ohte", u"docesi")) #egg
		
		d.append(  (u"Cemen", u"Cemen", u"Ladijotisi")) #earth
		d.append(  (u"Anar", u"Anar", u"Lakitisi") ) #sun
		#d.append(  Periphrase(g["noun"], u"i Ertaini Nóri") ) #United States
		d.append(  (u"Vintamurta", u"Vintamurta", u"Laryoxodugi") ) #New York City
		d.append(  (u"Colindor", u"Colindor", u"Ladyadugi") ) #India
		d.append(  (u"Marasildor", u"Marasildor", u"Lazidugi") ) #Brazil
		d.append(  (u"Rusindor", u"Rusindor", u"Larudugi") ) #Russia
		d.append(  (u"Canata", u"Canata", u"Lakadugi") ) #Canada
		d.append(  (u"Mornerdor", u"Mornerdor", u"Lajidugi") ) #Nigeria
		d.append(  (u"Endor", u"Endor", u"Lacundugi") ) #China
		d.append(  (u"Peicing", u"Peicin", u"Lacunxodugi") ) #Peking
		d.append(  (u"Mexicosto", u"Mexicosto", u"Laxixodugi") ) #Mexico City
		d.append(  (u"Mumba", u"Mumbai", u"Labunxodugi", [(u"Mumbai", (u"pl",u"Nom",u"0"))]) ) #Bombay
		d.append(  (u"Sampaulo", u"Sampaulo", u"Lapawxodugi") ) #São Paulo
		d.append(  (u"Sanga", u"Sangai", u"Lazanxodugi", [(u"Sangai", (u"pl",u"Nom",u"0"))]) ) #Shanghai
		d.append(  (u"Masiqua", u"Masiqua", u"Laruxodugi") ) #Moscow
		d.append(  (u"Isil", u"Isil", u"Labatisi") ) #moon
		
		return d


	def verbs():
		d = []
		d.append(  (u"na", u"Nom", u"dapa", [(u"ne", (u"past",u"s",u"0"))]) ) 
		d.append(  (u"ea", u"Loc", u"zoga", [(u"ea", (u"pres",u"s",u"0")), (u"engie", (u"perf",u"s",u"0")), (u"enge", (u"past",u"s",u"0"))]) ) 
		d.append(  (u"cen", u"Acc", u"kiva") ) 
		d.append(  (u"mel", u"Acc", u"bakopa") )  #love
		d.append(  (u"mat", u"0", u"fucala") ) #eat
		d.append(  (u"suc", u"0", u"bofucala") ) #drink
		d.append(  (u"ista", u"Acc", u"kopa", [(u"sinte", (u"past",u"s",u"0")), (u"isintie", (u"perf",u"s",u"0"))]) ) 
		d.append(  (u"lelya", u"0", u"ticala", [(u"lende", (u"past",u"s",u"0"))]) )  
		d.append(  (u"ulya", u"Acc", u"tibokavasa", [], 1) )  
		d.append(  (u"ulya", u"0", u"tibokava", [], 2) )  
		d.append(  (u"mar", u"0", u"kwicala", [(u"ambárie", (u"perf",u"s",u"0"))]) )
 		d.append(  (u"móta", u"0", u"bucala") ) #work
		d.append(  (u"mel", u"Acc", u"bakopa") ) #love
		#d.append(  (u"mára", u"Acc", u"zoykopa") ) #like
		d.append(  (u"tyal", u"0", u"dwecala" ) ) #play
		d.append(  (u"canta", u"Acc", u"joykavapa") ) #fix
		d.append(  (u"rac", u"Acc", u"joyjuvapa") ) #break
		d.append(  (u"nyar", u"Acc+Dat", u"tega") ) #tell
		d.append(  (u"quet", u"Dat", u"tegapa") ) #tell
		d.append(  (u"mala", u"0", u"xonkepa") ) #suffer
		d.append(  (u"lor", u"0", u"kunkepa") ) #sleep
		d.append(  (u"mer", u"Acc", u"cakopa") ) #want
		d.append(  (u"appa", u"Acc", u"kenbusa") ) #touch
		d.append(  (u"anta", u"Acc+Dat", u"ximamba", [(u"áne", (u"past",u"s",u"0"))]) )  #give
		return d


	def adjs():
		d = []
		d.append(  (u"sina", u"baso") ) #this
		d.append(  (u"tana", u"zaso") ) #that
		d.append(  (u"alwa", u"joykepo") ) #healthy
		d.append(  (u"mára", u"cakemo") ) #good
		d.append(  (u"olca", u"cafomo") ) #bad
		d.append(  (u"pitya", u"fomo") ) #small
		d.append(  (u"alta", u"kemo") ) #big
		d.append(  (u"yára", u"zonculo") ) #old (vs.young)
		d.append(  (u"silque", u"cinzigo") ) #white
		d.append(  (u"more", u"kunzigo") ) #black
		d.append(  (u"nessa", u"zondelo") ) #young
		d.append(  (u"carne", u"zozigo") ) #red
		d.append(  (u"yerna", u"dawfomo") ) #old (vs.new)
		d.append(  (u"luin",  u"dazigo") ) #blue
		d.append(  (u"malina",  u"fezigo") ) #yellow
		d.append(  (u"hlaiwa", u"joykolo") ) #sick
		d.append(  (u"lauca", u"feculo") ) #warm
		d.append(  (u"ringa", u"fedelo") ) #cold		
		return d
		
	l = Lect(u"qya")
	l.name = u"Quenya"
	l.english_name = u"Quenya"
	l.append_p_o_s(u"v", (u"arguments",), (u"tense", u"person", u"object person"))
	l.append_p_o_s(u"n", (), (u"number", u"case", u"person"))
	l.append_p_o_s(u"adj", (), (u"number", u"case", u"degree"))
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

