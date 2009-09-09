#!/usr/bin.run()thon

"""
Unit tests.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "pytext en"

import core.bnf as bnf
import core.expression as expression
import core.fsa as fsa
import core.grammar as grammar
import core.interlingua as interlingua
import core.inflection as inflection
import core.lect as lect
import core.lexicon as lexicon
import core.optiontree as optiontree
import core.tokenizer as tokenizer
import core.utilities as utilities

def run():
	bnf.run()
	expression.run()
	fsa.run()
	inflection.run()
	interlingua.run()
	lect.run()
	lexicon.run()
	optiontree.run()
	tokenizer.run()
	utilities.run()
	grammar.run()
