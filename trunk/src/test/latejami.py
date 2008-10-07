#!/usr/bin/python

"""
A module to create Latejami lect file.
"""

from core.lect import Lect
from core.grammar import Grammar
from core.bnf import Reference, POSITIVE_CLOSURE, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from core.lexicon import Lexicon, Particle, Word, Lemma
from core.wordfilter import WordCategoryFilter, WordFilter, CategoryFilter
from core.interlingua import Interlingua, Concept

def run():
	def show(s):
		print
		print s
		for i, x in enumerate(l.read(s)):
			print "%d. " % i, x

	w = build_words()

	l = Lect("ltj")
	l.name = "Latejami"
	p_o_s = ["N", "V", "A", "D", "C"]
	arg_struct = ["0-n"]
	arg_struct += [(a + f + "-" + d) for a in ("P", "AP", "A/P") for f in ("", "/F") for d in ("s","d")]
	arg_struct += [(a + "-" + d) for a in ("F", "F/P") for d in ("s", "d")]
	for p in p_o_s:
		l.append_p_o_s(p, ("argument-structure",))
	l.lexicon = build_lexicon(w, l.properties)
	l.grammar = build_grammar(w)
	l.properties["capitalization"] = 2 #Only lexical
	print l.grammar
	l.save("test/ltj.lg")
	

	show("kokwacala kokwabegi")
	print l.lexicon.check(l)
	
def build_word(w0):
	if (w0[2] == "V" or w0[2] == "D") and w0[4] == "0-n":
		return Particle(w0[0], w0[1], w0[2])
	else:		
		return Word(w0[0], Lemma(w0[0], w0[1], w0[2], (w0[4],), w0[3]))

def build_words():
	w = {}
	ltj = Interlingua("Latejami")
	ltj.load("data/Latejami.ilt")
	
	for t in ltj.taxonomy:
		w[t.interlingua] = (t.interlingua, 1, t.p_o_s, t.interlingua, t.arg_struct)
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
	g["open-noun"] = WordCategoryFilter("N", {"argument-structure": CategoryFilter("in", ["P/F-s"])})
	g["adjective"] = WordCategoryFilter("A")
	g["open-adjective"] = WordCategoryFilter("A", {"argument-structure": CategoryFilter("in", ["P/F-s"])})
	g["verb"] = WordCategoryFilter("V")
	g["adverb"] = WordCategoryFilter("D")
	g["case-tag"] = WordCategoryFilter("D", {"argument-structure": CategoryFilter("in", ["P/F-s","P/F-d"])})
	g["disjunct"] = WordCategoryFilter("D", {"argument-structure": CategoryFilter("in", ["P/F-s","P/F-d"])})
	g["vocative-noun-phrase"] =  WordCategoryFilter("N", {"suffix": CategoryFilter("in", ["-we"])})
	g["heavy-topicalization-particle"] = WordFilter(build_word(w["xojopa"])) 
	g["reference-switching-particle"] = WordFilter(build_word(w["zunjopa"]))
	g["valency-terminator"] = WordFilter(build_word(w["jojope"]))


	g.compile(True)
	
	return g

if __name__ == "__main__":
	run()
