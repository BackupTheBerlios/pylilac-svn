#!/usr/bin/python

"""

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

import pickle

class Interlingua:
	def __init__(self, name):
		"""
		Create an interlingua object.
		It encapsulate serialization and high-leven functionality.

		@type name: str
		@param name:
			The interlingua name.
		"""
		self.name = name
		self.p_o_s = []
		self.arg_struct = []
		self.taxonomy = Taxonomy()


	def __tuple(self):
		return (self.name, self.p_o_s, self.arg_struct, self.taxonomy)

	def save(self, filename = None):
		if filename is None:
			filename = "%s.ilt" % self.name
		f = open(filename, "wb")
		pickle.dump(self.__tuple(), f, 2)
		f.flush()
		f.close()

	def load(self, filename = None):
		if filename is None:
			filename = "%s.ilt" % self.name
		f = open(filename, "rb")
		tuple = pickle.load(f)
		self.name, self.p_o_s, self.arg_struct, self.taxonomy = tuple
		f.close()


class Concept:
	def __init__(self, interlingua, p_o_s, arg_struct, meaning, baseconcept = None, derivation = None):
		self.interlingua = interlingua
		self.p_o_s = p_o_s
		self.arg_struct = arg_struct
		self.meaning = meaning
		self.baseconcept = baseconcept
		self.derivation = derivation
		self.notes = ""
		self.reference = None

	def __repr__(self):
		return self.interlingua
	

class Taxonomy:
	def __init__(self):
		self.__nodes = {}
		self.__tree = {None: {}}
	def get(self, key):
		return self.__nodes[key]
	def set(self, concept):
		old_concept = self.__nodes.get(concept.interlingua)
		key = concept.interlingua
		self.__nodes[key] = concept
		if self.__tree.has_key(concept.baseconcept):
			siblings = self.__tree[concept.baseconcept]
		else:
			siblings = {}
			self.__tree[concept.baseconcept] = siblings
		#mode === adding mode
		if old_concept is None:
			mode = True
		else:
			old_baseconcept = old_concept.baseconcept
			mode = old_baseconcept == concept.baseconcept
		if mode:
			siblings[key] = concept
		else:
			old_siblings = self.__tree[old_baseconcept]
			del old_siblings[key]
			siblings[key] = concept
		return mode
	def remove(self, key):
		if key is not None:
			if self.__tree.has_key(key):
				for k in self.__tree[key].keys():
					self.remove(k)
			parent_key = self.__nodes[key].baseconcept
			siblings = self.__tree[parent_key]
			del siblings[key]
			if len(siblings) == 0:
				del self.__tree[parent_key]
			del self.__nodes[key]
		else: #key == None, clear
			self.__nodes = []
			self.__tree = {None: {}}
	def subconcepts(self, key):
		if key is not None and not self.__nodes.has_key(key):
			raise ValueError(key)
		if self.__tree.has_key(key):
			return self.__tree[key].values()
		else:
			return []
	def __iter__(self):
		def add_node(node):
			sequencing.append(node)
			if self.__tree.has_key(node.interlingua):
				for c in self.__tree[node.interlingua].values():
					add_node(c)
		sequencing = []
		for r in self.__tree[None].values():
			add_node(r)
		return iter(sequencing)

	def __repr__(self):
		return repr(self.__tree)
		
def _test():
	interlingua = Interlingua("IL")
	t = interlingua.taxonomy
	t.set(Concept("to", "A", "0-n", "TO"))
	t.set(Concept("tomo", "A", "P-s", "TO", "to", "D"))
	interlingua.save()
	interlingua.load()
	
	

if __name__ == "__main__":
	_test()
