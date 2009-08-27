#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to build expressions in the Extended Backus-Naur Form (EBNF).
They are used as right hand symbols when defining the rules of a L{grammar.Grammar}.

Class Diagram
=============

The classes in this pachage implement a strict object oriented implementation, according to this class tree:

G{classtree NormalExpression}

The top level class, NormalExpression, is an abstract class and can not be instantiated.

Some classes are for package use only:
	- L{ParallelExpression<_ParallelExpression>} is an internal implementation for the subclasses of L{NormalExpression} and their combinations using operators.
	- L{Closure<_Closure>} and L{Epsilon<_Epsilon>} are accessible using constants.


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

Closures
========

When it is not quantified by a closure, an expression must occur once.

In other words, its cardinality is 1.

To change minimum or maximum occurrences for a reference, these closures can be used:

	- L{Optional or interrogative closure<OPTIONAL_CLOSURE>}, "C{?}"

	- L{Positive or multiple closure<POSITIVE_CLOSURE>}, "C{+}"

	- L{Kleene closure<KLEENE_CLOSURE>}, "C{+}"
	

Use of closures
---------------

	Closures are constants which can be accessed by the C{*} operator;
	for example, the code to represent M{Z ::= (X Y)*} is:

		>>> g["Z"] = Reference("XY") * KLEENE_CLOSURE
		>>> g["XY"] = Reference("X") + Reference("Y")



Resolving cyclic references
---------------------------

	Set of recursive rules such as the following are discouraged.

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


Interaction with other modules
==============================

Grammar compilation
-------------------
	When L{compiling<grammar.Grammar.compile>} a L{grammar<grammar.Grammar>}, rules are converted into a L{Deterministic Finite State Automaton<fsa.FSA>}, to enable expression parsing.
	The technique is based on the representation in form of graph of the different symbols and implemented by the recursive use of L{insert_transitions<NormalExpression.insert_transitions>} method.

Linguistic Literals
-------------------
	Terminal symbols in a natural language grammar are subclasses of L{literals<Literal>} such as L{WordFilter<lexicon.WordFilter>} or L{WordCategoryFilter<lexicon.WordCategoryFilter>}.
	They implement the I{tag method} C{match} as specialization of the equality operator.


Operator use example
====================
To model this simple grammar:
	>>> <clause>  ::= <subject> <verb>
	... <subject> ::= {noun}
	... <verb>    ::= {vt} <object> | {vi}
	... <object>  ::= {noun}

The following statements using operators can be used:
	>>> G["clause"]  = Reference("subject") + Reference("verb")
	>>> G["subject"] = Literal("noun")
	>>> G["verb"]    = (Literal("vt") + Reference("object")) | Literal("vi")
	>>> G["object"]  = Literal("noun")

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.5

@todo: an unordered concatenation operation M{&}

"""

__docformat__ = "epytext en"

from utilities import Utilities

class NormalExpression(object):
	"""
	An abstract class to model a Backus-Naur form (BNF) expression.
	It provides the basic construction element for more complex BNF expressions.
	"""
	def __init__(self):
		"""
		Prevent the class from being instantiated.
		To build an expression, the subclasses must be combined using operators.
		"""	
		if self.__class__ is NormalExpression: raise TypeError("NormalExpression is abstract and can not be instantiated.")
		
	def to_expression(self):
		"""
		Internally simplify the expression into an I{alternative} of I{concatenations}.

		@rtype: NormalExpression
		"""
		return _ParallelExpression([[self]])
		
	def __add__(self, b):
		"""
		Concatenate with another expression.
		The resulting expression expresses a sequence of the two operands.
		M{A + (X|YZ) S{hArr} A + X | A + YZ S{equiv} AX | AYZ}

		@param b: The expression to concatenate.
		@type b: NormalExpression		
		@rtype: NormalExpression		
		"""
		if not b: #espilon or None
			return _ParallelExpression([(self,)])
		else:
			return _ParallelExpression([(self,) + conc for conc in b.to_expression()])

	def __or__(self, b):
		"""
		Alternate with another symbol.
		The resulting expression expresses a choice between the two operands.
		M{A | (X|YZ) S{hArr} A | X | YZ S{equiv} X | YZ | A}

		@param b: The expression to alternate.
		@type b: NormalExpression	
		@rtype: NormalExpression
		"""
		c = [conc for conc in b.to_expression()]
		c.append([self])
		return _ParallelExpression(c)

	def __eq__(self, other):
		"""
		Compare two expressions.
		Equivalence between normal expressions is not trivial, but defined by the properties on M{S{Sigma}}:
			- Both M{|} and M{+} are associative
			- M{|} is commutative
			- M{+} is distributive respect to M{|}
			- Idempotence respect to M{|}
			- M{S{epsilon}} is the identity respect to M{|} and M{+}

		@param other: The expression to compare.
		@type other: NormalExpression	
		@rtype: bool
		@return: True if two expressions are equivalent			   
		"""
		if isinstance(other, NormalExpression):
			return self.to_expression() == other.to_expression()	
		elif other is None:
			return False
		else:
			return NotImplemented

	def __ne__(self, other):
		"""
		Compare two expressions for inequality.

		@param other: The expression to compare.
		@type other: NormalExpression
		@rtype: bool
		@return: True if two expressions are not equivalent
		"""	
		return not self.__eq__(other)

	def __hash__(self):
		"""
		Generate a hash code.

		@rtype: int
		"""	
		return hash(self.__class__)

	def __repr__(self):
		"""
		Return a string representation according to BNF.

		@rtype: str
		"""
		return "<>"

	def dependencies(self):
		"""
		Compute the I{non-terminal} symbols (references) the normal expression depends on.

		@rtype: frozenset
		"""
		return frozenset()

	def insert_transitions(self, grammar, fsa, initial, final, tag, max_levels):
		"""
		Insert a sub-FSA in a L{FSA<fsa.FSA>} according to the rules in a L{grammar<grammar.Grammar>}.

		@type grammar: Grammar
		@param grammar: The grammar providing the rules and options to build the sub-FSA.
		@type fsa: FSA
		@param fsa: The Finite-state Automaton in which the sub-graph must be inserted.
		@type initial: FSA node
		@param initial: The state from which the sub-graph departs.
		@type final: FSA node
		@param final: The state in which the sub-graph ends.
		@type tag: FSA tag
		@param tag: The initial tag for the arcs.
		@type max_levels: int
		@param max_levels: The maximum number of levels of recursion to accept.
		"""
		return

	def __nonzero__(self):
		"""
		Convert the expression into a boolean.

		@rtype: bool
		@return: False if S{epsilon}
		"""	
		return True

	def __mul__(self, closure):
		"""
		Apply a closure to the expression.

		@param closure: The closure to apply.
		@type closure: Closure constant
		@rtype: NormalExpression
		"""	
		raise TypeError("NormalExpression is abstract and does not support closures")

class Reference(NormalExpression):
	"""
	A non-terminal symbol.
	A non-terminal symbol is a symbol which has the capability of being further defined in terms of terminals and/or non-terminals.

	@see: Literal
	"""
	def __init__(self, reference):
		"""
		Create a non-terminal symbol.
		It contains a link to a symbol defined somewhere else.
		
		@param reference: The link to the symbol.
		@type reference: str
		"""
		self.reference = reference

	def __eq__(self, other):
		"""
		Compare a non-terminal to another.
		
		@param other: The non-terminal symbol to compare.
		@type other: Reference	
		@rtype: bool
		@return: True if the two links are the same.
		"""
		if isinstance(other, Reference):
			return self.reference == other.reference
		elif other is None:
			return False
		else:
			return NotImplemented
	
	def __hash__(self):
		return hash(self.__class__) ^ hash(self.reference)

	def __repr__(self):
		return "<%s>" % self.reference

	def dependencies(self):
		return frozenset([self.reference])

	def insert_transitions(self, grammar, fsa, initial, final, tag, max_levels):
		if max_levels == 0: return
		tag = Utilities.nvl(tag, ())
		rhs = grammar[self.reference]
		rhs.insert_transitions(grammar, fsa, initial, final, tag + (self.reference,), max_levels - 1)

	def __mul__(self, closure):
		return _Closure(self, closure)


class Literal(NormalExpression):
	"""
	A terminal symbol.

	A terminal symbol can be thought of as an indivisible entity.
	It is not possible to express a literal in terms of other literals or references.

	During token parsing, the methods L{match} and L{process} are called.
	
	@see: Reference
	"""
	def __init__(self, content):
		"""
		Create a terminal symbol.
		@param content: An object to wrap in th symbol.
		@type content: object
		"""
		self.content = content

	def __eq__(self, other):
		"""
		Compare a terminal to another.
		
		@param other: The literal to compare.
		@type other: Literal
		@rtype: bool
		@return: True if the two contents are equal.
		"""
		if isinstance(other, Literal):
			return self.content == other.content
		elif other is None:
			return False
		else:
			return NotImplemented

	def __hash__(self):
		return hash(self.__class__) ^ hash(self.content)

	def __repr__(self):
		return `self.content`

	def match(self, token):
		"""
		Verify that a token can be pocessed.
		It is used in parsing.
		It is often overridden for specialized behavior.
		
		@see: fsa.Parse
		@param token: The object to check.
		@type token: object
		@rtype: bool
		@return: True if the content is equal to the token.
		"""
		return self.content == token

	def process(self, token):
		"""
		Process the token and return the appropriate tag.
		It is used in parsing.
		It is often overridden for specialized behavior.
		
		@see: fsa.Parse
		@param token: The object to process.
		@type token: object
		@rtype: hashable
		@return: The token itself.
		"""
		return token

	def insert_transitions(self, grammar, fsa, initial, final, tag, max_levels):
		fsa.add_transition(initial, self, final, tag)


class _ParallelExpression(NormalExpression):
	"""
	A L{NormalExpression} implemented as parallel, i.e. concatenation of alternatives.
	@note: For internal use only.
	"""
	def __init__(self, double_iterable):
		"""
		Create an instance of ParallelExpression based on an alternative of concatenations.
		M{(A1+A2+...)|(B1+B2+...)|...}
		@note: For internal use only.
		@param double_iterable: A matrix of literals.
		
		"""
		self.__fsot = frozenset([tuple(conc) for conc in double_iterable])

	def __iter__(self):
		return self.__fsot.__iter__()

	def to_expression(self):
		return self

	def __repr__(self):
		r = []
		for t in self.__fsot:
			r.append(" ".join([`s` for s in t]))
		return " | ".join(r)

	def __add__(self, b):
		if not b: #epsilon or none
			return _ParallelExpression(self.__fsot)
		else:
			return _ParallelExpression([x + y for x in self.__fsot for y in b.to_expression()])

	def __or__(self, b):
		return _ParallelExpression(self.__fsot | b.to_expression().__fsot)

	def __eq__(self, other):
		if isinstance(other, _ParallelExpression):
			return self.__fsot == other.__fsot
		elif other is None:
			return False
		else:
			return NotImplemented

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

	def insert_transitions(self, grammar, fsa, initial, final, tag, max_levels):
		def concatenation_build(symbols, grammar, fsa, initial, final, tag):
			prev = initial
			for n, symbol in enumerate(symbols):
				if n + 1 == len(symbols):
					next = final
				else:
					next = fsa.add_state()
				symbol.insert_transitions(grammar, fsa, prev, next, tag, max_levels - 1)
				prev = next
				
		if max_levels == 0: return
		tag = Utilities.nvl(tag, ())
		for concatenation in self.__fsot:
			concatenation_build(concatenation, grammar, fsa, initial, final, tag)

class _Closure(Reference):
	"""
	Container for a quantified reference.

	Closures can be accessed by the C{*} operator;
	for example, the code to represent M{Z ::= (X Y)*} is:
	
		>>> g["Z"] = Reference("XY") * KLEENE_CLOSURE
		>>> g["XY"] = Reference("X") + Reference("Y")
	"""
	def __init__(self, expression, forward_back):
		"""
		Create a closure.
		
		The closure are depicted by using alternative S{epsilon} transitions in parallel::
		
				 Forward  Backward
			()!                    
			()?     Y              
			()+               Y    
			()*     Y         Y    
		
		@param expression: The expression to apply the closure to.
		@type expression: Literal
		@param forward_back: Two booleans to indicate if the closure adds an S{epsilon} transition in parallel
		@type forward_back: tuple of bool
		"""
		Reference.__init__(self, expression.reference)
		self.__forward, self.__back = forward_back


	def insert_transitions(self, grammar, fsa, initial, final, tag, max_levels):
		def build_reference(grammar, fsa, initial_node, final_node, tag, max_levels):
			Reference.insert_transitions(self, grammar, fsa, initial_node, final_node, tag, max_levels)
			
		def insert_back():
			# initial -> b super;
			# b -> initial epsilon;
			# b -> final epsilon
			
			back_end = fsa.add_state()
			build_reference(grammar, fsa, initial, back_end, tag, max_levels)
			fsa.add_transition(back_end, EPSILON_SYMBOL, initial)
			fsa.add_transition(back_end, EPSILON_SYMBOL, final)

		if max_levels == 0 : return
		if self.__forward:
			fsa.add_transition(initial, EPSILON_SYMBOL, final)
		if self.__back:
			insert_back()
		else:
			build_reference(grammar, fsa, initial, final, tag, max_levels)
			
	def __repr__(self):
		index = (self.__back & 1) << 1 | (self.__forward & 1)
		CHARS = "!?+*"
		return Reference.__repr__(self) + CHARS[index]

#{ Closure constants

OPTIONAL_CLOSURE = (True, False)
"""

The optional or interrogative closure. (C{?})

The expression is optional.
	
In other words, its cardinality can be 0 or 1.

@type: tuple of bool

"""
POSITIVE_CLOSURE = (False, True)
"""

The positive or multiple closure. (C{+})

The expression is mandatory and can be repeated any number of times.
	
In other words, its cardinality can be 1 to S{infin}.

@type: tuple of bool
"""
KLEENE_CLOSURE = (True, True)
"""

The Kleene closure. (C{*})

The expression is optional and can be repeated any number of times.
	
In other words, its cardinality can be 0 to S{infin}.

@type: tuple of bool
"""
#}

class _Epsilon(Literal):
	"""
	The class for alternative and juxtapositive identity.
	"""

	def __init__(self):
		Literal.__init__(self, None)

	def __add__(self, b):
		"""
		Concatenate with another expression.
		The identity is absorbed.
		
		M{S{epsilon}+(X|YZ) S{hArr} X | YZ}
		
		@param b: The expression to concatenate.
		@type b: NormalExpression
		@rtype: NormalExpression
		"""
		if not b:
			return EPSILON_SYMBOL
		else:
			return _pack(b._to_concatenations())

	def __eq__(self, other):
		"""
		Compare to a normal expressions.

		@param other: The expression to compare.
		@type other: NormalExpression	
		@rtype: bool
		@return: True if the parameter is S{epsilon} or C{None}, False if it is a different normal expression.
		"""
		if other is None or isinstance(other, _Epsilon):
			return True
		elif isinstance(other, NormalExpression):
			return False
		else:
			return NotImplemented

	def __repr__(self):
		return "{epsilon}"

	def insert_transitions(self, grammar, fsa, initial, final, tag, max_levels):
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

