#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit test.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.utilities import *


def run():
	a = None
	print Utilities.nvl(a, "NULL")
	w = u"lómi"
	v = Utilities.unidecode(w)
	print v
	


if __name__ == "__main__":
	run()
