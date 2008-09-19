#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
An interface to build expressions in the Backus-Naur form (BNF), used as right hand symbols in the rules of a L{grammar.Grammar}.

Hierarchy
=========


The classes in this module follow this hierarchy:


G{classtree _Symbol Literal _Epsilon Reference _Closure _Expression}



Supported operations
====================

Over the set M{S{Sigma}} of possible BNF expressions, two operations are defined:

    - concatenation (M{+}), for example: M{A + B S{equiv} AB}

    - alternation (M{|}) or choice, for example: M{A | B}

M{S{Sigma}} has the following properties:

    - Closure of M{S{Sigma}} under M{|} and M{+}
      - For all M{a}, M{b} belonging to M{S{Sigma}}, both M{a | b} and M{a + b} belong to M{S{Sigma}} (or more formally, M{|} and M{+} are binary operations on M{S{Sigma}}).

    - Both M{|} and M{+} are associative
      - For all M{a}, M{b}, M{c} in M{S{Sigma}}, M{a | (b | c) = (a | b) | c} and M{a + (b + c) = (a + b) + c}.

    - M{|} is commutative
      - For all M{a}, M{b}, M{c} belonging to M{S{Sigma}}, M{a | b = b | a}.

    - The operation M{+} is distributive over the operation M{|}
      - For all M{a}, M{b}, M{c} belonging to M{S{Sigma}}, M{a + (b | c) = (a + b) | (a + c)}.

    - Idempotence respect to M{|}
      - For all M{a} belonging to M{S{Sigma}}, M{a | a = a}.

    - Existence of a multiplicative or juxtapositive (i.e. for M{+}) identity
      - There exists an element M{S{epsilon}} in M{S{Sigma}}, such that for all M{a} belonging to M{S{Sigma}}, M{a + S{epsilon} = a}.

Conversion to a Graph
=====================

A L{grammar<grammar.Grammar>} can be converted into a L{Finite State Automaton<fsa.FSA>} by the recursive use of L{insert_transitions<_Symbol.insert_transitions>} method, applied to its starting symbol.

The technique is based on the representation in form of graph of the different symbols.


@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@todo: an unordered concatenation operation M{&}

"""

__docformat__ = "epytext en"

from utilities import Utilities

class _Symbol:
	"""
	A BNF symbol or expression.
	"""
	def to_expression(self):
		"""
		Convert the symbol into an I{alternative} of I{concatenations}.
		"""
		return _Expression([[self]])
	def __add__(self, b):
		"""
		Concatenate with another expression.
		M{A + (X|YZ) S{hArr} A + X | A + YZ S{equiv} AX | AYZ}
		"""
		if not b: #espilon or None
			return _Expression([(self,)])
		else:
			return _Expression([(self,) + conc for conc in b.to_expression()])

	def __or__(self, b):
		"""
		Alternate with another symbol.
		M{A | (X|YZ) S{hArr} A | X | YZ S{equiv} X | YZ | A}
		"""
		c = [conc for conc in b.to_expression()]
		c.append([self])
		return _Expression(c)

	def __eq__(self, other):
		"""
		Compare two symbols.
		"""
		if isinstance(other, _Symbol):
			return self.to_expression() == other.to_expression()	
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)


	def __hash__(self):
		return hash(self.__class__)

	def __repr__(self):
		"""
		Build up a verbose representation according to BNF.
		"""
		return "<>"

	def dependencies(self):
		"""
		Compute the I{non-terminals} the symbol depends on.
		"""
		return frozenset()

	def insert_transitions(self, grammar, fsa, initial, final, tag = None):
		"""
		Inserts a sub-FSA in a L{FSA<fsa.FSA>} according to the rules in a L{grammar<grammar.Grammar>}.
		"""
		return

	def __nonzero__(self):
		return True

class Reference(_Symbol):
	"""
	A non-terminal symbol.

	A non-terminal symbol is that symbol which has the capability of being further defined in terms of terminals and/or non-terminals.

	It may be said to be a glyph or mark that is further decomposable.

	@see: Literal
	"""
	def __init__(self, reference):
		self.reference = reference

	def __eq__(self, other):
		"""
		Compare a non-terminal to another.
		Two non-terminals are equal if their references are the same.
		"""
		if isinstance(other, Reference):
			return self.reference == other.reference
		else:
			return False
	def __hash__(self):
		return hash(self.__class__) ^ hash(self.reference)

	def __repr__(self):
		return "<%s>" % self.reference

	def dependencies(self):
		return frozenset([self.reference])

	def insert_transitions(self, grammar, fsa, initial, final, tag = None):
		tag = Utilities.nvl(tag, ())
		rhs = grammar[self.reference]
		rhs.insert_transitions(grammar, fsa, initial, final, tag + (self.reference,))

	def __mul__(self, closure):
		return _Closure(self, closure)


class Literal(_Symbol):
	"""
	A terminal symbol.

	A terminal symbol can be thought of as an indivisible entity.

	It is not possible to express a terminal in terms of other terminals or nonterminals.

	@see: Reference
	"""
	def __init__(self, content):
		self.content = content

	def __eq__(self, other):
		"""
		Compare a terminal to another.
		Two terminals are equal if their contents are the same.
		"""
		if isinstance(other, Literal):
			return self.content == other.content
		else:
			return False

	def __hash__(self):
		return hash(self.__class__) ^ hash(self.content)

	def __repr__(self):
		return `self.content`

	def match(self, token):
		return self.content == token

	def process(self, token):
		return token

	def insert_transitions(self, grammar, fsa, initial, final, tag = None):
		fsa.add_transition(initial, self, final, tag)


class _Expression(_Symbol):
	def __init__(self, double_iterable):
		self.__fsot = frozenset([tuple(conc) for conc in double_iterable])

	def __iter__(self):
		return self.__fsot.__iter__()

	def to_expression(self):
		return self

	def __repr__(self):
		r = []
		for t in self.__fsot:
			r.append(" ".join([repr(s) for s in t]))
		return " | ".join(r)

	def __add__(self, b):
		"""
		Concatenate with another symbol.
		M{(A|BC)+(X|YZ) S{hArr} A+X | BC+X | A+YZ | BC+YZ S{equiv} AX | BCX | AYZ | BCYZ}
		"""
		if not b: #epsilon or none
			return _Expression(self.__fsot)
		else:
			return _Expression([x + y for x in self.__fsot for y in b.to_expression()])

	def __or__(self, b):
		"""
		Alternate with another symbol.
		M{(A|BC)|(X|YZ) S{hArr} A | BC | Y | YZ}
		"""
		return _Expression(self.__fsot | b.to_expression().__fsot)

	def __eq__(self, other):
		if isinstance(other, _Expression):
			return self.__fsot == other.__fsot
		else:
			return False

	def __hash__(self):
		return hash(self.__class__) ^ hash(self.__fsot)

	def __nonzero__(self):
		for c in self.__fsot:
			for t in c:
				if not t: return False
		return True

	def dependencies(self):
		dep = set()
		for c in self.__fsot:
			for s in c:
				dep |= s.dependencies()
		return frozenset(dep)

	
	def insert_transitions(self, grammar, fsa, initial, final, tag = None):
		def concatenation_insert_transitions(symbols, grammar, fsa, initial, final, tag = None):
			tag = Utilities.nvl(tag, ())
			prev = initial
			for n, symbol in enumerate(symbols):
				if n + 1 == len(symbols):
					next = final
				else:
					next = fsa.add_state()
				symbol.insert_transitions(grammar, fsa, prev, next, tag)
				prev = next
		tag = Utilities.nvl(tag, ())
		for concatenation in self.__fsot:
			concatenation_insert_transitions(concatenation, grammar, fsa, initial, final, tag)

class _Closure(Reference):
	"""
	Container for a quantified reference.

	Closures can be accessed by the C{*} operator;
	for example, the code to represent M{Z ::= (X Y)*} is:
	
		>>> g["Z"] = Reference("XY") * KLEENE_CLOSURE
		>>> ["XY"] = Reference("X") + Reference("Y")


	Typical closures
	================

	When it's not quantified by a closure, an expression must occur only once.
	
	In other words, its cardinality is 1.

	To change minimum or maximum occurrences for a reference, these closures can be used:

		- L{Optional or interrogative closure<OPTIONAL_CLOSURE>}, "C{?}"

		- L{Positive or multiple closure<POSITIVE_CLOSURE>}, "C{+}"

		- L{Kleene closure<KLEENE_CLOSURE>}, "C{+}"



	Resolving cyclic references
	===========================

	Set of recursive rules such as the following are not accepted.

	The translation into closures is more evident when rules are unrolled.

	For example the rules::
	
		A ::= A1 C A2 | B
		C ::= C1 A C2
		
	correspond to::
	
		A ::= (A1 C1)* B (C2 A2)*
		
	thus, they can be converted into::
	
		A ::= B1* B B2*
		B1 ::= A1 C1
		B2 ::= C2 A2

	Again, the rule::
	
		X ::= X | Y
		
	is equivalent to::
	
		X ::= Y+

	
	"""
	def __init__(self, non_terminal, forward_back):
		# ! False, False
		# ? True, False
		# + False, True
		# * True, True
		Reference.__init__(self, non_terminal.reference)
		self.__forward, self.__back = forward_back


	def insert_transitions(self, grammar, fsa, initial, final, tag = None):
		def insert_reference_transitions(initial_node, final_node):
			Reference.insert_transitions(self, grammar, fsa, initial_node, final_node, tag)
		def insert_back():
			# initial -> b super;
			# b -> initial epsilon;
			# b -> final epsilon
			
			back_end = fsa.add_state()
			insert_reference_transitions(initial, back_end)
			fsa.add_transition(back_end, EPSILON_SYMBOL, initial)
			fsa.add_transition(back_end, EPSILON_SYMBOL, final)

		if self.__forward:
			fsa.add_transition(initial, EPSILON_SYMBOL, final)
		if self.__back:
			insert_back()
		else:
			insert_reference_transitions(initial, final)
			
	def __repr__(self):
		index = (self.__back & 1) << 1 | (self.__forward & 1)
		CHARS = "!?+*"
		return Reference.__repr__(self) + CHARS[index]

OPTIONAL_CLOSURE = (True, False)
"""

The optional or interrogative closure. (C{?})

The expression is optional.
	
In other words, its cardinality can be 0 or 1.

@type: C{sequence} of C{bool}

"""
POSITIVE_CLOSURE = (False, True)
"""

The positive or multiple closure. (C{+})

The expression is mandatory and can be repeated any number of times.
	
In other words, its cardinality can be 1 to S{infin}.

@type: C{sequence} of C{bool}
"""
KLEENE_CLOSURE = (True, True)
"""

The Kleene closure. (C{*})

The expression is optional and can be repeated any number of times.
	
In other words, its cardinality can be 0 to S{infin}.

@type: C{sequence} of C{bool}
"""

class _Epsilon(Literal):
	"""
	The class for alternative and juxtapositive identity.

	Also used as the I{null} label in transitions.
	"""

	def __init__(self):
		Literal.__init__(self, None)

	def __add__(self, b):
		"""
		Concatenate with another symbol, being absorbed.
		M{S{epsilon}+(X|YZ) S{hArr} X | YZ}
		"""
		if not b:
			return EPSILON_SYMBOL
		else:
			return _pack(b._to_concatenations())

	def __eq__(self, b):
		if b is None or isinstance(b, _Epsilon):
			return True
		else:
			return False

	def __repr__(self):
		return "e"

	def insert_transitions(self, grammar, fsa, initial, final, tag = None):
		fsa.add_transition(initial, EPSILON_SYMBOL, final, tag)

	def __nonzero__(self):
		return False

EPSILON_SYMBOL = _Epsilon()
"""

The alternative and juxtapositive identity.

@type: C{_Epsilon}

"""

def __test():
	_if = Literal("if")
	_condition = Reference("condition")
	_then = Literal("then")
	_stmt = Reference("statement")
	_else = Literal("else")
	print _if + _then + _else
	s = _if + _condition + _then + _stmt
	s |= s + _else + _stmt
	print s
	print
	ns = Literal("north")|Literal("south")
	print ns+(Literal("east")|Literal("west"))
	print ns+ns+ns
	print ns|ns
	print (Literal("north")|Literal("south"))+Literal("east")
	print Literal("south")+(Literal("east")|Literal("west"))
	print EPSILON_SYMBOL
	print EPSILON_SYMBOL | Literal("a") + Literal("b"), "= ab|0"
	print Literal("a") + Literal("b") | EPSILON_SYMBOL  , "= ab|0"
	print Literal("a") + (Literal("b") | Literal("b")) + EPSILON_SYMBOL == Literal("a") + Literal("b")
	print Literal("a") | Literal("a") | EPSILON_SYMBOL == Literal("a")

	a_k=Reference("a")*KLEENE_CLOSURE
	print a_k, "*"
	a_p = Reference("a")*POSITIVE_CLOSURE
	print a_p, "+"
	a_o = Reference("a")*OPTIONAL_CLOSURE
	print a_o, "?"

	print _else.match("else")

	
	#x = Literal("kk") | Reference("s") + s
	#x = s | Literal("null")
	#print x

if __name__ == "__main__":
	__test()

