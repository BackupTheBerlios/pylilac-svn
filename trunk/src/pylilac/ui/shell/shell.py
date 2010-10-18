#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for shell management utilities.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"


class SGR(object):
	__DEC_CODES = "pBFIUSRNCXpppppppppppbiusrncx"
	def __init__(self, fbd, decorations = "", font = None):
		if type(fbd) is int:
			fbd = str(fbd)
		if len(fbd) == 0:
			fbd = "88"
		elif len(fbd) == 1:
			if fbd[0] in SGR.__DEC_CODES:
				fbd = "88" + fbd[0]
			else:
				fbd = fbd[0] + "8"
		for i, p in enumerate(fbd):
			if (p < "0" or p > "9") and (i < 2 or p not in SGR.__DEC_CODES):
				raise ValueError(p)
		self.fg = int(fbd[0])
		self.bg = int(fbd[1])
		decorations = []
		for d in fbd[2:]:
			if d >= "0" and d <= "9":
				x = SGR.__DEC_CODES[int(d)]
			elif d in SGR.__DEC_CODES:
				x = d
			decorations.append(x)
		self.decorations = "".join(decorations)
		self.font = font

	def __repr__(self):
		COLORS = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "unchanged", "default")
		d = self.decorations
		if d == "":
			d = "P"
		return COLORS[self.fg]+"|"+COLORS[self.bg]+"|"+d

	def __str__(self):
		r = []
		if self.fg <> 8:
			r.append(str(30 + self.fg))
		if self.bg <> 8:
			r.append(str(40 + self.bg))
		for d in self.decorations:
			r.append(str(SGR.__DEC_CODES.index(d)))
		if self.font is not None:
			r.append(str(10 + self.bg))
		return "\033["+";".join(r)+"m"

class Shell(object):
	BLACK = "0"
	RED = "1"
	GREEN = "2"
	YELLOW = "3"
	BLUE = "4"
	MAGENTA = "5"
	CYAN = "6"
	WHITE = "7"
	UNCHANGED = "8"
	DEFAULT = "9"
	RESET = "p"
	BOLD = "B"
	UNDERLINE = "U"
	REVERSED = "N"
	def __init__(self, ansi = true, width = 40):
		self.ansi = ansi
		self.width = 40

	def sgr(self, fgd, font = None):
		if self.ansi:
			return str(SGR(fgd, font))
		else:
			return ""
	def sgr_reset(self):
		return sgr("P")

	def clear(self):
		if self.ansi:
			print "\033[2J\033[0;0f"
		else:
			print

	def read_line(self, message):
		try:
			line = raw_input(self.sgr(self.BLUE)+message+self.sgr_reset())
		except EOFError, KeyboardInterrupt:
			print
			raise KeyboardInterrupt
		return line
	def write(self, line):
		print line,
	def write_line(self, line):
		print line
	def show_message(self, message, type = 0):
		if type == 0:
			print self.sgr(self.RED),"[*] ",self.sgr_reset(),line
		elif type == 1:
			print self.sgr(self.YELLOW),"[!] ",self.sgr_reset(),line
		else:
			print self.sgr(self.GREEN),"[.] ",self.sgr_reset(),line
