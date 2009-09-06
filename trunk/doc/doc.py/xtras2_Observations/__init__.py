#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""

In this section we have collected different jottings and observations about automatic translation.

This material emerged during the long development of the software and maturated side by side with it.

@summary: Free jottings about automatic translation.
@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
"""
class Miscellaneous:
	"""
	In this section we have collected different jottings and observations about automatic translation.

	This material emerged during the long development of the software and maturated side by side with it.

	@summary: Free jottings about automatic translation.
	"""
	class Machine_Translation:
		"""
		In this chapter you will find some material about machine translation.

		We have preferred a pragmatic approach to a theoretical one.


		The Interlingua
		===============

			When the aim is to translate from a set of languages to another,
			the technique cannot be that of establishing rules from each single language to each other:
			input must be translated from the source language to a fixed I{interlingua}, and then from
			the interlingua to the destination language.

			Also partial operations can be meaningful: comprehension and synthesis.

		The Translation
		===============

		The translation patterns
		------------------------
			The I{gloss} attached to a lemma can convey a lot of information to perform a translation.
			During the comprehension phase, sentence chunks (i.e. the terminal and non terminal symbols defined in the grammar) are mapped to interlingua expressions.
			On the other hand, the synthesis requires the interlingua to be encoded into a sentence chunk.
			Sometimes, the mapping is not trivial, and some adjustments are necessary.

			Here is an example throughout the translation process:
			The English verb "to like" (in English glossed to C{"zoykopa (P/F-s)"}) in other languages is often translated with a periphrasis, where grammatical roles are different::

				English (eng): "My mother likes flowers"
				Italian (ita): "A mia madre piacciono i fiori"
				Toki Pona (tko): "kasi kule li pona tawa mama mi"

			First of all, we want to translate from Italian into the machine interlingua: C{"zoykopanga luzimbemi ditasaw bavi"} or C{"zoykopa ditasaw bavi luzimbemi"}.
			Now we want to focus on the C{"ditasaw (P/F-s)"}: for the Italian "madre" we have the gloss C{"ditasaw {spec}, ditasaw {POS(attr/agg(poss))}…"} meaning that the focus for a C{"P/F-s"} noun must be searched matching different patterns.
			The good one is the one searching for a possessive adjective withing the attributes, transforming its gloss from an adjective to a noun.
			Also the verb shows some complications.
			The interlingua C{"zoykopa (P/F-s)"} and its transformations can accept a patient (the mother) and a focus (the flowers).
			Here, the grammatical roles of the patient and the focus in Italian are not the default ones (C{"v(P/F) {S;O}"}), they are: C{"{term;S}"}.
			To account for that, the gloss is C{"zoykopa {term;S}"}.


		@summary: Observations about machine translation.
		"""
		pass

	class Solutions:
		"""
		In this chapter you will find some jottings about the solutins we attempted or chose in our application.

		The Non Deterministic Finite-State Automaton
		============================================

		Lexica and grammars are structures difficult to use during expression parsing, therefore it's compiled into a Finite-State Automaton (FSA).
		An FSA is an oriented graph containing arcs that can be traversed without consuming tokens (I{epsilon} transitions), reduplicated transitions and states.
		To allow a deterministic traversal, these anomalies must be solved.
		To determinize an FSA epsilon and reduplicated transitions must be eliminated.
		Eliminating reduplicated states too can give an improvement in memori consumtion and efficiency.

		Epsilon closure
		---------------
			The I{epsilon closure} for a given set of states is the set of the states that can be reached traversing only epsilon transitions.
			Namely, when the parser is in the given set, it may reach any of the states in the epsilon closure without consuming any token.

		Reduction or Determinization
		----------------------------

		Basically, the states in the deterministic FSA (DSA) are grouping of I{equivalent} states in the non-deterministic FSA (NSA).

		A draft for the algorithm can be:

		>>> while nfa_states.peek():
		... 	dfa_state, nfas = nfa_states.pop() # pop
		... 	for exit, tag in transactions_from(nfas): # for all label exiting the class
		... 		k = epsilon_closure(move(nfas, exit, tag)) # states reachable using the exit
		... 		node = groupings.add_or_update(k) # create a class for it
		... 		nfa_states.add_or_update(k, ) # enqueue a state in nfa for it
		... 		dfa.add_transition(dfa_state, exit, node, tag) # create a transition


		Minimization
		------------
		For minimization, a dictionary C{adj_dict} is used to store all the adjaciencies (set of exiting labels) and the states having them.
		Then, all states having the same exits are collapsed into one.

		>>> for state, transition in transitions.itetitems()
		...		adj_dict[transitions] += state
		... for eq_set in adj_dict.values():
		...		for sec un eq_set:
		...			eq_dict[sec] = eq_set[0]

		The Expression Reader
		=====================

		The expression reader or lexer is the class used to scan a string and obtain a list of possible tokens (words).
		The problem might extend even a step further in the case of idioms, but initially this seemed a complex problem which could only be analyzed while finding a combined solution for lexing and parsing.
		>>> lxr = Lexer(properties)
		>>> lxr("Ba ca da")
		>>> [[ba, ca, da], [ba, ca da]]
		The first solution, tokenizing, presented some serious issues of computation complexity.
		The second solution, a specialized FSA gave good performances, keeping the same features.
		It also helped in verifying the implementation of the FSA, optimizing its implementation.




		Parallel lexical and syntax parsing
		===================================

		TBD.


		The Pure Python plugin
		======================
		TBD.

		See the virual documentation:
			- B{U{purepython<http://pylilac.berlios.de/doc/purepython-module.html>}:} I{A module for using pylilac on native platforms, such as IronPython.}


		@summary: Observations about I{pylilac} implementative solutions.
		"""
		pass
	pass

class Languages:
	"""
	We have used some languages, either natural or artificial, as I{case studies} to understand the needed features and as I{test scenarios} to test the implementations.

	To feed our system with grammar rules and lexicons, we had to treat in the same way languages that are very different.
	For example, we had to write simple and comprehensive rules for simple languages as L{toki pona<toki_pona>}, or more complicated rules for natural or other
	imaginary languages, but both had to be written using the same tools and the same format.

	Also, some lexical encoding like U{Ergane<http://www.travlang.com/Ergane/>} were examined, to provide a way to relate I{pylilac} to other projects targeting universal dicitonaries.

	Defining a lexicon
	==================

	For all the test languages we used the union of a common set of useful words and some words particularly important in each language.

	Standard lexicon
	----------------

	>>> block:
		  <table width="100%" class="summary" border="1" cellpadding="3" cellspacing="0">
			<tr valign="top" bgcolor="#70b0f0" class="table-header">
			  <td align="left" colspan="3"><span class="table-header">Common lexicon</span></td></tr>
			<tr valign="top" class="table-header">
			  <td align="left">
				<span class="table-header">Word</span></td>
			  <td align="left">
				<span class="table-header">English gloss</span></td>
			  <td align="left">
				<span class="table-header">Translations</span></td>
			</tr>
			<tr bgcolor="white">
			<td width="15%" class="py-output">jutakovemu</td><td><span class="summary">Cicca cicca.</span></td><td><p>Cicca cicca.</p></td>
			</tr>
			<tr bgcolor="white">
			<td width="15%" class="py-output">jutakovemu</td><td><span class="summary">Cicca cicca.</span></td><td><p>Cicca cicca.</p></td>
			</tr>
			<tr bgcolor="white">
			<td width="15%" class="py-output">jutakovemu</td><td><span class="summary">Cicca cicca.</span></td><td><p>Cicca cicca.</p></td>
			</tr>
			<tr bgcolor="white">
			<td width="15%" class="py-output">jutakovemu</td><td><span class="summary">Cicca cicca.</span></td><td><p>Cicca cicca.</p></td>
			</tr>
		  </table>


	Defining a minimal grammar
	==========================

	To define a minimal grammar and translation logics, we picked up two texts all languages should be able to comprehend, synthesize and translate.


	Standard text
	-------------

	There are some standard texts which can be used to compare languages.

	Sometimes they are use to evaluate the completeness of an artificial language, sometimes to sample some of the languages features.

	The test plan is that of finding or making a simple translation of the text, and submitting it sentence by sentend to our engine for comprehension.
	Then the result will be submitted to our engine for synthesis.

	For example, here are two texts: one is more complex and narrative, the other is more colloquial.
	For the first, see U{Omniglot<http://www.omniglot.com/babel/>} page.

			>>> Babel Text
			1. Now the whole world had one language and a common speech.
			2. As men moved eastward, they found a plain in Shinar and settled there.
			3. They said to each other, "Come, let's make bricks and bake them thoroughly."
			They used brick instead of stone, and tar for mortar.
			4. Then they said, "Come, let us build ourselves a city, with a tower that reaches to the heavens,
			so that we may make a name for ourselves and not be scattered over the face of the whole earth."
			5. But the Lord camedown to see the city and the tower that the men were building.
			6. The Lord said, "If as one people speaking the same language they have begun to do this,
			then nothing they plan to do will be impossible for them.
			7. Come, let us go down and confuse their language so they will not understand each other."
			8. So the Lord scattered them from there over all the earth, and they stopped building the city.
			9. That is why it was called Babel - because there the Lord confused the language of the whole world.
			From there the Lord scattered them over the face of the whole earth.

			>>> Small talk - idioms
			1. Hi. Hi.
			2. I would like a cup of coffee and some milk.
			3. Would you like an egg or a glass of water?
			4. Give me the egg. I don't want the glass of water.
			5. Would you like to come to the cinema tonight?
			6. I cannot come. We can meet at the station.
			7. I will come by train. I like travelling by train and I don't like driving.
			8. I am tired. I have to go.
			9. See you. Bye.


	@summary: The modeling of some natural and artificial languages.
	"""
	class toki_pona:
		"""

		U{Toki Pona<http://www.tokipona.org>} is an artificial, philosophical language designed by Sonja Elen Kisa.


		ISO codes::
			ISO 639-1: none
			ISO 639-1: art
			ISO/FDIS 639-3: tko

		Not included in ISO/FDIS 639-3, but usually C{tko} sequence is adopted.


		Lexicon
		=======

		Toki Pona lexicon is limited and essential, so it can be covered with no limitation.




		Grammar
		=======

		Toki Pona grammar is limited and essential, so it can be covered with no limitation.

		Simple sentence
		---------------

		The simplest sentence is:

				>>> <sentence> ::= <pronoun-or-subject> <predicate>

		Verbs
		-----

		Verbs only present three aspects.
				- Telic (I{kama})
				- Volitive (I{wile})
				- Potential (I{ken})

		Appendices
		==========

		Babel text
		----------

		>>> Babel Text
		... 1. ma ali li jo e toki wan en sama.
		... 2. jan ali li kama tan nasin pi kama suno, li kama lon ma Sinale, li awen lon ni.
		... 3. jan li toki e ni: "o kama! mi mute o pali e kiwen tomo, o seli e ona."
		... 4. jan mute li toki e ni: "o kama! mi mute o pali e ma tomo e tomo palisa suli. lawa pi tomo palisa li lon sewi kon.
		... 5. o nimi pi mi mute li kama suli! mi wile ala e ni: mi mute li kan ala. mi mute li lon ma ali."
		... 6. jan sewi Jawe li kama anpa, li lukin e ma tomo e tomo palisa pi jan lili mute.
		... 7. jan sewi Jawe li toki e ni: "jan ni li jo e ma wan, li jo e toki sama, li pali e tomo palisa. tenpo ni la ona mute li ken pali mute ike. mi wile tawa anpa, mi pakala e toki pi jan mute ni. o jan li sona ala e toki pi jan ante."
		... 8. jan sewi Jawe li pali e ni: jan ali li poki ala jan, li lon ma mute, li ken ala pali e ma tomo.
		... 9. nimi pi ma tomo ni li Pape tan ni: jan sewi Jawe li pakala e toki pi jan ali. tan ma tomo Pape la jan sewi Jawe li tawa e jan tawa ma mute.

		@summary: An artificial, philosophical language designed by Sonja Elen Kisa.
		"""
		pass

	class Quenya:
		"""
		Quenya is the famous artificial language used by J. R. R. Tolkien.
		The one we develop here is an unofficial version based on the direct reading of his work and on the (enourmous) corpus of resources on the internet.
		See also U{Ambar Eldaron<http://www.ambar-eldaron.com/english/>} and U{Ardalambion<http://www.uib.no/people/hnohf>}.

		ISO codes::
			ISO 639-1: none
			ISO 639-1: art
			ISO/FDIS 639-3: qya

		Quenya has a original representation, I{Tengwar}.
		The representation system chosen is a two-way transliteration, based on the traditional Latin transliteration with diacrytics.
		To preserve the possibility to estrapolate the original writing, the changes we introduced are:
			- initial I{ñoldo}/I{ngoldo}, is represented with C{"ñ"} - medially there is no possible confusion
			- I{þúle}/I{thúle} is always represented with C{"þ"}
			- initial preconsonantal I{h-} is always preserved

		Lexicon
		=======

				Quenya lexicon shows a lot of irregularities and a wide use of inflection.
				The lexicon is not sensitive to gender, but has a sofisticated system for number.
				The words for a lemma can range to almost 300 forms, owing to the use of pronominal suffixes.

				Parts of Speech
				---------------
				The parts of speech in Quenya and their categories are:
						- Nouns (C{n})
								- Number (C{number}): Singular (C{s}), Plural (C{pl}), Dual (C{d}), Partitive (C{part})
								- Case (C{case}): Nominative (C{Nom}), Genitive (C{Gen}), Possessive (C{Poss}), Dative (C{Dat}), Ablative (C{Abl}), Allative (C{All}), Locative (C{Loc}), Instrumental (C{Instr}), Respective (C{Resp})
								- Person, Number and Gender (C{person}), as possessive: C{1s}, C{2}, C{3s}, C{1d}, C{1+2+3}, exclusive I{we} (C{1+3}), C{3pl}, C{0}
						- Verbs (C{v}), with their transitiveness/arguments: intransitive (C{0}), transitive (C{Acc}), nominal predicates (C{Nom}), dative constructs (C{Acc+Dat})
								- Mode, Tense and Aspect (C{tense}): present (C{pres}), aorist (C{hab}), past (C{past}), perfect (C{pp}), future (C{fut}), imperative (C{imp}), infinite (C{inf}), passive participle (C{pass-part}), active participle (C{act-part})
								- Person, Number and Gender (C{person}): C{1s}, C{2s}, formal you C{2sf}, C{3s}, C{3sm}, C{3sf}, C{1d}, C{1+2+3}, exclusive I{we} (C{1+3}), C{2+3}, C{3pl}, plain singular (C{S}), plain plural C{pl}, plain dual C{d})
								- Object Person, Number and Gender (C{object person}): C{1s}, C{2s}, formal you C{2sf}, C{3s}, C{2+3}, C{3pl}, C{0}
						- Adjectives (C{adj}), with their arguments: closed (C{0}), dative (C{Dat})
								- Number (C{number}): Singular (C{s}), Plural (or Partitive) (C{pl}), Dual (C{d})
								- Case (C{case}): Nominative (C{Nom}), Genitive (C{Gen}), Possessive (C{Poss}), Dative (C{Dat}), Ablative (C{Abl}), Allative (C{All}), Locative (C{Loc}), Instrumental (C{Instr}), Respective (C{Resp})
								- Degree: Positive (C{0}), Relative (C{rel}), Absolute (C{abs})

				Inflections
				-----------

				Inflections in Quenya are the most complex part of the work.
				They usually consist of suffixations, sometimes in alternations between two sets of vowels and/or affixations.
				The peculiar cases of alternations between consonants will be handled with exceptions.


				Nouns
				-----
				The creation of the lexicon for nouns is based on the lemma entry form (stem-form) and, often, on the singular nominative (basic-form).
				Sometimes, some exceptions must be specified.
				In the nous system, some mobile vowels or consonants: I{toron}C{(s Nom 0)}->I{torno}C{(s Gen 0)}; they will be modeled as C{toron}.

				Verb
				----
				The verbs are lexicalized by their stem.
				There are some interesting but limited exceptions for I{etymological} reasons.

				Adjectives
				----------
				Adjectives are in two classes:



		Grammar
		=======

				The grammar is as much complicated as that of natural languages.
				There are concordance rules
				Word order is pretty free, besides some fixed structures.

				Basic clause
				------------

				The subject and the object can, with some restriction, be incorporated in the verb as suffixes.
				If the subject is not incorporated, the object must not be incorporated as well and usually immediately follow the verb.
				The indirect complements can also precede the verb, while the other complements more frequently follow.
				Indirect complements and object tend to stay close to the verb
				We will model the most common orders, leaving the possibility to further extensions.


				Basic clause
				~~~~~~~~~~~~
				The first distinction is made by the verb argument structure:
					1. intransitive verbs
					2. transitive verbs
					3. intransitive indirect verbs
					4. transitive indirect verbs

				For example, indicrect verbs can be those that require a dative case as indirect complement.
				We will use a blank to express that order is important. When two or more symbols are grouped together, they can sequence in free order.

				    >>> <clause> ::= (<Vs> | <S V>) <C>*
						Clause with intransitive verb.
				    >>> <clause> ::= (<Vso> | <VsO> | <S V O>) <C>*
						Clause with transitive verb.
				    >>> <clause> ::= (<VsD> | <SVD>) <C>*
						Clause with intransitive dative verb.
				    >>> <clause> ::= (<VsoD> | <VsD O> | <SV O D>) <C>*
						Clause with transitive dative verb.

				Some indirect complements, such as the locative complement, can also be a generic circumstantial complements:

				    >>> <clause> ::= (<VsoL> | <VsL O> | <SVL O> | <SV O L>) <-L>*
						Clause with transitive locative verb.


				Nominal predicate
				-----------------
				Nominal clauses have a more fixed structure, ending with the copula:

				    >>> <clause> ::= (<N Vs> | <SN V>) <C>*
				    >>> <clause> ::= (<ND Vs> | <SND V>) <C>*

				For third persons, usually the copula is understood:

				    >>> <clause> ::= <S N> <C>*

				Locative construct
				------------------

						>>> <sentence> ::= ... <locative-complement>(n){* Loc}
						... Ean coasse.


				Allative construct
				------------------

						>>> <sentence> ::= ... <allative-complement>(n){* All}
						... Lenden ostonna.

		Appendices
		==========

		Babel text
		----------

		>>> Babel Text
		... 1. Ilya ambar sinte lambe er ar yuhtanes quetie er.
		... 2. Ar martane, lelyientasse rómenna, i hirnente nanda nóresse Shinar; ar marnante tasse.
		... 3. Ar quentante ilenilenen, "Lel, karealve telar, ar urtealve te ilyave." Ar arnente telar ve ondo, ar (*bitumen*) arnente ve (*mortar*).
		... 4. Ar quentente, "Lel, karealve osto, ar mindon, yo telme na menelenna, ar karealve esselva; ikoi ú rernar nealve or ilya ambarwa."
		... 5. Ar Eru nu-lende vélienna i-osto ar i-mindon, ya i-atanion híni akarnente.
		... 6. Ar Eru quente, "Véla, nante er lie, ar ilyar arante er lambe; ar sina na ya yestanente; ar sí ú avatanar nuvante (*any*) karyiello, yan noante.
		... 7. Lel, nu-lendean, ar tasse handútean lambenta, ikoi ú hanyeante ilenilenwa quentie."
		... 8. Take Eru rerne te pallave tallo or ambar; ar pustanente kaarie i-osto.
		... 9. Take esserwa yenne Babel, ike Eru tasse handunte i-lambe ilya ambarwa; ar tallo Eru rerne te or i-ambar.



		@summary: The most famous artificial language in those developed by J. R. R. Tolkien.

		"""
		pass

	pass
