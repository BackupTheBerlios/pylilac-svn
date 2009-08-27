#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to create Quenya language file.
"""

from pylilac.core.lect import Lect
from pylilac.core.bnf import Reference, POSITIVE_CLOSURE, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from pylilac.core.lexicon import Lexicon, Particle, Word, Lexeme, CategoryFilter, WordCategoryFilter, WordFilter, DEFECTIVE
from pylilac.core.inflection import BASED_ON_ENTRY_FORM
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
				correct_word(table, w[i]+u"x",  v[i]+u"x")
				correct_word(table, w[i]+u"([^lnhcgr])y",  v[i]+u"\\1y")
				correct_word(table, w[i]+u"([^lnhgr])w",  v[i]+u"\\1w")		

		for h in nouns():
			if len(h)>4:
				id = h[4]
			else:
				id = 1
			lemma = Lexeme(h[0], id, "n", (), h[2])
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
			lemma = Lexeme(h[0], id, "v", (h[1],), h[2])
			words = []
			if len(h)>3:
				for j in h[3]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			if lemma.entry_form == u"na":
				lemma = Lexeme(u"ná", 1, lemma.p_o_s, lemma.categories, lemma.gloss)
				for k in ft.iterkeys():
					ft[k] = ft[k].copy(lemma)
				ft[("aor", "s", "0")]=Word(u"ná", lemma, ("aor", "s", "0"))
				ft[("past", "s", "0")]=Word(u"né", lemma, ("past", "s", "0"))

			correct_table(ft)			
			l.add_lemma(lemma)
			for w in ft.itervalues():
				l.add_word(w)
				
		for h in adjs():
			if len(h)>3:
				id = h[3]
			else:
				id = 1
			lemma = Lexeme(h[0], id, "adj", (), h[1])
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
			l.add_word(Word(adverb, Lexeme(adverb, id, "adv", (), adverb_gloss), ()))
		
		l.add_word(Word(u"i", Particle(u"i", 1, "adj", ()), ("0", "0", "0")))
		l.add_word(Word(u"er", Particle(u"er", 1, "adj", ()), ("0", "0", "0")))
		


	def correct_word(table, old, new):
		for k, v in table.iteritems():
			if re.search(old, v.form, re.I):
				v2 = Word(re.sub(old, new, v.form, re.I), v.lemma, v.categories)
				table[k] = v2

	def build_inflections(fl):
		f = fl.create_inflection("n")

		tr = f.create_form(("s", "Nom", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM)

		tr = f.create_form(("s", "Gen", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quo")
		c.append_step(u"gu$", u"gwo")
		c.append_step(u"hu$", u"hwo")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"w$") 
		c.append_step(u"w$", u"vo")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=i)e$", u"é")
		c.append_step(u"[ao]?$", u"o")

		tr = f.create_form(("s", "Poss", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[^aeioáéíóú]*[aeiou][^aeiouáéíóúx][aeiou]$")
		#c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiou][^aeiouáéíóúx][aeiou]$")
		c.append_step(u"a$", u"áva")
		c.append_step(u"e$", u"éva")
		c.append_step(u"i$", u"íva")
		c.append_step(u"o$", u"óva")
		c.append_step(u"u$", u"úva")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ie$")
		c.append_step(u"e$", u"éva")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"c$")
		c.append_step(u"c$", u"qua")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"v$")
		c.append_step(u"$", u"a")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[nlrm][^aeiouáéíóú]$")
		c.append_step(u"[^aeiouáéíóú]$", u"wa")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ts$")
		c.append_step(u"s$", u"wa")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"w$")
		c.append_step(u"w$", u"va")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[^aeiouáéíóú][^aeiouáéíóú]$")
		c.append_step(u"$", u"eva")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiouáéíóú]$")
		c.append_step(u"$", u"va")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"$", u"wa")

		tr = f.create_form(("s", "Dat", "0")) 
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"[aeiouáéíóú]$")
		c.append_step(u"$", u"n")
		c = tr.create_transform(("s", "Gen", "0"))
		c.append_step(u"o$", u"en")

		tr = f.create_form(("s", "Abl", "0")) 
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"ll?$")
		c.append_step(u"ll?$", u"llo") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"rr?$")
		c.append_step(u"rr?$", u"llo") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"llo")

		tr = f.create_form(("s", "All", "0")) 
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"ll?$")
		c.append_step(u"ll?$", u"lda") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"nn?$")
		c.append_step(u"nn?$", u"nna") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"nna")

		tr = f.create_form(("s", "Loc", "0")) 
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"lde") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"nn?$")
		c.append_step(u"nn?$", u"nde") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ss?$")
		c.append_step(u"ss?$", u"sse") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiou]ts?$")
		c.append_step(u"s?$", u"se")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"sse")

		tr = f.create_form(("s", "Instr", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiou][ct]$")
		c.append_step(u"([ct])$", u"n\\1en")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiou]p$")
		c.append_step(u"p$", u"mpen")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"lden")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"nn?$")
		c.append_step(u"nn?$", u"nnen")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"rr?$")
		c.append_step(u"rr?$", u"rnen")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"m$")
		c.append_step(u"$", u"nen")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=i)e$", u"é")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"nen")


		tr = f.create_form(("s", "Resp", "0")) 
		c = tr.create_transform(("s", "Dat", "0"))
		c.append_step(u"n$", u"s")



		#plural

		tr = f.create_form(("pl", "Nom", "0")) 
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[^aeiouáéíóú][cgh]u$")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"gu$", u"gwi")
		c.append_step(u"hu$", u"hwi")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aiouáéíóú]$|ie$") 
		c.append_step(u"$", u"r")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$") 
		c.append_step(u"e$", u"i")
		c = tr.create_transform(("s", "Gen", "0"))
		c.append_step(u"e?o$", u"i")


		#Indirect plural

		tr = f.create_form(("pl", "Gen", "0")) 
		c = tr.create_transform(("pl", "Nom", "0"))
		c.append_step(u"ier$", u"iér") 
		c.append_step(u"$", u"on") 

		tr = f.create_form(("pl","Poss", "0"))
		c = tr.create_transform(("pl","Dat", "0"))
		tr.append_step(u"n$", u"va")

		tr = f.create_form(("pl","Dat", "0")) 
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quín")
		c.append_step(u"gu$", u"gwín")
		c.append_step(u"hu$", u"hwín")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"i$|e$|(ie)$")
		c.append_step(u"i$|e$|(ie)$", u"ín") 
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"$", u"in")

		tr = f.create_form(("pl","Abl", "0"))  
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quillon")
		c.append_step(u"gu$", u"gwillon")
		c.append_step(u"hu$", u"hwillon")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"llon")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"rr?$")
		c.append_step(u"rr?$", u"llon")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"llon")

		tr = f.create_form(("pl","All", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quinnar")
		c.append_step(u"gu$", u"gwinnar")
		c.append_step(u"hu$", u"hwinnar")
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"nn?$")
		c.append_step(u"nn?$", u"nnar")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"nnar")

		tr = f.create_form(("pl","Loc", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ts$")
		c.append_step(u"$", u"en")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"c$")
		c.append_step(u"c$", u"xen")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quissen")
		c.append_step(u"gu$", u"gwissen")
		c.append_step(u"hu$", u"hwissen")
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"ss?$")
		c.append_step(u"ss?$", u"ssen")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"ssen")


		tr = f.create_form(("pl","Instr", "0"))
		c = tr.create_transform(("pl","Dat", "0"))
		tr.append_step(u"$", u"en")

		tr = f.create_form(("pl","Resp", "0"))
		c = tr.create_transform(("pl","Dat", "0"))
		tr.append_step(u"n$", u"s")





		#Indirect dual

		tr = f.create_form(("d", "Nom", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"u$|ie$")
		c.append_step(u"$", u"t")
		c = tr.create_transform(("s", "Gen", "0"), u"[dt].{0,4}o$")
		c.append_step(u"o$", u"u")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeioáéíóú]$")
		c.append_step(u"$", u"t")
		c = tr.create_transform(("s", "Gen", "0"))
		c.append_step(u"o$", u"et")

		tr = f.create_form(("d", "Gen", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"eu$", u"et")
		tr.append_step(u"([aeiouáéíóú][lnrs])et$", u"\\1t")
		tr.append_step(u"iet$", u"iét")
		c.append_step(u"$", u"o")

		tr = f.create_form(("d", "Poss", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"u$", u"uva")
		tr.append_step(u"t$", u"twa")

		tr = f.create_form(("d", "Dat", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"u$", u"un")
		tr.append_step(u"t$", u"nt")

		tr = f.create_form(("d", "Abl", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"u$", u"ullo")
		tr.append_step(u"t$", u"lto")

		tr = f.create_form(("d", "All", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"u$", u"unna")
		tr.append_step(u"t$", u"nta")

		tr = f.create_form(("d", "Loc", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"u$", u"usse")
		tr.append_step(u"t$", u"tse")

		tr = f.create_form(("d", "Instr", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"u$", u"unen")
		tr.append_step(u"t$", u"nten")

		tr = f.create_form(("d", "Resp", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"u$", u"us")
		tr.append_step(u"t$", u"tes")


		#Indirect partitive
		tr = f.create_form(("part", "Nom", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quili")
		c.append_step(u"gu$", u"gwili")
		c.append_step(u"hu$", u"hwili")
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"ll?$")
		c.append_step(u"ll?$", u"lli")
		c = tr.create_transform(BASED_ON_ENTRY_FORM,  u"rr?$")
		c.append_step(u"rr?$", u"lli")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"li")
		
		tr = f.create_form(("part", "Gen", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"$", u"on")

		tr = f.create_form(("part", "Poss", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"([aeiou])li$", u"\\1lí")
		tr.append_step(u"$", u"va")

		tr = f.create_form(("part", "Dat", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"$", u"n")

		tr = f.create_form(("part", "Abl", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"$", u"llon")

		tr = f.create_form(("part", "All", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"$", u"nnar")

		tr = f.create_form(("part", "Loc", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"$", u"ssen")

		tr = f.create_form(("part", "Instr", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"([aeiou])li$", u"\\1lí")
		tr.append_step(u"$", u"nen")

		tr = f.create_form(("part", "Resp", "0"))
		c = tr.create_transform(("part", "Nom", "0"))
		tr.append_step(u"$", u"s")

		#Personal forms

		POSS = {"1s":u"nya", "2":u"lya", "3s":u"rya", "1+2+3": u"lva", "1+3": u"lma", "1d": u"mma", "3pl":u"nta"}
		def add_personal(number, case, person):
			x = f.create_form((number, case, person)) 
			z = x.create_transform(BASED_ON_ENTRY_FORM)
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

			#f.create_form(("s", "Gen", p))
			#c = tr.create_transform(("s", "Nom", p))
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
		def add_verb_inflection(args, transitive):
			f = fl.create_inflection("v", None, (args,))

			tr = f.create_form(("aor", "s", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"u$")
			c.append_step(u"u$", u"o")
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"e")
			tr = f.create_form(("aor", "pl", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[au]$")
			c.append_step(u"$", u"r")
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"ir")

			tr = f.create_form(("pres", "s", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
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
			tr = f.create_form(("pres", "pl", "0")) 
			c = tr.create_transform(("pres", "s", "0"))
			c.append_step(u"$", u"r")


			tr = f.create_form(("past", "s", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ha$")
			c.append_step(u"$", u"ne")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"wa$")
			c.append_step(u"wa$", u"ngwe")

			if transitive:
				c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ya$")
				c.append_step(u"$", u"ne")
			else:
				c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[rnm]ya$")
				c.append_step(u"ya$", u"ne")
				c = tr.create_transform(BASED_ON_ENTRY_FORM, u"tya$")
				c.append_step(u"tya$", u"nte")
				c = tr.create_transform(BASED_ON_ENTRY_FORM, u"pya$")
				c.append_step(u"pya$", u"mpe")
				c = tr.create_transform(BASED_ON_ENTRY_FORM, u"lya$")
				c.append_step(u"lya$", u"lle")
				c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[sv]ya$")
				c.append_step(u"a([sv]ya)$", u"á\\1")
				c.append_step(u"e([sv]ya)$", u"é\\1")
				c.append_step(u"o([sv]ya)$", u"ó\\1")
				c.append_step(u"([^aeiouáíéóú])i([sv]ya)$", u"\\1í\\2")
				c.append_step(u"([^aeiouáíéóú])u([sv]ya)$", u"\\1ú\\2")
				c.append_step(u"$", u"e")
				c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ya$")
				c.append_step(u"ya$", u"ne")

			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[rnm]$")
			c.append_step(u"$", u"ne")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[ptc]{2}[au]$")
			c.append_step(u"$", u"ne")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"p[au]?$")
			c.append_step(u"p[au]?$", u"mpe")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"([tc]$)|(qu$)")
			c.append_step(u"([tc]$)|(qu$)", u"n\\1e")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"tt[au]$")
			c.append_step(u"tt[au]$", u"nne")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"pp[au]?$")
			c.append_step(u"pp[au]?$", u"mme")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"t[au]$")
			c.append_step(u"n?t[au]$", u"nte")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"p[au]?$")
			c.append_step(u"p[au]?$", u"mpe")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"l[au]?$")
			c.append_step(u"l[au]?$", u"lle")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[sv]$")
			c.append_step(u"a([sv]$)", u"á\\1")
			c.append_step(u"e([sv]$)", u"é\\1")
			c.append_step(u"o([sv]$)", u"ó\\1")
			c.append_step(u"([^aeiouáíéóú])i([sv])$", u"\\1í\\2")
			c.append_step(u"([^aeiouáíéóú])u([sv])$", u"\\1ú\\2")
			c.append_step(u"$", u"e")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[^aeiouáíéóú]qu[au]$")
			c.append_step(u"$", u"ne") 
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"x[au]$")
			c.append_step(u"$", u"ne")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiou][ui][^aeiouáíéóú][au]$")
			c.append_step(u"$", u"ne")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[^aeiou][^aeiouáíéóú][au]$")
			c.append_step(u"$", u"ne")
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"ne") 
			tr = f.create_form(("past", "pl", "0")) 
			c = tr.create_transform((u"past", "s", "0"))
			c.append_step(u"$", u"r")



			tr = f.create_form(("perf", "s", "0"))
			c = tr.create_transform(BASED_ON_ENTRY_FORM,u"^[aeiouáíéóú]")
			c.append_step(u"y*[au]?$", u"ie")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiou]{2}([^aeiouáíéóú]|qu)y*[au]?$")
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)([aeiou])([aeiou])([^aeiouáíéóú]|qu)$", u"\\2\\1\\2\\3\\4")
			c.append_step(u"$", u"ie")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[aeiouáíéóú]([^aeiouáíéóú]|qu)y*[au]?$")
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)[aá]([^aeiouáíéóú]|qu)$", u"a\\1á\\2")
			c.append_step(u"^(.*)[eé]([^aeiouáíéóú]|qu)$", u"e\\1é\\2")
			c.append_step(u"^(.*)[ií]([^aeiouáíéóú]|qu)$", u"i\\1í\\2")
			c.append_step(u"^(.*)[oó]([^aeiouáíéóú]|qu)$", u"o\\1ó\\2")
			c.append_step(u"^(.*)[uú]([^aeiouáíéóú]|qu)$", u"u\\1ú\\2")
			c.append_step(u"$", u"ie")
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)a", u"a\\1a")
			c.append_step(u"^(.*)e", u"e\\1e")
			c.append_step(u"^(.*)i", u"i\\1i")
			c.append_step(u"^(.*)o", u"o\\1o")
			c.append_step(u"^(.*)u", u"u\\1u")
			c.append_step(u"$", u"ie")
			tr = f.create_form(("perf", "pl", "0")) 
			c = tr.create_transform(("perf", "s", "0"))
			c.append_step(u"$", u"r")

			tr = f.create_form(("fut", "s", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"u$")
			c.append_step(u"u$", u"úva")
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
			c.append_step(u"a?$", u"uva")
			tr = f.create_form(("fut", "pl", "0")) 
			c = tr.create_transform(("fut", "s", "0"))
			c.append_step(u"$", u"r")


			tr = f.create_form(("inf", "0", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"u$")
			c.append_step(u"u$", u"o")
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"e")
			

			tr = f.create_form(("imp", "2", "0")) 
			c = tr.create_transform(("inf", "0", "0"))
			
			tr = f.create_form(("act-part", "0", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
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
			
			tr = f.create_form(("pass-part", "0", "0")) 
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"qu$")
			c.append_step(u"a(?=qu)$", u"á")
			c.append_step(u"e(?=qu)$", u"é")
			c.append_step(u"o(?=qu)$", u"ó")
			c.append_step(u"(?<=[^aeiou])i(?=qu)$", u"í")
			c.append_step(u"(?<=[^aeiouá])u(?=qu)$", u"ú")
			c.append_step(u"$", u"ina")
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[au]$")
			c.append_step(u"$", u"na")	
			c = tr.create_transform(BASED_ON_ENTRY_FORM, u"l$")
			c.append_step(u"$", u"da")	
			c = tr.create_transform(BASED_ON_ENTRY_FORM)
			c.append_step(u"a(?=[^aeiouáíéóú][yw]?)$", u"á")
			c.append_step(u"e(?=[^aeiouáíéóú][yw]?)$", u"é")
			c.append_step(u"o(?=[^aeiouáíéóú][yw]?)$", u"ó")
			c.append_step(u"(?<=[^aeiou])i(?=[^aeiouáíéóú][yw]?)$", u"í")
			c.append_step(u"(?<=[^aeiou])u(?=[^aeiouáíéóú][yw]?)$", u"ú")
			c.append_step(u"(?<=[^rmn])$", u"i")
			c.append_step(u"$", u"na")	

			TENSE = ["aor","pres","past","perf","fut"]
			SUBJ = {"1s":[u"nye",u"n"], "2":[u"lye",u"l"], "3s":[u"rye",u"s"], "1+2+3": [u"lve"], "1+3": [u"lme"], "1d": [u"mme"], "3pl":[u"nte"]}
			OBJ = {"1s":u"n", "2":u"l", "3s":u"s", "3pl":u"t"}
			for t in TENSE:
				for k,v in SUBJ.iteritems():
					tr = f.create_form((t, k, "0"))
					c = tr.create_transform((t, "s", "0"))
					if t==u"aor":
						c.append_step(u"e$", u"i")
					if len(v)==1:
						c.append_step(u"$", v[0])
					else:
						c.append_step(u"$", v[1])
					if transitive:
						for k1, v1 in OBJ.iteritems():
							tr = f.create_form((t, k, k1))
							c = tr.create_transform((t, "s", "0"))
							c.append_step(u"$", v[0]+v1)

			if transitive:
				for k1, v1 in OBJ.iteritems():
					tr = f.create_form(("inf", "0", k1))
					c = tr.create_transform(BASED_ON_ENTRY_FORM)
					c.append_step(u"(?<=[^au])$", u"i")
					c.append_step(u"$", u"ta"+v1)

		add_verb_inflection( CategoryFilter("in", ("Acc", "Acc+Dat")), True)
		add_verb_inflection( CategoryFilter("ni", ("Acc", "Acc+Dat")), False)
		
		f = fl.create_inflection(u"adj")

		tr = f.create_form(("s", "Nom", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM)

		tr = f.create_form(("s", "Gen", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"o")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"io")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"do")
		tr = f.create_form(("s", "Poss", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"ava")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"iva")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"wa")
		tr = f.create_form(("s", "Dat", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"$", u"n")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"in")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"den")
		tr = f.create_form(("s", "Abl", "0"))
		c = tr.create_transform(("s", "Dat", "0"))
		c.append_step(u"n$", u"llo")
		tr = f.create_form(("s", "All", "0"))
		c = tr.create_transform(("s", "Dat", "0"))
		c.append_step(u"n$", u"nna")
		tr = f.create_form(("s", "Loc", "0"))
		c = tr.create_transform(("s", "Dat", "0"))
		c.append_step(u"n$", u"sse")
		tr = f.create_form(("s", "Instr", "0"))
		c = tr.create_transform(("s", "Dat", "0"))
		c.append_step(u"$", u"en")
		tr = f.create_form(("s", "Resp", "0"))
		c = tr.create_transform(("s", "Dat", "0"))
		c.append_step(u"n$", u"s")


		tr = f.create_form(("pl", "Nom", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ea$")
		c.append_step(u"ea$", u"ie")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"e")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"i")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"di")
		tr = f.create_form(("pl", "Gen", "0"))
		c = tr.create_transform(("pl", "Nom", "0"), u"ie")
		c.append_step(u"ie$", u"iéon")
		c = tr.create_transform(("pl", "Nom", "0"))
		c.append_step(u"$", u"on")
		tr = f.create_form(("pl", "Poss", "0"))
		c = tr.create_transform(("pl", "Dat", "0"))
		c.append_step(u"n$", u"va")
		tr = f.create_form(("pl", "Dat", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ea$")
		c.append_step(u"ea$", u"ín")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"ain")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"ín")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"din")
		tr = f.create_form(("pl", "Abl", "0"))
		c = tr.create_transform(("s", "Abl", "0"))
		c.append_step(u"$", u"n")
		tr = f.create_form(("pl", "All", "0"))
		c = tr.create_transform(("s", "All", "0"))
		c.append_step(u"$", u"r")
		tr = f.create_form(("pl", "Loc", "0"))
		c = tr.create_transform(("s", "Loc", "0"))
		c.append_step(u"$", u"n")
		tr = f.create_form(("pl", "Instr", "0"))
		c = tr.create_transform(("pl", "Dat", "0"))
		c.append_step(u"$", u"en")
		tr = f.create_form(("pl", "Resp", "0"))
		c = tr.create_transform(("pl", "Dat", "0"))
		c.append_step(u"n$", u"s")

		tr = f.create_form(("d", "Nom", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ea$")
		c.append_step(u"ea$", u"iet")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"at")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"it")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"det")

		tr = f.create_form(("d", "Gen", "0"))
		c = tr.create_transform(("d", "Nom", "0"), u"iet")
		c.append_step(u"et$", u"éto")
		c = tr.create_transform(("d", "Nom", "0"))
		c.append_step(u"t$", u"to")

		tr = f.create_form(("d", "Poss", "0"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"ea$")
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"t$", u"twa")

		tr = f.create_form(("d", "Dat", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"t$", u"nt")

		tr = f.create_form(("d", "Abl", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"t$", u"lto")

		tr = f.create_form(("d", "All", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"t$", u"nta")

		tr = f.create_form(("d", "Loc", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"t$", u"tse")

		tr = f.create_form(("d", "Instr", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"t$", u"nten")

		tr = f.create_form(("d", "Resp", "0"))
		c = tr.create_transform(("d", "Nom", "0"))
		tr.append_step(u"t$", u"tes")

		def add_grd(g):
			tr = f.create_form(("s", "Gen", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"a$", u"o")
			tr = f.create_form(("s", "Poss", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"va")
			tr = f.create_form(("s", "Dat", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"n")
			tr = f.create_form(("s", "Abl", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"llo")
			tr = f.create_form(("s", "All", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"nna")
			tr = f.create_form(("s", "Loc", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"sse")
			tr = f.create_form(("s", "Instr", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"nen")
			tr = f.create_form(("s", "Resp", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"s")

			tr = f.create_form(("pl", "Nom", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"a$", u"e")
			tr = f.create_form(("pl", "Gen", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"a$", u"eon")
			tr = f.create_form(("pl", "Poss", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"iva")
			tr = f.create_form(("pl", "Dat", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"in")
			tr = f.create_form(("pl", "Abl", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"llon")
			tr = f.create_form(("pl", "All", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"llar")
			tr = f.create_form(("pl", "Loc", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"ssen")
			tr = f.create_form(("pl", "Instr", g))
			c = tr.create_transform(("pl", "Dat", g))
			c.append_step(u"$", u"en")
			tr = f.create_form(("pl", "Resp", g))
			c = tr.create_transform(("pl", "Dat", g))
			c.append_step(u"n$", u"s")

			tr = f.create_form(("d", "Nom", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"t")

			tr = f.create_form(("d", "Gen", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"to")

			tr = f.create_form(("d", "Poss", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"twa")

			tr = f.create_form(("d", "Dat", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"nt")

			tr = f.create_form(("d", "Abl", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"lto")

			tr = f.create_form(("d", "All", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"nta")

			tr = f.create_form(("d", "Loc", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"tse")

			tr = f.create_form(("d", "Instr", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$",u"nten")

			tr = f.create_form(("d", "Resp", g))
			c = tr.create_transform(("s", "Nom", g))
			c.append_step(u"$", u"tes")		

		tr = f.create_form(("s", "Nom", "rel"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"alda")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"ilda")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"[ie]n$")
		c.append_step(u"(?<=[ie]n)$", u"ilda")

		add_grd("rel")

		tr = f.create_form(("s", "Nom", "abs"))
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"^[lmrs]")
		c.append_step(u"^([lmrs])", u"a\\1\\1")
		c = tr.create_transform(BASED_ON_ENTRY_FORM, u"^p")
		c.append_step(u"^", u"am")
		c = tr.create_transform(BASED_ON_ENTRY_FORM)
		c.append_step(u"^", u"an")

		add_grd("abs")

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
		d.append(  (u"cas", u"cár", "cesi") ) #head
		d.append(  (u"cumbo", u"cumbo", "fucesi") ) #belly
		d.append(  (u"hon", u"hón", "kawcesi") ) #heart
		d.append(  (u"esse", u"esse", "tedapemi", [(u"essi", ("pl","Nom","0"))] ) ) #name
		d.append(  (u"sambe", u"sambe", "depi") ) #room
		d.append(  (u"card", u"car", "byekigi") ) #building
		d.append(  (u"telme", u"telme", "bidetavi") ) #blanket
		d.append(  (u"limpe", u"limpe", "zoyfupi") ) #spirits
		#d.append(  (u"0", u"síra", "bape-tovay") ) #today
		d.append(  (u"sovasamb", u"sovasan", "bodepi") ) #restroom
		d.append(  (u"lindale", u"lindale", "dinjami") ) #music
		d.append(  (u"colla", u"colla", "byetavi") ) #garment
		d.append(  (u"tecil", u"tecil", "bofifusi") ) #pen
		d.append(  (u"hríve", u"hríve", "cayfemi") ) #winter
		d.append(  (u"laire", u"laire", "fefemi") ) #summer
		d.append(  (u"henets", u"henet", "kifigi", [(u"henetwa", ("s","Poss","0"))] ) ) #window
		d.append(  (u"rancu", u"ranco", "twecesi") ) #arm
		d.append(  (u"nonwa", u"nonwa", "kobisi") ) #computer
		d.append(  (u"palancen", u"palancen", "kifabisi") ) #television
		d.append(  (u"asta", u"asta", "ketovi") ) #month
		d.append(  (u"nolyasse", u"nolyasse", "kokigi") ) #school
		d.append(  (u"ner", u"nér", "loybegi") ) #man
		d.append(  (u"niss", u"nís", "lawbegi") ) #woman
		d.append(  (u"híni", u"hína", "fobegi", [(u"híni", ("pl","Nom","0"))] ) )#child
		d.append(  (u"huo", u"huo", "zovi") ) #dog
		d.append(  (u"yaule", u"yaule", "kwizovi") ) #cat
		d.append(  (u"aiwe", u"aiwe", "byedami") ) #bird
		d.append(  (u"lingwi", u"lingwe", "byebomi") ) #fish
		d.append(  (u"mas", u"mar", "kigi") ) #house
		d.append(  (u"yaxe", u"yaxe", "lawfutigi") ) #cow
		d.append(  (u"ilim", u"ilin", "bazopi") ) #milk
		d.append(  (u"massa", u"massa", "josi") ) #bread
		d.append(  (u"norolle", u"norolle", "timi") ) #car
		d.append(  (u"ori", u"ore", "cindonfupi") ) #rice-grain
		d.append(  (u"vinya", u"vinya", "dawkemo") ) #new
		d.append(  (u"orva", u"orva", "zobemi") ) #apple
		d.append(  (u"apsa", u"apsa", "fayzopi") ) #meat
		d.append(  (u"celva", u"celva", "byefasi") ) #animal
		d.append(  (u"quen", u"quén", "begi") ) #person
		d.append(  (u"hanta", u"hanta", "xentegemu") ) #thank you
		d.append(  (u"nen", u"nén", "bocivi") ) #water
		d.append(  (u"telco", u"telco", "jicesi", [(u"telqui", ("pl","Nom","0"))]) ) #leg
		d.append(  (u"polca", u"polca","jotigi") ) #pig
		d.append(  (u"meldo", u"meldo", "zoyzevi") ) #friend
		d.append(  (u"aure", u"aure", "tovi") ) #day
		d.append(  (u"ear", u"ear", "kebivi") ) #sea
		d.append(  (u"malle", u"malle", "zegi", [(u"maller", ("pl","Nom","0"))]))#road
		d.append(  (u"caima", u"caima", "kunjisi") ) #bed
		d.append(  (u"telpe", u"telpe", "jafimi") ) #money
		d.append(  (u"ando", u"ando", "tifigi") ) #door
		d.append(  (u"tyurd", u"tyur", "caybafupi") ) #cheese
		d.append(  (u"palallon", u"palallon", "tebisi") ) #telphone
		d.append(  (u"lómi", u"lóme", "kunfemi") ) #night
		d.append(  (u"miriand", u"mirian", "cayjafimi") ) #coin
		d.append(  (u"toron", u"toron", "zutasaw", [(u"torno", ("s","Gen","0"))])) #brother
		d.append(  (u"alda", u"alda", "jigi") ) #tree
		d.append(  (u"amill", u"amil", "ditasaw") ) #mother
		d.append(  (u"elen", u"elen", "kitisi") ) #star
		d.append(  (u"filic", u"filit", "byedami") ) #bird (little)
		d.append(  (u"sell", u"seler", "zitasaw", [(u"selerwa", ("s","Poss","0")), (u"selernen", ("s","Instr","0"))] ) )
		d.append(  (u"atar", u"atar", "dutasaw") ) #father
		d.append(  (u"tie", u"tie", "zuzegi") ) #path
		d.append(  (u"máqua", u"máqua", "zicesi") ) #hand
		d.append(  (u"tal", u"tál", "cucesi", [(u"talan", ("s","Dat","0")) , (u"talain", ("pl","Dat","0"))] ))#foot
		d.append(  (u"toll", u"tol", "ketisi", [(u"tollon", ("s","Dat","0")), (u"tolloin", ("pl","Dat","0"))] ) )#island
		d.append(  (u"ráv", u"rá", "xozovi") ) #lion
		d.append(  (u"raine", u"raine", "baxasoni") ) #peace
		d.append(  (u"cos", u"cor", "bizozugi") ) #war
		d.append(  (u"coa", u"coa", "kigi", [(u"có", ("s","Gen","0")),(u"coava", ("s","Poss","0"))] ) )#house
		d.append(  (u"mas", u"mar", "kwicalaymi",[], 2) ) #home
		d.append(  (u"nelc", u"nelet", "futevi", [(u"neletse", ("s","Loc","0"))] ) ) #tooth
		d.append(  (u"hend", u"hen", "kicesi") ) #eye
		d.append(  (u"pé", u"pé", "teduncesi", [(u"péu", ("d","Nom","0")), (u"pein", ("pl","Dat","0"))]) ) #lip
		d.append(  (u"lar", u"lár", "foycesi", [(u"laru", ("d","Nom","0"))]) ) #ear
		d.append(  (u"fiond", u"fion", "bedami") ) #hawk
		d.append(  (u"ré", u"ré", "tovi", [(u"rein", ("pl","Dat","0"))]) ) #24hours
		d.append(  (u"pí", u"pí", "byekagi", [(u"pín", ("pl","Dat","0"))]) ) #insect
		d.append(  (u"oxi", u"ohte", "docesi")) #egg
		d.append(  (u"lasse", u"lasse", "boybemi")) #leaf
		
		d.append(  (u"ambar", u"ambar", "jotisi")) #planet, world
		d.append(  (u"istar", u"istar", "joybegi", [(u"istari", ("pl","Nom","0"))])) #doctor, wizard
		
		d.append(  (u"Cemen", u"Cemen", "Ladijotisi")) #earth
		d.append(  (u"Anar", u"Anar", "Lakitisi") ) #sun
		#d.append(  Periphrase(g["noun"], "i Ertaini Nóri") ) #United States
		d.append(  (u"Vintamurta", u"Vintamurta", "Laryoxodugi") ) #New York City
		d.append(  (u"Colindor", u"Colindor", "Ladyadugi") ) #India
		d.append(  (u"Marasildor", u"Marasildor", "Lazidugi") ) #Brazil
		d.append(  (u"Rusindor", u"Rusindor", "Larudugi") ) #Russia
		d.append(  (u"Canata", u"Canata", "Lakadugi") ) #Canada
		d.append(  (u"Mornerdor", u"Mornerdor", "Lajidugi") ) #Nigeria
		d.append(  (u"Endor", u"Endor", "Lacundugi") ) #China
		d.append(  (u"Formenherosto", u"Formenherosto", "Lacunxodugi") ) #Peking
		d.append(  (u"Mexicosto", u"Mexicosto", "Laxixodugi") ) #Mexico City
		d.append(  (u"Mumba", u"Mumbai", "Labunxodugi", [(u"Mumbai", ("pl","Nom","0"))]) ) #Bombay
		d.append(  (u"Sampaulo", u"Sampaulo", "Lapawxodugi") ) #São Paulo
		d.append(  (u"Sanga", u"Sangai", "Lazanxodugi", [(u"Sangai", ("pl","Nom","0"))]) ) #Shanghai
		d.append(  (u"Masiqua", u"Masiqua", "Laruxodugi") ) #Moscow
		d.append(  (u"Isil", u"Isil", "Labatisi") ) #moon
		d.append( (u"kuiveyulda", u"kuiveyulda", "cafefupi") ) #coffee
		#d.append( (u"norolle liéva ", u"norolle liéva ", "zetimi") ) #bus
		d.append( (u"vilyacirya", u"vilyacirya", "datimi") ) #airplane
		d.append( (u"vilyahopasse", u"vilyahopasse", "dakigi") ) #airport
		d.append( (u"sarno", u"sarno", "bujisi") ) #table
		d.append( (u"yáve", u"yáve", "babemi") ) #fruit (a -)
		d.append( (u"olpe", u"olpe", "finzipi") ) #bottle
		d.append( (u"angatea", u"angatea", "kuzegi") ) #railroad
		#d.append( (u"norolle angaina", "norolle angaina", u"kuzetimi") ) #train
		d.append( (u"lambe", u"lambe", "tejami") ) #language
		d.append( (u"quetta", u"quetta", "tekusi") ) #word
		d.append( (u"tów", u"tó", "twazopi") ) #wool
		
		return d


	def verbs():
		d = []
		d.append(  (u"na", "Nom", "dapa", [(u"ne", ("past","s","0"))]) ) 
		d.append(  (u"ea", "Loc", "zoga", [(u"ea", ("pres","s","0")), (u"engie", ("perf","s","0")), (u"enge", ("past","s","0"))]) ) 
		d.append(  (u"cen", "Acc", "kiva") ) 
		d.append(  (u"mel", "Acc", "bakopa") )  #love
		d.append(  (u"mat", "0", "fucala") ) #eat
		d.append(  (u"suc", "0", "bofucala") ) #drink
		d.append(  (u"ista", "Acc", "kopa", [(u"sinte", ("past","s","0")), (u"isintie", ("perf","s","0")), (u"sinwa", ("pass-part","0","0"))]) ) 
		d.append(  (u"lelya", "0", "ticala", [(u"lende", ("past","s","0"))]) )  
		d.append(  (u"ulya", "Acc", "tibokavasa", [], 1) )  
		d.append(  (u"ulya", "0", "tibokava", [], 2) )  
		d.append(  (u"mar", "0", "kwicala", [(u"ambárie", ("perf","s","0"))]) )
		d.append(  (u"móta", "0", "bucala") ) #work
		#d.append(  (u"mára", "Acc", u"zoykopa") ) #like
		d.append(  (u"tyal", "0", "dwecala" ) ) #play
		d.append(  (u"canta", "Acc", "joykavapa") ) #fix
		d.append(  (u"rac", "Acc", "joyjuvapa") ) #break
		d.append(  (u"nyar", "Acc+Dat", "tega") ) #tell
		d.append(  (u"quet", "Dat", "tegapa", [(u"equétie", ("perf","s","0"))]) ) #speak to 
		d.append(  (u"mala", "0", "xonkepa") ) #suffer
		d.append(  (u"lor", "0", "kunkepa") ) #sleep
		d.append(  (u"mer", "Acc", "cakopa") ) #want
		d.append(  (u"appa", "Acc", "kenbusa") ) #touch
		d.append(  (u"anta", "Acc+Dat", "ximamba", [(u"áne", ("past","s","0"))]) )  #give
		d.append(  (u"yuhta", "Acc", "busasa") ) #use, control
		d.append(  (u"lanta", u"0", "dafagupa") ) #fall
		return d


	def adjs():
		d = []
		d.append(  (u"sina", "baso") ) #this
		d.append(  (u"tana", "zaso") ) #that
		d.append(  (u"alwa", "joykepo") ) #healthy
		d.append(  (u"mára", "cakemo") ) #good
		d.append(  (u"olca", "cafomo") ) #bad, evil
		d.append(  (u"pitya", "fomo") ) #small
		d.append(  (u"alta", "kemo") ) #big
		d.append(  (u"yára", "zonculo") ) #old (vs.young)
		d.append(  (u"silque", "cinzigo") ) #white
		d.append(  (u"more", "kunzigo") ) #black
		d.append(  (u"nessa", "zondelo") ) #young
		d.append(  (u"carne", "zozigo") ) #red
		d.append(  (u"yerna", "dawfomo") ) #old (vs.new)
		d.append(  (u"luin",  "dazigo") ) #blue
		d.append(  (u"malina", "fezigo") ) #yellow
		d.append(  (u"hlaiwa", "joykolo") ) #sick
		d.append(  (u"lauca", "feculo") ) #warm
		d.append(  (u"ringa", "fedelo") ) #cold		
		d.append(  (u"vanya", "kekaykemo", [(u"ambanya", ("s","Nom","abs"))]) )   #beautiful
		d.append(  (u"vára", "cinjuvo", [(u"anwára", ("s","Nom","abs"))]) )   #dirty
		d.append(  (u"laurea", "todapyu taykocivo")  ) #golden
		d.append(  (u"ilya", "bikavo")  ) #all, whole
		
		return d

	def adv():
		d = []
		d.append((u"ehtala", "dipe-tovay")) #tomorrow
		return d

	l = Lect(u"qya")
	l.name = u"Quenya"
	l.english_name = "Neo-Quenya"
	l.append_p_o_s("v", ("arguments",), ("tense", "person", "object person"))
	l.append_p_o_s("n", (), ("number", "case", "person"))
	l.append_p_o_s("adj", (), ("number", "case", "degree"))
	l.append_p_o_s("adv", (), ())
	l.append_p_o_s("prep", ("argument",), ("object person",))
	build_inflections(l.inflections)
	build_lexicon(l.lexicon, l.inflections)
	print str(l.lexicon)
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
	show(u"melin fion ringa")
	show(u"cor vanya mele i lauca alda")
	show(u"melin lóme")
	lome = l.read(u"melin lóme")[0].subtree(('nucleus', 'Vs O', 'O', 'noun-phrase,Nom', 'noun-phrase,s,Nom', 'n'))
	for i in lome.iter_items():
		print i.form
	for w in l.lexicon.retrieve_words(None, (u"lasse",1), (CategoryFilter("in",("s","pl")), None, "0")):
		print " ".join(w.categories),":", w.form

if __name__ == "__main__":
	run()

