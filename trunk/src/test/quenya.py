﻿#!/bin/python
# -*- coding: utf-8 -*-

"""
A module to create Quenya language file.
"""

from core.lect import Lect
from core.bnf import Reference, POSITIVE_CLOSURE, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from core.lexicon import Lexicon, Particle, Word, Lemma, CategoryFilter, WordCategoryFilter, WordFilter
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
			lemma = Lemma(h[0], id, "n", (), h[2])
			word = Word(h[1], lemma, ("s","Nom","0"))
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
				if proper == 0 or (proper == 1 and w.categories[0] == "s" and w.categories[2] == "0")or (proper == 2 and w.categories[0] == "pl" and w.categories[2] == "0"):
					l.add_word(w)

		for h in verbs():
			if len(h)>4:
				id = h[4]
			else:
				id = 1
			lemma = Lemma(h[0], id, "v", (h[1],), h[2])
			words = []
			if len(h)>3:
				for j in h[3]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			if lemma.entry_form == u"na":
				lemma.entry_form = u"ná"
				ft[("aor", "s", "0")]=Word(u"ná", lemma, (u"aor", "s", "0"))
				ft[(u"past", "s", "0")]=Word(u"né", lemma, (u"past", "s", "0"))

			correct_table(ft)			
			l.add_lemma(lemma)
			for w in ft.itervalues():
				l.add_word(w)
				
		for h in adjs():
			if len(h)>3:
				id = h[3]
			else:
				id = 1
			lemma = Lemma(h[0], id, "adj", (), h[1])
			words = []
			if len(h)>2:
				for j in h[2]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			correct_table(ft)			
			
			l.add_lemma(lemma)
			for w in ft.itervalues():
				l.add_word(w)
				
			if h[0][-1] == u"a":
				adverb = re.sub(u"a$",u"ave", h[0])
			elif h[0][-1] == u"e":
				adverb = re.sub(u"e$",u"ive", h[0])
			elif h[0][-1] == u"n":
				adverb = re.sub(u"n$",u"mbe", h[0])
			if h[0] == u"mára":
				adverb = u"vande"
			
			adverb_gloss = re.sub(u"o$",u"e", h[1])
			l.add_word(Word(adverb, Lemma(adverb, id, "adv", (), adverb_gloss), ()))
		
		l.add_word(Word(u"i", Particle(u"i", 1, "adj", ()), ("0", "0", "0")))
		l.add_word(Word(u"er", Particle(u"er", 1, "adj", ()), ("0", "0", "0")))
		


	def correct_word(table, old, new):
		for k, v in table.iteritems():
			if re.search(old, v.form, re.I):
				v2 = Word(re.sub(old, new, v.form, re.I), v.lemma, v.categories)
				table[k] = v2

	def build_flexions(fl):
		f = fl.create_flexion("n",())

		tr = f.create_transform(("s", "Nom", "0"))
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"°", u"") 

		tr = f.create_transform(("s", "Gen", "0")) #no V°
		c = tr.create_chain(BASED_ON_LEMMA, u"ie$") 
		c.append_step(u"[aeiou]?°", u"") 
		c.append_step(u"e$", u"éo")
		c = tr.create_chain(BASED_ON_LEMMA, u"cu$") 
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"cu$", u"quo")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"[ao]?$", u"o")

		tr = f.create_transform(("s", "Poss", "0")) #no C°
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

		tr = f.create_transform(("s", "Dat", "0"))  #no V°
		c = tr.create_chain(BASED_ON_LEMMA) 
		c.append_step(u"[aeiou]?°", u"") 
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"n")

		tr = f.create_transform(("s", "Abl", "0")) #no C°
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"(?<=[aeiouáéíóú])[lnrs]$", u"")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"llo")

		tr = f.create_transform(("s", "All", "0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"(?:[aeiou]l$)|(?:ll°$)")
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"$", u"da")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"(?<=[aeiouáéíóú])n$", u"")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"nna")

		tr = f.create_transform(("s", "Loc", "0")) 
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

		tr = f.create_transform(("s", "Instr", "0"))
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


		tr = f.create_transform(("s", "Resp", "0")) 
		c = tr.create_chain(("s", "Dat", "0"))
		c.append_step(u"n$", u"s")





		#Nominative non singular

		tr = f.create_transform(("pl", "Nom", "0")) #no V°
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

		tr = f.create_transform(("d", "Nom", "0"))
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

		tr = f.create_transform(("part", "Nom", "0"))
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

		tr = f.create_transform(("pl", "Gen", "0")) 
		c = tr.create_chain(("pl", "Nom", "0"))
		c.append_step(u"ier$", u"iér") 
		c.append_step(u"$", u"on") 

		tr = f.create_transform(("pl","Poss", "0"))
		c = tr.create_chain(("pl","Dat", "0"))
		tr.append_step(u"n$", u"va")

		tr = f.create_transform(("pl","Dat", "0")) 
		c = tr.create_chain(BASED_ON_LEMMA, u"i$|e$|(ie)$")
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"i$|e$|(ie)$", u"ín") 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[aeiou]?°", u"")
		c.append_step(u"cu$", u"qu")
		c.append_step(u"$", u"in")

		tr = f.create_transform(("pl","Abl", "0")) 
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"([aeiouáéíóú])l$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"llon")

		tr = f.create_transform(("pl","All", "0"))
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"[^aeiou]?°", u"")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"([aeiouáéíóú])n$", u"\\1")
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"nnar")

		tr = f.create_transform(("pl","Loc", "0"))
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


		tr = f.create_transform(("pl","Instr", "0"))
		c = tr.create_chain(("pl","Dat", "0"))
		tr.append_step(u"$", u"en")

		tr = f.create_transform(("pl","Resp", "0"))
		c = tr.create_chain(("pl","Dat", "0"))
		tr.append_step(u"n$", u"s")





		#Indirect dual

		tr = f.create_transform(("d", "Gen", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"eu$", u"et")
		tr.append_step(u"([aeiouáéíóú][lnrs])et$", u"\\1t")
		tr.append_step(u"iet$", u"iét")
		c.append_step(u"$", u"o")

		tr = f.create_transform(("d", "Poss", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"u$", u"uva")
		tr.append_step(u"t$", u"twa")

		tr = f.create_transform(("d", "Dat", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"u$", u"un")
		tr.append_step(u"t$", u"nt")

		tr = f.create_transform(("d", "Abl", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"u$", u"ullo")
		tr.append_step(u"t$", u"lto")

		tr = f.create_transform(("d", "All", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"u$", u"unna")
		tr.append_step(u"t$", u"nta")

		tr = f.create_transform(("d", "Loc", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"u$", u"usse")
		tr.append_step(u"t$", u"tse")

		tr = f.create_transform(("d", "Instr", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"u$", u"unen")
		tr.append_step(u"t$", u"nten")

		tr = f.create_transform(("d", "Resp", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"u$", u"us")
		tr.append_step(u"t$", u"tes")


		#Indirect partitive
		tr = f.create_transform(("part", "Gen", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"$", u"on")

		tr = f.create_transform(("part", "Poss", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"([^l])li$", u"\\1lí")
		tr.append_step(u"$", u"va")

		tr = f.create_transform(("part", "Dat", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"$", u"n")

		tr = f.create_transform(("part", "Abl", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"$", u"llon")

		tr = f.create_transform(("part", "All", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"$", u"nnar")

		tr = f.create_transform(("part", "Loc", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"$", u"ssen")

		tr = f.create_transform(("part", "Instr", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"([^l])li$", u"\\1lí")
		tr.append_step(u"$", u"nen")

		tr = f.create_transform(("part", "Resp", "0"))
		c = tr.create_chain(("part", "Nom", "0"))
		tr.append_step(u"$", u"s")

		#Personal forms

		POSS = {u"1s":u"nya", u"2":u"lya", u"3s":"rya", u"1+2+3": u"lva", u"1+3": u"lma", u"1d": u"mma", u"3pl":u"nta"}
		def add_personal(number, case, person):
			x = f.create_transform((number, case, person)) 
			z = x.create_chain(BASED_ON_LEMMA)
			z.append_step(u"[^aeiou]?°", u"")
			v = u"e"
			if number == "pl" or number == "part" or person == "1":
				v = u"i"
			elif number == "d":
				v = u"u"
			initial = POSS[person][0]
			z.append_step(u"([^aeiouáíéóú"+initial+u"])$", u"\\1"+v)
			z.append_step(initial + u"$", u"")
			z.append_step(u"$", POSS[person])
			return z

		for p in POSS.iterkeys():
			c = add_personal("s", "Nom", p)

			c = add_personal("s", "Gen", p)
			c.append_step(u"a$", u"o")

			#f.create_transform(("s", "Gen", p))
			#c = tr.create_chain(("s", "Nom", p))
			#c.append_step(u"a$", u"o")

			c = add_personal("s", "Poss", p)
			c.append_step(u"$", u"va")
			c = add_personal("s", "Dat", p)
			c.append_step(u"$", u"n")
			c = add_personal("s", "Abl", p)
			c.append_step(u"$", u"llo")
			c = add_personal("s", "All", p)
			c.append_step(u"$", u"nna")
			c = add_personal("s", "Loc", p)
			c.append_step(u"$", u"sse")
			c = add_personal("s", "Instr", p)
			c.append_step(u"$", u"nen")
			c = add_personal("s", "Resp", p)
			c.append_step(u"$", u"s")

			c = add_personal("pl", "Nom", p)
			c.append_step(u"$", u"r")
			c = add_personal("pl", "Gen", p)
			c.append_step(u"$", u"ron")
			c = add_personal("pl", "Poss", p)
			c.append_step(u"$", u"iva")
			c = add_personal("pl", "Dat", p)
			c.append_step(u"$", u"in")
			c = add_personal("pl", "Abl", p)
			c.append_step(u"$", u"llon")
			c = add_personal("pl", "All", p)
			c.append_step(u"$", u"nnar")
			c = add_personal("pl", "Loc", p)
			c.append_step(u"$", u"ssen")
			c = add_personal("pl", "Instr", p)
			c.append_step(u"$", u"inen")
			c = add_personal("pl", "Resp", p)
			c.append_step(u"$", u"is")

			c = add_personal("d", "Nom", p)
			c.append_step(u"$", u"t")
			c = add_personal("d", "Gen", p)
			c.append_step(u"$", u"to")
			c = add_personal("d", "Poss", p)
			c.append_step(u"$", u"twa")
			c = add_personal("d", "Dat", p)
			c.append_step(u"$", u"nt")
			c = add_personal("d", "Abl", p)
			c.append_step(u"$", u"lto")
			c = add_personal("d", "All", p)
			c.append_step(u"$", u"nta")
			c = add_personal("d", "Loc", p)
			c.append_step(u"$", u"tse")
			c = add_personal("d", "Instr", p)
			c.append_step(u"$", u"nten")
			c = add_personal("d", "Resp", p)
			c.append_step(u"$", u"tes")

			c = add_personal("part", "Nom", p)
			c.append_step(u"$", u"li")
			c = add_personal("part", "Gen", p)
			c.append_step(u"$", u"lion")
			c = add_personal("part", "Poss", p)
			c.append_step(u"$", u"líva")
			c = add_personal("part", "Dat", p)
			c.append_step(u"$", u"lin")
			c = add_personal("part", "Abl", p)
			c.append_step(u"$", u"lillon")
			c = add_personal("part", "All", p)
			c.append_step(u"$", u"linnar")
			c = add_personal("part", "Loc", p)
			c.append_step(u"$", u"lisse")
			c = add_personal("part", "Instr", p)
			c.append_step(u"$", u"línen")
			c = add_personal("part", "Resp", p)
			c.append_step(u"$", u"lis")


		#verbs
		def add_verb_flexion(args, transitive):
			f = fl.create_flexion(u"v", (args,))

			tr = f.create_transform((u"aor", "s", "0")) 
			c = tr.create_chain(BASED_ON_LEMMA, "a$")
			c = tr.create_chain(BASED_ON_LEMMA, "u$")
			c.append_step(u"u$", u"o")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"$", u"e")
			tr = f.create_transform((u"aor", "pl", "0")) 
			c = tr.create_chain(BASED_ON_LEMMA, "[au]$")
			c.append_step(u"$", u"r")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"$", u"ir")

			tr = f.create_transform((u"pres", "s", "0")) 
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
			tr = f.create_transform((u"pres", "pl", "0")) 
			c = tr.create_chain((u"pres", "s", "0"))
			c.append_step(u"$", u"r")


			tr = f.create_transform((u"past", "s", "0")) 
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
			tr = f.create_transform((u"past", "pl", "0")) 
			c = tr.create_chain((u"past", "s", "0"))
			c.append_step(u"$", u"r")



			tr = f.create_transform(("perf", "s", "0"))
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
			tr = f.create_transform(("perf", "pl", "0")) 
			c = tr.create_chain(("perf", "s", "0"))
			c.append_step(u"$", u"r")

			tr = f.create_transform(("fut", "s", "0")) 
			c = tr.create_chain(BASED_ON_LEMMA, "u$")
			c.append_step(u"u$", u"úva")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"a?$", u"uva")
			tr = f.create_transform(("fut", "pl", "0")) 
			c = tr.create_chain(("fut", "s", "0"))
			c.append_step(u"$", u"r")


			tr = f.create_transform((u"inf", "0", "0")) 
			c = tr.create_chain(BASED_ON_LEMMA, "a$")
			c = tr.create_chain(BASED_ON_LEMMA, "u$")
			c.append_step(u"u$", u"o")
			c = tr.create_chain(BASED_ON_LEMMA)
			c.append_step(u"$", u"e")
			

			tr = f.create_transform((u"imp", u"2", "0")) 
			c = tr.create_chain((u"inf", "0", "0"))
			
			tr = f.create_transform((u"act-part", "0", "0")) 
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
			
			tr = f.create_transform((u"pass-part", "0", "0")) 
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

			TENSE = [u"aor",u"pres",u"past","perf","fut"]
			SUBJ = {u"1s":[u"nye",u"n"], u"2":[u"lye",u"l"], u"3s":["rye","s"], u"1+2+3": [u"lve"], u"1+3": [u"lme"], u"1d": [u"mme"], u"3pl":[u"nte"]}
			OBJ = {u"1s":u"n", u"2":u"l", u"3s":"s", u"3pl":u"t"}
			for t in TENSE:
				for k,v in SUBJ.iteritems():
					tr = f.create_transform((t, k, "0"))
					c = tr.create_chain((t, u"s", "0"))
					if len(v)==1:
						c.append_step(u"$", v[0])
					else:
						if t==u"aor":
							c.append_step(u"e$", u"i")
						c.append_step(u"$", v[1])
					if transitive:
						for k1, v1 in OBJ.iteritems():
							tr = f.create_transform((t, k, k1))
							c = tr.create_chain((t, u"s", "0"))
							c.append_step(u"$", v[0]+v1)

			if transitive:
				for k1, v1 in OBJ.iteritems():
					tr = f.create_transform((u"inf", "0", k1))
					c = tr.create_chain(BASED_ON_LEMMA)
					c.append_step(u"(?<=[^au])$", u"i")
					c.append_step(u"$", u"ta"+v1)

		add_verb_flexion( CategoryFilter("in", (u"Acc", u"Acc+Dat")), True)
		add_verb_flexion( CategoryFilter("ni", (u"Acc", u"Acc+Dat")), False)
		
		f = fl.create_flexion(u"adj",())

		tr = f.create_transform(("s", "Nom", "0"))
		c = tr.create_chain(BASED_ON_LEMMA)

		tr = f.create_transform(("s", "Gen", "0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"o")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"io")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"do")
		tr = f.create_transform(("s", "Poss", "0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"ava")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"iva")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"wa")
		tr = f.create_transform(("s", "Dat", "0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"$", u"n")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"in")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"den")
		tr = f.create_transform(("s", "Abl", "0"))
		c = tr.create_chain(("s", "Dat", "0"))
		c.append_step(u"n$", u"llo")
		tr = f.create_transform(("s", "All", "0"))
		c = tr.create_chain(("s", "Dat", "0"))
		c.append_step(u"n$", u"nna")
		tr = f.create_transform(("s", "Loc", "0"))
		c = tr.create_chain(("s", "Dat", "0"))
		c.append_step(u"n$", u"sse")
		tr = f.create_transform(("s", "Instr", "0"))
		c = tr.create_chain(("s", "Dat", "0"))
		c.append_step(u"$", u"en")
		tr = f.create_transform(("s", "Resp", "0"))
		c = tr.create_chain(("s", "Dat", "0"))
		c.append_step(u"n$", u"s")


		tr = f.create_transform(("pl", "Nom", "0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c.append_step(u"ea$", u"ie")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"e")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"i")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"di")
		tr = f.create_transform(("pl", "Gen", "0"))
		c = tr.create_chain(("pl", "Nom", "0"), u"ie")
		c.append_step(u"ie$", u"iéon")
		c = tr.create_chain(("pl", "Nom", "0"))
		c.append_step(u"$", u"on")
		tr = f.create_transform(("pl", "Poss", "0"))
		c = tr.create_chain(("pl", "Dat", "0"))
		c.append_step(u"n$", u"va")
		tr = f.create_transform(("pl", "Dat", "0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c.append_step(u"ea$", u"ín")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"ain")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"ín")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"din")
		tr = f.create_transform(("pl", "Abl", "0"))
		c = tr.create_chain(("s", "Abl", "0"))
		c.append_step(u"$", u"n")
		tr = f.create_transform(("pl", "All", "0"))
		c = tr.create_chain(("s", "All", "0"))
		c.append_step(u"$", u"r")
		tr = f.create_transform(("pl", "Loc", "0"))
		c = tr.create_chain(("s", "Loc", "0"))
		c.append_step(u"$", u"n")
		tr = f.create_transform(("pl", "Instr", "0"))
		c = tr.create_chain(("pl", "Dat", "0"))
		c.append_step(u"$", u"en")
		tr = f.create_transform(("pl", "Resp", "0"))
		c = tr.create_chain(("pl", "Dat", "0"))
		c.append_step(u"n$", u"s")

		tr = f.create_transform(("d", "Nom", "0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c.append_step(u"ea$", u"iet")
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"at")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"it")
		c = tr.create_chain(BASED_ON_LEMMA, u"n$")
		c.append_step(u"$", u"det")

		tr = f.create_transform(("d", "Gen", "0"))
		c = tr.create_chain(("d", "Nom", "0"), u"iet")
		c.append_step(u"et$", u"éto")
		c = tr.create_chain(("d", "Nom", "0"))
		c.append_step(u"t$", u"to")

		tr = f.create_transform(("d", "Poss", "0"))
		c = tr.create_chain(BASED_ON_LEMMA, u"ea$")
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"t$", u"twa")

		tr = f.create_transform(("d", "Dat", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"t$", u"nt")

		tr = f.create_transform(("d", "Abl", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"t$", u"lto")

		tr = f.create_transform(("d", "All", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"t$", u"nta")

		tr = f.create_transform(("d", "Loc", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"t$", u"tse")

		tr = f.create_transform(("d", "Instr", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"t$", u"nten")

		tr = f.create_transform(("d", "Resp", "0"))
		c = tr.create_chain(("d", "Nom", "0"))
		tr.append_step(u"t$", u"tes")

		def add_grd(g):
			tr = f.create_transform(("s", "Gen", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"a$", u"o")
			tr = f.create_transform(("s", "Poss", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"va")
			tr = f.create_transform(("s", "Dat", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"n")
			tr = f.create_transform(("s", "Abl", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"llo")
			tr = f.create_transform(("s", "All", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"nna")
			tr = f.create_transform(("s", "Loc", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"sse")
			tr = f.create_transform(("s", "Instr", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"nen")
			tr = f.create_transform(("s", "Resp", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"s")

			tr = f.create_transform(("pl", "Nom", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"a$", u"e")
			tr = f.create_transform(("pl", "Gen", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"a$", u"eon")
			tr = f.create_transform(("pl", "Poss", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"iva")
			tr = f.create_transform(("pl", "Dat", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"in")
			tr = f.create_transform(("pl", "Abl", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"llon")
			tr = f.create_transform(("pl", "All", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"llar")
			tr = f.create_transform(("pl", "Loc", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"ssen")
			tr = f.create_transform(("pl", "Instr", g))
			c = tr.create_chain(("pl", "Dat", g))
			c.append_step(u"$", u"en")
			tr = f.create_transform(("pl", "Resp", g))
			c = tr.create_chain(("pl", "Dat", g))
			c.append_step(u"n$", u"s")

			tr = f.create_transform(("d", "Nom", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"t")

			tr = f.create_transform(("d", "Gen", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"to")

			tr = f.create_transform(("d", "Poss", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"twa")

			tr = f.create_transform(("d", "Dat", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"nt")

			tr = f.create_transform(("d", "Abl", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"lto")

			tr = f.create_transform(("d", "All", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"nta")

			tr = f.create_transform(("d", "Loc", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"tse")

			tr = f.create_transform(("d", "Instr", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$",u"nten")

			tr = f.create_transform(("d", "Resp", g))
			c = tr.create_chain(("s", "Nom", g))
			c.append_step(u"$", u"tes")		

		tr = f.create_transform(("s", "Nom", u"rel"))
		c = tr.create_chain(BASED_ON_LEMMA, u"a$")
		c.append_step(u"a$", u"alda")
		c = tr.create_chain(BASED_ON_LEMMA, u"e$")
		c.append_step(u"e$", u"ilda")
		c = tr.create_chain(BASED_ON_LEMMA, u"[ie]n$")
		c.append_step(u"(?<=[ie]n)$", u"ilda")

		add_grd(u"rel")

		tr = f.create_transform(("s", "Nom", u"abs"))
		c = tr.create_chain(BASED_ON_LEMMA, u"^[lmrs]")
		c.append_step(u"^([lmrs])", u"a\\1\\1")
		c = tr.create_chain(BASED_ON_LEMMA, u"^p")
		c.append_step(u"^", u"am")
		c = tr.create_chain(BASED_ON_LEMMA)
		c.append_step(u"^", u"an")

		add_grd(u"abs")

	def build_grammar(gr):
		def free_order(*symbols):
			def perm(symbols):
				if len(symbols) == 2:
					return [[symbols[0], symbols[1]], [symbols[1], symbols[0]]]
				else:
					p = []
					for i, s in enumerate(symbols):
						for m in perm(symbols[:i] + symbols[i+1:]):
							n = [s] + m
							p.append(n)
					return p
			cond = None
			for z in perm(symbols):
				expr = None
				for y in z:
					if expr is None:
						expr = y
					else:
						expr = expr + y
				if cond is None:
					cond = expr
				else:
					cond = cond | expr
			return cond

		fin = CategoryFilter("in", ("pres", "past", "perf", "aor", "fut"))
		n0 = CategoryFilter("ni", "0")
		
		def auto_noun_phrase(gr):
			for case in ("Gen", "Poss", "Dat", "Abl", "All", "Loc", "Instr", "Resp"):
				for num in ("s", "d", "pl", "part"):
					if num == "part":
						gr["noun-phrase,"+case] = WordCategoryFilter("n", (), (num, case, None)) + WordCategoryFilter("adj", (), ("pl", "Nom", None))
						gr["noun-phrase,"+case] = WordCategoryFilter("adj", (), ("pl", "Nom", None)) + WordCategoryFilter("n", (), (num, case, None))
						gr["noun-phrase,"+case] = WordCategoryFilter("n", (), (num, case, None))
					else:
						gr["noun-phrase,"+case] = WordCategoryFilter("n", (), (num, "Nom", None)) + WordCategoryFilter("adj", (), (num, case, None))
						gr["noun-phrase,"+case] = WordCategoryFilter("adj", (), (num, "Nom", None)) + WordCategoryFilter("n", (), (num, case, None))
						gr["noun-phrase,"+case] = WordCategoryFilter("n", (), (num, case, None))

			
		gr["sentence"] = Reference("nucleus") + Reference("complements")
		gr["nucleus"] = Reference("Vso")|Reference("Vs O")|Reference("S Vo")|Reference("S V O") # verbal sentence: o === 0/O
		#gr["nucleus"] = Reference("Cs N") | Reference("S C N")  # nominal sentence 
		#gr["nucleus"] = Reference("Vso D")|Reference("Vs O D")|Reference("S V O D") # dative sentence
		
		gr["S Vo"] = free_order(Reference("S,s"), Reference("Vo,s"))|free_order(Reference("S,m"), Reference("Vo,m"))
		gr["Vs O"] = free_order(Reference("Vs"), Reference("O"))
		gr["S V O"] = free_order(Reference("S,s"), Reference("V,s"), Reference("O")) | free_order(Reference("S,m"), Reference("V,m"), Reference("O"))

		#gr["Cs N"] = free_order(Reference("Cs"), Reference("N"))|free_order(Reference("Cs,s"), Reference("Na,s"))|free_order(Reference("Cs,m"), Reference("Na,m"))
		#gr["S C N"] = free_order(Reference("S,s"), Reference("C,s"), Reference("N")) | free_order(Reference("S,m"), Reference("C,m"), Reference("N"))

	
		
		gr["Vso"] = WordCategoryFilter("v", ("0",), (fin, n0, "0"))
		gr["Vso"] = WordCategoryFilter("v", ("Acc",), (fin, n0, n0))
		gr["Vo,s"] = WordCategoryFilter("v", ("0",), (fin, "s", "0"))
		gr["Vo,s"] = WordCategoryFilter("v", ("Acc",), (fin, "s", n0))
		gr["Vo,m"] = WordCategoryFilter("v", ("0",), (fin, "pl", "0"))
		gr["Vo,m"] = WordCategoryFilter("v", ("Acc",), (fin, "pl", n0))
		gr["V,s"] = WordCategoryFilter("v", ("Acc",), (fin, "s", "0"))
		gr["V,m"] = WordCategoryFilter("v", ("Acc",), (fin, "pl", "0"))
		gr["Vs"] = WordCategoryFilter("v", ("Acc",), (fin, CategoryFilter("ni", ("s", "pl")), "0"))
		gr["O"] = Reference("article") * OPTIONAL_CLOSURE + Reference("noun-phrase,Nom") + Reference("noun-complements")
		gr["S,s"] = Reference("article") * OPTIONAL_CLOSURE + Reference("noun-phrase,s,Nom") + Reference("noun-complements")
		gr["S,m"] = Reference("article") * OPTIONAL_CLOSURE + Reference("noun-phrase,m,Nom") + Reference("noun-complements")
		gr["noun-phrase,Nom"] = Reference("noun-phrase,s,Nom")|Reference("noun-phrase,m,Nom")
		gr["noun-phrase,s,Nom"] = WordCategoryFilter("n", (), ("s", "Nom", None)) + WordCategoryFilter("adj", (), ("s", "Nom", None))
		gr["noun-phrase,s,Nom"] = WordCategoryFilter("adj", (), ("s", "Nom", None)) + WordCategoryFilter("n", (), ("s", "Nom", None))
		gr["noun-phrase,s,Nom"] = WordCategoryFilter("n", (), ("s", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("n", (), ("pl", "Nom", None)) + WordCategoryFilter("adj", (), ("pl", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("adj", (), ("pl", "Nom", None)) + WordCategoryFilter("n", (), ("pl", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("n", (), ("pl", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("n", (), ("d", "Nom", None)) + WordCategoryFilter("adj", (), ("d", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("adj", (), ("d", "Nom", None)) + WordCategoryFilter("n", (), ("d", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("n", (), ("d", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("n", (), ("part", "Nom", None)) + WordCategoryFilter("adj", (), ("pl", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("adj", (), ("pl", "Nom", None)) + WordCategoryFilter("n", (), ("part", "Nom", None))
		gr["noun-phrase,m,Nom"] = WordCategoryFilter("n", (), ("part", "Nom", None))
		gr["article"] = WordFilter(Word(u"i", Particle(u"i", 1, "adj")))
		gr["noun-complements"] = Reference("noun-complement") * KLEENE_CLOSURE
		gr["noun-complement"] = Reference("Cposs") | Reference("Cgen")
		gr["Cposs"] = Reference("article") * OPTIONAL_CLOSURE + Reference("noun-phrase,Poss")
		gr["Cgen"] = Reference("article") * OPTIONAL_CLOSURE + Reference("noun-phrase,Gen")
		gr["complements"] = Reference("noun-complement") * KLEENE_CLOSURE
		gr["complement"] = Reference("Cloc") | Reference("Cmod") | Reference("adverb")
		gr["Cloc"] = Reference("article") * OPTIONAL_CLOSURE + Reference("noun-phrase,Loc")
		gr["Cmod"] = Reference("article") * OPTIONAL_CLOSURE + Reference("noun-phrase,Instr")
		gr["adverb"] = WordCategoryFilter("adv")
		auto_noun_phrase(gr)
		
	
	def nouns():
		d = []
		d.append(  (u"cas", u"cár", u"cesi") ) #head
		d.append(  (u"cumbo", u"cumbo", u"fucesi") ) #belly
		d.append(  (u"hon", u"hón", u"kawcesi") ) #heart
		d.append(  (u"esse", u"esse", u"tedapemi", [(u"essi", ("pl","Nom","0"))] ) ) #name
		d.append(  (u"sambe", u"sambe", u"depi") ) #room
		d.append(  (u"card", u"car", u"byekigi") ) #building
		d.append(  (u"telme", u"telme", u"bidetavi") ) #blanket
		d.append(  (u"limpe", u"limpe", u"zoyfupi") ) #spirits
		d.append(  (u"síra", "0", u"bape-tovay") ) #today
		d.append(  (u"sovasamb", u"sovasan", u"bodepi") ) #restroom
		d.append(  (u"lindale", u"lindale", u"dinjami") ) #music
		d.append(  (u"colla", u"colla", u"byetavi") ) #garment
		d.append(  (u"tecil", u"tecil", u"bofifusi") ) #pen
		d.append(  (u"hríve", u"hríve", u"cayfemi") ) #winter
		d.append(  (u"laire", u"laire", u"fefemi") ) #summer
		d.append(  (u"henets", u"henet", u"kifigi", [(u"henetwa", ("s","Poss","0"))] ) ) #window
		d.append(  (u"rancu", u"ranco", u"twecesi") ) #arm
		d.append(  (u"nonwa", u"nonwa", u"kobisi") ) #computer
		d.append(  (u"palancen", u"palancen", u"kifabisi") ) #television
		d.append(  (u"asta", u"asta", u"ketovi") ) #month
		d.append(  (u"nolyasse", u"nolyasse", u"kokigi") ) #school
		d.append(  (u"ner", u"nér", u"loybegi") ) #man
		d.append(  (u"niss", u"nís", u"lawbegi") ) #woman
		d.append(  (u"híni", u"hína", u"fobegi", [(u"híni", ("pl","Nom","0"))] ) )#child
		d.append(  (u"huo", u"huo", u"zovi") ) #dog
		d.append(  (u"yaule", u"yaule", u"kwizovi") ) #cat
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
		d.append(  (u"malle", u"malle", u"zegi", [(u"maller", ("pl","Nom","0"))]))#road
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
		d.append(  (u"sell", u"seler", u"zitasaw", [(u"selerwa", ("s","Poss","0")), (u"selernen", ("s","Instr","0"))] ) )
		d.append(  (u"atar", u"atar", u"dutasaw") ) #father
		d.append(  (u"tie", u"tie", u"zuzegi") ) #path
		d.append(  (u"máqua", u"máqua", u"zicesi") ) #hand
		d.append(  (u"tal", u"tál", u"cucesi", [(u"talan", ("s","Dat","0")) , (u"talain", ("pl","Dat","0"))] ))#foot
		d.append(  (u"toll°", u"tol", u"ketisi", [(u"tollon", ("s","Dat","0")), (u"tolloin", ("pl","Dat","0"))] ) )#island
		d.append(  (u"ráv", u"rá", u"xozovi") ) #lion
		d.append(  (u"raine", u"raine", u"baxasoni") ) #peace
		d.append(  (u"cos", u"cor", u"bizozugi") ) #war
		d.append(  (u"coa", u"coa", u"kigi", [(u"coavo", ("s","Gen","0")),(u"coava", ("s","Poss","0"))] ) )#house
		d.append(  (u"mas", u"mar", u"kwicalaymi",[], 2) ) #home
		d.append(  (u"nelc", u"nelet", u"futevi", [(u"neletse", ("s","Loc","0"))] ) ) #tooth
		d.append(  (u"hend", u"hen", u"kicesi") ) #eye
		d.append(  (u"pé", u"pé", u"teduncesi", [(u"péu", ("d","Nom","0")), (u"pein", ("pl","Dat","0"))]) ) #lip
		d.append(  (u"lar", u"lár", u"foycesi", [(u"laru", ("d","Nom","0"))]) ) #ear
		d.append(  (u"fiond", u"fion", u"bedami") ) #hawk
		d.append(  (u"ré", u"ré", u"tovi", [(u"rein", ("pl","Dat","0"))]) ) #24hours
		d.append(  (u"pí", u"pí", u"byekagi", [(u"pín", ("pl","Dat","0"))]) ) #insect
		d.append(  (u"oxi", u"ohte", u"docesi")) #egg
		
		d.append(  (u"ambar", u"ambar", u"jotisi")) #planet, world
		d.append(  (u"istar", u"istar", u"joybegi", [(u"istari", ("pl","Nom","0"))])) #doctor, wizard
		
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
		d.append(  (u"Mumba", u"Mumbai", u"Labunxodugi", [(u"Mumbai", ("pl","Nom","0"))]) ) #Bombay
		d.append(  (u"Sampaulo", u"Sampaulo", u"Lapawxodugi") ) #São Paulo
		d.append(  (u"Sanga", u"Sangai", u"Lazanxodugi", [(u"Sangai", ("pl","Nom","0"))]) ) #Shanghai
		d.append(  (u"Masiqua", u"Masiqua", u"Laruxodugi") ) #Moscow
		d.append(  (u"Isil", u"Isil", u"Labatisi") ) #moon
		d.append( (u"kuiveyulda", u"kuiveyulda", u"cafefupi") ) #coffee
		#d.append( (u"norolle liéva ", u"norolle liéva ", u"zetimi") ) #bus
		d.append( (u"vilyacirya", u"vilyacirya", u"datimi") ) #airplane
		d.append( (u"vilyahopasse", u"vilyahopasse", u"dakigi") ) #airport
		d.append( (u"sarno", u"sarno", u"bujisi") ) #table
		d.append( (u"yáve", u"yáve", u"babemi") ) #fruit (a -)
		d.append( (u"olpe", u"olpe", u"finzipi") ) #bottle
		d.append( (u"angatea", u"angatea", u"kuzegi") ) #railroad
		#d.append( (u"norolle angaina", u"norolle angaina", u"kuzetimi") ) #train
		d.append( (u"lambe", u"lambe", u"tejami") ) #language
		d.append( (u"quetta", u"quetta", u"tekusi") ) #word
		
		return d


	def verbs():
		d = []
		d.append(  (u"na", "Nom", u"dapa", [(u"ne", (u"past","s","0"))]) ) 
		d.append(  (u"ea", "Loc", u"zoga", [(u"ea", (u"pres","s","0")), (u"engie", ("perf","s","0")), (u"enge", (u"past","s","0"))]) ) 
		d.append(  (u"cen", u"Acc", u"kiva") ) 
		d.append(  (u"mel", u"Acc", u"bakopa") )  #love
		d.append(  (u"mat", "0", u"fucala") ) #eat
		d.append(  (u"suc", "0", u"bofucala") ) #drink
		d.append(  (u"ista", u"Acc", u"kopa", [(u"sinte", (u"past","s","0")), (u"isintie", ("perf","s","0")), (u"sinwa", ("pass-part","0","0"))]) ) 
		d.append(  (u"lelya", "0", u"ticala", [(u"lende", (u"past","s","0"))]) )  
		d.append(  (u"ulya", u"Acc", u"tibokavasa", [], 1) )  
		d.append(  (u"ulya", "0", u"tibokava", [], 2) )  
		d.append(  (u"mar", "0", u"kwicala", [(u"ambárie", ("perf","s","0"))]) )
 		d.append(  (u"móta", "0", u"bucala") ) #work
		#d.append(  (u"mára", u"Acc", u"zoykopa") ) #like
		d.append(  (u"tyal", "0", u"dwecala" ) ) #play
		d.append(  (u"canta", u"Acc", u"joykavapa") ) #fix
		d.append(  (u"rac", u"Acc", u"joyjuvapa") ) #break
		d.append(  (u"nyar", u"Acc+Dat", u"tega") ) #tell
		d.append(  (u"quet", "Dat", u"tegapa") ) #speak to 
		d.append(  (u"mala", "0", u"xonkepa") ) #suffer
		d.append(  (u"lor", "0", u"kunkepa") ) #sleep
		d.append(  (u"mer", u"Acc", u"cakopa") ) #want
		d.append(  (u"appa", u"Acc", u"kenbusa") ) #touch
		d.append(  (u"anta", u"Acc+Dat", u"ximamba", [(u"áne", (u"past","s","0"))]) )  #give
		d.append(  (u"yuhta", u"Acc", u"busasa") ) #use, control
		d.append(  (u"lanta", u"0", u"dafagupa") ) #fall
		return d


	def adjs():
		d = []
		d.append(  (u"sina", u"baso") ) #this
		d.append(  (u"tana", u"zaso") ) #that
		d.append(  (u"alwa", u"joykepo") ) #healthy
		d.append(  (u"mára", u"cakemo") ) #good
		d.append(  (u"olca", u"cafomo") ) #bad, evil
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
		d.append(  (u"vanya", u"kekaykemo", [(u"ambanya", ("s","Nom",u"abs"))]) )   #beautiful
		d.append(  (u"vára", u"cinjuvo", [(u"anwára", ("s","Nom",u"abs"))]) )   #dirty
		d.append(  (u"laurea", u"todapyu taykocivo")  ) #golden
		d.append(  (u"ilya", u"bikavo")  ) #all, whole
		
		return d

	def adv():
		d = []
		d.append((u"ehtala", u"dipe-tovay")) #tomorrow
		return d

	l = Lect(u"qya")
	l.name = u"Quenya"
	l.english_name = u"Neo-Quenya"
	l.append_p_o_s(u"v", (u"arguments",), (u"tense", u"person", u"object person"))
	l.append_p_o_s(u"n", (), (u"number", u"case", u"person"))
	l.append_p_o_s(u"adj", (), (u"number", u"case", u"degree"))
	l.append_p_o_s(u"adv", (), ())
	l.append_p_o_s(u"prep", (u"argument",), (u"object person",))
	build_flexions(l.flexions)
	build_lexicon(l.lexicon, l.flexions)
	print l.lexicon
	build_grammar(l.grammar)
	l.properties["capitalization"] = 2 #lexical
	l.properties["separator"] = u" " #lexical
	print "now compiling"
	l.compile()
	print "compiled"
	print "now saving"
	l.save("test/qya.lct", True)
	print "done!"
	print "now reading"
	print l.read(u"malan")
	print l.read(u"melin fion ringa")
	print l.read(u"cor vanya mele i lauca alda")
	print l.read(u"ilya ambar sinte lambe er ar yuhtane quetie er.")


if __name__ == "__main__":
	run()

