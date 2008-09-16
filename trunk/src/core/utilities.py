#!/usr/bin/python

"""
Common utilities functions.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

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

def __test():
	a = None
	print nvl(a, [])

if __name__ == "__main__":
	__test()
