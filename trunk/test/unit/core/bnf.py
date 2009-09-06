#!/usr/bin/python
# -*- coding: utf-8 -*-


from pylilac.core.bnf import *


def run():
	_if = Literal("if")
	_condition = Reference("condition")
	_then = Literal("then")
	_stmt = Reference("statement")
	_else = Literal("else")
	print _if + _then + _else
	s = _if + _condition + _then + _stmt
	s |= s + _else + _stmt
	print s
	print
	ns = Literal("north")|Literal("south")
	print ns+(Literal("east")|Literal("west"))
	print ns+ns+ns
	print ns|ns
	print (Literal("north")|Literal("south"))+Literal("east")
	print Literal("south")+(Literal("east")|Literal("west"))
	print EPSILON_SYMBOL
	print EPSILON_SYMBOL | Literal("a") + Literal("b"), "= ab|0"
	print Literal("a") + Literal("b") | EPSILON_SYMBOL  , "= ab|0"
	print Literal("a") + (Literal("b") | Literal("b")) + EPSILON_SYMBOL == Literal("a") + Literal("b")
	print Literal("a") | Literal("a") | EPSILON_SYMBOL == Literal("a")

	a_k=Reference("a")*KLEENE_CLOSURE
	print a_k, "*"
	a_p = Reference("a")*POSITIVE_CLOSURE
	print a_p, "+"
	a_o = Reference("a")*OPTIONAL_CLOSURE
	print a_o, "?"

	print _else.match("else")

	
	#x = Literal("kk") | Reference("s") + s
	#x = s | Literal("null")
	#print x
	
if __name__ == "__main__":
	run()

