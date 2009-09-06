#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The PYthon LInguistic Laboratory (pylilac) is a Python library and a set of tools to help in studying, analyzing and engineering languages.
In the initial study of a natural or constructed language, the need for a framework to store the language characteristics may rise.
In particular when studying several languages, it can be useful a tool to bring the study to a I{normalized} form, to highlight the things in common with other languages.
PyLilac wants to provide a library and a set of tools to study, analyze and engineer languages as composed by:
	- A lexicon
	- An inflective system
	- A grammar
When exposed to a new language, the user will be able to describe it and, later on, he will be able to browse through the schema they have built.
On the other hand, another user will be able to open the same file and to explore the language prepared by someone else.
They both will be going to use a graphical interface tool to work with the data.
Eventually, a third user might want to develop a linguistic software (for training purpose, documentation, study and so on) and he will be going to use the library directly.

Structure
=========

G{packagetree pylilac}

G{importgraph core}

The library is contained in the L{pylilac.core} package, while the implementation of tools is in the L{pylilac.ui} 

@summary: The pylilac project.
@see: U{BerliOS<http://pylilac.berlios.de>} project site.
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.5
"""

__docformat__ = "epytext en"

from ui.la import LAApp

def run_la():
	"""
	Run the Language Architect GUI.
	@see: U{Graphical User documentation<http://pylilac.berlios.de/doc/Tools.Language_Architect-module.html>}.
	"""
	app = LAApp(0)
	app.MainLoop()

if __name__ == "__main__":
	run_la()
