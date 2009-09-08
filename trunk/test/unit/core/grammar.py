#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.grammar import *
from pylilac.core.bnf import *



def run():
	g = Grammar("Recurse")
	g.ignore_recursion = True
	g["SV"] = Reference("S") + Reference("V")
	g["V"] = Literal(u"verb")
	g["S"] =  Reference("S2") * KLEENE_CLOSURE
	g["S2"] =  Literal(u"stop")
	#g["S2"] =  Reference("S3") | Reference("S2")
	#g["S3"] =Reference("S4") | Reference("S3")
	#g["S4"] = Literal(u"noun")
	print `g`
	print g.browse()
	p = g.compile()
	print repr(p)
	#print p([u"noun",u"noun",u"verb"])
	#print p([u"noun",u"noun",u"noun",u"noun",u"stop",u"verb"])


if __name__ == "__main__":
	run()

