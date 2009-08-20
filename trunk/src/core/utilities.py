#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common utilities functions.

This module also encapsulates the (potentially) unsupported features in I{non pure-Python} environments.
In that case, a pure-Python plugin for some classes and funcions must implemented and referenced.

"""

# General info
__version__ = "0.1"
__author__ = "Paolo Olmino"
__url__ = "http://pylilac.berlios.de/"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

import sys

try: 
    from gzip import GzipFile
except ImportError: 
    raise ImportError("A plugin for module gzip is needed.")
    #from purepython import GzipFile

try: 
    from csv import writer, reader
except ImportError: 
    raise ImportError("A plugin for module csv is needed.")
    #from purepython import writer, reader

class Utilities:

	@staticmethod
	def nvl(obj, default):
		"""
		Resolve I{null} values.
		
		@return: the given C{obj} parameter if it is not C{None}, otherwise it returns C{default}.
		"""
		if obj is not None:
			return obj
		else:
			return default

	@staticmethod
	def unicode(str):
		"""
		Safely encodes a string into Unicode.
		
		@return: the given string encoded using Unicode
		"""
		if isinstance(str, unicode):
			return str
		else:
			return unicode(str)
			

class SortedDict(dict):
	def __init__(self):
		dict.__init__(self)
		self.__sort = []
	def __setitem__(self, key, value):
		is_new = dict.__contains__(self, key)
		dict.__setitem__(self, key, value)
		if not is_new: self.__sort.append(key)
	def iterkeys(self):
		for key in self.__sort:
			yield key
	def itervalues(self):
		for key in self.__sort:
			yield self[key]
	def iteritems(self):
		for key in self.__sort:
			yield (key, self[key])
	def __repr__(self):
		s = []
		for key in self.__sort:
			if s:
				s.append(", ")
			else:
				s.append("{[")
			s.append(`key` + " : ")
			s.append(`self[key]`)
		s.append("]}")
		return "".join(s)

	def __unicode__(self):
		s = []
		for key in self.__sort:
			if s:
				s.append(u", ")
			else:
				s.append(u"{[")
			s.append(unicode(key) + u" : ")
			s.append(unicode(self[key]))
		s.append(u"]}")
		return u"".join(s)

class ZipFile(GzipFile):
	pass
	    
class Csv:
	@staticmethod
	def writer(file):
	    return writer(file)
	@staticmethod
	def reader(file):
	    return reader(file)
 

def __test():
	a = None
	print nvl(a, [])

if __name__ == "__main__":
	__test()
