#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module for the generation of inflected forms.

Inflection is the change of form that words undergo to mark such distinctions as those of case, gender, number, tense, person, mood, or voice.
For example, in the Quenya fragment I{"lassi aldaron"}, meaning I{«leaves of trees»}, the single words refer to the lemmas I{"lasse"}, I{«leaf»} and I{«alda»}, I{«tree»}.
Again, the same fragment in latin would be: I{"foliae arborum"}, from lemmas I{"folia"} and I{"arbor"}.

Structure of inflection
=======================
G{classtree Inflection, Transform}

Inflections
-----------
	Inflexions accept lemmas satisfying some conditions and route them to the appropriate forms.

	Example of inflexions can be:
		- the Quenya noun declension
		- the Latin I (or I{a}) declension, to which I{"folia"} belongs

	While modeling languages, one of two apporaches may be chosen to model inflection:
		- One inflection for all, with dedicated transforms on occasion.
		- Several inflections with transforms usually different.

		For languages where inflection is more analytic, usually the former fits better; it is the case of Quenya noun declensions.
		When inflection is more syntetic and varies throughout the forms for different classes of words, the latter is easier; this is the case of Latin.

		For instance, while the genitive forms I{"lasseo"} and I{"aldo"} end in I{"-o"} for both Quenya I{"lasse"} and I{"alda"} and only need a slight adjustment; in Latin the genitive forms I{"foliae"} and I{"arboris"} are systematically different, and must be separed at inflection level.

Transforms
----------
	Transforms accept word forms satisfying some conditions and define the generation of other words forms.
	Examples for transforms can be:
		- the lengthening and suffixation for Quenya present forms
		- the suffixation of "-is" for the singular genitive in Latin III declension
	In Quenya: from the verb stem I{"cava"} the present form I{"cávea"} can be seen as applying different mutation steps, one in the middle and one at the end of the stem.
	It can be done by applying three mutation steps to the stem:
		1. alternation (apophony) of the last short vowel I{"-a-"} and I{"-á-"}, giving the intermediate form I{"cáva"}*
		2. alternation of the final I{"-a"} and I{"-e"}, giving the intermediate form I{"cáve"}*
		3. suffixation of I{"-a"}, giving the final form I{"cávea"}
	In Latin, on the other hand, transforms are usually easier, because lemmas are separated at a higher level: we can obtain from I{"arboris"} I{"arbor"} by a single step.

Mutation steps
--------------
	Mutation steps define the steps in transforms.

	Steps are tuples:
		>>> (search, substitution, mandatory)

	Search and substitution strings are U{regular expressions<http://www.regular-expressions.info>}.

	All the occurrences of the C{search} string in the base form are replace with the C{substitution}.
	If C{mandatory} is C{True} and there are no occurrences of the C{search} string the operation will abort.
	See the L{call<Inflections.__call__>} method for details on execution.

	In the example above, the steps from I{"cava"} to I{"cávea"} can be seen as follows:
		1. C{a(?=[^aeiouáíéóú][yw]?[au]?$)} S{->} C{á}
		2. C{a$} S{->} C{e}

Complete example
----------------

	>>> decl = Inflections()
	Instantiate inflections
	>>> decl1 = decl.create_inflection("n", u"a$")
	Declare inflection for nouns ending in “-a”
	>>> decl1.create_transform(("s","N"), BASED_ON_ENTRY_FORM)
	Declare a transform identical to the canonical form of lemma for singular nominative.
	>>> decl1G = decl1.create_transform(("s","G"))
	Using a default, declare a transform starting from canonical form of lemma for singular genitive.
	>>> decl1G.append_step(u"a$", u"ae", True)
	Declare a mandatory step for “-ae” suffixation.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.6
"""

__docformat__ = "epytext en"

import re
from lexicon import Word, Lexicon, CategoryFilter, DEFECTIVE
from utilities import SortedDict, Utilities

BASED_ON_ENTRY_FORM = "-"
"""
It indicated a transform will take as initial form the entry form of the lemma.
It is used for the C{based_on} parameter in L{Inflection.create_transform}.
"""

class TransformSyntaxError(ValueError):
	"""
	Exception to indicate that the definition of a transform is syntactically malformed and can not be compiled.

	@see: L{Regular Expressions <re>}
	"""
	pass
class InflectionError(RuntimeError):
	"""
	Exception to indicate that no definitions suit the given form.
	"""
	pass



class Inflections(object):
	"""
	A collection of inflections.
	It is used to collect, generate and call instances of L{Inflection}.
	"""
	def __init__(self):
		"""
		Initialize an empty collection of instances of L{Inflection}.
		"""
		self.__inflections = []

	def create_inflection(self, p_o_s, condition = None, lemma_categories = None):
		"""
		Create a new instance of L{Inflection} and append it.

		@param p_o_s: The part of speech accepted by the inflection.
		@type p_o_s: str
		@param condition: The regular expression filtering the entry forms accepted by the inflection.
		@type condition: unicode
		@param lemma_categories: The categories of the lemmas accepted by the inflection.
		@type lemma_categories: tuple of str/CategoryFilter
		@return: The new inflection.
		@rtype: Inflection
		@raise TransformSyntaxError: If the condition can not be compiled.
		"""
		inflection = Inflection(p_o_s, condition, lemma_categories)
		self.__inflections.append(inflection)
		return inflection

	def __call__(self, lemma, words = ()):
		"""
		Find a suitable L{Inflection} and call it, generating the inflection table for the lemma, preserving the given words.

		@param lemma: The lemma to inflect.
		@type lemma: Lemma
		@param words: The inflected forms (usually a list of irregular forms).
		@type words: sequence of Word
		@return: The inflection table of the lemma.
		@rtype: utilities.SortedDict
		@raise InflectionError: If no inflection accept the lemma.
		@raise TransformSyntaxError: If the substitution pattern in some step can not be compiled.
		"""
		for inflection in self.__inflections:
			if inflection.accept(lemma):
				return inflection(lemma, words)
		raise InflectionError("can not inflect %s" % `lemma`)

class Inflection(object):
	"""
	A class to define the inflected forms for a class of lemmas.
	"""
	def __init__(self, p_o_s, condition, lemma_categories):
		"""
		Create a new instance of inflection.

		@param p_o_s: The part of speech accepted by the inflection.
		@type p_o_s: str
		@param condition: The regular expression filtering the entry forms accepted by the inflection.
		@type condition: unicode
		@param lemma_categories: The categories of the lemmas accepted by the inflection.
		@type lemma_categories: tuple of str/CategoryFilter
		@raise TransformSyntaxError: If the condition can not be compiled.
		@note: In the process of modeling inflections, use the L{Inflections.create_inflection} method instead.
		"""
		self.p_o_s = p_o_s
		if condition == u".":
			condition = None
		cco = None
		if condition:
			if not isinstance(condition, unicode):
				raise TypeError("%s is not Unicode" % repr(condition))
			try:
				cco = re.compile(condition, re.IGNORECASE)
			except Exception, e:
				raise TransformSyntaxError("can not compile %s: %s" % (`condition`, `e`))
		self.condition = condition
		self.lemma_categories = lemma_categories
		self.__cco = cco
		self.__forms = SortedDict() #of []

	def create_transform(self, categories, based_on = BASED_ON_ENTRY_FORM, condition = u".", lemma_categories = None, steps = ()):
		"""
		Create a new instance of L{transform<Transform>} and append it.
		The transform will generate a word form for the given categories based on the given base form if the lemma respects the conditions.

		@param categories: The categories of the word generated by the transform.
		@type categories: tuple of str
		@param based_on: The base form to start from.
		@type based_on: tuple of str/CategoryFilter/L{BASED_ON_ENTRY_FORM}
		@param condition: The regular expression filtering the base forms accepted by the transform.
		@type condition: unicode
		@param lemma_categories: The categories of the lemmas accepted by the transform.
		@type lemma_categories: tuple of str/CategoryFilter
		@param steps: The steps to append at the beginning of the transform.
		@type steps: sequence of C{(search, substitution, mandatory)} tuples
		@return: The new transform.
		@rtype: Transform
		@raise TransformSyntaxError: If the condition can not be compiled.
		"""
		if not isinstance(categories, tuple):
			raise TypeError(categories)
		for c in categories:
			if not isinstance(c, str): #and not isinstance(c, unicode)?
				raise TypeError(c)
		t = Transform(self, based_on , condition, lemma_categories, steps)
		if categories in self.__forms:
			form = self.__forms[categories]
		else:
			form = []
			self.__forms[categories] = form
		form.append(t)
		return t

	def iter_forms(self):
		"""
		Return an iterator on the inflection forms.

		@rtype: iterator of tuple (str, SortedDict)
		"""
		return self.__forms.iteritems()

	def do_form(self, lemma, categories, words = ()):
		"""
		Generate the specified inflected form for the lemma, preserving the given words.
		When a word form is provided, it is returned; when not, it is generated applying the appropriate inflection form.

		@param lemma: The lemma to inflect.
		@type lemma: Lemma
		@param categories: The categories of the word to generate.
		@type categories: tuple of str/CategoryFilter
		@param words: The inflected forms (usually a list of irregular forms).
		@type words: sequence of Word
		@return: The inflected word form for the lemma.
		@rtype: Word
		@raise InflectionError: If the inflection form can not accept the lemma respecting mandatory steps.
		@raise TransformSyntaxError: If the substitution pattern in some step can not be compiled.
		"""
		word = None
		#Find is there is a default form
		for w in words:
			if CategoryFilter.test(categories, w.categories):
				word = w
				break
		if word is None:
			#Get the form == dict of transforms
			form = self.__forms[categories]
			s = None
			#Iterate over transforms
			for transform in form:
				s = transform(lemma, words)
				if s is not None:
					break
			if s is None:
				raise InflectionError("Inflection can not generate %s for lemma '%s'" % (Utilities.tuple_str(categories), `lemma`))
			word = Word(s, lemma, categories)
		return word

	def accept(self, lemma):
		"""
		Verify if the inflection accepts a lemma.

		@param lemma: The lemma to verify.
		@type lemma: Lemma
		@return: True if the inflection can accept the lemma.
		@rtype: bool
		"""
		cco = self.__cco
		if self.p_o_s == lemma.p_o_s and (cco is None or cco.search(lemma.entry_form)) and CategoryFilter.test(self.lemma_categories, lemma.categories):
			return True
		else:
			return False

	def __call__(self, lemma, words=()):
		"""
		Generate the inflection table for the lemma, preserving the given words.
		When a word form is provided, it is used; when not, it is generated applying the appropriate inflection form.
		For each inflection form, if it is not defective, a word is generated and appended.

		@see: do_form
		@param lemma: The lemma to inflect.
		@type lemma: Lemma
		@param words: The inflected forms (usually a list of irregular forms).
		@type words: sequence of Word
		@return: The inflection table of the lemma.
		@rtype: utilities.SortedDict
		@raise InflectionError: If any inflection forms can not accept the lemma respecting mandatory steps.
		@raise TransformSyntaxError: If the substitution pattern in some step can not be compiled.
		"""
		table = SortedDict()
		for categories in self.__forms.iterkeys():
			word = self.do_form(lemma, categories, words)
			if word.form <> DEFECTIVE:
				table[word.categories] = word
		return table

	def __str__(self):
		"""
		Return a short string representation.

		@rtype: str
		"""
		s = [self.p_o_s]
		if self.condition:
			s.append(self.condition)
		if self.lemma_categories:
			s.append(Utilities.tuple_str(self.lemma_categories))
		return " ".join(s)


class Transform(object):
	"""
	A class to define the creation of an inflected forms for a class of base forms.

	A transform is a sequence of mutation steps.

	Mutation steps
	==============

	Steps are modeled as tuple:
		>>> (search, substitution, mandatory)

	All the occurrences of the C{search} string in the base form are replace with the C{substitution}.
	If C{mandatory} is C{True} and there are no occurrences of the C{search} string the operation will abort.
	See the L{call<__call__>} method for details on execution.

	If one of the initial regular expressions is not satisfied and the step is not defined as mandatory, it's neglected and the execution goes on to the next step.
	In this example, the second step might be seen as optional, since stems not ending in «I{-a}» simply go on to the last step : «I{hir}» S{->} «I{híra}» .
	"""
	def __init__(self, parent_inflection, based_on, condition, lemma_categories, steps = ()):
		"""
		Create a new instance of L{transform<Transform>}.

		@param parent_inflection: The inflection the transform belongs to.
		@type parent_inflection: Inflection
		@param based_on: The base form to start from.
		@type based_on: tuple of str/CategoryFilter/L{BASED_ON_ENTRY_FORM}
		@param condition: The regular expression filtering the base forms accepted by the transform.
		@type condition: unicode
		@param lemma_categories: The categories of the lemmas accepted by the transform.
		@type lemma_categories: tuple of str/CategoryFilter
		@param steps: The steps to append at the beginning of the transform.
		@type steps: sequence of C{(search, substitution, mandatory)} tuples
		@raise TransformSyntaxError: If the condition can not be compiled.
		@note: For internal use only. Use the L{Inflection.create_transform} method instead.
		"""
		if not isinstance(condition, unicode):
			raise TypeError("%s is not Unicode" % repr(condition))
		self.__parent = parent_inflection

		self.based_on = based_on
		self.condition = condition
		self.lemma_categories = lemma_categories
		try:
			self.__cco = re.compile(condition, re.IGNORECASE)
		except Exception, e:
			raise TransformSyntaxError("can not compile %s: %s" % (`condition`, `e`))
		self.__steps = []
		if steps:
			for step in steps:
				if len(step)<3:
					self.append_step(step[0], step[1])
				else:
					self.append_step(step[0], step[1], step[2])

	def append_step(self, search, substitution, mandatory = False):
		"""
		Append a step.

		@see: Substitution in regular expressions.
		@param search: The regular expression that the step search for.
		@type search: unicode
		@param substitution: The substitution pattern.
		@type substitution: unicode
		@param mandatory: True if the step must always be applied.
		@type mandatory: bool
		@raise TransformSyntaxError: If the search string can not be compiled.
		"""
		if not isinstance(search, unicode):
			raise TypeError("%s is not Unicode" % repr(search))
		if not isinstance(substitution, unicode):
			raise TypeError("%s is not Unicode" % repr(substitution))
		try:
			cre = re.compile(search, re.IGNORECASE)
		except Exception, e:
			raise TransformSyntaxError("can not compile %s for %s: %s" % (`substitution`, `search`, e.message))
		self.__steps.append((search, cre, substitution, mandatory))

	def iter_steps(self):
		"""
		Return an iterator over the steps.
		@rtype: iterator of C{(search, substitution, mandatory)} tuples
		"""
		for search, cre, substitution, mandatory in self.__steps:
			yield (search, substitution, mandatory)

	def __call__(self, lemma, words = ()):
		"""
		Apply the transform to the lemma, preserving the given words.
		When a word form is provided, it is returned; when not, it is generated applying the appropriate inflection form.
		If the transform does not accept the lemma or violates any mandatory step, nothing is returned.

		@param lemma: The lemma to inflect.
		@type lemma: Lemma
		@param words: The inflected forms (usually a list of irregular forms).
		@type words: sequence of Word
		@return: The inflected form (string) for the lemma.
		@rtype: str
		@raise TransformSyntaxError: If the substitution pattern in some step can not be compiled.
		"""
		if not CategoryFilter.test(self.lemma_categories, lemma.categories):
			return None
		if self.based_on == BASED_ON_ENTRY_FORM:
			s = lemma.entry_form
		else:
			s = None
			for w in words:
				if CategoryFilter.test(self.based_on, w.categories):
					s = w.form
					break
			if not s:
				w = self.__parent.do_form(lemma, self.based_on, words)
				s = w.form
		if not s:
			return None
		if DEFECTIVE == s:
			return DEFECTIVE #propagation
		if not self.__cco.search(s):
			return None
		for r, cre, substitution, mandatory in self.__steps:
			if cre.search(s):
				try:
					s = cre.sub(substitution, s)
				except:
					raise TransformSyntaxError("Invalid form %s for %s" % (`substitution`, `r`))
			elif mandatory:
				return None
		return s
