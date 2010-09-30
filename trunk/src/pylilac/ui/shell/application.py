#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for the shell based application.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

from os.path import expanduser

try:
	import read_line
except ImportError:
	pass

class Page(object):
	def __init__(self, title, caption, app, page_actions = {}):
		self.title = title
		self.caption = caption
		self.app = app
		merged_actions = app.actions.copy()
		merged_actions.update(page_actions)
		self.actions = merged_actions

	def show(self):
		print "-" * self.app.state["screen width"]
		print self.title
		print self.caption
		try:
			line = raw_input(">>> ")+" "
		except EOFError:
			raise KeyboardInterrupt
		return line.split(" ")[:-1]

	def __repr__(self):
		return "<Page "+self.title+">"

class App(object):
	def __init__(self, name):
		self.name = name
		self.pages = {}
		self.actions = {}
		self.__history = []
		self.__index = None
		self.__location = None
		self.state = {"screen width": 40}
		self.add_action("!", self.do_history)
		self.add_action("?", self.display)
		self.add_action("", self.show_actions)
		self.add_action("quit", lambda: "quit")
		self.add_action("save", self.save)
		self.add_action("load", self.load)

	def set_index(self, index):
		self.__index = index
		if self.__location is None:
			self.__location = index

	def add_action(self, verb, action):
		self.actions[verb] = action

	def show(self, page):
		if page not in self.pages:
			raise KeyError(page, "unknown page")
		return self.pages[page].show()

	def __call__(self, gesture):
		def varcall(f, parm):
			if (len(parm) == 0):
				return f()
			elif (len(parm) == 1):
				return f(parm[0])
			elif (len(parm) == 2):
				return f(parm[0], parm[1])
			elif (len(parm) == 3):
				return f(parm[0], parm[1], parm[2])
			elif (len(parm) == 4):
				return f(parm[0], parm[1], parm[2], parm[3])
			elif (len(parm) == 5):
				return f(parm[0], parm[1], parm[2], parm[3], parm[4])
			else:
				raise NotImplementedError("Too many parameters (%i>5)" % len(parm))
		if gesture[0] not in self.actions:
			raise KeyError(gesture[0], "unknown gesture")
		return varcall(self.actions[gesture[0]], gesture[1:])

	def add_page(self, title, caption, page_actions = {}):
		self.pages[title] = Page(title, caption, self, page_actions)
		if self.__index is None:
			self.set_index(title)

	def main_loop(self):
		while(self.__location <> "quit"):
			try:
				gesture = self.show(self.__location)
				if gesture[0] != "!":
					self.__history.append(gesture)
				page = self(gesture)
				if page is not None: self.__location = page
			except KeyboardInterrupt:
				print
				break
			except Exception, e:
				print "[!!] " +`e`
				raise


	def do_history(self, step = "-1"):
		try:
			return self(self.__history[int(step)])
		except:
			for i, s in enumerate(self.__history):
				print i, s.join(" ")

	def show_actions(self):
		page = self.pages[self.__location]
		for g in page.actions.iterkeys():
			print g

	def __repr__(self):
		return "<Application "+self.name+": "+`self.pages.values()`+", "+`self.state`+">"

	def display(self):
		print `self`

	def save(self):
		pass

	def load(self):
		pass