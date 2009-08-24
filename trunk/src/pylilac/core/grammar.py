#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
A module to manage Extended Backus-Naur (EBNF) rules.


"""

# General info
__version__ = "0.4"
__author__ = "Paolo Olmino"
__license__ = "GNU GPL v3"
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
		Call the C{match} method for the label.
		Usually, it calls the L{match<lexicon.WordFilter.match>} method.
		@rtype: bool
		"""
		return label.match(token)

	def process(self, label, token):
		"""
		Call the C{process} method for the label.
		Usually, it calls the L{process<lexicon.WordFilter.process>} method.
		@rtype: I{Tag}
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
		self.ignore_recursion = False
		self.__compiled = None
		self.__valid = False

	def __setitem__(self, lhs, rhs):
		"""
		Add a definition to a symbol.
		
		M{<lhs> ::= <EBNF expression>}

		If the symbol was already defined, the new definition is appended as an alternative.
		
		@param lhs: The symbol to define or to add a new definition for.
		@type lhs: str
		@param rhs: The expression to define the symbol.
		@type rhs: bnf.NormalExpression
		"""
		if lhs in self.__rules:
			self.__rules[lhs] |= rhs.to_expression()
		else:
			self.__rules[lhs] = rhs.to_expression()
			self.__symbols.append(lhs)
		if self.starting is None:
			self.starting = lhs

	def __getitem__(self, lhs):
		"""
		Get the definition for a symbol.
		
		@param lhs: The symbol defined.
		@type lhs: str
		@return: The definition of the symbol, as s parallel EBNF expression.
		@rtype: bnf.NormalExpression
		"""
		return self.__rules[lhs]

	def __delitem__(self, lhs):
		"""
		Delete all definitions for a symbol.
		
		@param lhs: The symbol to clear.
		@type lhs: str
		"""
		del self.__rules[lhs]
		self.__symbols.remove(lhs)
		if self.starting == lhs:
			if len(self.__symbols) == 0:
				self.starting = None
			else:
				self.starting = self.__symbols[0]

	def __contains__(self, lhs):
		"""
		@rtype: bool
		"""
		return lhs in self.__rules

	def __str__(self):
		"""
		@rtype: str
		"""
		representation = []
		representation.append("\"Start Symbol\" = <%s>" % self.starting)
		for symbol in self.__symbols:
			representation.append("<%s> ::= %s" % (symbol, str(self.__rules[symbol])))
		return "\n".join(representation)


	def __repr__(self):
		"""
		@rtype: str
		"""
		representation = []
		representation.append("\"Name\" = \'%s\'" % self.name)
		representation.append("\"Start Symbol\" = <%s>" % self.starting)
		for symbol in self.__symbols:
			representation.append("<%s> ::= %s" % (symbol, repr(self.__rules[symbol])))
		return "\n".join(representation)

		

	def browse(self):
		"""
		Check for anomalies in the grammar.
		
		These anomalies will trigger an error:

			- No starting symbol defined
			- Unresolved references
			- Cyclic references (if C{ignore_recursion} is off)
		
		@returns: returns the maximum depths with no recursion
		@rtype: int
		
		"""
		def descend(lhs, ancestors = ()):
			if lhs not in self.__rules:
				raise UndefinedSymbolError(lhs)
			rhs = self.__rules[lhs]
			max_depth = 0
			for dep in rhs.dependencies():
				d = 0
				if dep in ancestors:
					if not self.ignore_recursion:
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
		Compile the set of rules into a Deterministic State Automaton (DFSA).

		If the grammar has never been compiled or it has been modified after last compilation, it will be translated into an FSA.
		The result will be kept available until the rules are modified or the grammar reset.

		The algorithm calls recursively the L{bnf.NormalExpression.insert_transitions} method.

		@param force: Recompile grammar even if it's already been validated and compiled.
		@rtype: fsa.Parser
		@return: A parser for the grammar.
		
		@see: L{Finite State Automaton<fsa.FSA>}
		"""

		if force or not self.__valid and self.__compiled is None:
			self.__valid = False
			
			depth = self.browse()
			if self.ignore_recursion:
				max_levels = int(depth * 1.8 + 4) #pretty deep, but it should takes seconds
			else:
				max_levels = 100 #very very deep, endless, a technological limit

			nfa = FSA()
			initial = nfa.add_state()
			nfa.set_initial(initial)
			final = nfa.add_state()
			nfa.set_final(final)
			
			s = self.__rules[self.starting]
			s.insert_transitions(self, nfa, initial, final, (), max_levels)
			#rewriting to save memory
			nfa = nfa.reduced()
			nfa = nfa.minimized()
			self.__compiled = _GrammarParser(nfa)
			self.__valid = True
		return self.__compiled


	def reset(self):
		"""
		Delete the internal result of the last compiling.
		"""
		del self.__compiled
		self.__compiled = None
		self.__valid = False



def _test():
	pass


if __name__ == "__main__":
	_test()

