#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for compiling grammars and parsing, i.e. traversing and tagging a token sequence using a compiled grammar.
The L{Finite State Automaton<FSA>} class is used to compile grammars and the L{Parser} class to parse streams.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

from optiontree import OptionTree


class StateError(KeyError):
	"""
	Exception indicating that the state does not exist in the FSA.
	"""
	pass
class TransitionError(KeyError):
	"""
	Exception indicating that no transition with the given start, label and end exists in the FSA.
	"""
	pass

EPSILON = None
"""
The I{null} label.
"""

class FSA:
	"""
	A compiled natural grammar.

	A Finite-state Automaton, or Finite-state Machine (FSA) used for compiling natural languages grammars.
	
	A compiled grammar consists of a tuple M{(S, S{Lambda}, s, F, S{delta})} where

		- M{S}, a finite set of states
		- S{Lambda}, a set of label which can be related to the language S{Sigma}.
		In the usual representation of a FSA used in parsing artificial languages, M{S{Lambda} S{equiv} S{Sigma}}.
		Even though this is supported, S{Lambda} will contain C{(label, tag)} tuples.
		- M{s S{isin} S}, the start state
		- M{F S{sube} S}, the set of final states
  		- M{S{delta}: S S{times} (S{Lambda}S{cup}{S{epsilon}}) S{->} S*}, transition function
	
	
	
	Implementation of M{S}, S{Lambda}
	=================================

	The structure is designed to support different data types, even though the states are usually numbers and the input tokens are strings.

	In general, the classes that implement states, labels and tags must support I{equivalence} and I{possibility to be used as a key}.
	This means that they must implement:
	     - C{__eq__}
	     - C{__hash__}
	In particular:
	     - for common operations, states and labels must support I{equivalence}
	     - for I{reduction}, states must also support I{hash method} and tags must support I{equivalence}
	     - for I{minimization}, all classes must support I{equivalence} and I{hash method}

	Tags
	====
	
	The use of tags is intended to extend the classical FSA.

	Tags can be used to distinguish between transitions having the same labels: the L{reduction operation<reduced>}
	will not reduce transitions having different tags.
	S{epsilon}-Transitions have empty tag.

	If tags are not used, the L{reduction operation<reduced>} returns a Deterministic FSA (DSA).

	Since the FSA is intended to be used mainly as an extension of the classical FSA, tags are implemented
	as a separate attribute, not encapsulated inside transition labels.


	Equivalence between Finite-state Automata
	=========================================
	
	Paths
	-----
	A path on a FSA with tags is a sequence of tuples M{(S{lambda}, t) S{isin} S{Lambda}} that can 
	be gathered while traversing the FSA from the initial state to any of the final states.

	The set of all the paths of a FSA (M{S{Pi}}) can be non-finite.
	
	Two FSA's are I{equivalent} when they share the same set of paths.
	
	"""


	def __init__(self):
		"""
		Create an empty FSA M{(S{empty}, S{Lambda}, I{?}, S{empty}, S{empty})}: 
		"""
		self.__initial_state = None
		self.__final_states = set()
		self.__states = set()
		self.__transitions = {} #{start: [(label, end, tag)...]}

	def __len__(self):
		return len(self.__transitions)

	#States
	def states(self):
		"""
		Return M{S}, the states of the FSA.
		"""
		return self.__states

	def _get_next_available_state(self):
		if self.__states:
			m = max(self.__states)
			if type(m) is int:
				return m + 1
			else:
				raise TypeError(m)
		else:
			return 0

	def add_state(self, state = None):
		"""
		Add a new state to M{S}.

		@param state: An object to be enlisted as state.
		@raise StateError: Fired if the state already belongs to M{S}.
		"""
		if state is None:
			state = self._get_next_available_state()
		else:
			if state in self.__states:
				raise StateError(state)
		self.__states.add(state)
		self.__transitions[state] = []
		return state

	def has_state(self, state):
		"""
		Verifies the existence of a state in M{S}.

		@param state: A state.
		"""
		if state in self.__states:
			return True
		else:
			return False

	def remove_state(self, state):
		"""
		Remove a state from M{S}.

		If the state is initial, another state is set to initial.

		@param state: An existing state. 
		@raise StateError: Fired if the state does not exist.
		"""
		if state not in self.__states:
			raise StateError(state)
		self.__states.remove(state)
		del self.__transitions[state]
		for transitions in self.__transitions:
			for transition in transitions:
				if transition[1] == state: #State.__eq__
					transitions.remove(transition)
		if self.__initial_state == state:
			if self.__states:
				self.__initial_state = self.__states[0]
			else:
				self.__initial_state = None
		if state in self.__final_states:
			self.__final_states.remove(state)

	def get_initial(self):
		"""
		Return the initial state M{s}.
		"""
		return self.__initial_state

	def get_final(self):
		"""
		Return the sets of final states M{F}.
		"""
		return self.__final_states

	def set_initial(self, state):
		"""
		Set the initial state M{s}.

		@param state: An existing state. 
		@raise StateError: Fired if the state does not exist.
		"""
		if state not in self.__states:
			raise StateError(state)
		self.__initial_state = state

	def set_final(self, state):
		"""
		Add a state to the set of final states M{F}.

		@param state: An existing state. 
		@raise StateError: Fired if the state does not exist.
		"""
		if state not in self.__states:
			raise StateError(state)
		self.__final_states.add(state)

	def unset_final(self, state):
		"""
		Remove a state from the set of final states M{F}.

		@param state: An existing state. 
		@raise StateError: Fired if the state does not exist.
		"""
		if state not in self.__states:
			raise StateError(state)
		self.__final_states.remove(state)

	#Start/Label/End...transitions


	def transitions_from(self, start):
		"""
		Return M{(S{lambda}(1), e, S{lambda}(2))} where M{e S{isin} S{delta}(C{start}, S{lambda})}

		@param start: An existing state. 
		@return: a list of C{(label, tag} tuples, each representing a transition
		@raise StateError: Fired if the state does not exist.
		"""
		if start not in self.__states:
			raise StateError(start)
		return self.__transitions[start] #State.__eq__, State.__hash__


	def add_transition(self, start, label, end, tag = None):
		"""
		Define a new association M{S{delta}(C{start}, C{(label, tag)}) S{->} C{end}}.

		@param start: The start state of the transitions to add. 
		@param label: The label of the transitions to add.
		@param end: The end state of the transitions to add. 
		"""
		if self.__initial_state is None:
			self.__initial_state = start
		self.__states.add(start)
		self.__states.add(end)
		if not label:
			tag = None
		self.__transitions.setdefault(start, []).append((label, end, tag))
		if not self.__transitions.has_key(end):
			self.__transitions[end] = []

	def remove_transitions(self, start, label, end):
		"""
		Remove all existing associations between M{S{delta}(C{start}, S{lambda}) S{->} C{end}, S{lambda}(1) = C{label}}.

		@param start: The start state of the transitions to remove. 
		@param label: The label of the transitions to remove.
		@param end: The end state of the transitions to remove. 
		@raise StateError: Fired if the state does not exist.
		@raise TransitionError: Fired if the label does not connect to any state.
		"""
		if start not in self.__states:
			raise StateError(start)
		found = 0
		transitions = self.__transitions[start]
		for transition in self.__transitions[start]:
			if transition[0] == label and transition[1] == end: #State.__eq__, State.__hash__, Label.__eq__
				transitions.remove(transition)
				found += 1
		if found == 0:
			raise TransitionError(start, label, end)
		else:
			return found
		


	#Transformations and methods

	def iter_transitions(self):
		for state, transitions in self.__transitions.iteritems():
			for transition in transitions:
				yield (state, transition[0], transition[1], transition[2])
		

	def __repr__(self):
		def format_state(state):
			f = ["", `state`, ""]
			if state == self.__initial_state:
				f[0] = ">"
			if state in self.__final_states:
				f[2] = ">"
			return "".join(f)
		def format_transition(transition):
			EPSILON_REPR = "ɛ"
			if transition[3] is None:
				tag = ""
			else:
				tag = " "+`transition[3]`
			if transition[1] is None:
				f = [`transition[0]`, `transition[2]`, EPSILON_REPR, tag]
			else:
				f = [`transition[0]`, `transition[2]`, `transition[1]`, tag]
			return "%s -> %s %s%s" % tuple(f)
		states = ", ".join([format_state(state) for state in self.__states])
		if self.__transitions:
			transitions = ";\n".join([format_transition(transition) for transition in self.iter_transitions()])
			return "%s{\n%s.\n%s\n}" % (self.__class__.__name__, states, transitions)
		else:
			return "%s{\n%s\n}" % (self.__class__.__name__, states)

	def epsilon_closure(self, states):
		"""
		Evaluate I{S{epsilon}-closure}(C{states}).

		@type states: set
		@param states: A subset of the FSA states.
		@rtype: frozenset
		@return: The I{S{epsilon}-closure} of the given set of states.
		"""
		if type(states) is list:
			v_s = states
		elif type(states) is set:
			v_s = [s for s in states]
		else:
			v_s = [states]
		index = 0
		while index < len(v_s):
			state, index = v_s[index], index + 1
			if not state in self.__states: #State.__eq__
				raise StateError(state)
			for l, end, t in self.__transitions[state]:
				if l == EPSILON and end not in v_s: #State.__eq__, State.__hash__, Label.__eq__
					v_s.append(end)
		return frozenset(v_s)#State.__hash__, State.__eq__

	def __instance(self):
		return self.__class__()

	def is_reduced(self):
		for transitions in self.__transitions.itervalues():
			t = set()
			for label, e, tag in transitions:
				if label == EPSILON: 
					return False
				if (label, tag) in t: 
					return False
				else:
					t.add((label, tag)) 
		return True

	def is_minimized(self):
		EXIT = None
		start_dict = {}
		for start, transitions in self.__transitions.iteritems():
			start_dict[start] = transitions[:]
		for state in self.__final_states:
			start_dict[state].append(EXIT)

		t = set()
		for v in start_dict.itervalues():
			fv = frozenset(v)
			if fv in t:
				return False
			else:
				t.add(fv)
		
		return True

	def reduced(self):
		"""
		Return an FSA I{equivalent} to the current, having no S{epsilon} or reduplicated transitions.
		
		@rtype: FSA
		@return: The reduced equivalent FSA.
		"""
		def move(starts, label, tag):
			mv = []
			for start in starts:
				for l, end, t in self.__transitions[start]:
					if l == label and t == tag:
						mv.append(end)
			return mv
		def tr_from(starts):
			d = set()
			for start in starts:
				for label, e, tag in self.__transitions[start]:
					if label != EPSILON:
						d.add((label, tag))
			return d
		
		dfa = self.__instance()
		dfa.add_state(0)
		dfa.set_initial(0)

		e0 = self.epsilon_closure(self.__initial_state)
		groupings = {e0: 0}
		nfa_states = [(0, e0)]
		index = 0
		
		while index < len(nfa_states):
			dfa_state, nfas = nfa_states[index]
			for exit, tag in tr_from(nfas):
				k = self.epsilon_closure(move(nfas, exit, tag))
				existing_new_node = groupings.get(k)
				if not existing_new_node is None:
					node = existing_new_node
				else:
					groupings[k] = node = len(dfa.states())
					nfa_states.append((node, k))
				dfa.add_transition(dfa_state, exit, node, tag)
			index += 1
		for grouping, state in groupings.iteritems():
			if grouping & self.__final_states:
				dfa.set_final(state)
		return dfa


	def minimized(self):
		"""
		Return an FSA I{equivalent} to the current, having no reduplicated states.

		Two states are reduplicated when all departing transitions are identical. 
		
		@rtype: FSA
		@return: The minimized equivalent FSA.
		"""
		#Label, State, Tag.__hash__ + __eq__
		EXIT = None
		start_dict = {}
		for start, transitions in self.__transitions.iteritems():
			start_dict[start] = transitions[:]
		for state in self.__final_states:
			start_dict[state].append(EXIT)

		# freeze it
		# start_dict == {0: frozenset([('a', 1)]), 1: frozenset([('b', 2), ('a', 1)]), 2: frozenset([EXIT])}
		for k, v in start_dict.iteritems():
			start_dict[k] = frozenset(v)
		
		adj_dict = {} # a dictionary associating all adjacencies set to the states that have them
		# adj_dict == {frozenset([('a', 1)]): [0], frozenset([('b', 2), ('a', 1)]): [1], frozenset([EXIT]): 2}
		for start, adj in start_dict.iteritems():
			adj_dict.setdefault(adj, []).append(start)

		eq_dict = {}
		# eq_dict == {0: 0, 1: 1, 2: 2}
		for eq_set in adj_dict.values():
			class_leader = eq_set[0]
			for sec in eq_set:
				eq_dict[sec] = class_leader


		mfa = self.__instance()
		mfa.__initial_state = eq_dict.get(self.__initial_state, self.__initial_state)
		mfa.__final_states = set([eq_dict.get(f,f) for f in self.__final_states])
		mfa.__states = set([eq_dict.get(f,f) for f in self.__states])
		for start in mfa.__states:
			z = []
			for label, end, tag in self.__transitions[start]:
				z.append((label, eq_dict.get(end, end), tag))
			mfa.__transitions[start] = z
		return mfa

	def copy(self):
		"""
		Create a (shallow) copy of the FSA. 
		"""
		cp = self.__instance()
		cp.__initial_state = self.__initial_state
		cp.__final_states = self.__final_states.copy()
		cp.__states = self.__states.copy()
		for state, transitions in self.__transitions.iteritems():
			cp.__transitions[state] = transitions[:]
		return cp

class ParseError(StandardError):
	def __init__(self, tokens, state):
		self.tokens = tuple(tokens)
		self.state = state

	def __len__(self):
		return len(self.tokens)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		if len(self.tokens)>0:
			return "[" + " ".join([repr(t) for t in self.tokens[:-1]]) + " ?" + repr(self.tokens[-1]) + "]@"+ str(self.state)
		else:
			return "[]@%d" % self.state


class ExpectedStopError(ParseError):
	def __str__(self):
		return "[" + " ".join([repr(t) for t in self.tokens]) + " ?]@"+ str(self.state)


def _eq(x, y):
	return x == y
def _sec_elem(x, y):
	return y
	

class Parser:
	"""
	An FSA adapter.
	It encapsulates a reduced and minimized copy of the FSA, the I{match} logics and the I{process} logics.
	"""
	def __init__(self, fsa, match = None, process = None):
		if fsa.is_reduced() and fsa.is_minimized():
			self.__fsa = fsa.copy()
		else:
			self.__fsa = fsa.reduced().minimized()
		if match is None:
			self.__match = _eq
		else:
			self.__match = match
		if process is None:
			self.__process = _sec_elem
		else:
			self.__process = process
	

	def __call__(self, tokens):
		def parse_from(fsa, tokens, index, state):
			output = OptionTree()
			expected_final = index == len(tokens)
			is_final = state in fsa.get_final()
			if expected_final:
				if is_final:
					return output
				else:
					raise ExpectedStopError(tokens[:index+1], state)
			transitions = fsa.transitions_from(state)
			token = tokens[index]
			matching = [(label, end, tag) for label, end, tag in transitions if self.__match(label, token)]
			if len(matching) == 0:
				raise ParseError(tokens[:index+1], state)
			
			m_pe = None
			for label, end, tag in matching:
				try:
					following = parse_from(fsa, tokens, index + 1, end) 
					following.element = (self.__process(label, token), tag)
					output.append(following)
				except ParseError, pe:
					if (not m_pe) or len(pe) > len(m_pe):
						m_pe = pe
			if len(output) == 0:
				if m_pe:
					raise m_pe
				else:
					raise ParseError(tokens[:index+1], state)
			return output


		return parse_from(self.__fsa, tokens, 0, self.__fsa.get_initial())
	

def __test():
	def add_token(fsa, str):
		s = str + " "
		for i, c in enumerate(s):
			if i == len(s) - 1:
				fsa.add_transition(s[:i], c, fsa.get_initial(), str)
				break
			else:
				fsa.add_transition(s[:i], c, s[:i+1])

	def tokenize(parser, dict, stream):
		def explode_list(dict, lst, pos):
			t = OptionTree()
			if pos < len(lst):
				for obj in dict[lst[pos]]:
					c = explode_list(dict, lst, pos + 1)		
					c.element = obj
					t.append(c)
			return t
		p = parser(stream + " ")
		ot = OptionTree()
		for u in p.expand():
			ot.append(explode_list(dict, [y[1] for y in u if y[1] is not None], 0))
		return ot
		

	#accepts e|a(a|b)*b
	eaabb = FSA()
	eaabb.add_transition(0, EPSILON, 2, None)
	eaabb.set_final(2)
	eaabb.add_transition(0, 'a', 1, None)
	eaabb.add_transition(1, 'a', 1, None)
	eaabb.add_transition(1, EPSILON, 3, None)
	eaabb.add_transition(3, 'b', 1, None)
	eaabb.add_transition(3, 'b', 2, None)
	print eaabb
	print eaabb.reduced()
	print eaabb.reduced().minimized()
	
	d = {"a": ["A"], "b": ["B"], "ab": ["AB"], "cab": ["CAB"]}	
	td = FSA()
	td.add_state("")
	td.set_initial("")
	td.add_transition("", "a", "a")
	td.add_transition("a", EPSILON, "a*", "a")
	td.set_final("a*")
	td.add_transition("", "b", "b")
	td.add_transition("b", EPSILON, "b*", "b")
	td.set_final("b*")
	td.add_transition("", "a", "a")
	td.add_transition("a", "b", "ab")
	td.add_transition("ab", EPSILON, "ab*", "ab")
	td.set_final("ab*")
	td.add_transition("", "c", "c")
	td.add_transition("c", "a", "ca")
	td.add_transition("ca", "b", "cab")
	td.add_transition("cab", EPSILON, "cab*", "cab")
	td.set_final("cab*")
	print td
	print td.reduced()
	print td.reduced().minimized()
	print "Td is min", td.is_minimized()
	print "Td is red", td.is_reduced()
	print "Td.rm is red", td.reduced().minimized().is_reduced()
	print "Td.rm is min", td.reduced().minimized().is_minimized()

	f = FSA() #vi, vivo, vi do
	f.add_state("")
	f.set_initial("")
	f.set_final("")


	add_token(f, "vi")
	add_token(f, "vivo")

	add_token(f, "do")
	add_token(f, "vi do")

	p = Parser(f)

	d = {"vi":["vi1", "vi2"], "do":["do1","do2","do3"], "vi do": ["vi do"]}

	print tokenize(p, d, "vi do")
	
	k = f.copy()


if __name__ == "__main__":
	__test()
