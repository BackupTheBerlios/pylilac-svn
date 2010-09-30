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
	g["SV"] = Reference("S") + Reference("V")
	g["V"] = Literal(u"verb")
	g["S"] =   Literal(u"noun") | Reference("S2")
	g["S2"] =  Literal(u"subnoun")
	print `g`
	print g.browse()
	p = g.compile()
	print repr(p)
	#print p([u"noun",u"noun",u"noun",u"noun",u"stop",u"verb"])


if __name__ == "__main__":
	run()

