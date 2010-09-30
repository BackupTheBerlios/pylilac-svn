#!/usr/bin/python

"""
Unit for no regression.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "pytext en"

import unittest

import unit.core.bnf as bnf
import unit.core.expression as expression
import unit.core.fsa as fsa
import unit.core.grammar as grammar
import unit.core.interlingua as interlingua
import unit.core.inflection as inflection
import unit.core.lect as lect
import unit.core.lexicon as lexicon
import unit.core.optiontree as optiontree
import unit.core.tokenizer as tokenizer
import unit.core.utilities as utilities

class NoRegressionRoutine(unittest.TestCase):
    def setUp(self):
        pass

    def test_core(self):
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

if __name__ == '__main__':
    unittest.main()

