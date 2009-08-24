#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PyLilac Poject
==============

U{http://pylilac.berlios.de}

@summary: User interface for pyLilac
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

# General info
__version__ = "0.4"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

from la import LAApp

def run():
	app = LAApp(0)
	app.MainLoop()

