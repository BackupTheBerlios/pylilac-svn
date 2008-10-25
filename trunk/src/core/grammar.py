#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
A module to manage Extended Backus-Naur (EBNF) rules.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

from fsa import FSA, Parser

class GrammarError(ValueError):
	"""
	Exception meaning that some attribute of the grammar is not correctly specified.
	"""
	pass
class UndefinedSymbolError(GrammarError):
	"""
	Exception meaning that a given symbol was used in a right hand expression without being previously defined as a left hand member.
	"""
	pass
class CyclicReferenceError(GrammarError):
	"""
	Exception meaning that a cyclic reference or recursion has been attempted.
	"""
	def __str__(self):
		return "<%s>(<%s>)" % self.args 

class _GrammarParser(Parser):
	def match(self, label, token):
		"""
		Call L{match<lexicon.WordFilter.match>} method.
		"""
		return label.match(token)

	def process(self, label, token):
		"""
		Call L{match<lexicon.WordFilter.process>} method.
		"""
		return label.process(token)

class Grammar:
	"""
	A container for EBNF rules.

	Cyclic reference or recursion is not supported, but it can be traslated using L{closures<bnf._Closure>}.
	"""
	def __init__(self, name):
		self.name = name
		self.starting = None
		self.__symbols = []
		self.__rules = {}
		self.ignore_loops = False
		self.__compiled = None
		self.__valid = False

	def __setitem__(self, lhs, rhs):
		"""
		Add a definition to a left hand symbol.

		If the symbol was already defined, the new definition is appended as an alternative.
		"""
		if lhs in self.__rules:
			self.__rules[lhs] |= rhs.to_expression()
		else:
			self.__rules[lhs] = rhs.to_expression()
			self.__symbols.append(lhs)
		if self.starting is None:
			self.starting = lhs

	def __getitem__(self, lhs):
		return self.__rules[lhs]

	def __delitem__(self, lhs):
		del self.__rules[lhs]
		self.__symbols.remove(lhs)
		if self.starting == lhs:
			if len(self.__symbols) == 0:
				self.starting = None
			else:
				self.starting = self.__symbols[0]

	def __contains__(self, lhs):
		return lhs in self.__rules

	def __str__(self):
		representation = []
		representation.append("\"Start Symbol\" = <%s>" % self.starting)
		for symbol in self.__symbols:
			representation.append("<%s> ::= %s" % (symbol, str(self.__rules[symbol])))
		return "\n".join(representation)


	def __repr__(self):
		representation = []
		representation.append("\"Name\" = \'%s\'" % self.name)
		representation.append("\"Start Symbol\" = <%s>" % self.starting)
		for symbol in self.__symbols:
			representation.append("<%s> ::= %s" % (symbol, repr(self.__rules[symbol])))
		return "\n".join(representation)

		

	def _browse(self):
		"""
		Check for anomalies in the grammar.
		
		These anomalies will trigger an error:

			- No starting symbol defined
			- Unresolved references
			- Cyclic references (if C{ignore_recursion} is off)
		@returns: returns the maximum depths with no recursion
		
		"""
		def descend(lhs, ancestors = ()):
			if lhs not in self.__rules:
				raise UndefinedSymbolError(lhs)
			rhs = self.__rules[lhs]
			max_depth = 0
			for dep in rhs.dependencies():
				d = 0
				if dep in ancestors:
					if not self.ignore_loops:
						raise CyclicReferenceError(lhs, dep)
					else:
						d = 1# don't descend to avoid endless loop
				else:
					d = descend(dep, ancestors + (lhs,)) + 1
				if d > max_depth:
					max_depth = d
			return max_depth

		if self.starting is None:
			raise GrammarError("No starting symbol defined")
		return descend(self.starting)

	def compile(self, force = False):
		"""
		Compile the set of rules into a Finite State Automaton (FSA).

		If the grammar has never been compiled or it has been modified after last compilation, it will be translated into an FSA.
		The result will be kept available inside a private member until the rules are modified or the grammar reset.

		The algorithm calls recursively the L{bnf._Symbol.insert_transitions} method.

		@param force: recompile grammar if it's already been compiled and validated
		@param ignore_loops: check for cyclic references is skipped, and recursion is unrolled up to 32 levels
		"""

		if force or not self.__valid and self.__compiled is None:
			self.__valid = False
			
			depth = self._browse()
			if self.ignore_loops:
				max_levels = int(depth * 1.8 + 4) #pretty deep, but it should takes seconds
			else:
				max_levels = 100 #very very deep, endless, a technological limit

			nfa = FSA()
			initial = nfa.add_state()
			nfa.set_initial(initial)
			final = nfa.add_state()
			nfa.set_final(final)
			
			s = self.__rules[self.starting]
			s.build(self, nfa, initial, final, (), max_levels)
			dfa = nfa.reduced().minimized()
			nfa = None #saves memory
			self.__compiled = _GrammarParser(dfa)
			self.__valid = True
		return self.__compiled


	def reset(self):
		"""
		Delete the result of the last compiling.
		"""
		del self.__compiled
		self.__compiled = None
		self.__valid = False



def _test():
	pass


if __name__ == "__main__":
	_test()

