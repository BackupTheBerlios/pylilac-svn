#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to create Latejami lect file.
"""

from pylilac.core.lect import Lect
from pylilac.core.grammar import Grammar
from pylilac.core.bnf import Reference, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from pylilac.core.lexicon import Lexicon, Particle, Word, Lexeme, WordCategoryFilter, WordFilter, CategoryFilter
from pylilac.core.interlingua import Interlingua

def run():
	def show(s):
		print
		print s
		for i, x in enumerate(l.read(s)):
			print "%d. " % i, x

	w = build_words()

	l = Lect("ltq")
	l.name = u"Latejami"
	l.english_name = u"Latejami"
	l.append_p_o_s(u"V", ("argument-structure",), ())
	l.append_p_o_s(u"N", ("argument-structure",), ())
	l.append_p_o_s(u"A", ("argument-structure",), ())
	l.append_p_o_s(u"D", ("argument-structure",), ())
	l.append_p_o_s(u"C", ("argument-structure",), ())

	l.lexicon = build_lexicon(w, l.properties)
	l.grammar = build_grammar(w)
	l.properties["capitalization"] = 2 #Only lexical
	print repr(l.grammar)
	print l.lexicon
	l.save("data/ltq.lct", True)


	show(u"kokwacala kokwabegi")
	print l.lexicon._check(l)

def build_word(w0):
	if (w0[2] == "V" or w0[2] == "D") and w0[4] == "0-n":
		return Word(w0[0], Particle(w0[0], w0[1],  w0[2], (w0[4],)), ())
	else:		
		return Word(w0[0], Lexeme(w0[0], w0[1], w0[2], (w0[4],), w0[3]))

def build_words():
	w = {}
	ltj = Interlingua("trunk/src/data/Latejami.csv")
	ltj.load()

	for t in ltj.taxonomy:
		w[t.interlingua] = (unicode(t.interlingua), 1, t.p_o_s, t.interlingua, t.arg_struct)
	return w

def build_lexicon(w, props):
	lx = Lexicon()

	for w0 in w.values():	
		lx.add_word(build_word(w0))
	lx.compile(props)
	return lx

def build_grammar(w):
	"""
	Latejami grammar:

	"""
	g = Grammar("Latejami")

	g["sentence"] = Reference("topic") * OPTIONAL_CLOSURE + Reference("clause") | Reference("vocative-noun-phrase")


	g["topic"] = Reference("topic-particle") + Reference("argument")


	g["topic-particle"] = Reference("heavy-topicalization-particle") | Reference("reference-switching-particle")


	g["clause"] = Reference("disjunct") * KLEENE_CLOSURE + Reference("verb") + Reference("argument") * KLEENE_CLOSURE + Reference("valency-terminator") * OPTIONAL_CLOSURE


	g["argument"] = Reference("expression") | Reference("oblique-argument")


	g["oblique-argument"] = Reference("adverb") | Reference("case-tag") + Reference("expression")


	g["expression"] = Reference("noun-phrase") | Reference("clause")


	g["noun-phrase"] = Reference("noun") + Reference("noun-modifier") * KLEENE_CLOSURE
	g["noun-phrase"] = Reference("open-noun") + Reference("noun-modifier") * KLEENE_CLOSURE + Reference("expression")


	g["noun-modifier"] = Reference("light-modifier") | Reference("heavy-modifier")


	g["light-modifier"] = Reference("adjective")


	g["heavy-modifier"] = Reference("open-adjective") + Reference("expression")

	g["noun"] = WordCategoryFilter("N")
	g["open-noun"] = WordCategoryFilter("N", (CategoryFilter("in", ["P/F-s"]),))
	g["adjective"] = WordCategoryFilter("A")
	g["open-adjective"] = WordCategoryFilter("A", (CategoryFilter("in", ["P/F-s"]),))
	g["verb"] = WordCategoryFilter("V")
	g["adverb"] = WordCategoryFilter("D")
	g["case-tag"] = WordCategoryFilter("D", (CategoryFilter("in", ["P/F-s","P/F-d"]),))
	g["disjunct"] = WordCategoryFilter("D", (CategoryFilter("in", ["P/F-s","P/F-d"]),))
	g["vocative-noun-phrase"] =  WordCategoryFilter("N", (CategoryFilter("in", ["-we"]),))#????
	g["heavy-topicalization-particle"] = WordFilter(build_word(w["xojopa"]))
	g["reference-switching-particle"] = WordFilter(build_word(w["zunjopa"]))
	g["valency-terminator"] = WordFilter(build_word(w["jojope"]))
	g.compile(True)

	return g

if __name__ == "__main__":
	run()

