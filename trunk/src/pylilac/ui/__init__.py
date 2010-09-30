#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for the graphic user interface.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""
__docformat__ = "epytext en"


def probe_module():
	try:
		import wxversion
		return "wx"
	except ImportError:
		try:
			import qt
			return "qt"
		except ImportError:
			return "shell"

def run_la():
	"""
	Run the Language Architect GUI.
	@see: U{Graphical User documentation<http://pylilac.berlios.de/doc/Tools.Language_Architect-module.html>}.
	"""
	module = probe_module()
	if module == "wx":
		from wx.la import LAApp
		app = LAApp(0)
		app.MainLoop()
	elif module == "shell":
		from shell.la import LAApp
		app = LAApp()
		app.main_loop()
	else:
		from shell.la import LAApp
		app = LAApp()
		app.main_loop()