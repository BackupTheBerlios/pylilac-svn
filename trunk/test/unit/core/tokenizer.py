#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit test for tokenizer.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

from pylilac.core.tokenizer import *


def run():
	t = Tokenizer({"a": ["1"], "b": ["2"]}, {"separator": " "})
	c = t("a a b b a a")
	print c
	t2 = Tokenizer({"ala": ["ALA"], "mi": ["MI"], "pona": ["PONA","BENE"], "mi ala": ["MIALA"]}, {"separator": " "})
	print t2("mi ala pona")
	t3 = Tokenizer({"a": ["*a*"], "bb": ["*bb*"], "b": ["*b*"]}, {"separator": ""})
	c3 = t3("abba")
	print c3



if __name__ == "__main__":
	run()
