#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for using I{pylilac} on native platforms, such as IronPython.

It is hidden by the L{utilities} module, which tries to load the standard Python libraries and then loads from a module called {purepython}.
The module has not been implemented, but only these specifications are released for documentation purposes.

@summary: Code behind for the Language Laboratory.
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

import re

def reader(file):
	"""
	Create a CSV reader function from a file.

	At each iteration, C{next} returns the comma separated values.

	@param file: A binary readable (C{"rb"}) file object.
	@type file: file
	@return: A reader functions
	@rtype: iterator
	"""
	return _CsvReader(file)

def writer(file):
	"""
	Create a CSV writer function from a file.

	At each iteration, the method C{writerow} accepts the comma separated values and writes it.

	@param file: A binary writable (C{"wb"}) file object.
	@type file: file
	@return: A writer functions
	@rtype: object with a C{writerow} method
	"""
	return _CsvReader(file)

class _CsvReader:
	"""
	Simple CSV reader
	"""
	R = re.compile(",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))")
	def __init__(self, file):
		self.__file = file
	def __iter__(self):
		return self
	def next(self):
		row = self.__file.next()
		s = self.R.split(row)
		return s

class _CsvWriter:
	"""
	Simple CSV writer
	"""
	def __init__(self, file):
		self.__file = file
	def writerow(self, tuple):
		self.__file.write(",".join(tuple))
		self.__file.flush()

class GzipFile(file):
	"""
	A file class implementing GZ compression.
	"""
	pass
