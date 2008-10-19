#!/usr/bin/python

"""
Run WX interface.
"""

from ui.la import LAApp

def __main():
	app = LAApp(0)
	app.MainLoop()

if __name__ == "__main__":
	__main()

