#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for the shell based application.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

from application import App
from shell import Shell


class LAApp(App):
	def __init__(self):
		App.__init__(self, "pylilac Language Architect")
		self.data = LAFacade(self)
		self.shell = Shell()
		self.add_screen(Form("Home", "Who are you?", (("Nome",""),("Cognome",Link("Cognome")),("Età",EtaChooser()))
		self.add_screen(Screen("Cognome", (("Nome",""),("Cognome",Link("Cognome")),("Età",EtaChooser()))
		self.add_screen(Screen("Bye", ))

class LAFacade(object):
	def __init__(self, app):
		self.app = app
	def load_lect(self):
		pass
	def parse_lect(self):
		pass



