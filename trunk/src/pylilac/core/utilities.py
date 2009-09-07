#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common utilities functions.

This module also encapsulates the (potentially) unsupported features in I{non pure-Python} environments.
In that case, a pure-Python plugin for some classes and funcions must implemented and referenced.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

import sys

#Native language libraries
try: 
	from gzip import GzipFile
except ImportError:
	try: 
		from purepython import GzipFile
	except ImportError: 
		raise ImportError("Module gzip is unsupported.")

try: 
	from csv import writer, reader
except ImportError: 
	try: 
		from purepython import writer, reader
	except ImportError: 
		raise ImportError("Module csv is unsupported.")
		

#Optional libraries
try: 
	from unidecode import unidecode as _complete_unidecode
	_unidecode = _complete_unidecode
except ImportError: 
	_unidecode = lambda u: u.encode(sys.getdefaultencoding(), "replace")

class Utilities(object):

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


	@staticmethod
	def dict_str(map):
		z = ["{"]
		s = []
		for key, value in map.iteritems():
			s.append("%s: %s" % (str(key), str(value)))
		z.append(", ".join(s))
		z.append("}")
		return "".join(z)

	@staticmethod
	def tuple_str(t):
		z = ["("]
		s = []
		for elem in t:
			s.append(str(elem))
		z.append(", ".join(s))
		z.append(")")
		return "".join(z)

class SortedDict(object):
	def __init__(self):
		self.__dict = {}
		self.__sort = []

	def __getitem__(self, key):
		return self.__dict[key]

	def __contains__(self, key):
		return key in self.__dict

	def __setitem__(self, key, value):
		has_key = key in self.__dict
		self.__dict[key] = value
		if not has_key:
			self.__sort.append(key)

	def __delitem__(self, key):
		del self.__dict[key]
		self.__sort.remove(key)

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
		z = ["{"]
		s = []
		for key in self.__sort:
			value = self.__dict[key]
			if value is None:
				s.append(`key`)
			else:
				s.append("%s: %s" % (`key`, `value`))
		z.append(", ".join(s))
		z.append("}")
		return "".join(z)

	def __unicode__(self):
		z = [u"{"]
		s = []
		for key in self.__sort:
			value = self.__dict[key]
			if value is None:
				s.append(unicode(key))
			else:
				s.append(u"%s: %s" % (unicode(key), unicode(value)))
		z.append(u", ".join(s))
		z.append(u"}")
		return u"".join(z)

class ZipFile(GzipFile):
	pass
		
class Csv(object):
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
 