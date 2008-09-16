#!/usr/bin/python

"""
Run WX interface.
"""

from ui.la import LAApp

def __main():
	language_architect = LAApp(0)
	language_architect.MainLoop()

if __name__ == "__main__":
	__main()

