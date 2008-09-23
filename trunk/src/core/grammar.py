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

def call_match_method(label, token):
	"""
	Call L{match<wordfilter.WordFilter.match>} method.
	"""
	return label.match(token)

def call_process_method(label, token):
	"""
	Call L{match<wordfilter.WordFilter.process>} method.
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

		

	def _browse(self, ignore_recursion = False):
		"""
		Check for anomalies in the grammar.

		These anomalies will trigger an error:

			- No starting symbol defined
			- Unresolved references
			- Cyclic references	
		"""
		def descend(lhs, ancestors = ()):
			if lhs not in self.__rules:
				raise UndefinedSymbolError(lhs)
			rhs = self.__rules[lhs]
			for dep in rhs.dependencies():
				if dep in ancestors:
					if not ignore_recursion:
						raise CyclicReferenceError(lhs, dep)
				else:
					descend(dep, ancestors + (lhs,))

		if self.starting is None:
			raise GrammarError("No starting symbol defined")
		descend(self.starting)

	def compile(self, ignore_loops = False, force = False):
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
			if ignore_loops:
				max_levels = 32 #pretty deep, but it should takes seconds
			else:
				max_levels = 64 #it can takes minutes, but a lot of languages with no recursion need this
			self._browse(ignore_loops)

			nfa = FSA()
			initial = nfa.add_state()
			nfa.set_initial(initial)
			final = nfa.add_state()
			nfa.set_final(final)

			s = self.__rules[self.starting]
			s.insert_transitions(self, nfa, initial, final, None, max_levels)

			self.__compiled = Parser(nfa, call_match_method, call_process_method)
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
	"""
	Toki Pona grammar::

		<sentence> ::= [<sentence-adverb> "la"] <pron-or-subject> <predicate>
		<pron-or-subject> ::= "mi" | "sina" | <subject> "li"
		<sentence-adverb> ::= <noun-phrase> 
		<subject> ::= <noun-phrase> | <compound-subject>
		<compound-subject> ::= <subject> "en" <subject> S{equiv} <subject> ::= <noun-phrase> ("en" <noun-phrase>)*
		<predicate> ::= <verb-phrase> | <compound-predicate>
		<compound-predicate> ::= <predicate> "li" <predicate> S{equiv} <predicate> ::= <verb-phrase> ("li" <verb-phrase>)*
		<noun-phrase> ::= <noun> <adjective>* 
		<verb-phrase> ::= <verb> <adverb>* <direct-object>*
		<direct-object> ::= "e" <noun-phrase>
	"""

	from bnf import Reference, EPSILON_SYMBOL, KLEENE_CLOSURE, OPTIONAL_CLOSURE, Literal
	from lexicon import Particle, Word, Headword
	from wordfilter import WordCategoryFilter, WordFilter, AttributeFilter

	g = Grammar("Toki pona")

	_particles = {"la": Particle("la", 1), "li": Particle("li", 1), "en": Particle("en", 1), "li2": Particle("li", 2), "e": Particle("e", 1)}
	_words = {"mi": Word("mi", Headword("mi", 1, "pronoun")), "sina": Word("sina", Headword("sina", 1, "pronoun"))}

	g["sentence"] = (Reference("sentence-adverb") + WordFilter(_particles["la"]) | EPSILON_SYMBOL) + Reference("pron-or-subject") + Reference("predicate")
	g["pron-or-subject"] = WordFilter(_words["mi"]) | WordFilter(_words["sina"]) | Reference("subject") + WordFilter(_particles["li"])
	g["sentence-adverb"] = Reference("noun-phrase")
	g["subject"] = Reference("noun-phrase") + Reference("subject-specification") * KLEENE_CLOSURE
	g["predicate"] = Reference("verb-phrase") + Reference("predicate-specification") * KLEENE_CLOSURE
	g["subject-specification"] = WordFilter(_particles["en"]) + Reference("noun-phrase")
	g["predicate-specification"] = WordFilter(_particles["li2"]) + Reference("verb-phrase")
	g["noun-phrase"] = WordCategoryFilter("noun") + Reference("adjective") * KLEENE_CLOSURE
	g["verb-phrase"] = WordCategoryFilter("verb") + Reference("adverb") * KLEENE_CLOSURE + Reference("direct-object") * KLEENE_CLOSURE
	g["adjective"] = WordCategoryFilter("adjective")
	g["adverb"] = WordCategoryFilter("adverb")
	g["direct-object"] = WordFilter(_particles["e"]) + Reference("noun-phrase")
	#g["transitive-verb*"] = WordCategoryFilter("verb", {"transitive": "y"})
	#g["intransitive-verb*"] = WordCategoryFilter("verb", {"transitive": AttributeFilter("ne", ["y"])})
	#g["noun*"] = WordCategoryFilter("noun")
	#g["noun**"] = WordCategoryFilter("noun")
	
	
	print g.compile(True)

	y = Grammar("A-A")
	y["sentence"] = Reference("pre") * OPTIONAL_CLOSURE + Reference("main") + Reference("post") * OPTIONAL_CLOSURE
	y["pre"] = Literal("e")
	y["post"] = y["pre"]
	y["main"] = Literal("e") | Literal("o")
	print "e can only be a main"
	print "e e can be pre main or main post"
	print y
	c = y.compile(True)
	print c


if __name__ == "__main__":
	_test()

