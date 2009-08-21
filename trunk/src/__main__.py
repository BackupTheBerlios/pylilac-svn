#!/usr/bin/python

"""
Run WX interface.
"""
import sys
#sys.path.insert(0, "pylilac.pyz")

from ui.la import LAApp

def __main():
	app = LAApp(0)
	app.MainLoop()

if __name__ == "__main__":
	__main()

