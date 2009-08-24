#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common utilities functions.

This module also encapsulates the (potentially) unsupported features in I{non pure-Python} environments.
In that case, a pure-Python plugin for some classes and funcions must implemented and referenced.

"""

# General info
__version__ = "0.4"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
__docformat__ = "epytext en"

import sys

#Native language libraries
try: 
	from gzip import GzipFile
except ImportError: 
	#raise ImportError("A plugin for module gzip is needed.")
	from purepython import GzipFile

try: 
	from csv import writer, reader
except ImportError: 
	#raise ImportError("A plugin for module csv is needed.")
	from purepython import writer, reader

#Optional libraries
try: 
	from unidecode import unidecode as _complete_unidecode
	_unidecode = _complete_unidecode
except ImportError: 
	_unidecode = lambda u: u.encode(sys.getdefaultencoding(), "replace")

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
	def unidecode(unistring):
		"""
		Decode a unicode string.
		
		The C{unidecode} module is optional.
		If C{unidecode} is available, the string is I{meaningfully} decoded, otherwise non ASCII characters are replace with C{'?'}.
		
		@return: The given string decoded into ASCII.
		
		@see: U{unidecode<http://www.tablix.org/~avian/blog/archives/2009/01/unicode_transliteration_in_python/>}
		"""
		if isinstance(unistring, unicode):
			return _unidecode(unistring)
		else:
			raise TypeError(unistring)
			

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
				s.append("{")
			s.append(`key` + " : ")
			s.append(`self[key]`)
		s.append("}")
		return "".join(s)

	def __unicode__(self):
		s = []
		for key in self.__sort:
			if s:
				s.append(u", ")
			else:
				s.append(u"{")
			s.append(key + u" : ")
			s.append(self[key])
		s.append(u"}")
		return u"".join(s)

class ZipFile(GzipFile):
	pass
		
class Csv:
	@staticmethod
	def writer(file):
		"""
		Create a CSV writer function from a file.
		
		At each iteration, the method C{writerow} accepts the comma separated values and writes it.
		
		@param file: A binary writable (C{"wb"}) file object.
		@type file: file
		@return: A writer functions
		@rtype: object with a C{writerow} method
		"""
		return writer(file)
	@staticmethod
	def reader(file):
		"""
		Create a CSV reader function from a file.
		
		At each iteration, C{next} returns the comma separated values.
		
		@param file: A binary readable (C{"rb"}) file object.
		@type file: file
		@return: A reader functions
		@rtype: iterator
		"""
		return reader(file)
 

def __test():
	a = None
	print Utilities.nvl(a, "NULL")
	w = u"lómi"
	v = Utilities.unidecode(w)
	print v
	
 

if __name__ == "__main__":
	__test()
