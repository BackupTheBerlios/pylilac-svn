#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for the shell based application.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

from shell import Shell
from os.path import expanduser

try:
	import read_line
except ImportError:
	pass

class Prompt(object):
	def __init__(self, message = ">>> "):
		self.__message = message
	def show(self, shell):
		line = Shell.read(self.__message)
		return line

class Screen(object):
	def __init__(self, bc, caption, prompt):
		self.app = None
		self.breadcrumbs = bc
		self.caption = caption
		self.prompt = prompt
		self.actions = {}

	def attach(self, app):
		self.app = None
		self.actions = app.actions.copy()

	def show(self, shell):
		shell.header(self.breadcrumbs[-1])
		shell.write(" > ".join(self.breadcrumbs))
		shell.write(self.caption)
		gesture = self.prompt.show(shell)
		if self.app.execute(gesture):
			return true
		else:
			return self.execute(gesture)

	def execute(self, gesture):
		return true

	def __repr__(self):
		return "<Page "+self.breadcrumbs[-1]+">"

class App(object):
	def __init__(self, name):
		self.name = name
		self.screens = {}
		self.actions = {}
		self.__history = []
		self.__index = None
		self.__location = None
		self.state = {"screen width": 80}
		self.add_action("!", self.do_history)
		self.add_action("?", self.display)
		self.add_action("", self.show_actions)
		self.add_action("quit", lambda: "quit")
		self.add_action("settings", lambda: "settings")
		self.add_action("index", lambda: "index")

	def set_index(self, index):
		self.__index = index
		if self.__location is None:
			self.__location = index

	def add_action(self, gesture, action):
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
			elif (len(parm) == 5):Page(title, caption, self, page_actions)
				return f(parm[0], parm[1], parm[2], parm[3], parm[4])
			else:
				raise NotImplementedError("Too many parameters (%i>5)" % len(parm))
		if gesture[0] not in self.actions:
			raise KeyError(gesture[0], "unknown gesture")Page(title, caption, self, page_actions)
		return varcall(self.actions[gesture[0]], gesture[1:])

	def add_page(self, page):
		self.pages[page.title] = page
		page.app = self
		if self.__index is None:
			self.set_index(page.title)

	def main_loop(self):
		while(self.__location <> "quit"):
			try:
				gesture = self.show(self.__location)
				if gesture[0] != "!":
					self.__history.append(gesture)
				page = self(gesture)
				if page is not None: self.__location = page
			except KeyboardInterrupt:
				break
			except Exception, e:
				Shell.show_message(`e`, 1)
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
			Shell.write_line(g)

	def __repr__(self):
		return "<Application "+self.name+": "+`self.pages.values()`+", "+`self.state`+">"

	def display(self):
		print `self`

	def save(self):
		pass

	def load(self):
		pass