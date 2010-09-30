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


class LAApp(App):
	def __init__(self):
		App.__init__(self, "pylilac Language Architect")
		self.add_page("pylilac Language Architect", "Welcome world")
		self.add_action("ll", self.load_lect)

	def load_lect(self):
		pass