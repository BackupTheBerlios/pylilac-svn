#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
A module to define and manage grammar rules.
The notation used to model rules is Extended Backus-Naur (EBNF) rules, supported by the L{bnf} module.
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.5
"""

__docformat__ = "epytext en"

from fsa import FSA, Parser

class GrammarError(ValueError):
	"""
	Exception indicating that some attribute of the grammar is not correctly specified.
	"""
	pass
class UndefinedSymbolError(GrammarError):
	"""
	Exception indicating that a given symbol was used in a right hand expression without being previously defined as a left hand member.
	"""
	pass
class CyclicReferenceError(GrammarError):
	"""
	Exception indicating that a cyclic reference or recursion has been encountered when not expected or attempted and failed.
	"""
	def __str__(self):
		return "<%s>(<%s>)" % self.args 

class _GrammarParser(Parser):
	def match(self, label, token):
		"""
		Verify if a label in the FSA matches a token, calling the C{match} method of the label.
		Typically, it calls the L{match<lexicon.WordFilter.match>} method.
		
		@return: True if the label matches the token.
		@rtype: bool
		"""
		return label.match(token)

	def process(self, label, token):
		"""
		Process a token, returning the tag to append to the parsing result., calling the C{process} method of the label.
		
		Typically, it calls the L{process<lexicon.WordFilter.process>} method.
		@return: The tag to add to the parsing.
		@rtype: tag
		"""
		return label.process(token)

class Grammar(object):
	"""
	A container for EBNF rules.
	"""
	def __init__(self, name):
		"""
		Create a Grammar with the given name.
		"""
		self.name = name
		self.start = None
		self.__symbols = []
		self.__rules = {}
		self.ignore_recursion = False
		self.__compiled = None
		self.__valid = False

	def __setitem__(self, symbol, rhs):
		"""
		Add a definition to a symbol.
		
		M{<symbol> ::= <EBNF expression>}

		If the symbol was already defined, the new definition is appended as an alternative.
		
		@param symbol: The symbol to define or to add a new definition for.
		@type symbol: str
		@param rhs: The expression to define the symbol.
		@type rhs: bnf.NormalExpression
		"""
		if symbol in self.__rules:
			self.__rules[symbol] |= rhs.to_expression()
		else:
			self.__rules[symbol] = rhs.to_expression()
			self.__symbols.append(symbol)
		if self.start is None:
			self.start = symbol

	def __getitem__(self, symbol):
		"""
		Get the definition for a symbol.
		
		@param symbol: The symbol defined.
		@type symbol: str
		@return: The definition of the symbol, as s parallel EBNF expression.
		@rtype: bnf.NormalExpression
		"""
		return self.__rules[symbol]

	def __delitem__(self, symbol):
		"""
		Delete all definitions for a symbol.
		
		@param symbol: The symbol to clear.
		@type symbol: str
		"""
		del self.__rules[symbol]
		self.__symbols.remove(symbol)
		if self.start == symbol:
			if len(self.__symbols) == 0:
				self.start = None
			else:
				self.start = self.__symbols[0]

	def __contains__(self, symbol):
		"""
		Check if a symbol is defined.
		
		@param symbol: The symbol to search.
		@type symbol: str
		@rtype: bool
		"""
		return symbol in self.__rules

	def __str__(self):
		"""
		Return a short string representation for the symbols defined in the grammar.
		@rtype: str
		"""
		representation = []
		for symbol in self.__symbols:
			if symbol == self.start:
				is_start = "^"
			else:
				is_start = ""
			representation.append("%s<%s>" % (is_start, symbol))
		return "<" + ", ".join(representation) + ">"


	def __repr__(self):
		"""
		Return a verbose string representation for the grammar.
		@rtype: str
		"""
		representation = []
		for symbol in self.__symbols:
			if symbol == self.start:
				is_start = "^"
			else:
				is_start = ""
			representation.append("%s<%s> ::= %s" % (is_start, symbol, repr(self.__rules[symbol])))
		return "\n".join(representation)

		

	def browse(self):
		"""
		Check the grammar for anomalies.
		These anomalies will trigger an error:

			- No start symbol defined
			- Unresolved references
			- Cyclic references (if the grammar does not ignore recursion)
		
		@returns: The maximum depth with no recursion
		@rtype: int
		@raise GrammarError: If anomalies are encountered while browsing.
		
		"""
		def descend(symbol, ancestors = ()):
			if symbol not in self.__rules:
				raise UndefinedSymbolError(symbol)
			rhs = self.__rules[symbol]
			max_depth = 0
			for dep in rhs.dependencies():
				d = 0
				if dep in ancestors:
					if not self.ignore_recursion:
						raise CyclicReferenceError(symbol, dep)
					else:
						d = 1# don't descend to avoid endless loop
				else:
					d = descend(dep, ancestors + (symbol,)) + 1
				if d > max_depth:
					max_depth = d
			return max_depth

		if self.start is None:
			raise GrammarError("No start symbol defined")
		return descend(self.start)

	def compile(self, force = False):
		"""
		Compile the set of rules into a Deterministic State Automaton (DFSA).

		If the grammar has never been compiled or it has been modified after last compilation, it will be translated into an FSA.
		The result will be kept available until the rules are modified or the grammar reset.

		The algorithm calls recursively the L{bnf.NormalExpression.insert_transitions} method.
		
		In case a recursive rule is encountered and the flag C{ignore_recursion} is on, the grammar tries to crawl down the recursion.

		If the C{force} flag is off and the grammar was already compiled and was not updated, the old result is taken with no recompiling.

		@see: L{Finite State Automaton<fsa.FSA>}
		@param force: Recompile grammar even if it has already been validated and compiled.
		@type force: bool
		@raise GrammarError: If anomalies are encountered while precompiling.
		@return: A parser for the grammar.
		@rtype: fsa.Parser
		
		"""

		if force or not self.__valid and self.__compiled is None:
			self.__valid = False
			
			depth = self.browse()
			if self.ignore_recursion:
				max_levels = int(depth * 1.8 + 4) #pretty deep, but it should take seconds
			else:
				max_levels = 100 #very very deep, endless, a technological limit

			nfa = FSA()
			initial = nfa.add_state()
			nfa.set_initial(initial)
			final = nfa.add_state()
			nfa.set_final(final)
			
			s = self.__rules[self.start]
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

