#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PyLilac Poject
==============

U{http://pylilac.berlios.de}

G{packagetree core.lect,core.lexicon,core.grammar,core.inflection}

G{importgraph core.lect,core.lexicon,core.grammar,core.inflection}

G{classtree core.lect.Lect,core.lexicon.Lexicon,core.grammar.Grammar,core.inflection.Inflections}

G{callgraph core.grammar.Grammar.compile}

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""


# General info
__version__ = "0.4"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

from ui.la import LAApp

def run_la():
	app = LAApp(0)
	app.MainLoop()

if __name__ == "__main__":
	run_la()
