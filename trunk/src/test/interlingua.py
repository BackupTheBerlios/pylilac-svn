#!/usr/bin/python

"""
A module to create Latejami language file.
"""

from core.interlingua import Interlingua, Concept
import csv
import sys

def run():
	def build(i, p, a, m, b, d, n, r):
		c = Concept(i, p, a, m, b, d)
		c.notes = n
		c.reference = r
		return c
	l = Interlingua("data/Latejami.csv")
	#l.p_o_s = ["N", "V", "A", "D", "C"]
	#l.arg_struct = ["0-n"]
	#l.arg_struct += [(a + f + "-" + d) for a in ("P", "AP", "A/P") for f in ("", "/F") for d in ("s","d")]
	#l.arg_struct += [(a + "-" + d) for a in ("F", "F/P") for d in ("s", "d")]
	t = l.taxonomy
	
	filename = "data/Latejami2.csv"
	
	reader = csv.reader(open(filename, "rb"))
	try:
		l.name = reader.next()[0]
		l.p_o_s = list(reader.next())
		l.arg_struct = list(reader.next())
		for (i, pos, as, m, bc, d, n, r) in reader:
			if bc == "":
				bc = None
			c = build(i, pos, as, m, bc, d, n, r)
			t.set(c)
	except csv.Error, e:
		sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
		
	print "Now saving."
	l.save()

	writer = csv.writer(open("data/Latejami3.csv", "wb"))
	writer.writerow((l.name, ))
	writer.writerow(l.p_o_s)
	writer.writerow(l.arg_struct)
	for c in l.taxonomy:
		writer.writerow((c.interlingua, c.p_o_s, c.arg_struct, c.meaning, c.baseconcept, c.derivation, c.notes, c.reference))



if __name__ == "__main__":
	run()

