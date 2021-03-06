#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for grammar compiling and for parsing.
Parsing is meant as traversing and tagging token sequences using a compiled grammar.
The L{Finite State Automaton<FSA>} class is used to compile grammars and the L{Parser} class to parse token streams.
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
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

class FSA(object):
	"""
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

	In general, the classes that implement states, labels and tags must support I{equivalence} and I{possibility to be used as a key}; equivalently, they must be I{hashable} objects.
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


	Paths
	=====
	A path on a FSA with tags is a sequence of tuples M{(S{lambda}, t) S{isin} S{Lambda}} that can
	be collected while traversing the FSA from the initial state to any of the final states.

	The set of all the paths of a FSA (M{S{Pi}}) can be non-finite.

	Two FSA's are I{equivalent} when they share the same set of paths.

	"""


	def __init__(self):
		"""
		Create an empty FSA M{(S{empty}, S{Lambda}, I{?}, S{empty}, S{empty})}.
		"""
		self.__initial_state = None
		self.__final_states = set()
		self.__states = set()
		self.__transitions = {} #{start: [(label, end, tag)...]}

	def __len__(self):
		"""
		Return the number of transitions M{S{delta}} in the FSA.
		@rtype: int
		"""
		return len(self.__transitions)

	#{ Methods for manipulating states

	def states(self):
		"""
		Return M{S}, the states of the FSA.
		@rtype: set of states
		"""
		return self.__states

	def _get_next_available_state(self):
		"""
		If the states are integers, return the next available state number.

		@return: Next available state.
		@rtype: int
		"""
		if self.__states:
			m = max(self.__states)
			if isinstance(m,  int):
				return m + 1
			else:
				raise TypeError(m)
		else:
			return 0

	def add_state(self, state = None):
		"""
		Add a new state to M{S}.

		@param state: An object to be enlisted as state. If C{None}, a new state is automatically generated.
		@type state: hashable
		@raise StateError: Fired if the state already belongs to M{S}.
		@raise TypeError: Fired if the state was not provided and existing maximum state is not an integer.

		@return: The state provided or automatically generated.
		@rtype: hashable
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
		Verify the existence of a state in M{S}.

		@param state: A state.
		@type state: hashable
		@return: True if the state belongs to the FSA.
		@rtype: bool
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
		@type state: hashable
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

		@rtype: hashable
		"""
		return self.__initial_state

	def get_final(self):
		"""
		Return the sets of final states M{F}.

		@rtype: set of hashable
		"""
		return self.__final_states

	def set_initial(self, state):
		"""
		Set the initial state M{s}.

		@param state: An existing state.
		@type state: hashable
		@raise StateError: Fired if the state does not exist.
		"""
		if state not in self.__states:
			raise StateError(state)
		self.__initial_state = state

	def set_final(self, state):
		"""
		Add a state to the set of final states M{F}.

		@param state: An existing state.
		@type state: hashable
		@raise StateError: Fired if the state does not exist.
		"""
		if state not in self.__states:
			raise StateError(state)
		self.__final_states.add(state)

	def unset_final(self, state):
		"""
		Remove a state from the set of final states M{F}.

		@param state: An existing state.
		@type state: hashable
		@raise StateError: Fired if the state does not exist.
		"""
		if state not in self.__states:
			raise StateError(state)
		self.__final_states.remove(state)

	#}

	#{ Methods for manipulating transitions

	def transitions_from(self, start):
		"""
		Return M{(S{lambda}(1), e, S{lambda}(2))} where M{e S{isin} S{delta}(C{start}, S{lambda})}

		@param start: An existing state.
		@type start: hashable
		@return: a list of transitions
		@rtype: list of C{(label, tag)} tuples
		@raise StateError: Fired if the state does not exist.
		"""
		if start not in self.__states:
			raise StateError(start)
		return self.__transitions[start] #State.__eq__, State.__hash__


	def add_transition(self, start, label, end, tag = None):
		"""
		Define a new association M{S{delta}(C{start}, C{(label, tag)}) S{->} C{end}}.

		@param start: The start state of the transitions to add.
		@type start: hashable
		@param label: The label of the transitions to add.
		@type label: hashable
		@param end: The end state of the transitions to add.
		@type end: hashable
		"""
		if self.__initial_state is None:
			self.__initial_state = start
		self.__states.add(start)
		self.__states.add(end)
		if not label:
			tag = None
		self.__transitions.setdefault(start, []).append((label, end, tag))
		if end not in self.__transitions:
			self.__transitions[end] = []

	def remove_transitions(self, start, label, end):
		"""
		Remove all existing associations between M{S{delta}(C{start}, S{lambda}) S{->} C{end}, S{lambda}(1) = C{label}}.

		@param start: The start state of the transitions to remove.
		@type start: hashable
		@param label: The label of the transitions to remove.
		@type label: hashable
		@param end: The end state of the transitions to remove.
		@type end: hashable
		@raise StateError: Fired if the state does not exist.
		@raise TransitionError: Fired if the label does not connect to any state.
		@return: The count of the removed transitions.
		@rtype: int
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


	def iter_transitions(self):
		"""
		Return an iterator on all transitions.

		@return: An iterator on all transitions.
		@rtype: iteration of hashable
		"""
		for state, transitions in self.__transitions.items():
			for transition in transitions:
				yield (state, transition[0], transition[1], transition[2])

	#}

	def __repr__(self):
		"""
		Represent the FSA, as a colection of states and transitions.

		@rtype: str
		"""
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


	#{ Methods for transformations
	def epsilon_closure(self, states):
		"""
		Evaluate I{S{epsilon}-closure}(C{states}).

		@param states: A subset of the FSA states.
		@type states: set of hashable
		@return: The I{S{epsilon}-closure} of the given set of states.
		@rtype: frozenset
		"""
		if isinstance(states, list):
			v_s = states
		elif isinstance(states, set):
			v_s = [s for s in states]
		else:
			v_s = [states]
		index = 0
		while index < len(v_s):
			state, index = v_s[index], index + 1
			if not state in self.__states: #State.__eq__
				raise StateError(state)
			for label, end, t in self.__transitions[state]:
				if label == EPSILON and end not in v_s: #State.__eq__, State.__hash__, Label.__eq__
					v_s.append(end)
		return frozenset(v_s)#State.__hash__, State.__eq__

	def __instance(self):
		return self.__class__()

	def is_reduced(self):
		"""
		Evaluate if the FSA is I{reduced}.
		A reduced FSA is characterized by unique and I{not null} (i.e. different than S{epsilon}) transitions.

		@return: True if the FSA is reduced.
		@rtype: bool
		"""
		for transitions in self.__transitions.values():
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
		"""
		Evaluate if the FSA is I{minimized}.
		A minimized FSA is characterized by unique states.
		Two states are reduplicated when all departing transitions are identical.

		@return: True if the FSA is minimized.
		@rtype: bool
		"""
		EXIT = None
		start_dict = {}
		for start, transitions in self.__transitions.items():
			start_dict[start] = transitions[:]
		for state in self.__final_states:
			start_dict[state].append(EXIT)

		t = set()
		for v in start_dict.values():
			fv = frozenset(v)
			if fv in t:
				return False
			else:
				t.add(fv)

		return True

	def reduced(self):
		"""
		Return an FSA I{equivalent} to the current, having no S{epsilon} or reduplicated transitions.

		@return: The reduced equivalent FSA.
		@rtype: FSA
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
		for grouping, state in groupings.items():
			if grouping & self.__final_states:
				dfa.set_final(state)
		return dfa


	def minimized(self):
		"""
		Return an FSA I{equivalent} to the current, having no reduplicated states.

		Two states are reduplicated when all departing transitions are identical.

		@return: The minimized equivalent FSA.
		@rtype: FSA
		"""
		#Label, State, Tag.__hash__ + __eq__

		EXIT = (None,  None,  None)


		current_initial_state = self.__initial_state
		current_final_states = self.__final_states
		current_states = self.__states
		current_transitions = self.__transitions

		was_minimized = False
		while not was_minimized:
			start_dict = {} #dictionary of transitions
			for start, transitions in current_transitions.items():
				if start in current_final_states:
					start_dict[start] = frozenset(transitions + [EXIT])
				else:
					start_dict[start] = frozenset(transitions)

			adj_dict = {} # a dictionary associating all adjacencies and the states that have them
			for start, adj in start_dict.items():
				adj_dict.setdefault(adj, []).append(start)

			eq_dict = {} # a dictionary for equivalence classes
			was_minimal = True
			# eq_dict == {0: 0, 1: 1, 2: 2}
			for eq_set in adj_dict.values():
				class_leader = eq_set[0]
				if len(eq_set)>1: #the FSA was not minimal
					was_minimal = False
				for sec in eq_set:
					eq_dict[sec] = class_leader


			#get(x,x) for disconnected states
			last_final_states = set([eq_dict[f] for f in current_final_states if f in eq_dict])
			last_initial_state = eq_dict[current_initial_state]
			last_states = set([eq_dict[f] for f in current_states if f in eq_dict])
			last_transitions = {}
			for start in last_states:
				last_transitions[start] = [(label, eq_dict[end], tag) for label, end, tag in current_transitions[start] if end in eq_dict]

			if was_minimal:
				mfa = self.__instance()
				mfa.__initial_state = last_initial_state
				mfa.__final_states = last_final_states
				mfa.__states = last_states
				mfa.__transitions = last_transitions
				return mfa
			else:
				current_initial_state = last_initial_state
				current_final_states = last_final_states
				current_states = last_states
				current_transitions = last_transitions


	def copy(self):
		"""
		Create a copy of the FSA.

		@return: A (shallow) copy of the FSA.
		@rtype: FSA
		"""
		cp = self.__instance()
		cp.__initial_state = self.__initial_state
		cp.__final_states = self.__final_states.copy()
		cp.__states = self.__states.copy()
		for state, transitions in self.__transitions.items():
			cp.__transitions[state] = transitions[:]
		return cp
	#}


class ParseError(StandardError):
	"""
	Exception indicating a parsing error.
	"""
	def __init__(self, tokens, state):
		self.tokens = tuple(tokens)
		self.state = state

	def __len__(self):
		return len(self.tokens)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		if len(self.tokens)>0:
			return "[" + " ".join([`t` for t in self.tokens[:-1]]) + " ?" + repr(self.tokens[-1]) + "]@"+ str(self.state)
		else:
			return "[]@%d" % self.state


class ExpectedStopError(ParseError):
	"""
	Exception indicating a parsing error caused by an unexpected symbol encountered while parsing.
	"""
	def __str__(self):
		return "[" + " ".join([`t` for t in self.tokens]) + " ?]@"+ str(self.state)


class Parser(object):
	"""
	An FSA adapter.
	It wraps a deterministic FSA, the I{match} logics and the I{stamp} logics.
	"""
	def __init__(self, fsa):
		"""
		Create a new parser based on the given FSA.
		The FSA must be deterministic, i.e. reduced and minimized.

		@param fsa: The deterministic FSA to use for parsing.
		@type fsa: FSA
		@raise ValueError: Fired if the FSA is not deterministic.
		"""
		rm = 0
		if not fsa.is_reduced():
			rm = 1
		if not fsa.is_minimized():
			rm += 2
		if rm>0:
			err_str = ("not reduced", "not minimized", "neither reduced nor minimized")
			raise ValueError("FSA is not deterministic: it is %s." % err_str[rm-1])
		self.__fsa = fsa

	def __call__(self, tokens):
		"""
		Parse the given sequence.

		@param tokens: The sequence to parse.
		@type tokens: sequence
		@raise ParseError: If parsing fails for an unexpected token or stop.
		@return: A tree of the possible tags encountered.
		@rtype: L{OptionTree<optiontree.OptionTree>}
		"""
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
			matching = [(label, end, tag) for label, end, tag in transitions if self.match(label, token)]
			if len(matching) == 0:
				raise ParseError(tokens[:index+1], state)

			m_pe = None
			for label, end, tag in matching:
				try:
					following = parse_from(fsa, tokens, index + 1, end)
					following.element = (self.process(label, token), tag)
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

	def match(self, label, token):
		"""
		Verify if a label in the FSA matches a token.
		Override this method to implement specialized behaviors.

		@return: True if the label is equal to the token.
		@rtype: bool
		"""
		return label == token

	def process(self, label, token):
		"""
		Process a token, returning the tag to append to the parsing result.
		Override this method to implement specialized behaviors.

		@return: The token.
		@rtype: tag
		"""
		return token
	def __repr__(self):
		return "Parse:"+`self.__fsa`