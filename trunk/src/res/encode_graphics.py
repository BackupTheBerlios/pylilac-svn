
"""
This is a way to save the startup time when running img2py on lots of
files...
"""


from wx.tools import img2py

command_lines = [
	"-u -i -n Lilac graphics/lilac.16x16.png images.py",
	"-u -a -i -n Idea graphics/la/pos/idea.16.png images.py",
	"-u -a -i -n Action graphics/la/pos/action.16.png images.py",
	"-u -a -i -n Label graphics/la/pos/label.16.png images.py",
	"-u -a -i -n Brackets graphics/la/pos/brackets.16.png images.py",
	"-u -a -i -n Link graphics/la/pos/link.16.png images.py"
]

if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)

