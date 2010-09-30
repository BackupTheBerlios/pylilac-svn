#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Unit test for C{pylilac.core.fsa}.


@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.fsa import *


def run():
	def add_token(fsa, str):
		s = str + " "
		for i, c in enumerate(s):
			if i == len(s) - 1:
				fsa.add_transition(s[:i], c, fsa.get_initial(), str)
				break
			else:
				fsa.add_transition(s[:i], c, s[:i+1])

	def tokenize(parser, dict, stream):
		def explode_list(dict, lst, pos):
			t = OptionTree()
			if pos < len(lst):
				for obj in dict[lst[pos]]:
					c = explode_list(dict, lst, pos + 1)		
					c.element = obj
					t.append(c)
			return t
		p = parser(stream + " ")
		ot = OptionTree()
		for u in p.expand():
			ot.append(explode_list(dict, [y[1] for y in u if y[1] is not None], 0))
		return ot
		

	#accepts e|a(a|b)*b
	eaabb = FSA()
	eaabb.add_transition(0, EPSILON, 2, None)
	eaabb.set_final(2)
	eaabb.add_transition(0, 'a', 1, None)
	eaabb.add_transition(1, 'a', 1, None)
	eaabb.add_transition(1, EPSILON, 3, None)
	eaabb.add_transition(3, 'b', 1, None)
	eaabb.add_transition(3, 'b', 2, None)
	print eaabb
	print eaabb.reduced()
	print eaabb.reduced().minimized()
	
	d = {"a": ["A"], "b": ["B"], "ab": ["AB"], "cab": ["CAB"]}	
	td = FSA()
	td.add_state("")
	td.set_initial("")
	td.add_transition("", "a", "a")
	td.add_transition("a", EPSILON, "a*", "a")
	td.set_final("a*")
	td.add_transition("", "b", "b")
	td.add_transition("b", EPSILON, "b*", "b")
	td.set_final("b*")
	td.add_transition("", "a", "a")
	td.add_transition("a", "b", "ab")
	td.add_transition("ab", EPSILON, "ab*", "ab")
	td.set_final("ab*")
	td.add_transition("", "c", "c")
	td.add_transition("c", "a", "ca")
	td.add_transition("ca", "b", "cab")
	td.add_transition("cab", EPSILON, "cab*", "cab")
	td.set_final("cab*")
	print td
	print td.reduced()
	print td.reduced().minimized()

	f = FSA() #vi, vivo, vi do
	f.add_state("")
	f.set_initial("")
	f.set_final("")


	add_token(f, "vi")
	add_token(f, "vivo")

	add_token(f, "do")
	add_token(f, "vi do")

	r = f.reduced()
	p = Parser(r)

	d = {"vi":["vi1", "vi2"], "do":["do1","do2","do3"], "vi do": ["vi do"]}

	print tokenize(p, d, "vi do")
	
	k = r.copy()
	
	#Quenya Locative bug ()
	"""
	FSA{
	>0, 1>, 2, 3, 4, 5.
	0 -> 2 'Noun' ();
	0 -> 4 'Pronoun' ();
	2 -> 3 'Verb' ('VO',);
	3 -> 1 'Object' ('VO',);
	4 -> 5 'Verb' ('VO',);
	5 -> 1 'Object' ('VO',)
	}
	
	Adjacency dict:
	[('Pronoun', 4, ()), ('Noun', 2, ())]: [0]
	[('Object', 1, ('VO',))]: [3, 5]
	[('Verb', 5, ('VO',))]: [4]
	[('Verb', 3, ('VO',))]: [2]
	[EXIT] : [1]
	CORRECT
	
	Class leaders: 0, 3, 4, 2, 1
	CORRECT
	
	initial state: 0
	
	"""
	loc = FSA()
	loc.add_state(0)
	loc.set_initial(0)
	loc.add_transition(0, "Noun", 2,  ( ))
	loc.add_transition(0, "Pronoun", 4,  ( ))
	loc.add_transition(2, "Verb", 3,  ("VO", ))
	loc.add_transition(3, "Object", 1,  ("VO", ))
	loc.add_transition(4, "Verb", 5,  ("VO", ))
	loc.add_transition(5, "Object", 1, ("VO", ))
	loc.set_final(1)
	print loc.minimized()
	assert loc.minimized().is_minimized(),  "Locative bug"
	


if __name__ == "__main__":
	run()
