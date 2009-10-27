#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to create and test Quenya language.
"""

from pylilac.core.bnf import KLEENE_CLOSURE
from pylilac.core.bnf import OPTIONAL_CLOSURE
from pylilac.core.bnf import Reference
from pylilac.core.inflection import BASED_ON_ENTRY_FORM
from pylilac.core.lect import Lect
from pylilac.core.lexicon import CategoryFilter
from pylilac.core.lexicon import Lexeme
from pylilac.core.lexicon import Particle
from pylilac.core.lexicon import Word
from pylilac.core.lexicon import WordCategoryFilter
from pylilac.core.lexicon import WordFilter
import re


def report_words():
	vc = open("test/words.txt", "r")
	from pylilac.core.interlingua import Interlingua
	il = Interlingua("trunk/src/data/Latejami.csv")
	il.load()
	tx = il.taxonomy
	for riga in vc:
		x = [manca.entry_form.encode("utf-8", "replace") for manca in l.lexicon.find_lemmas() if isinstance(manca, Lexeme) and riga.startswith(manca.gloss)]
		if x:
			pass#print riga[:-1],  x
		else:
			if tx.get(riga[:-1]):
				mn = tx.get(riga[:-1]).meaning
			else:
				mn = riga[:-1]
			print"\td.append( (u\"...\", u\"...\", \"" + riga[:-1] + "\") )  #" + mn
	vc.close()

def run():
	def show(s):
		print
		print `s`
		for i, x in enumerate(l.read(s)):
			print u"%d. " % i, x



	def build_lexicon(l, f):
		def correct_table(table):
			correct_word(table, u"^híninya", u"hínya")
			correct_word(table, u"^húa", u"hua")
			v, w = u"aeiou", u"áéíóú"
			for i in (0, 1, 2, 3, 4):
				correct_word(table, w[i] + u"ll", v[i] + u"ll")
				correct_word(table, w[i] + u"nn", v[i] + u"nn")
				correct_word(table, w[i] + u"ss", v[i] + u"ss")
				correct_word(table, w[i] + u"lv", v[i] + u"lv")
				correct_word(table, w[i] + u"mm", v[i] + u"mm")
				correct_word(table, w[i] + u"lm", v[i] + u"lm")
				correct_word(table, w[i] + u"lt", v[i] + u"lt")
				correct_word(table, w[i] + u"nt", v[i] + u"nt")
				correct_word(table, w[i] + u"ts", v[i] + u"ts")
				correct_word(table, w[i] + u"x", v[i] + u"x")
				correct_word(table, w[i] + u"([^lnhcgr])y", v[i] + u"\\1y")
				correct_word(table, w[i] + u"([^lnhgr])w", v[i] + u"\\1w")

		for h in nouns():
			if len(h) > 4:
				id = h[4]
			else:
				id = 1
			lemma = Lexeme(h[0], id, "n", (), h[2])
			word = Word(h[1], lemma, ("s", "Nom", "0"))
			words = [word]
			if len(h) > 3:
				for j in h[3]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			correct_table(ft)
			l.add_lemma(lemma)
			if ord(h[0][0]) < 91:
				proper = 1
			else:
				proper = 0
			for w in ft.values():
				if proper == 0 or (proper == 1 and w.categories[0] == "s" and w.categories[2] == "0")or (proper == 2 and w.categories[0] == "pl" and w.categories[2] == "0"):
					l.add_word(w)

		for h in verbs():
			if len(h) > 4:
				id = h[4]
			else:
				id = 1
			lemma = Lexeme(h[0], id, "v", (h[1],), h[2])
			words = []
			if len(h) > 3:
				for j in h[3]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			if lemma.entry_form == u"na":
				lemma = Lexeme(u"ná", 1, lemma.p_o_s, lemma.categories, lemma.gloss)
				for k in ft:
					ft[k] = ft[k].copy(lemma)
				ft[("aor", "s", "0")] = Word(u"ná", lemma, ("aor", "s", "0"))
				ft[("past", "s", "0")] = Word(u"né", lemma, ("past", "s", "0"))

			correct_table(ft)
			l.add_lemma(lemma)
			for w in ft.values():
				l.add_word(w)

		for h in adjs():
			if len(h) > 3:
				id = h[3]
			else:
				id = 1
			if len(h) > 4:
				arguments = h[4]
			else:
				arguments = ("0", )
			lemma = Lexeme(h[0], id, "adj", arguments, h[1])
			words = []
			if len(h) > 2:
				for j in h[2]:
					word = Word(j[0], lemma, j[1])
					words.append(word)
			ft = f(lemma, words)
			correct_table(ft)

			l.add_lemma(lemma)
			for w in ft.values():
				l.add_word(w)

			if h[0][-1] == u"a":
				adverb = re.sub(u"a$", u"ave", h[0])
			elif h[0][-1] == u"e":
				adverb = re.sub(u"e$", u"ive", h[0])
			elif h[0][-1] == u"n":
				adverb = re.sub(u"n$", u"mbe", h[0])
			if h[0] == u"mára":
				adverb = u"vande"

			adverb_gloss = re.sub(u"o$", u"e", h[1])
			l.add_word(Word(adverb, Lexeme(adverb, id, "adv", (), adverb_gloss), ()))

		l.add_word(Word(u"i", Particle(u"i", 1, "adj", ()), ("0", "0", "0")))



	def correct_word(table, old, new):
		for k, v in table.items():
			if re.search(old, v.form, re.I):
				v2 = Word(re.sub(old, new, v.form, re.I), v.lemma, v.categories)
				table[k] = v2

	def build_inflections(fl):
		f = fl.create_inflection("n")

		c = f.create_transform(("s", "Nom", "0"), BASED_ON_ENTRY_FORM)

		c = f.create_transform(("s", "Gen", "0"), BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quo")
		c.append_step(u"gu$", u"gwo")
		c.append_step(u"hu$", u"hwo")
		c = f.create_transform(("s", "Gen", "0"), BASED_ON_ENTRY_FORM, u"w$")
		c.append_step(u"w$", u"vo")
		c = f.create_transform(("s", "Gen", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=i)e$", u"é")
		c.append_step(u"[ao]?$", u"o")

		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"[aeio][aeiou][^aeiouáéíóúx][aeiou]$")
		c.append_step(u"$", u"va")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"[aeiou][^aeiouáéíóúx][aeiou]$")
		c.append_step(u"a$", u"áva")
		c.append_step(u"e$", u"éva")
		c.append_step(u"i$", u"íva")
		c.append_step(u"o$", u"óva")
		c.append_step(u"u$", u"úva")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"ie$")
		c.append_step(u"e$", u"éva")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"c$")
		c.append_step(u"c$", u"qua")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"v$")
		c.append_step(u"$", u"a")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"[nlrm][^aeiouáéíóú]$")
		c.append_step(u"[^aeiouáéíóú]$", u"wa")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"ts$")
		c.append_step(u"s$", u"wa")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"w$")
		c.append_step(u"w$", u"va")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"[^aeiouáéíóú][^aeiouáéíóú]$")
		c.append_step(u"$", u"eva")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"[aeiouáéíóú]$")
		c.append_step(u"$", u"va")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"$", u"wa")

		c = f.create_transform(("s", "Dat", "0"), BASED_ON_ENTRY_FORM, u"[aeiouáéíóú]$")
		c.append_step(u"$", u"n")
		c = f.create_transform(("s", "Dat", "0"), ("s", "Gen", "0"))
		c.append_step(u"o$", u"en")

		c = f.create_transform(("s", "Abl", "0"), BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"llo")
		c = f.create_transform(("s", "Abl", "0"), BASED_ON_ENTRY_FORM, u"rr?$")
		c.append_step(u"rr?$", u"llo")
		c = f.create_transform(("s", "Abl", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"llo")

		c = f.create_transform(("s", "All", "0"), BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"lda")
		c = f.create_transform(("s", "All", "0"), BASED_ON_ENTRY_FORM, u"nn?$")
		c.append_step(u"nn?$", u"nna")
		c = f.create_transform(("s", "All", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"nna")

		c = f.create_transform(("s", "Loc", "0"), BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"lde")
		c = f.create_transform(("s", "Loc", "0"), BASED_ON_ENTRY_FORM, u"nn?$")
		c.append_step(u"nn?$", u"nde")
		c = f.create_transform(("s", "Loc", "0"), BASED_ON_ENTRY_FORM, u"ss?$")
		c.append_step(u"ss?$", u"sse")
		c = f.create_transform(("s", "Loc", "0"), BASED_ON_ENTRY_FORM, u"[aeiou]ts?$")
		c.append_step(u"s?$", u"se")
		c = f.create_transform(("s", "Loc", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"sse")

		c = f.create_transform(("s", "Instr", "0"), BASED_ON_ENTRY_FORM, u"[aeiou][ct]$")
		c.append_step(u"([ct])$", u"n\\1en")
		c = f.create_transform(("s", "Instr", "0"), BASED_ON_ENTRY_FORM, u"[aeiou]p$")
		c.append_step(u"p$", u"mpen")
		c = f.create_transform(("s", "Instr", "0"), BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"lden")
		c = f.create_transform(("s", "Instr", "0"), BASED_ON_ENTRY_FORM, u"nn?$")
		c.append_step(u"nn?$", u"nnen")
		c = f.create_transform(("s", "Instr", "0"), BASED_ON_ENTRY_FORM, u"rr?$")
		c.append_step(u"rr?$", u"rnen")
		c = f.create_transform(("s", "Instr", "0"), BASED_ON_ENTRY_FORM, u"m$")
		c.append_step(u"$", u"nen")
		c = f.create_transform(("s", "Instr", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"(?<=i)e$", u"é")
		c.append_step(u"(?<=[^aeiouáéíóú])$", u"e")
		c.append_step(u"$", u"nen")


		c = f.create_transform(("s", "Resp", "0"), ("s", "Dat", "0"))
		c.append_step(u"n$", u"s")



		#plural

		c = f.create_transform(("pl", "Nom", "0"), BASED_ON_ENTRY_FORM, u"[^aeiouáéíóú][cgh]u$")
		c.append_step(u"cu$", u"qui")
		c.append_step(u"gu$", u"gwi")
		c.append_step(u"hu$", u"hwi")
		c = f.create_transform(("pl", "Nom", "0"), BASED_ON_ENTRY_FORM, u"[aiouáéíóú]$|ie$")
		c.append_step(u"$", u"r")
		c = f.create_transform(("pl", "Nom", "0"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"i")
		c = f.create_transform(("pl", "Nom", "0"), ("s", "Gen", "0"))
		c.append_step(u"e?o$", u"i")


		#Indirect plural

		c = f.create_transform(("pl", "Gen", "0"), ("pl", "Nom", "0"))
		c.append_step(u"ier$", u"iér")
		c.append_step(u"$", u"on")

		c = f.create_transform(("pl", "Poss", "0"), ("pl", "Dat", "0"))
		c.append_step(u"n$", u"va")

		c = f.create_transform(("pl", "Dat", "0"), BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quín")
		c.append_step(u"gu$", u"gwín")
		c.append_step(u"hu$", u"hwín")
		c = f.create_transform(("pl", "Dat", "0"), BASED_ON_ENTRY_FORM, u"i$|e$|(ie)$")
		c.append_step(u"i$|e$|(ie)$", u"ín")
		c = f.create_transform(("pl", "Dat", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"$", u"in")

		c = f.create_transform(("pl", "Abl", "0"), BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quillon")
		c.append_step(u"gu$", u"gwillon")
		c.append_step(u"hu$", u"hwillon")
		c = f.create_transform(("pl", "Abl", "0"), BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"llon")
		c = f.create_transform(("pl", "Abl", "0"), BASED_ON_ENTRY_FORM, u"rr?$")
		c.append_step(u"rr?$", u"llon")
		c = f.create_transform(("pl", "Abl", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"llon")

		c = f.create_transform(("pl", "All", "0"), BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quinnar")
		c.append_step(u"gu$", u"gwinnar")
		c.append_step(u"hu$", u"hwinnar")
		c = f.create_transform(("pl", "All", "0"), BASED_ON_ENTRY_FORM, u"nn?$")
		c.append_step(u"nn?$", u"nnar")
		c = f.create_transform(("pl", "All", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"nnar")

		c = f.create_transform(("pl", "Loc", "0"), BASED_ON_ENTRY_FORM, u"ts$")
		c.append_step(u"$", u"en")
		c = f.create_transform(("pl", "Loc", "0"), BASED_ON_ENTRY_FORM, u"c$")
		c.append_step(u"c$", u"xen")
		c = f.create_transform(("pl", "Loc", "0"), BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quissen")
		c.append_step(u"gu$", u"gwissen")
		c.append_step(u"hu$", u"hwissen")
		c = f.create_transform(("pl", "Loc", "0"), BASED_ON_ENTRY_FORM, u"ss?$")
		c.append_step(u"ss?$", u"ssen")
		c = f.create_transform(("pl", "Loc", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1i")
		c.append_step(u"$", u"ssen")


		c = f.create_transform(("pl", "Instr", "0"), ("pl", "Dat", "0"))
		c.append_step(u"$", u"en")

		c = f.create_transform(("pl", "Resp", "0"), ("pl", "Dat", "0"))
		c.append_step(u"n$", u"s")





		#Dual

		c = f.create_transform(("d", "Nom", "0"), BASED_ON_ENTRY_FORM, u"u$|ie$")
		c.append_step(u"$", u"t")
		c = f.create_transform(("d", "Nom", "0"), ("s", "Gen", "0"), u"[dt].{0,4}o$")
		c.append_step(u"o$", u"u")
		c = f.create_transform(("d", "Nom", "0"), BASED_ON_ENTRY_FORM, u"[aeioáéíóú]$")
		c.append_step(u"$", u"t")
		c = f.create_transform(("d", "Nom", "0"), ("s", "Gen", "0"))
		c.append_step(u"o$", u"et")

		c = f.create_transform(("d", "Gen", "0"), ("d", "Nom", "0"))
		c.append_step(u"eu$", u"et")
		c.append_step(u"([aeiouáéíóú][lnrs])et$", u"\\1t")
		c.append_step(u"iet$", u"iét")
		c.append_step(u"$", u"o")

		c = f.create_transform(("d", "Poss", "0"), ("d", "Nom", "0"))
		c.append_step(u"u$", u"uva")
		c.append_step(u"t$", u"twa")

		c = f.create_transform(("d", "Dat", "0"), ("d", "Nom", "0"))
		c.append_step(u"u$", u"un")
		c.append_step(u"t$", u"nt")

		c = f.create_transform(("d", "Abl", "0"), ("d", "Nom", "0"))
		c.append_step(u"u$", u"ullo")
		c.append_step(u"t$", u"lto")

		c = f.create_transform(("d", "All", "0"), ("d", "Nom", "0"))
		c.append_step(u"u$", u"unna")
		c.append_step(u"t$", u"nta")

		c = f.create_transform(("d", "Loc", "0"), ("d", "Nom", "0"))
		c.append_step(u"u$", u"usse")
		c.append_step(u"t$", u"tse")

		c = f.create_transform(("d", "Instr", "0"), ("d", "Nom", "0"))
		c.append_step(u"u$", u"unen")
		c.append_step(u"t$", u"nten")

		c = f.create_transform(("d", "Resp", "0"), ("d", "Nom", "0"))
		c.append_step(u"u$", u"us")
		c.append_step(u"t$", u"tes")


		#Partitive
		c = f.create_transform(("part", "Nom", "0"), BASED_ON_ENTRY_FORM, u"[cgh]u$")
		c.append_step(u"cu$", u"quili")
		c.append_step(u"gu$", u"gwili")
		c.append_step(u"hu$", u"hwili")
		c = f.create_transform(("part", "Nom", "0"), BASED_ON_ENTRY_FORM, u"ll?$")
		c.append_step(u"ll?$", u"lli")
		c = f.create_transform(("part", "Nom", "0"), BASED_ON_ENTRY_FORM, u"rr?$")
		c.append_step(u"rr?$", u"lli")
		c = f.create_transform(("part", "Nom", "0"), BASED_ON_ENTRY_FORM)
		c.append_step(u"([^aeiouáéíóú])$", u"\\1e")
		c.append_step(u"$", u"li")

		c = f.create_transform(("part", "Gen", "0"), ("part", "Nom", "0"))
		c.append_step(u"$", u"on")

		c = f.create_transform(("part", "Poss", "0"), ("part", "Nom", "0"))
		c.append_step(u"([aeiou])li$", u"\\1lí")
		c.append_step(u"$", u"va")

		c = f.create_transform(("part", "Dat", "0"), ("part", "Nom", "0"))
		c.append_step(u"$", u"n")

		c = f.create_transform(("part", "Abl", "0"), ("part", "Nom", "0"))
		c.append_step(u"$", u"llon")

		c = f.create_transform(("part", "All", "0"), ("part", "Nom", "0"))
		c.append_step(u"$", u"nnar")

		c = f.create_transform(("part", "Loc", "0"), ("part", "Nom", "0"))
		c.append_step(u"$", u"ssen")

		c = f.create_transform(("part", "Instr", "0"), ("part", "Nom", "0"))
		c.append_step(u"([aeiou])li$", u"\\1lí")
		c.append_step(u"$", u"nen")

		c = f.create_transform(("part", "Resp", "0"), ("part", "Nom", "0"))
		c.append_step(u"$", u"s")

		#Personal forms

		POSS = {"1s":u"nya", "2":u"lya", "3s":u"rya", "1+2+3": u"lva", "1+3": u"lma", "1d": u"mma", "3pl":u"nta"}
		def add_personal(number, case, person):
			z = f.create_transform((number, case, person), BASED_ON_ENTRY_FORM)
			z.append_step(u"[^aeiou]?°", u"")
			v = u"e"
			if number == "pl" or number == "part" or person == "1":
				v = u"i"
			elif number == "d":
				v = u"u"
			initial = POSS[person][0]
			z.append_step(u"([^aeiouáíéóú" + initial + u"])$", u"\\1" + v)
			z.append_step(initial + u"$", u"")
			z.append_step(u"$", POSS[person])
			return z

		for p in POSS:
			c = add_personal("s", "Nom", p)

			c = add_personal("s", "Gen", p)
			c.append_step(u"a$", u"o")

			#f.create_form(("s", "Gen", p))
			#c = f.create_transform(("s", "Nom", p))
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

			c = f.create_transform(("aor", "s", "0"), BASED_ON_ENTRY_FORM, u"a$")
			c = f.create_transform(("aor", "s", "0"), BASED_ON_ENTRY_FORM, u"u$")
			c.append_step(u"u$", u"o")
			c = f.create_transform(("aor", "s", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"e")
			c = f.create_transform(("aor", "pl", "0"), BASED_ON_ENTRY_FORM, u"[au]$")
			c.append_step(u"$", u"r")
			c = f.create_transform(("aor", "pl", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"ir")
			c = f.create_transform(("aor", "d", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"it")

			c = f.create_transform(("pres", "s", "0"), BASED_ON_ENTRY_FORM)
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
			c = f.create_transform(("pres", "pl", "0"), ("pres", "s", "0"))
			c.append_step(u"$", u"r")
			c = f.create_transform(("pres", "d", "0"), ("pres", "s", "0"))
			c.append_step(u"$", u"t")


			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"ha$")
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"wa$")
			c.append_step(u"wa$", u"ngwe")

			if transitive:
				c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"ya$")
				c.append_step(u"$", u"ne")
			else:
				c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[rnm]ya$")
				c.append_step(u"ya$", u"ne")
				c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"tya$")
				c.append_step(u"tya$", u"nte")
				c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"pya$")
				c.append_step(u"pya$", u"mpe")
				c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"lya$")
				c.append_step(u"lya$", u"lle")
				c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[sv]ya$")
				c.append_step(u"a([sv]ya)$", u"á\\1")
				c.append_step(u"e([sv]ya)$", u"é\\1")
				c.append_step(u"o([sv]ya)$", u"ó\\1")
				c.append_step(u"([^aeiouáíéóú])i([sþv]ya)$", u"\\1í\\2")
				c.append_step(u"([^aeiouáíéóú])u([sþv]ya)$", u"\\1ú\\2")
				c.append_step(u"$", u"e")
				c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"ya$")
				c.append_step(u"ya$", u"ne")

			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[rnm]$")
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[ptc]{2}[au]$")
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"p[au]?$")
			c.append_step(u"p[au]?$", u"mpe")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"([tc]$)|(qu$)")
			c.append_step(u"([tc]$)|(qu$)", u"n\\1e")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"tt[au]$")
			c.append_step(u"tt[au]$", u"nne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"pp[au]?$")
			c.append_step(u"pp[au]?$", u"mme")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"t[au]$")
			c.append_step(u"n?t[au]$", u"nte")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"p[au]?$")
			c.append_step(u"p[au]?$", u"mpe")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"l[au]?$")
			c.append_step(u"l[au]?$", u"lle")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[sv]$")
			c.append_step(u"a([sv]$)", u"á\\1")
			c.append_step(u"e([sv]$)", u"é\\1")
			c.append_step(u"o([sv]$)", u"ó\\1")
			c.append_step(u"([^aeiouáíéóú])i([sv])$", u"\\1í\\2")
			c.append_step(u"([^aeiouáíéóú])u([sv])$", u"\\1ú\\2")
			c.append_step(u"$", u"e")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[^aeiouáíéóú]qu[au]$")
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"x[au]$")
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[aeiou][ui][^aeiouáíéóú][au]$")
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM, u"[^aeiou][^aeiouáíéóú][au]$")
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "s", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"ne")
			c = f.create_transform(("past", "pl", "0"), (u"past", "s", "0"))
			c.append_step(u"$", u"r")
			c = f.create_transform(("past", "d", "0"), ("past", "s", "0"))
			c.append_step(u"$", u"t")



			c = f.create_transform(("perf", "s", "0"), BASED_ON_ENTRY_FORM, u"^[aeiouáíéóú]")
			c.append_step(u"y*[au]?$", u"ie")
			c = f.create_transform(("perf", "s", "0"), BASED_ON_ENTRY_FORM, u"[aeiou]{2}([^aeiouáíéóú]|qu)y*[au]?$")
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)([aeiou])([aeiou])([^aeiouáíéóú]|qu)$", u"\\2\\1\\2\\3\\4")
			c.append_step(u"$", u"ie")
			c = f.create_transform(("perf", "s", "0"), BASED_ON_ENTRY_FORM, u"[aeiouáíéóú]([^aeiouáíéóú]|qu)y*[au]?$")
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)[aá]([^aeiouáíéóú]|qu)$", u"a\\1á\\2")
			c.append_step(u"^(.*)[eé]([^aeiouáíéóú]|qu)$", u"e\\1é\\2")
			c.append_step(u"^(.*)[ií]([^aeiouáíéóú]|qu)$", u"i\\1í\\2")
			c.append_step(u"^(.*)[oó]([^aeiouáíéóú]|qu)$", u"o\\1ó\\2")
			c.append_step(u"^(.*)[uú]([^aeiouáíéóú]|qu)$", u"u\\1ú\\2")
			c.append_step(u"$", u"ie")
			c = f.create_transform(("perf", "s", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"y*[au]?$", u"")
			c.append_step(u"^(.*)a", u"a\\1a")
			c.append_step(u"^(.*)e", u"e\\1e")
			c.append_step(u"^(.*)i", u"i\\1i")
			c.append_step(u"^(.*)o", u"o\\1o")
			c.append_step(u"^(.*)u", u"u\\1u")
			c.append_step(u"$", u"ie")

			c = f.create_transform(("perf", "pl", "0"), ("perf", "s", "0"))
			c.append_step(u"$", u"r")
			c = f.create_transform(("perf", "d", "0"), ("perf", "s", "0"))
			c.append_step(u"$", u"t")

			c = f.create_transform(("fut", "s", "0"), BASED_ON_ENTRY_FORM, u"u$")
			c.append_step(u"u$", u"úva")
			c = f.create_transform(("fut", "s", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"a?$", u"uva")

			c = f.create_transform(("fut", "pl", "0"), ("fut", "s", "0"))
			c.append_step(u"$", u"r")
			c = f.create_transform(("fut", "d", "0"), ("fut", "s", "0"))
			c.append_step(u"$", u"t")


			c = f.create_transform(("inf", "0", "0"), BASED_ON_ENTRY_FORM, u"a$")
			c = f.create_transform(("inf", "0", "0"), BASED_ON_ENTRY_FORM, u"u$")
			c.append_step(u"u$", u"o")
			c = f.create_transform(("inf", "0", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"$", u"e")

			c = f.create_transform(("imp", "2", "0"), ("inf", "0", "0"))

			c = f.create_transform(("act-part", "0", "0"), BASED_ON_ENTRY_FORM)
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

			c = f.create_transform(("pass-part", "0", "0"), BASED_ON_ENTRY_FORM, u"qu$")
			c.append_step(u"a(?=qu)$", u"á")
			c.append_step(u"e(?=qu)$", u"é")
			c.append_step(u"o(?=qu)$", u"ó")
			c.append_step(u"(?<=[^aeiou])i(?=qu)$", u"í")
			c.append_step(u"(?<=[^aeiouá])u(?=qu)$", u"ú")
			c.append_step(u"$", u"ina")
			c = f.create_transform(("pass-part", "0", "0"), BASED_ON_ENTRY_FORM, u"[au]$")
			c.append_step(u"$", u"na")
			c = f.create_transform(("pass-part", "0", "0"), BASED_ON_ENTRY_FORM, u"l$")
			c.append_step(u"$", u"da")
			c = f.create_transform(("pass-part", "0", "0"), BASED_ON_ENTRY_FORM)
			c.append_step(u"a(?=[^aeiouáíéóú][yw]?)$", u"á")
			c.append_step(u"e(?=[^aeiouáíéóú][yw]?)$", u"é")
			c.append_step(u"o(?=[^aeiouáíéóú][yw]?)$", u"ó")
			c.append_step(u"(?<=[^aeiou])i(?=[^aeiouáíéóú][yw]?)$", u"í")
			c.append_step(u"(?<=[^aeiou])u(?=[^aeiouáíéóú][yw]?)$", u"ú")
			c.append_step(u"(?<=[^rmn])$", u"i")
			c.append_step(u"$", u"na")

			TENSE = ["aor", "pres", "past", "perf", "fut"]
			SUBJ = {"1s":[u"nye", u"n"], "2s":[u"cce", u"t"], "3s":[u"rye", u"s"], "1+2+3": [u"lve"], "2+3":[u"lye", u"l"], "1+3": [u"lme"], "1d": [u"mme"], "3pl":[u"nte"]}
			SUBJ2 = {"1s":u"ne", "2s":u"cce", "3s":u"rye", "3sm":u"ro", "3sf":u"re", "1+2+3": u"lve", "2+3":u"le", "1+3": u"lme", "1d": u"mme", "3pl":u"nte"}
			OBJ = {"1s":u"n", "2s":u"c", "3s":u"s", "2+3":u"l", "3pl":u"t"}
			for t in TENSE:
				for k, v in SUBJ.items():
					c = f.create_transform((t, k, "0"), (t, "s", "0"))
					if t == u"aor":
						c.append_step(u"e$", u"i")
					if len(v) == 1:
						c.append_step(u"$", v[0])
					else:
						c.append_step(u"$", v[1])

				if transitive:
					for k, v in SUBJ2.items():
						for k1, v1 in OBJ.items():
							if k <> k1:
								c = f.create_transform((t, k, k1), (t, "s", "0"))
								if t == u"aor":
									c.append_step(u"e$", u"i")
								c.append_step(u"$", v + v1)

			if transitive:
				for k1, v1 in OBJ.items():
					c = f.create_transform(("inf", "0", k1), BASED_ON_ENTRY_FORM)
					c.append_step(u"(?<=[^au])$", u"i")
					c.append_step(u"$", u"ta" + v1)

		add_verb_inflection(CategoryFilter("in", ("Acc", "Acc+Dat")), True)
		add_verb_inflection(CategoryFilter("ni", ("Acc", "Acc+Dat")), False)

		f = fl.create_inflection(u"adj")

		c = f.create_transform(("s", "Nom", "0"), BASED_ON_ENTRY_FORM)

		c = f.create_transform(("s", "Gen", "0"), BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"o")
		c = f.create_transform(("s", "Gen", "0"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"io")
		c = f.create_transform(("s", "Gen", "0"), BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"do")

		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"ava")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"iva")
		c = f.create_transform(("s", "Poss", "0"), BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"wa")

		c = f.create_transform(("s", "Dat", "0"), BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"$", u"n")
		c = f.create_transform(("s", "Dat", "0"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"in")
		c = f.create_transform(("s", "Dat", "0"), BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"den")

		c = f.create_transform(("s", "Abl", "0"), ("s", "Dat", "0"))
		c.append_step(u"n$", u"llo")

		c = f.create_transform(("s", "All", "0"), ("s", "Dat", "0"))
		c.append_step(u"n$", u"nna")

		c = f.create_transform(("s", "Loc", "0"), ("s", "Dat", "0"))
		c.append_step(u"n$", u"sse")

		c = f.create_transform(("s", "Instr", "0"), ("s", "Dat", "0"))
		c.append_step(u"$", u"en")

		c = f.create_transform(("s", "Resp", "0"), ("s", "Dat", "0"))
		c.append_step(u"n$", u"s")


		c = f.create_transform(("pl", "Nom", "0"), BASED_ON_ENTRY_FORM, u"ea$")
		c.append_step(u"ea$", u"ie")
		c = f.create_transform(("pl", "Nom", "0"), BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"e")
		c = f.create_transform(("pl", "Nom", "0"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"i")
		c = f.create_transform(("pl", "Nom", "0"), BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"di")

		c = f.create_transform(("pl", "Gen", "0"), ("pl", "Nom", "0"), u"ie")
		c.append_step(u"ie$", u"iéon")
		c = f.create_transform(("pl", "Gen", "0"), ("pl", "Nom", "0"))
		c.append_step(u"$", u"on")

		c = f.create_transform(("pl", "Poss", "0"), ("pl", "Dat", "0"))
		c.append_step(u"n$", u"va")

		c = f.create_transform(("pl", "Dat", "0"), BASED_ON_ENTRY_FORM, u"ea$")
		c.append_step(u"ea$", u"ín")
		c = f.create_transform(("pl", "Dat", "0"), BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"ain")
		c = f.create_transform(("pl", "Dat", "0"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"ín")
		c = f.create_transform(("pl", "Dat", "0"), BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"din")

		c = f.create_transform(("pl", "Abl", "0"), ("s", "Abl", "0"))
		c.append_step(u"$", u"n")

		c = f.create_transform(("pl", "All", "0"), ("s", "All", "0"))
		c.append_step(u"$", u"r")

		c = f.create_transform(("pl", "Loc", "0"), ("s", "Loc", "0"))
		c.append_step(u"$", u"n")

		c = f.create_transform(("pl", "Instr", "0"), ("pl", "Dat", "0"))
		c.append_step(u"$", u"en")

		c = f.create_transform(("pl", "Resp", "0"), ("pl", "Dat", "0"))
		c.append_step(u"n$", u"s")

		c = f.create_transform(("d", "Nom", "0"), BASED_ON_ENTRY_FORM, u"ea$")
		c.append_step(u"ea$", u"iet")
		c = f.create_transform(("d", "Nom", "0"), BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"at")
		c = f.create_transform(("d", "Nom", "0"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"it")
		c = f.create_transform(("d", "Nom", "0"), BASED_ON_ENTRY_FORM, u"n$")
		c.append_step(u"$", u"det")

		c = f.create_transform(("d", "Gen", "0"), ("d", "Nom", "0"), u"iet")
		c.append_step(u"et$", u"éto")
		c = f.create_transform(("d", "Gen", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"to")

		c = f.create_transform(("d", "Poss", "0"), BASED_ON_ENTRY_FORM, u"ea$")

		c = f.create_transform(("d", "Poss", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"twa")

		c = f.create_transform(("d", "Dat", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"nt")

		c = f.create_transform(("d", "Abl", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"lto")

		c = f.create_transform(("d", "All", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"nta")

		c = f.create_transform(("d", "Loc", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"tse")

		c = f.create_transform(("d", "Instr", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"nten")

		c = f.create_transform(("d", "Resp", "0"), ("d", "Nom", "0"))
		c.append_step(u"t$", u"tes")

		def add_grd(g):
			c = f.create_transform(("s", "Gen", g), ("s", "Nom", g))
			c.append_step(u"a$", u"o")

			c = f.create_transform(("s", "Poss", g), ("s", "Nom", g))
			c.append_step(u"$", u"va")

			c = f.create_transform(("s", "Dat", g), ("s", "Nom", g))
			c.append_step(u"$", u"n")

			c = f.create_transform(("s", "Abl", g), ("s", "Nom", g))
			c.append_step(u"$", u"llo")

			c = f.create_transform(("s", "All", g), ("s", "Nom", g))
			c.append_step(u"$", u"nna")

			c = f.create_transform(("s", "Loc", g), ("s", "Nom", g))
			c.append_step(u"$", u"sse")

			c = f.create_transform(("s", "Instr", g), ("s", "Nom", g))
			c.append_step(u"$", u"nen")

			c = f.create_transform(("s", "Resp", g), ("s", "Nom", g))
			c.append_step(u"$", u"s")

			c = f.create_transform(("pl", "Nom", g), ("s", "Nom", g))
			c.append_step(u"a$", u"e")

			c = f.create_transform(("pl", "Gen", g), ("s", "Nom", g))
			c.append_step(u"a$", u"eon")

			c = f.create_transform(("pl", "Poss", g), ("s", "Nom", g))
			c.append_step(u"$", u"iva")

			c = f.create_transform(("pl", "Dat", g), ("s", "Nom", g))
			c.append_step(u"$", u"in")

			c = f.create_transform(("pl", "Abl", g), ("s", "Nom", g))
			c.append_step(u"$", u"llon")

			c = f.create_transform(("pl", "All", g), ("s", "Nom", g))
			c.append_step(u"$", u"llar")

			c = f.create_transform(("pl", "Loc", g), ("s", "Nom", g))
			c.append_step(u"$", u"ssen")

			c = f.create_transform(("pl", "Instr", g), ("pl", "Dat", g))
			c.append_step(u"$", u"en")

			c = f.create_transform(("pl", "Resp", g), ("pl", "Dat", g))
			c.append_step(u"n$", u"s")

			c = f.create_transform(("d", "Nom", g), ("s", "Nom", g))
			c.append_step(u"$", u"t")

			c = f.create_transform(("d", "Gen", g), ("s", "Nom", g))
			c.append_step(u"$", u"to")

			c = f.create_transform(("d", "Poss", g), ("s", "Nom", g))
			c.append_step(u"$", u"twa")

			c = f.create_transform(("d", "Dat", g), ("s", "Nom", g))
			c.append_step(u"$", u"nt")

			c = f.create_transform(("d", "Abl", g), ("s", "Nom", g))
			c.append_step(u"$", u"lto")

			c = f.create_transform(("d", "All", g), ("s", "Nom", g))
			c.append_step(u"$", u"nta")

			c = f.create_transform(("d", "Loc", g), ("s", "Nom", g))
			c.append_step(u"$", u"tse")

			c = f.create_transform(("d", "Instr", g), ("s", "Nom", g))
			c.append_step(u"$", u"nten")

			c = f.create_transform(("d", "Resp", g), ("s", "Nom", g))
			c.append_step(u"$", u"tes")

		c = f.create_transform(("s", "Nom", "rel"), BASED_ON_ENTRY_FORM, u"a$")
		c.append_step(u"a$", u"alda")
		c = f.create_transform(("s", "Nom", "rel"), BASED_ON_ENTRY_FORM, u"e$")
		c.append_step(u"e$", u"ilda")
		c = f.create_transform(("s", "Nom", "rel"), BASED_ON_ENTRY_FORM, u"[ie]n$")
		c.append_step(u"(?<=[ie]n)$", u"ilda")

		add_grd("rel")

		c = f.create_transform(("s", "Nom", "abs"), BASED_ON_ENTRY_FORM, u"^[lmrs]")
		c.append_step(u"^([lmrs])", u"a\\1\\1")
		c = f.create_transform(("s", "Nom", "abs"), BASED_ON_ENTRY_FORM, u"^p")
		c.append_step(u"^", u"am")
		c = f.create_transform(("s", "Nom", "abs"), BASED_ON_ENTRY_FORM)
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
						for m in perm(symbols[:i] + symbols[i + 1:]):
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
		pers = CategoryFilter("in", ("s", "pl", "d"))
		pers_s = CategoryFilter("in", ("1s", "2s", "3s", "s"))
		pers_pl = CategoryFilter("in", ("1+2+3", "1+3", "2+3", "3pl", "pl"))
		pers_d = CategoryFilter("in", ("1d", "d"))


		def auto_noun_phrase(gr):
			for case in ("Nom", "Gen", "Poss", "Dat", "Loc", "Instr", "Resp"):
				for num in ("s", "d", "pl", "part"):
					if num == "part":
						gr[case] = WordCategoryFilter("n", (), (num, case, None)) + WordCategoryFilter("adj", (), ("pl", "Nom", None))
						gr[case] = WordCategoryFilter("adj", (), ("pl", "Nom", None)) + WordCategoryFilter("n", (), (num, case, None))
						gr[case] = WordCategoryFilter("n", (), (num, case, None))
					else:
						gr[case] = WordCategoryFilter("n", (), (num, "Nom", None)) + WordCategoryFilter("adj", (), (num, case, None))
						gr[case] = WordCategoryFilter("adj", (), (num, "Nom", None)) + WordCategoryFilter("n", (), (num, case, None))
						gr[case] = WordCategoryFilter("n", (), (num, case, None))

		def add_verb(gr, case, tr, nick):
			if case == "0":
				acc = "Acc"
			else:
				acc = "Acc+" + case
			if tr == "tr":
				n2 = ":"+acc
			else:
				n2 = ":"+case
			V = {}
			V[("intr", "V")] = WordCategoryFilter("v", (case,), (fin, pers, "0"))
			V[("tr", "V")] = WordCategoryFilter("v", (acc,), (fin, pers, "0"))
			V[("intr", "Vs")] = WordCategoryFilter("v", (case,), (fin, n0, "0"))
			V[("tr", "Vs")] = WordCategoryFilter("v", (acc,), (fin, n0, "0"))
			V[("tr", "Vso")] = WordCategoryFilter("v", (acc,), (fin, n0, n0))
			V[("intr", "V/s")] = WordCategoryFilter("v", (case,), (fin, "s", "0"))
			V[("intr", "V/p")] = WordCategoryFilter("v", (case,), (fin, "pl", "0"))
			V[("intr", "V/d")] = WordCategoryFilter("v", (case,), (fin, "d", "0"))
			V[("tr", "V/s")] = WordCategoryFilter("v", (acc,), (fin, "s", "0"))
			V[("tr", "V/p")] = WordCategoryFilter("v", (acc,), (fin, "pl", "0"))
			V[("tr", "V/d")] = WordCategoryFilter("v", (acc,), (fin, "d", "0"))
			gr[nick+n2] = V[(tr, nick)]

		gr["clause"] = (Reference("Vs") | Reference("SV")) + Reference("C") * KLEENE_CLOSURE
		gr["clause"] = (Reference("Vso") | Reference("VsO") | Reference("S V O")) + Reference("C") * KLEENE_CLOSURE
		gr["clause"] = (Reference("VsD") | Reference("SVD")) + Reference("C") * KLEENE_CLOSURE
		gr["clause"] = (Reference("VsoD") | Reference("VsOD") | Reference("S V OD")) + Reference("C") * KLEENE_CLOSURE
		add_verb(gr, "0", "intr", "Vs")
		gr["Vs"] = Reference("Vs:0")
		for pers in "spd":
			add_verb(gr, "0", "intr", "V/"+pers)
			gr["SV"] = free_order(Reference("S/"+pers), Reference("V/"+pers+":0"))
		add_verb(gr, "0", "tr", "Vso")
		gr["Vso"] = Reference("Vso:Acc")
		add_verb(gr, "0", "tr", "Vs")
		gr["VsO"] = free_order(Reference("Vs:Acc"), Reference("O"))
		for pers in "spd":
			add_verb(gr, "0", "tr", "V/"+pers)
			gr["S V O"] = Reference("S/"+pers) + Reference("V/"+pers+":Acc") + Reference("O")

		add_verb(gr, "Dat", "intr", "Vs")
		gr["VsD"] = free_order(Reference("Vs:Dat"), Reference("D"))
		add_verb(gr, "Dat", "intr", "V/s")
		gr["SVD"] = free_order(Reference("S/s"), Reference("V/s:Dat"), Reference("D"))
		for pers in "spd":
			add_verb(gr, "Dat", "intr", "V/"+pers)
			gr["SVD"] = Reference("S/"+pers) + Reference("V/"+pers+":Dat") + Reference("D")

		add_verb(gr, "Dat", "tr", "Vso")
		gr["VsoD"] = free_order(Reference("Vso:Acc+Dat"), Reference("D"))

		add_verb(gr, "Dat", "tr", "Vs")
		gr["VsOD"] = free_order(Reference("Vs:Acc+Dat"), Reference("O"), Reference("D"))

		for pers in "spd":
			add_verb(gr, "Dat", "tr", "V/"+pers)
			gr["S V OD"] = Reference("S/"+pers) +Reference("V/"+pers+":Acc+Dat") + free_order(Reference("O"), Reference("D"))


		gr["clause"] = (Reference("VsL") | Reference("SVL")) + Reference("C-L") * KLEENE_CLOSURE
		gr["clause"] = (Reference("VsoL") | Reference("VsOL") | Reference("S V OL")) + Reference("C-L") * KLEENE_CLOSURE

		add_verb(gr, "Loc", "intr", "Vs")
		gr["VsL"] = free_order(Reference("Vs:Loc"), Reference("L"))
		
		for pers in "spd":
			add_verb(gr, "Loc", "intr", "V/"+pers)
			gr["SVL"] = free_order(Reference("S/s"), Reference("V/"+pers+":Loc"), Reference("L"))
		

		add_verb(gr, "Loc", "tr", "Vso")
		gr["VsoL"] = free_order(Reference("Vso:Acc+Loc"), Reference("L"))
		add_verb(gr, "Loc", "tr", "Vs")
		gr["VsOL"] = free_order(Reference("Vs:Acc+Loc"), Reference("O"), Reference("L"))

		for pers in "spd":
			add_verb(gr, "Loc", "tr", "V/"+pers)
			gr["S V OL"] = Reference("S/"+pers) + Reference("V/"+pers+":Acc+Loc") + free_order(Reference("O"), Reference("L"))

		gr["clause"] = (Reference("N Vs") | Reference("S N V")) + Reference("C") * KLEENE_CLOSURE
		gr["clause"] = Reference("S N") + Reference("C") * KLEENE_CLOSURE

		gr["clause"] = (Reference("N DVs") | Reference("S N DV")) + Reference("C") * KLEENE_CLOSURE

		gr["V-s:Nom"] = WordCategoryFilter("v", ("Nom",), (fin, pers_s, "0"))
		gr["V-p:Nom"] = WordCategoryFilter("v", ("Nom",), (fin, pers_pl, "0"))
		gr["V-d:Nom"] = WordCategoryFilter("v", ("Nom",), (fin, pers_d, "0"))
		gr["N Vs"] = Reference("N/s") + Reference("V-s:Nom")
		gr["N Vs"] = Reference("N/p") + Reference("V-p:Nom")
		gr["N Vs"] = Reference("N/d") + Reference("V-d:Nom")


		for pers in "spd":
			add_verb(gr, "Nom", "intr", "V/"+pers)
			gr["S N V"] = Reference("S/s") + Reference("N/s") + Reference("V/"+pers+":Nom")
			
		gr["S N"] = Reference("S/s") + Reference("N/s")
		gr["S N"] = Reference("S/p") + Reference("N/p")
		gr["S N"] = Reference("S/d") + Reference("N/d")

		gr["V-s:Nom+Dat"] = WordCategoryFilter("v", ("Nom+Dat",), (fin, pers_s, "0"))
		gr["V-p:Nom+Dat"] = WordCategoryFilter("v", ("Nom+Dat",), (fin, pers_pl, "0"))
		gr["V-d:Nom+Dat"] = WordCategoryFilter("v", ("Nom+Dat",), (fin, pers_d, "0"))
		gr["N DVs"] = Reference("N/s") + free_order(Reference("D"), Reference("V-s:Nom+Dat"))
		gr["N DVs"] = Reference("N/p") + free_order(Reference("D"), Reference("V-p:Nom+Dat"))
		gr["N DVs"] = Reference("N/d") + free_order(Reference("D"), Reference("V-d:Nom+Dat"))

		for pers in "spd":
			add_verb(gr, "Nom+Dat", "intr", "V/"+pers)
			gr["S N DV"] = Reference("S/s") + Reference("N/s") + free_order(Reference("D"), Reference("V/"+pers+":Nom+Dat"))

		gr["N/s"] = WordCategoryFilter("adj", (), ("s", "Nom", None)) | (Reference("article") * OPTIONAL_CLOSURE + Reference("Nom/s"))
		gr["N/p"] = WordCategoryFilter("adj", (), ("pl", "Nom", None)) | (Reference("article") * OPTIONAL_CLOSURE + Reference("Nom/p"))
		gr["N/d"] = WordCategoryFilter("adj", (), ("d", "Nom", None)) | (Reference("article") * OPTIONAL_CLOSURE + Reference("Nom/d"))

		gr["O"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Nom") + Reference("nC") * KLEENE_CLOSURE
		gr["D"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Dat") + Reference("nC") * KLEENE_CLOSURE
		gr["S/s"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Nom/s") + Reference("nC") * KLEENE_CLOSURE
		gr["S/p"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Nom/p") + Reference("nC") * KLEENE_CLOSURE
		gr["S/d"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Nom/d") + Reference("nC") * KLEENE_CLOSURE

		gr["Nom/s"] = free_order(WordCategoryFilter("n", (), ("s", "Nom", None)), WordCategoryFilter("adj", (), ("s", "Nom", None)))
		gr["Nom/s"] = WordCategoryFilter("n", (), ("s", "Nom", None))
		gr["Nom/d"] = free_order(WordCategoryFilter("n", (), ("d", "Nom", None)), WordCategoryFilter("adj", (), ("d", "Nom", None)))
		gr["Nom/d"] = WordCategoryFilter("n", (), ("d", "Nom", None))
		gr["Nom/p"] = free_order(WordCategoryFilter("n", (), ("pl", "Nom", None)), WordCategoryFilter("adj", (), ("pl", "Nom", None)))
		gr["Nom/p"] = WordCategoryFilter("n", (), ("pl", "Nom", None))
		gr["Nom/p"] = free_order(WordCategoryFilter("n", (), ("part", "Nom", None)), WordCategoryFilter("adj", (), ("pl", "Nom", None)))
		gr["Nom/p"] = WordCategoryFilter("n", (), ("part", "Nom", None))
		gr["article"] = WordFilter(Word(u"i", Particle(u"i", 1, "adj")))

		gr["nC"] = Reference("P") | Reference("G")
		gr["P"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Poss")
		gr["G"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Gen")
		gr["C"] = Reference("adverb") | Reference("I") | Reference("L")
		gr["C-L"] = Reference("adverb") | Reference("I")
		gr["L"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Loc")
		gr["I"] = Reference("article") * OPTIONAL_CLOSURE + Reference("Instr")
		gr["adverb"] = WordCategoryFilter("adv")
		auto_noun_phrase(gr)


	def nouns():
		d = []
		d.append((u"cas", u"cár", "cesi")) #head
		d.append((u"cumbo", u"cumbo", "fucesi")) #belly
		d.append((u"hon", u"hón", "kawcesi")) #heart
		d.append((u"esse", u"esse", "tedapemi", [(u"essi", ("pl", "Nom", "0"))])) #name
		d.append((u"þambe", u"þambe", "depi")) #room
		d.append((u"card", u"car", "byekigi")) #building
		d.append((u"telme", u"telme", "bidetavi")) #blanket
		d.append((u"limpe", u"limpe", "zoyfupi")) #spirits
		#d.append(  (u"0", u"síra", "bape-tovay") ) #today
		d.append((u"sovaþamb", u"sovaþan", "bodepi")) #restroom
		d.append((u"lindale", u"lindale", "dinjami")) #music
		d.append((u"hampe", u"hampe", "byetavi")) #garment
		d.append((u"tecil", u"tecil", "bofifusi")) #pen
		d.append((u"hríve", u"hríve", "cayfemi")) #winter
		d.append((u"laire", u"laire", "fefemi")) #summer
		d.append((u"henets", u"henet", "kifigi", [(u"henetwa", ("s", "Poss", "0"))])) #window
		d.append((u"rancu", u"ranco", "twecesi")) #arm
		d.append((u"ñonwa", u"ñonwa", "kobisi")) #computer
		d.append((u"palancen", u"palancen", "kifabisi")) #television
		d.append((u"asta", u"asta", "ketovi")) #month
		d.append((u"ñolyasse", u"ñolyasse", "kokigi")) #school
		d.append((u"ner", u"nér", "loybegi")) #man
		d.append((u"niss", u"nís", "lawbegi")) #woman
		d.append((u"híni", u"hína", "fobegi", [(u"híni", ("pl", "Nom", "0"))]))#child
		d.append((u"huo", u"huo", "zovi")) #dog
		d.append((u"yaule", u"yaule", "kwizovi")) #cat
		d.append((u"aiwe", u"aiwe", "byedami")) #bird
		d.append((u"lingwi", u"lingwe", "byebomi")) #fish
		d.append((u"mas", u"mar", "kigi")) #house
		d.append((u"yaxe", u"yaxe", "lawfutigi")) #cow
		d.append((u"ilim", u"ilin", "bazopi")) #milk
		d.append((u"massa", u"massa", "josi")) #bread
		d.append((u"norolle", u"norolle", "timi")) #car
		d.append((u"ori", u"ore", "cindonfupi")) #rice-grain
		d.append((u"vinya", u"vinya", "dawkemo")) #new
		d.append((u"orva", u"orva", "zobemi")) #apple
		d.append((u"apsa", u"apsa", "fayzopi")) #meat
		d.append((u"celva", u"celva", "byefasi")) #animal
		d.append((u"quen", u"quén", "begi")) #person
		d.append((u"hanta", u"hanta", "xentegemu")) #thank you
		d.append((u"nen", u"nén", "bocivi")) #water
		d.append((u"telco", u"telco", "jicesi", [(u"telqui", ("pl", "Nom", "0"))])) #leg
		d.append((u"polca", u"polca", "jotigi")) #pig
		d.append((u"meldo", u"meldo", "zoyzevi")) #friend
		d.append((u"ear", u"ear", "kebivi")) #sea
		d.append((u"malle", u"malle", "zegi", [(u"maller", ("pl", "Nom", "0"))]))#road
		d.append((u"caima", u"caima", "kunjisi")) #bed
		d.append((u"telpe", u"telpe", "jafimi")) #money
		d.append((u"ando", u"ando", "tifigi")) #door
		d.append((u"tyurd", u"tyur", "caybafupi")) #cheese
		d.append((u"palallon", u"palallon", "tebisi")) #telphone
		d.append((u"lómi", u"lóme", "kunfemi")) #night
		d.append((u"miriand", u"mirian", "cayjafimi")) #coin
		d.append((u"toron", u"toron", "zutasaw", [(u"torno", ("s", "Gen", "0"))])) #brother
		d.append((u"alda", u"alda", "jigi")) #tree
		d.append((u"amill", u"amil", "ditasaw")) #mother
		d.append((u"elen", u"elen", "kitisi")) #star
		d.append((u"filic", u"filit", "byedami")) #bird (little)
		d.append((u"sell", u"seler", "zitasaw", [(u"selerwa", ("s", "Poss", "0")), (u"selernen", ("s", "Instr", "0"))]))
		d.append((u"atar", u"atar", "dutasaw")) #father
		d.append((u"tie", u"tie", "zuzegi")) #path
		d.append((u"máqua", u"máqua", "zicesi")) #hand
		d.append((u"tal", u"tál", "cucesi", [(u"talan", ("s", "Dat", "0")), (u"talain", ("pl", "Dat", "0"))]))#foot
		d.append((u"toll", u"tol", "ketisi", [(u"tollon", ("s", "Dat", "0")), (u"tolloin", ("pl", "Dat", "0"))]))#island
		d.append((u"ráv", u"rá", "xozovi")) #lion
		d.append((u"raine", u"raine", "baxasoni")) #peace
		d.append((u"cos", u"cor", "bizozugi")) #war
		d.append((u"coa", u"coa", "kigi", [(u"có", ("s", "Gen", "0")), (u"coava", ("s", "Poss", "0"))]))#house
		d.append((u"mas", u"mar", "kwicalaymi", [], 2)) #home
		d.append((u"nelc", u"nelet", "futevi", [(u"neletse", ("s", "Loc", "0"))])) #tooth
		d.append((u"hend", u"hen", "kicesi")) #eye
		d.append((u"pé", u"pé", "teduncesi", [(u"péu", ("d", "Nom", "0")), (u"pein", ("pl", "Dat", "0"))])) #lip
		d.append((u"lar", u"lár", "foycesi", [(u"laru", ("d", "Nom", "0"))])) #ear
		d.append((u"fiond", u"fion", "bedami")) #hawk
		d.append((u"ré", u"ré", "tovi", [(u"rein", ("pl", "Dat", "0"))])) #24hours
		d.append((u"pí", u"pí", "byekagi", [(u"pín", ("pl", "Dat", "0"))])) #insect
		d.append((u"oxi", u"ohte", "docesi")) #egg
		d.append((u"lasse", u"lasse", "boybemi")) #leaf

		d.append((u"ambar", u"ambar", "jotisi")) #planet, world
		d.append((u"istar", u"istar", "joybegi", [(u"istari", ("pl", "Nom", "0"))])) #doctor, wizard

		d.append((u"Cemen", u"Cemen", "Ladijotisi")) #earth
		d.append((u"Anar", u"Anar", "Lakitisi")) #sun
		d.append((u"Vintamurta", u"Vintamurta", "Laryoxodugi")) #New York City
		d.append((u"Colindor", u"Colindor", "Ladyadugi")) #India
		d.append((u"Hindien", u"Hindien", "Ladyadugi")) #India
		d.append((u"Yúlanor", u"Yúlanor", "Lazidugi")) #Brazil
		d.append((u"Vandanor", u"Vandanor", "Larudugi")) #Russia
		d.append((u"Canata", u"Canata", "Lakadugi")) #Canada
		d.append((u"Nigird", u"Nigir", "Lajidugi")) #Nigeria
		d.append((u"Tyena", u"Tyena", "Lacundugi")) #China
		d.append((u"Forméro", u"Forméro", "Lacunxodugi")) #Peking
		d.append((u"Tenótiþan", u"Mésicosto", "Laxixodugi")) #Mexico City
		d.append((u"Tollilónar", u"Mumba", "Labunxodugi")) #Bombay
		d.append((u"Ainapityonosto", u"Ainapityonosto", "Lapawxodugi")) #São Paulo
		d.append((u"Orear", u"Orear", "Lazanxodugi")) #Shanghai
		d.append((u"Mosiqua", u"Mosiqua", "Laruxodugi")) #Moscow
		d.append((u"Iþil", u"Iþil", "Labatisi")) #moon
		d.append((u"kuiveyulda", u"kuiveyulda", "cafefupi")) #coffee
		d.append((u"wilyacirya", u"wilyacirya", "datimi")) #airplane
		d.append((u"wilyahopasse", u"wilyahopasse", "dakigi")) #airport
		d.append((u"sarno", u"sarno", "bujisi")) #table
		d.append((u"yáve", u"yáve", "babemi")) #fruit (a -)
		d.append((u"olpe", u"olpe", "finzipi")) #bottle
		d.append((u"angatea", u"angatea", "kuzegi")) #railroad
		d.append((u"lambe", u"lambe", "tejami")) #language
		d.append((u"quetta", u"quetta", "tekusi")) #word
		d.append((u"tów", u"tó", "twazopi")) #wool
		d.append((u"þúri", u"þúre", "dafepi")) #wind

		d.append((u"varind", u"varin", "byukigi"))  #hotel, inn, hospice, roadhouse
		#d.append( (u"norolle liéva", u"norolle liéva", "zetimi") ) #bus
		#d.append( (u"...", u"...", "jatimi") )  #taxi/taxicab
		d.append((u"caimasse", u"caimasse", "bijoykigi"))  #hospital
		#d.append( (u"...", u"...", "xetimi") )  #bicycle
		#d.append( (u"norolle angaina", "norolle angaina", u"kuzetimi") ) #train
		d.append((u"asto", u"asto", "fawfimi"))  #garbage, rubbish, waste
		d.append((u"matasse", u"matasse", "fukigi"))  #restaurant, eatery, eating house
		d.append((u"colca", u"colca", "titwazipi"))  #suitcase, valise, portmanteau, trunk
		#d.append(  Periphrase(g["noun"], "i Ertaini Nóri") , "Lacodugi") #United States
		d.append((u"aure", u"aure", "kifemi"))  #day(time), daylight hours


		return d


	def verbs():
		d = []
		d.append((u"na", "Nom", "dapa", [(u"ne", ("past", "s", "0"))]))
		d.append((u"ea", "0", "kava", [(u"ea", ("pres", "s", "0")), (u"engie", ("perf", "s", "0")), (u"enge", ("past", "s", "0"))]))  #esserci(?)
		d.append((u"ea", "Loc", "zoga", [(u"ea", ("pres", "s", "0")), (u"engie", ("perf", "s", "0")), (u"enge", ("past", "s", "0"))], 2)) #trovarsi

		d.append((u"cen", "Acc", "kiva"))
		d.append((u"mel", "Acc", "bakopa"))  #love
		d.append((u"mat", "0", "fucala")) #eat
		d.append((u"suc", "0", "bofucala")) #drink
		d.append((u"ista", "Acc", "kopa", [(u"sinte", ("past", "s", "0")), (u"isintie", ("perf", "s", "0")), (u"sinwa", ("pass-part", "0", "0"))]))
		d.append((u"lelya", "0", "ticala", [(u"lende", ("past", "s", "0"))]))
		d.append((u"ulya", "Acc", "tibokavasa", [], 1))
		d.append((u"ulya", "0", "tibokava", [], 2))
		d.append((u"mar", "0", "kwicala", [(u"ambárie", ("perf", "s", "0"))]))
		d.append((u"móta", "0", "bucala")) #work
		d.append((u"tyal", "0", "dwecala")) #play
		d.append((u"canta", "Acc", "joykavapa")) #fix
		d.append((u"rac", "Acc", "joyjuvapa")) #break
		d.append((u"nyar", "Acc+Dat", "tega")) #tell
		d.append((u"quet", "Dat", "tegapa", [(u"equétie", ("perf", "s", "0"))])) #speak to
		d.append((u"mala", "0", "xonkepa")) #suffer
		d.append((u"lor", "0", "kunkepa")) #sleep
		d.append((u"mer", "Acc", "cakopa")) #want
		d.append((u"appa", "Acc", "kenbusa")) #touch
		d.append((u"anta", "Acc+Dat", "ximamba", [(u"áne", ("past", "s", "0"))]))  #give
		d.append((u"yuhta", "Acc", "busasa")) #use, control
		d.append((u"lanta", u"0", "dafagupa")) #fall
		d.append((u"sam", u"Acc", "ximunza", [(u"sáme", ("past", "s", "0"))]))  #have
		d.append((u"ten", "0", "zogipa"))  #arrive
		d.append((u"ten", "Loc", "zogimba", [], 2))  #arrive at
		d.append((u"um", "Nom", "jutamu dapa", [(u"úma", ("pres", "s", "0")), (u"úme", ("past", "s", "0")), (u"úmie", ("perf", "s", "0")), (u"úva", ("fut", "s", "0"))])) #not be
		d.append((u"um", "Inf", "jutamu", [(u"úma", ("pres", "s", "0")), (u"úme", ("past", "s", "0")), (u"úmie", ("perf", "s", "0")), (u"úva", ("fut", "s", "0"))], 2))  #not
		d.append((u"pol", "Inf", "dovu"))  #can


		return d


	def adjs():
		d = []
		d.append((u"sina", "baso")) #this
		d.append((u"tana", "zaso")) #that
		d.append((u"alwa", "joykepo")) #healthy
		d.append((u"ulca", "cafomo", [(u"ulda", ("s", "Nom", "rel"))])) #bad, evil
		d.append((u"pitya", "fomo")) #small
		d.append((u"alta", "kemo")) #big
		d.append((u"yára", "zonculo")) #old (vs.young)
		d.append((u"silque", "cinzigo")) #white
		d.append((u"more", "kunzigo")) #black
		d.append((u"neþþa", "zondelo")) #young
		d.append((u"carne", "zozigo")) #red
		d.append((u"yerna", "dawfomo")) #old (vs.new)
		d.append((u"luin", "dazigo")) #blue
		d.append((u"malina", "fezigo")) #yellow
		d.append((u"hlaiwa", "joykolo")) #sick
		d.append((u"lauca", "feculo")) #warm
		d.append((u"ringa", "fedelo")) #cold
		d.append((u"vanya", "kekaykemo", [(u"valda", ("s", "Nom", "rel")), (u"ambanya", ("s", "Nom", "abs"))]))   #beautiful
		d.append((u"muhtea", "cinjuvo"))   #dirty
		d.append((u"laurea", "todapyu taykocivo")) #golden
		d.append((u"ilya", "bikavo")) #all, whole
		d.append((u"mára", "cakemo",  [(u"melda", ("s", "Nom", "rel"))], 1)) #good
		d.append((u"mára", "zoykopa",  [(u"melda", ("s", "Nom", "rel"))], 2, ("Dat",))) #like
		return d

	def adv():
		d = []
		d.append((u"ehtala", "dipe-tovay")) #tomorrow
		d.append((u"bape", "bape")) #now
		d.append((u"lá", "jutamu")) #not
		return d

	l = Lect(u"qya")
	l.name = u"Quenya"
	l.english_name = "Neo-Quenya"
	l.append_p_o_s("v", ("arguments",), ("tense", "person", "object person"))
	l.append_p_o_s("n", (), ("number", "case", "person"))
	l.append_p_o_s("adj", ("arguments",), ("number", "case", "degree"))
	l.append_p_o_s("adv", (), ())
	l.append_p_o_s("prep", ("argument",), ("object person",))
	build_inflections(l.inflections)
	build_lexicon(l.lexicon, l.inflections)
	print str(l.lexicon)
	build_grammar(l.grammar)
	l.properties["capitalization"] = 2 #lexical
	l.properties["separator"] = u" " #lexical
	l.save("trunk/src/data/qya.lct")
	print "now compiling"
	l.compile()
	print "compiled"
	show(u"melin fion ringa")
	show(u"cor vanya mele i lauca alda")
	show(u"melin lóme")
	show(u"lantar laurie lassi þúrinen")
	show(u"nér nan")
	show(u"yerna nan")
	#lome = l.read(u"melin lóme")[0].subtree(('nucleus', 'Vs O', 'O', 'noun-phrase,Nom', 'noun-phrase,s,Nom', 'n'))
	#for i in lome.iter_items():
	#	print i.form
	#for w in l.lexicon.find_words(None, (u"lasse",1), (CategoryFilter("in",("s","pl")), None, "0")):
	#	print " ".join(w.categories),":", w.form


if __name__ == "__main__":
	run()


