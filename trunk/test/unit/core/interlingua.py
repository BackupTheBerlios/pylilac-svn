#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.interlingua import *

def run():
	il = Interlingua("trunk/src/data/Latejami.csv")
	il.load()
	tx = il.taxonomy
	print tx.get("byukigi")


if __name__ == "__main__":
	run()
