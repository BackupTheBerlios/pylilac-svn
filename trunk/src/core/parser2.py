#!/usr/bin/python

"""
A module for parsing, i.e. traversing and tagging a token sequence using a compiled grammar.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""

__docformat__ = "epytext en"

from optiontree import OptionTree

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
	It encapsulates an FSA, the I{match} logics and the I{process} logics.
	"""
	def __init__(self, fsa, match = None, process = None):
		self.__fsa = fsa
		if match is None:
			self.__match = _eq
		else:
			self.__match = match
		if process is None:
			self.__process = _sec_elem
		else:
			self.__process = process
	
	def next_states(self, start, token):
		"""
		Evaluate S{delta}(C{start}, C{label}).

		@param start: An existing state. 
		@param token: The token to match.
		@return: A set of states reachable by the transitions having the given label.
		@raise StateError: Fired if the state does not exist.
		"""
		return [end for l, end, t in self.transitions_from(start) if self.__match(l, token)]
	
	def __call__(self, tokens):
		def parse_from(tokens, index, state):
			output = OptionTree()
			expected_final = index == len(tokens)
			is_final = state in self.__fsa.get_final()
			if expected_final:
				if is_final:
					return output
				else:
					raise ExpectedStopError(tokens[:index+1], state)
			transitions = self.__fsa.transitions_from(state)
			token = tokens[index]
			matching = [(label, end, tag) for label, end, tag in transitions if self.__match(label, token)]
			if len(matching) == 0:
				raise ParseError(tokens[:index+1], state)
			
			m_pe = None
			for label, end, tag in matching:
				try:
					following = parse_from(tokens, index + 1, end) 
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
		
		return parse_from(tokens, 0, self.__fsa.get_initial())
	
	
	def __repr__(self):
		return repr(self.__fsa)


def __test():
	p = Parser("FSA")
	print p


if __name__ == "__main__":
	__test()


