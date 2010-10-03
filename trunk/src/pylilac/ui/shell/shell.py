#,, decoration = 0):,, decoration = 0):!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for shell management utilities.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"


class SGR(object):
	BOLD = "b"
	BRIGHT = "b"
	FAINT = "f"
	UNDERLINED = "u"
	ITALIC = "i"
	NEGATIVE = "n"
	BLINK = "s"
	PLAIN = "p"
	BLUE = "4"
	GREEN = "2"
	RED = "1"
	DEFAULT = "9"
	UNCHANGED = "8"
	RESET = "88P"
	__DEC_CODES = "PbfiusrncxPPPPPPPPPPPBFIUSRNCX"
	def __init__(self, fbd, decorations = "", font = None):
		if type(fbd) is int:
			fbd = str(fbd)
		if len(fbd) < 2:
			fbd = (fbd + "88")[:2]
		for i, p in enumerate(fbd):
			if (p < "0" or p > "9") and (i < 2 or p not in self.__DEC_CODES):
				raise ValueError(p)
		self.fg = int(fbd[0])
		self.bg = int(fbd[1])
		decorations = []
		for d in fbd[2:]:
			if d in "0123456789":
				x = self.__DEC_CODES[int(d)] 
			elif d in self.__DEC_CODES:
				x = d
			decorations.append(x)
		self.decorations = "".join(decorations)
		self.font = font

	def __repr__(self):
		COLORS = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "unchanged", "default")
		return COLORS[self.fg]+"|"+COLORS[self.bg]+"|"+self.decorations

	def __str__(self):
		r = []
		if self.fg <> 8:
			r.append(str(30 + self.fg))
		if self.bg <> 8:
			r.append(str(40 + self.bg))
		for d in self.decorations:
			r.append(str(self.__DEC_CODES.index(d)))
		if self.font is not None:
			r.append(str(10 + self.bg))
		return "\033["+";".join(r)+"m"

class Shell(object):
	@staticmethod
	def sgr(fgd, font = None):
		return str(SGR(fgd, font))
	@staticmethod
	def clear():
		print "\033[2J\033[0;0f"


Shell.clear()

b = SGR(SGR.BLUE)
print b.fg, b.bg, b.decorations
print repr(b)
print Shell.sgr(SGR.BLUE)+"blu blu"+Shell.sgr(SGR.RESET)
