#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to manage the I{machine interlingua} used to express universal concepts.

A machine interlingua is an artificial language designed specifically for use as an interlingua in machine translation.
Such a language must be designed to meet two primary goals:
  - it must be easier to accurately translate from the source natural language into the interlingua than into another natural language
 - it must be computationally easy to accurately translate from the interlingua into the target language
In other words, mapping between natural languages and the interlingua must be both accurate and made as easy as possible.

For an example of machine interlingua, see U{The Lexical Semantics of a Machine Translation Interlingua <http://www.eskimo.com/~ram/lexical_semantics.html>}.

@see: Literal

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

import pickle

class Interlingua:
	"""
	A representation for a machine interlingua.

	"""
	def __init__(self, name):
		"""
		Create an interlingua object.
		It encapsulates serialization and high-leven functionality.

		@type name: str
		@param name: The interlingua name.
		"""
		self.name = name
		self.p_o_s = []
		self.arg_struct = []
		self.taxonomy = Taxonomy()


	def __tuple(self):
		return (self.name, self.p_o_s, self.arg_struct, self.taxonomy)

	def save(self, filename):
		"""
		Save the interlingua object to a file, using the L{pickle} module.

		@param filename: The file name to use; if not specified the name of the language with the C{ilt} extension will be used..
		@type filename: str
		"""
		if filename is None:
			filename = "%s.ilt" % self.name
		f = open(filename, "wb")
		pickle.dump(self.__tuple(), f, 2)
		f.flush()
		f.close()

	def load(self, filename):
		"""
		Load the interlingua object from a file, using the L{pickle} module.
		The internal status of the onject is changed to the loaded values.

		@param filename: The file name to use; if not specified the name of the language with the C{ilt} extension will be used..
		@type filename: str
		"""
		if filename is None:
			filename = "%s.ilt" % self.name
		f = open(filename, "rb")
		tuple = pickle.load(f)
		self.name, self.p_o_s, self.arg_struct, self.taxonomy = tuple
		f.close()


class Concept:
	"""
	A  universal concept with its attributes:
	  - representation in the interlingua
	  - part of speech (PoS)
	  - argument structure
	  - English meaning
	  - base concept it's derived from and type of derivation
	  - notes

	"""
	def __init__(self, interlingua, p_o_s, arg_struct, meaning, baseconcept = None, derivation = None):
		"""
		Create a record to contain the data of a concept.

		@param interlingua: Representation using the interlingua.
		@type interlingua: str
		@param p_o_s: Part of speech:
			- C{'N'}: noun
			- C{'V'}: verb
			- C{'A'}: adverb
			- C{'D'}: disjunct
			- C{'C'}: conjunction
		@type p_o_s: str
		@param arg_struct: Argument structure (and dynamicity), which specified the relationship stated between agent, patient and focus.
		@type arg_struct: str
		@param meaning: Representation using the interlingua.
		@type meaning: str
		@param baseconcept: The base concept from which the concept is derived.
		@type baseconcept: str
		@param derivation: The way the concept is derived from its base concept: derivate, changed, affixed, modified, and so on.
		@type derivation: str
		"""
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
	"""
	A  hierarchy of concepts (I{taxa}).

	"""
	def __init__(self):
		self.__nodes = {}
		self.__tree = {None: {}}
	def get(self, key):
		return self.__nodes[key]
	def set(self, concept):
		"""
		Add or updates a concept in the taxonomy.

		If a concept having the given interlingua representation exists, it's replaced.
		Otherwise, the given concept is added.

		@param concept: The taxon to add to the taxonomy.
		@type concept: Concept
		"""
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
		"""
		Retrieve the subconcepts of the taxon having the given key.

		@param key: The interlingua representation of the base concept.
		@type key: str
		@return: The list of subconcepts.
		@rtype: list(Concept)
		@raise ValueError: If no taxa having the given key exist.
		"""
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
	pass
	
	

if __name__ == "__main__":
	_test()
