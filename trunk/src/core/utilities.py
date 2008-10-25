#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common utilities functions.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

import unicodedata, sys

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


class SortedDict(dict):
	def __init__(self):
		dict.__init__(self)
		self.__sort = []
	def __setitem__(self, key, value):
		is_new = dict.has_key(self, key)
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
		return unicode(self).encode("UTF-8", "replace")
	def __unicode__(self):
		s = []
		for key in self.__sort:
			if s:
				s.append(u", ")
			else:
				s.append(u"{[")
			s.append(unicode(key) + u" : " + unicode(self[key]))
		s.append(u"]}")
		return u"".join(s)



def __test():
	a = None
	print nvl(a, [])

if __name__ == "__main__":
	__test()
