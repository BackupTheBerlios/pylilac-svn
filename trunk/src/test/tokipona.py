#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A module to create Tokipona lect file.
"""
from pylilac.core.lect import Lect
from pylilac.core.grammar import Grammar
from pylilac.core.bnf import Reference, POSITIVE_CLOSURE, KLEENE_CLOSURE, OPTIONAL_CLOSURE
from pylilac.core.lexicon import Lexicon, Particle, Word, Lexeme, WordCategoryFilter, WordFilter, CategoryFilter


def prepare():
	w = build_words()

	l = Lect("tko")
	l.name = u"toki pona"
	l.english_name = "Toki Pona"
	l.append_p_o_s ("v", ("arguments",), ())
	l.append_p_o_s ("n", (), ())
	l.append_p_o_s ("mod", (), ())
	l.append_p_o_s ("prep", (), ())
	l.append_p_o_s ("sep", (), ())
	l.append_p_o_s ("conj", (), ())
	l.append_p_o_s ("interj", (), ())
	l.append_p_o_s ("aux", (), ())
	l.append_p_o_s ("cont", (), ())
	l.lexicon = build_lexicon(w, l.properties)
	l.grammar = build_grammar(w)
	l.properties["capitalization"] = 0
	return l

def run():
	def show(s):
		print
		print s
		for i, x in enumerate(l.read(unicode(s))):
			print "%d. " % i, x	
	l = prepare()
	print l.grammar
	l.save("test/tko.lct", False)

	show("mi moku")
#	show("telo li pona")
	show("ona li lukin e pipi")
	show("pipi li lukin li unpa")
	show("mi moku e kili e telo")

	show("ma ali li jo e toki wan en sama")
	show("jan ali li awen lon ni")
	show("jan li toki e ni")
	show("jan ali li kama tan nasin pi kama suno")
	show("jan ali li kama lon ma lili")
	#show("o kama")
	show("mi mute pali e kiwen tomo")
	show("jan mute li toki e ni")
	#show("o kama! mi mute o pali e ma tomo e tomo palisa suli")
	#show("lawa pi tomo palisa li lon sewi kon")
	#show("o nimi pi mi mute li kama suli! mi wile ala e ni: mi mute li kan ala. mi mute li lon ma ali")
	#show("jan sewi Jawe li kama anpa, li lukin e ma tomo e tomo palisa pi jan lili mute")
	#show("jan sewi Jawe li toki e ni: "jan ni li jo e ma wan, li jo e toki sama, li pali e tomo palisa. tenpo ni la ona mute li ken pali mute ike. mi wile tawa anpa, mi pakala e toki pi jan mute ni. o jan li sona ala e toki pi jan ante")
	#show("jan sewi Jawe li pali e ni: jan ali li poki ala jan, li lon ma mute, li ken ala pali e ma tomo")
	#show("nimi pi ma tomo ni li Pape tan ni: jan sewi Jawe li pakala e toki pi jan ali. tan ma tomo Pape la jan sewi Jawe li tawa e jan tawa ma mute")

	print l.lexicon.check(l)

def build_word(w0):
	if w0[2] == "sep":
		return Word(unicode(w0[0]), Particle(unicode(w0[0]), w0[1], "sep"), ())
	else:		
		pos = w0[2]
		cat = ()
		if pos == "vt":
			pos = "v"
			cat = ("tr",)
		if pos == "vi":
			pos = "v"
			cat = ("intr",)
		return Word(unicode(w0[0]), Lexeme(unicode(w0[0]), w0[1], pos, cat, w0[3]))

def build_words():
	w = {}
	w["a_interj"] = ("a", 1, "interj", "Kavemu.")	#(well)	It means "It's the way it is!".
	w["akesi_n"] = ("akesi", 1, "n", "byefegi")	#(reptile)
	w["akesi_n_1"] = ("akesi", 2, "n", "byekimi")	#(amphibian)
	w["ala_n"] = ("ala", 1, "n", "jutomi")	#(nothing)
	w["ala_mod"] = ("ala", 2, "mod", "jutomo, jutamu")	#(no, not)	Like all [mod_1]s, its translation depends whether it's an <adjective> or an <adverb>.
	w["ala_interj"] = ("ala", 3, "interj", "Jutamemu")	#(no!)
	w["ale_n"] = ("ale", 1, "n", "bikumi")	#(everything)
	w["ale_mod"] = ("ale", 2, "mod", "bikumo")	#(all)
	w["ali_n"] = ("ali", 1, "n", "bikumi")	#(everything)
	w["ali_mod"] = ("ali", 2, "mod", "bikumo")	#(all)
	w["anpa_n"] = ("anpa", 1, "n", "cenfagaymi")	#(bottom)
	w["anpa_mod"] = ("anpa", 2, "mod", "cenfagaymo")	#(bottom)
	w["anpa_mod_1"] = ("anpa", 3, "mod", "dadelo, dadela")	#(low)	Like all [mod_2]s, its translation depends whether it's attributive or used predicatively.
	w["ante_n"] = ("ante", 1, "n", "fesoni")	#(difference)
	w["ante_mod"] = ("ante", 2, "mod", "feso")	#(different)
	w["ante_vt"] = ("ante", 3, "vt", "fesapa")	#(change, alter, modify)
	w["ante_cont"] = ("ante", 4, "cont", "Daydapoma.")	#(otherwise, or else)
	w["anu_conj"] = ("anu", 1, "conj", "daytesye")	#(or)
	w["awen_mod"] = ("awen", 1, "mod", "dunkavo")	#(stable)
	w["awen_mod_1"] = ("awen", 2, "mod", "kawbeso")	#(stationary)
	w["awen_mod_2"] = ("awen", 3, "mod", "zogoso")	#(in place)	anti-passive [P-s] [+F]
	w["awen_vt"] = ("awen", 4, "vt", "zogasa")	#(keep)
	w["awen_vi"] = ("awen", 5, "vi", "zogisa")	#(stay)
	w["e_sep"] = ("e", 1, "sep", "")	#()
	w["en_conj"] = ("en", 1, "conj", "sye")	#(and)
	#w["esun_n"] = ("esun", 1, "n", "doykigi")	#(shop)
	w["ijo_n"] = ("ijo", 1, "n", "byezumi")	  #(object)
	w["ijo_mod"] = ("ijo", 2, "mod", "[ijo]")	#(of something)
	w["ijo_vt"] = ("ijo", 3, "vt", "byezumapa")	#(objectify)
	w["ike_n"] = ("ike", 1, "n", "cafomoni")	#(negativity, badness, evil)
	w["ike_mod"] = ("ike", 2, "mod", "cafomo")	#(bad, negative, wrong, evil, overly complex, (figuratively) unhealthy)
	w["ike_vt"] = ("ike", 3, "vt", "cafomapa")	#(to make bad, to worsen, to have a negative effect upon)
	w["ike_vi"] = ("ike", 4, "vi", "cafoma")	#(to be bad)
	w["ike_interj"] = ("ike", 5, "interj", "Cafomemu.")	#(oh dear! woe! alas!)
	w["ilo_n"] = ("ilo", 1, "n", "bufusi")	#(tool)
	w["ilo_n_1"] = ("ilo", 2, "n", "tobisi")	#(device)
	w["insa_n"] = ("insa", 1, "n", "fucesi")	#(stomach)
	w["insa_n_1"] = ("insa", 2, "n", "zizogi")	#(inside)
	w["insa_mod"] = ("insa", 3, "mod", "zizogaymo")	#(inner, internal)
	w["jaki_n"] = ("jaki", 1, "n", "cinjuvi")	#(dirt, pollution, garbage, filth)
	w["jaki_mod"] = ("jaki", 2, "mod", "cinjuvo")	#(dirty, gross, filthy)
	w["jaki_vt"] = ("jaki", 3, "vt", "cinjuvapa")	#(pollute, dirty)
	w["jaki_interj"] = ("jaki", 4, "interj", "[jaki]")	#(ew! yuck!)
	w["jan_n"] = ("jan", 1, "n", "begi")	#(person, people, human, being, somebody, anybody)
	w["jan_mod"] = ("jan", 2, "mod", "becami")	#(human, somebody's, personal, of people)
	w["jan_mod"] = ("jan", 3, "mod", "bexaso")	#(human, somebody's, personal, of people)
	w["jan_vt"] = ("jan", 4, "vt", "begapa")	#(personify, humanize, personalize)
	w["jelo_mod"] = ("jelo", 1, "mod", "fezigo")	#(yellow, light green)
	w["jo_n"] = ("jo", 1, "n", "ximunzoponi")	#(having)	ximunza -> ximunzopa (to possess)
	w["jo_vt"] = ("jo", 2, "vt", "ximunza")	#(have, contain)
	w["jo_kama"] = ("jo", 3, "aux", "ximumba")	#(receive, get, take, obtain)
	w["kala_n"] = ("kala", 1, "n", "byebomi")	#(fish, sea creature)
	w["kalama_n"] = ("kalama", 1, "n", "foyxogi")	#(sound, noise, voice)
	w["kalama_vt"] = ("kalama", 2, "vt", "byedinbisiga")	#(sound, ring, play (an instrument))	byedinbisi: musical instrument, byedinbisiga: play an instrument
	w["kalama_vi"] = ("kalama", 3, "vi", "xonfoyxogona")	#(make noise)
	w["kama_n"] = ("kama", 1, "n", "kavenvi")	#(event, happening, chance, arrival, beginning)
	w["kama_mod"] = ("kama", 2, "mod", "[kama]")	#(coming, future)
	w["kama_vt"] = ("kama", 3, "vt", "zogapa")	#(bring about, summon)
	w["kama_vi"] = ("kama", 4, "vi", "zogumba")	#(come, become, arrive, happen, pursue actions to arrive to (a certain state), manage to, start to)
	w["kama_vi"] = ("kama", 5, "aux", "???")	#(come, become, arrive, happen, pursue actions to arrive to (a certain state), manage to, start to)
	w["kasi_n"] = ("kasi", 1, "n", "byebosi")	#(plant, leaf, herb, tree, wood)
	w["ken_n"] = ("ken", 1, "n", "dovemi")	#(possibility, ability, power to do things, permission)
	w["ken_vt"] = ("ken", 2, "vt", "dovanza")	#(make possible, enable, allow, permit)
	w["ken_vi"] = ("ken", 3, "aux", "dovu")	#(can, is able to, is allowed to, may, is possible)
	w["ken_cont"] = ("ken", 4, "cont", "Tamemu")	#(it is possible that)
	w["kepeken_vt"] = ("kepeken", 1, "vt", "busega")	#(use)	busa --> busega....affect by something
	w["kepeken_prep"] = ("kepeken", 2, "prep", "busege")	#(with)
	w["kili_n"] = ("kili", 1, "n", "babemi")	#(fruit, pulpy vegetable, mushroom)
	w["kin_mod"] = ("kin", 1, "mod", "kedapoge")	#(also, too, even, indeed (emphasizes the word(s) before it))
	w["kiwen_n"] = ("kiwen", 1, "n", "xami")	#(hard thing, rock, stone, metal, mineral, clay)
	w["kiwen_mod"] = ("kiwen", 1, "mod", "cayculo")	#(hard, solid, stone-like, made of stone or metal)
	w["kiwen_mod"] = ("kiwen", 2, "n", "byejavi cayculo")	#(hard, solid, stone-like, made of stone or metal)
	w["ko_n"] = ("ko", 1, "mod", "caydelo")	#(semi-solid or squishy substance, e.g. paste, powder, gum)
	w["ko_n"] = ("ko", 2, "n", "byejavi caydelo")	#(semi-solid or squishy substance, e.g. paste, powder, gum)
	w["ko_n"] = ("ko", 1, "n", "jaycapi")	#(semi-solid or squishy substance, e.g. paste, powder, gum)
	w["kon_n"] = ("kon", 1, "n", "dafepi")	#(wind)
	w["kon_n_1"] = ("kon", 2, "n", "dajavi")	#(air, wind, smell, soul)
	w["kon_mod"] = ("kon", 3, "mod", "dajavi")	#(air-like, ethereal, gaseous)
	w["kule_n"] = ("kule", 1, "n", "zigoni")	#(colour, paint)
	w["kule_mod"] = ("kule", 2, "mod", "zigo")	#(colourful)
	w["kule_vt"] = ("kule", 3, "vt", "zigapa")	#(colour, paint)
	w["kulupu_n"] = ("kulupu", 1, "n", "bekujagi")	#(group, community, society, company, people)
	w["kulupu_n_1"] = ("kulupu", 2, "n", "zenjagi")	#(group, community, society, company, people)
	w["kulupu_mod"] = ("kulupu", 3, "mod", "finbeso")	#(communal, shared, public, of the society)
	w["kute_mod"] = ("kute", 1, "mod", "foykivono")	#(auditory, hearing)
	w["kute_vt"] = ("kute", 2, "vt", "foykiva")	#(listen)
	w["kute_vt_1"] = ("kute", 3, "vt", "foykivinza")	#(listen)
	w["la_sep"] = ("la", 1, "sep", "[la]")	#((between adverb or phrase of context and sentence))
	w["lape_n"] = ("lape", 1, "n", "kunkepa")	#(vi sleep, rest)
	w["lape_mod"] = ("lape", 2, "mod", "kunkepa")	#(sleeping, of sleep)
	w["laso_mod"] = ("laso", 1, "mod", "dazigo")	#(blue, blue-green)
	w["lawa_n"] = ("lawa", 1, "n", "cesi")	#(head, mind)
	w["lawa_mod"] = ("lawa", 2, "mod", "badakumo")	#(main, leading, in charge)
	w["lawa_mod"] = ("lawa", 3, "mod", "busasoso")	#(main, leading, in charge)
	w["lawa_vt"] = ("lawa", 4, "vt", "dubusa")	#(lead, control, rule, steer)
	w["len_n"] = ("len", 1, "n", "twacapi")	#(clothing, cloth, fabric)
	w["lete_n"] = ("lete", 1, "n", "fedelo")	#(cold)
	w["lete_mod"] = ("lete", 2, "mod", "jufecalaposo")	#(cold, uncooked)
	w["lete_vt"] = ("lete", 3, "vt", "fedelapa")	#(cool down, chill)
	w["li_sep"] = ("li", 1, "sep", "[li]")	#((between any subject except mi and sina and its verb)
	w["lili_mod"] = ("lili", 1, "mod", "fomo")	#(small, little, young, a bit, short, few, less)
	w["lili_vt"] = ("lili", 2, "vt", "fomapa")	#(reduce, shorten, shrink, lessen)
	w["linja_n"] = ("linja", 1, "n", "zezumi")	#(long, very thin, floppy thing, e.g. string, rope, hair, thread, cord, transform)
	w["linja_n"] = ("linja", 2, "n", "zezopi")	#(long, very thin, floppy thing, e.g. string, rope, hair, thread, cord, transform)
	w["linja_n"] = ("linja", 1, "mod", "twadelo")	#(long, very thin, floppy thing, e.g. string, rope, hair, thread, cord, transform)
	w["lipu_n"] = ("lipu", 1, "n", "dejumi")	#(flat and bendable thing, e.g. paper, card, ticket)
	w["lipu_n"] = ("lipu", 2, "n", "defimi")	#(flat and bendable thing, e.g. paper, card, ticket)
	w["loje_mod"] = ("loje", 1, "mod", "zozigo")	#(red)
	w["lon_vi"] = ("lon", 1, "vi", "kava")	#(be there, be present, be real/true, exist, be awake)
	w["lon_vi"] = ("lon", 2, "vi", "kunkola")	#(be there, be present, be real/true, exist, be awake)
	w["lon_prep"] = ("lon", 3, "vt", "zoga")	#(be (located) in/at/on)
	w["lon_prep"] = ("lon", 4, "prep", "zoge")	#(be (located) in/at/on)
	w["luka_n"] = ("luka", 1, "n", "twecesi")	#(hand, arm)
	w["luka_n_1"] = ("luka", 2, "n", "zicesi")	#(hand, arm)
	w["lukin_mod"] = ("lukin", 1, "mod", "kivono")	#(visual(ly))
	w["lukin_vt"] = ("lukin", 2, "vt", "kiva")	#(see, look at, watch, read)
	w["lukin_vt_1"] = ("lukin", 3, "vt", "kivinza")	#(see, look at, watch, read)
	w["lukin_vi"] = ("lukin", 4, "vi", "kivimba")	#(look, watch out, pay attention)
	w["lupa_n"] = ("lupa", 1, "n", "jaytisi")	#(hole, orifice, window, door)
	w["ma_n"] = ("ma", 1, "n", "tisi")	#(land, earth, country, (outdoor) area)
	w["mama_n"] = ("mama", 1, "n", "datasi")	#(parent, mother, father)
	w["mama_mod"] = ("mama", 2, "mod", "dataso")	#(of the parent, parental, maternal, fatherly)
	w["mani_n"] = ("mani", 1, "n", "jafimi")	#(money, material wealth, currency, dollar, capital)
	w["mani_n_1"] = ("mani", 2, "n", "jakusi")	#(money, material wealth, currency, dollar, capital)
	w["meli_n"] = ("meli", 1, "n", "lawbegi")	#(woman, female, girl, wife, girlfriend)
	w["meli_mod"] = ("meli", 2, "mod", "dokepono")	#(female, feminine, womanly)
	w["mi_n"] = ("mi", 1, "n", "[mi]")	#(I, we)
	w["mi_mod"] = ("mi", 2, "mod", "bamo")	#(my, our)
	w["mije_n"] = ("mije", 1, "n", "loybegi")	#(man, male, husband, boyfriend)
	w["mije_mod"] = ("mije", 2, "mod", "xakepono")	#(male, masculine, manly)
	w["moku_n"] = ("moku", 1, "n", "fupi")	#(food, meal)
	w["moku_vt"] = ("moku", 2, "vt", "fucalinza")	#(eat, drink, swallow, ingest, consume)
	w["moli_n"] = ("moli", 1, "n", "kolenvi")	#(death)
	w["moli_mod"] = ("moli", 2, "mod", "kolapono")	#(dead, deadly, fatal)
	w["moli_vt"] = ("moli", 3, "vt", "kolapa")	#(kill)
	w["moli_vi"] = ("moli", 4, "vi", "kolupa")	#(die, be dead)
	w["monsi_n"] = ("monsi", 1, "n", "jefagaymi")	#(back, rear end, butt, behind)
	w["monsi_mod"] = ("monsi", 2, "mod", "jefagaymo")	#(back, rear)
	w["mu_interj"] = ("mu", 1, "interj", "[mu]")	#(woof! meow! moo! etc. (cute animal noise))
	w["mun_n"] = ("mun", 1, "n", "batisi")	#(moon)
	w["mun_mod"] = ("mun", 2, "mod", "batiso")	#(lunar)
	w["musi_n"] = ("musi", 1, "n", "dwekopinki")	#(fun, playing, game, recreation, art, entertainment)
	w["musi_mod"] = ("musi", 2, "mod", "dwedinxaso")	#(artful, fun, recreational)
	w["musi_vt"] = ("musi", 3, "vt", "zoybusa")	#(amuse, entertain)
	w["musi_vi"] = ("musi", 4, "vi", "dwekopisa")	#(play)
	w["mute_n"] = ("mute", 1, "n", "kumoni")	#(amount, quantity)
	w["mute_n"] = ("mute", 1, "n", "joponi")	#(amount, quantity)
	w["mute_mod"] = ("mute", 2, "mod", "kekumo")	#(many, very, much, several, a lot, abundant, numerous, more)
	w["mute_vt"] = ("mute", 3, "vt", "kekumapa")	#(make many or much)
	w["nanpa_n"] = ("nanpa", 1, "n", "[nanpa]")	#(number)
	w["nanpa_oth"] = ("nanpa", 2, "n", "[nanpa]")	#(-th (ordinal numbers))
	w["nasa_mod"] = ("nasa", 1, "mod", "kwebeso")	#(silly, crazy, foolish, drunk, strange, stupid, weird)
	w["nasa_vt"] = ("nasa", 2, "vt", "kwebesapa")	#(drive crazy, make weird)
	w["nasin_n"] = ("nasin", 1, "n", "binjami")	#(way, manner, custom, road, path, doctrine, system, method)
	w["nena_n"] = ("nena", 1, "n", "tentisi")	#(mountain)
	w["nena_n_1"] = ("nena", 2, "n", "xancesi")	#(nose)
	w["ni_n"] = ("ni", 1, "n", "[ni]")	#(this, that)
	w["ni_mod"] = ("ni", 2, "mod", "coso")	#(this, that)
	w["nimi_n"] = ("nimi", 1, "n", "[nimi]")	#(name)
	w["nimi_n_1"] = ("nimi", 2, "n", "tekusi")	#(word)
	w["noka_n"] = ("noka", 1, "n", "cucesi")	#(foot)
	w["noka_n_1"] = ("noka", 2, "n", "jicesi")	#(leg)
	w["o_interj"] = ("o", 1, "interj", "Tomwe")	#(hey! (calling somebody's attention))
	w["o_sep"] = ("o", 2, "sep", "-(g)we")	#(O (vocative or imperative))
	w["oko_n"] = ("oko", 1, "n", "kicesi")	#(eye)
	w["olin_n"] = ("olin", 1, "n", "bakoponi")	#(love)
	w["olin_mod"] = ("olin", 2, "mod", "bakopono")	#(love)
	w["olin_vt"] = ("olin", 3, "vt", "bakopa")	#(to love (a person))
	w["ona_n"] = ("ona", 1, "n", "divi")	#(she, he, it, they)
	w["ona_mod"] = ("ona", 2, "mod", "dimo")	#(her, his, its, their)
	w["open_vt"] = ("open", 1, "vt", "doykavapa")	#(open, turn on)
	w["open_vt_1"] = ("open", 2, "vt", "kwekavapa")	#(turn on)
	w["pakala_n"] = ("pakala", 1, "n", "joyjuvenvi")	#(damage, breaking)
	w["pakala_n_1"] = ("pakala", 2, "n", "xonkusi")	#(blunder, mistake)
	w["pakala_mod"] = ("pakala", 3, "mod", "joyjuvo")	#(damaged, broken)
	w["pakala_vt"] = ("pakala", 4, "vt", "joyjuvapa")	#(screw up, fuck up, botch, ruin, break, hurt, injure, damage, spoil, ruin)
	w["pakala_vi"] = ("pakala", 5, "vi", "joyjuvupa")	#(screw up, fall apart, break)
	w["pakala_interj"] = ("pakala", 6, "interj", "[pakala]")	#(damn! fuck!)
	w["pali_n"] = ("pali", 1, "n", "busenvi")	#(activity, work, deed, project)
	w["pali_mod"] = ("pali", 2, "mod", "joykavo")	#(active, work-related, operating, working)
	w["pali_vt"] = ("pali", 3, "vt", "kavapa")	#(do, make, build, create)
	w["pali_vi"] = ("pali", 4, "vi", "joykava")	#(act, work, function)
	w["palisa_n"] = ("palisa", 1, "n", "jikigi")	#(long, mostly hard object, e.g. rod, stick, branch)
	w["palisa_n_1"] = ("palisa", 2, "n", "jitevi")	#(stick)
	#w["pan_n"] = ("pan", 1, "n", "josepi")			#(bread)
	w["pana_n"] = ("pana", 1, "n", "ximenvi")	#(giving, transfer, exchange)
	w["pana_vt"] = ("pana", 2, "vt", "cema")	#(give, put, send, place, release, emit, cause)
	w["pana_vt_1"] = ("pana", 3, "vt", "ximimba")	#(give, put, send, place, release, emit, cause)
	w["pi_sep"] = ("pi", 1, "sep", "[pi]")	#(of, belonging to)
	w["pilin_n"] = ("pilin", 1, "n", "kawcesi")	#(heart)
	w["pilin_n_1"] = ("pilin", 2, "n", "tokivoni")	#(feelings, emotion)
	w["pilin_vt"] = ("pilin", 3, "vt", "tokiva")	#(feel, think, sense, touch)
	w["pilin_vi"] = ("pilin", 4, "vi", "cukopusa")	#(feel)
	w["pimeja_n"] = ("pimeja", 1, "n", "[pimeja]")	#(darkness, shadows)
	w["pimeja_mod"] = ("pimeja", 2, "mod", "kunzigo")	#(black, dark)
	w["pimeja_vt"] = ("pimeja", 3, "vt", "kifomapa")	#(darken)
	w["pini_n"] = ("pini", 1, "n", "cifagaymi")	#(end, tip)
	w["pini_mod"] = ("pini", 2, "mod", "[pini]")	#(completed, finished, past, done, ago)
	w["pini_vt"] = ("pini", 3, "vt", "jebulapa")	#(finish, close, end, turn off)
	w["pipi_n"] = ("pipi", 1, "n", "byekagi")	#(bug, insect, spider)
	w["poka_n"] = ("poka", 1, "n", "dayzogaymi")	#(side)
	w["poka_n_1"] = ("poka", 2, "n", "jixucesi")	#(hip)
	w["poka_mod"] = ("poka", 3, "mod", "fofagawno")	#(neighbouring)
	w["poka_prep"] = ("poka", 4, "prep", "[poka]")	#(in the accompaniment of, with)
	w["poki_n"] = ("poki", 1, "n", "zipi")	#(container, box, bowl, cup, glass)
	w["pona_n"] = ("pona", 1, "n", "[pona]")	#(good, simplicity, positivity)
	w["pona_mod"] = ("pona", 2, "mod", "cakemo")	#(good, simple, positive, nice, correct, right)
	w["pona_vt"] = ("pona", 3, "vt", "cakemapa")	#(improve, fix, repair, make good)
	w["pona_vt_1"] = ("pona", 4, "vt", "joykavapa")	#(improve, fix, repair, make good)
	w["pona_interj"] = ("pona", 5, "interj", "[pona]")	#(great! good! thanks! OK! cool! yay!)
	w["sama_mod"] = ("sama", 1, "mod", "[sama]")	#(same, similar, equal, of equal status or position)
	w["sama_prep"] = ("sama", 2, "prep", "[sama]")	#(like, as, seem)
	w["seli_n"] = ("seli", 1, "n", "fexogi")	#(fire, warmth, heat)
	w["seli_mod"] = ("seli", 2, "mod", "feculo")	#(hot, warm, cooked)
	w["seli_vt"] = ("seli", 3, "vt", "?fecalinza")	#(cook)
	w["seli_vt_1"] = ("seli", 4, "vt", "feculupa")	#(heat, warm up)
	w["selo_n"] = ("selo", 1, "n", "?jocumbemi")	#(outside, surface, skin, shell, bark, shape, peel)
	w["selo_n_1"] = ("selo", 2, "n", "cuncesi")	#(skin)
	w["selo_n_2"] = ("selo", 3, "n", "cuntevi")	#(skin)
	w["selo_n_3"] = ("selo", 4, "n", "cunzipi")	#(outside, surface, skin, shell, bark, shape, peel)
	w["seme_oth"] = ("seme", 1, "n", "[seme]")	#(what, which, wh- (question word))
	w["sewi_n"] = ("sewi", 1, "n", "cenzogaymi")	#(top)
	w["sewi_mod"] = ("sewi", 2, "mod", "daculo")	#(high)
	w["sewi_mod_1"] = ("sewi", 3, "mod", "denkemo")	#(religious)
	w["sijelo_n"] = ("sijelo", 1, "n", "bicesi")	#(body)
	w["sike_n"] = ("sike", 1, "n", "bijojumi")	#(sphere)
	w["sike_n_1"] = ("sike", 2, "n", "jojumi")	#(circle)
	w["sike_n_2"] = ("sike", 3, "n", "tidagi")	#(circle, wheel, sphere, ball, cycle)
	w["sike_mod"] = ("sike", 4, "mod", "jokavo")	#(round)
	w["sin_mod"] = ("sin", 1, "mod", "dawkemo")	#(new)
	w["sin_vt"] = ("sin", 2, "vt", "dawkemapa")	#(renew, renovate, freshen)
	w["sina_n"] = ("sina", 1, "n", "xevi")	#(you)
	w["sina_n_1"] = ("sina", 2, "n", "zavi")	#(you)
	w["sina_mod"] = ("sina", 3, "mod", "xemo")	#(your)
	w["sina_mod_1"] = ("sina", 4, "mod", "zamo")	#(your)
	w["sinpin_n"] = ("sinpin", 1, "n", "[sinpin]")	#(front, chest, torso, face, wall)
	w["sinpin_n_1"] = ("sinpin", 2, "n", "figi")	#(wall)
	w["sinpin_n_2"] = ("sinpin", 3, "n", "juncesi")	#(face)
	w["sinpin_n_3"] = ("sinpin", 4, "n", "twacesi")	#(chest)
	w["sitelen_n"] = ("sitelen", 1, "n", "kifimi")	#(picture, image)
	w["sitelen_vt"] = ("sitelen", 2, "vt", "zicalinza")	#(draw, write)
	w["sona_n"] = ("sona", 1, "n", "koponi")	#(knowledge, wisdom, intelligence, understanding)
	w["sona_vt"] = ("sona", 2, "vt", "kopa")	#(know, understand, know how to)
	w["sona_vi"] = ("sona", 3, "vi", "kopusa")	#(know, understand)
	w["sona_kama"] = ("sona", 4, "aux", "[sona]")	#(learn, study)
	w["soweli_n"] = ("soweli", 1, "n", "byekupi")	#(animal, especially land mammal, lovable animal)
	w["suli_n"] = ("suli", 1, "n", "kemoni")	#(size)
	w["suli_mod"] = ("suli", 2, "mod", "jiculo")	#(big, tall, long, adult, important)
	w["suli_mod_1"] = ("suli", 3, "mod", "kemo")	#(big, tall, long, adult, important)
	w["suli_vt"] = ("suli", 4, "vt", "kemapa")	#(enlarge, lengthen)
	w["suno_n"] = ("suno", 1, "n", "kitisi")	#(sun, light)
	w["suno_n_1"] = ("suno", 2, "n", "kixogi")	#(sun, light)
	w["suno_mod"] = ("suno", 3, "mod", "kitiso")	#(oriental, solar, light)
	w["supa_n"] = ("supa", 1, "n", "byejisi")	#(table)
	w["supa_n_1"] = ("supa", 2, "n", "cufigi")	#(floor)
	w["supa_n_1"] = ("supa", 2, "n", "cufigi")	#(floor)
	w["supa_n_3"] = ("supa", 4, "n", "dadetisi")	#(horizontal surface)
	w["suwi_n"] = ("suwi", 1, "n", "zujosi")	#(candy, sweet food)
	w["suwi_mod"] = ("suwi", 2, "mod", "cankaykemo")	#(sweet, cute)
	w["suwi_mod_1"] = ("suwi", 3, "mod", "kayfupono")	#(sweet)
	w["suwi_vt"] = ("suwi", 4, "vt", "kayfupapa")	#(sweeten)
	w["tan_n"] = ("tan", 1, "n", "jedapangi")	#(origin, cause)
	w["tan_prep"] = ("tan", 2, "prep", "[tan]")	#(from, by, because of, since)
	w["taso_mod"] = ("taso", 1, "mod", "[taso]")	#(only, sole)
	w["taso_conj"] = ("taso", 2, "conj", "[taso]")	#(but)
	w["tawa_n"] = ("tawa", 1, "n", "tikavenvi")	#(movement, transportation)
	w["tawa_mod"] = ("tawa", 2, "mod", "tikavo")	#(moving, mobile)
	w["tawa_vt"] = ("tawa", 3, "vt", "tikavapa")	#(move, displace)
	w["tawa_vi"] = ("tawa", 4, "vi", "tikava")	#(go to, walk, travel, move, leave)
	w["tawa_prep"] = ("tawa", 5, "prep", "[tawa]")	#(to, in order to, towards, for, until)
	w["telo_n"] = ("telo", 1, "n", "bocivi")	#(water, liquid, juice, sauce)
	w["telo_vt"] = ("telo", 2, "vt", "cinbusa")	#(water, wash with water)
	w["tenpo_n"] = ("tenpo", 1, "n", "byefemi")	#(time, period of time, moment, duration, situation)
	w["toki_n"] = ("toki", 1, "n", "tejami")	#(lect, talking, speech, communication)
	w["toki_mod"] = ("toki", 2, "mod", "[toki]")	#(talking, verbal)
	w["toki_vt"] = ("toki", 3, "vt", "tegoma")	#(say)
	w["toki_vi"] = ("toki", 4, "vi", "[toki]")	#(talk, chat, communicate)
	w["toki_interj"] = ("toki", 5, "interj", "[toki]")	#(hello! hi!)
	w["tomo_n"] = ("tomo", 1, "n", "byekigi")	#(indoor constructed space, e.g. house, home, room, building)
	w["tomo_mod"] = ("tomo", 2, "mod", "kwixaso")	#(urban, domestic, household)
	w["tu_n"] = ("tu", 1, "n", "[tu]")	#(duo, pair)
	w["tu_mod"] = ("tu", 2, "mod", "xekumo")	#(two)
	w["tu_vt"] = ("tu", 3, "vt", "[tu]")	#(double, separate/cut/divide in two)
	w["unpa_n"] = ("unpa", 1, "n", "xadokepinki")	#(sex, sexuality)
	w["unpa_mod"] = ("unpa", 2, "mod", "xadokepo")	#(erotic, sexual)
	w["unpa_vt"] = ("unpa", 3, "vt", "tababusa")	#(have sex with, sleep with, fuck)
	w["unpa_vi"] = ("unpa", 4, "vi", "tababisa")	#(have sex)
	w["uta_n"] = ("uta", 1, "n", "tecesi")	#(mouth)
	w["uta_mod"] = ("uta", 2, "mod", "tecesi")	#(oral)
	w["utala_n"] = ("utala", 1, "n", "xezugi")	#(conflict, disharmony, competition, fight, war, battle, attack, blow, argument, physical or verbal violence)
	w["utala_vt"] = ("utala", 2, "vt", "zobusa")	#(hit, strike, attack, compete against)
	w["walo_n"] = ("walo", 1, "n", "[walo]")	#(white thing or part, whiteness, lightness)
	w["walo_mod"] = ("walo", 2, "mod", "cinzigo")	#(white, light (colour))
	w["wan_n"] = ("wan", 1, "n", "bakumoni")	#(unit, element, particle, part, piece)
	w["wan_mod"] = ("wan", 2, "mod", "bakumo")	#(one, a)
	w["wan_vt"] = ("wan", 3, "vt", "[wan]")	#(unite, make one)
	w["waso_n"] = ("waso", 1, "n", "byedami")	#(bird, winged animal)
	w["wawa_n"] = ("wawa", 1, "n", "xokemoni")	#(energy, strength, power)
	w["wawa_mod"] = ("wawa", 2, "mod", "xokemo")	#(energetic, strong, fierce, intense, sure, confident)
	w["wawa_vt"] = ("wawa", 3, "vt", "[wawa]")	#(strengthen, energize, empower)
	w["weka_n"] = ("weka", 1, "n", "fagoni")	#(absence)
	w["weka_mod"] = ("weka", 2, "mod", "[weka]")	#(away, absent, missing)
	w["weka_vt"] = ("weka", 3, "vt", "fagapa")	#(throw away, remove, get rid of)
	w["wile_n"] = ("wile", 1, "n", "kekesoni")	#(desire, need, will)
	w["wile_mod"] = ("wile", 2, "mod", "[wile]")	#(necessary)
	w["wile_vt"] = ("wile", 3, "vt", "cakopa")	#(to want, need, wish, have to, must, will, should)
	w["wile_vt_1"] = ("wile", 4, "vt", "kekesa")	#(need)
	w["pi_sep"] = ("pi", 1, "sep", "[pi]")	#(n pi (n mod)) vs. n n
	

	"""
	ante	1	cont	otherwise, or else
	ken	1	cont	it is possible that
	jo	1	kama	receive, get, take, obtain
	sona	1	kama	learn, study
	kepeken	1	prep	with
	lon	1	prep	be (located) in/at/on
	poka	3	prep	in the accompaniment of, with
	sama	2	prep	like, as, seem
	tan	2	prep	from, by, because of, since
	tawa	3	prep	to, in order to, towards, for, until
	"""
	return w

def build_lexicon(w, properties):
	lx = Lexicon()

	for w0 in w.values():	
		lx.add_word(build_word(w0))
	lx.compile(properties)
	return lx

def build_grammar(w):
	"""
	Toki Pona grammar:

	"""
	def add_phrase(name, sep_key):
		"""
		<xs> ::= <x> + (<conj> + <x>)*
		"""
		g[name+"s"] = Reference(name) + Reference(name+"-extension") * KLEENE_CLOSURE
		g[name+"-extension"] = WordFilter(build_word(w[sep_key])) + Reference(name)

	g = Grammar("toki pona")


	g["sentence"] = Reference("sentence-adverb") * OPTIONAL_CLOSURE + Reference("subject") + Reference("predicates")
	g["sentence-adverb"] = Reference("noun-phrase") + WordFilter(build_word(w["la_sep"]))

	g["subject"] = Reference("pronoun-phrase") 
	g["subject"] = Reference("noun-phrases") + WordFilter(build_word(w["li_sep"]))
	add_phrase("noun-phrase", "en_conj")

	g["pronoun-phrase"] = WordFilter(build_word(w["mi_n"])) | WordFilter(build_word(w["sina_n"]))
	g["noun-phrase"] = WordCategoryFilter("n") + Reference("adjectives") * OPTIONAL_CLOSURE
	g["noun-phrase"] = WordCategoryFilter("n") + WordFilter(build_word(w["pi_sep"])) + WordCategoryFilter("n") + Reference("adjectives")

	add_phrase("predicate", "li_sep")
	g["predicate"] =  Reference("intransitive-predicate") | Reference("transitive-predicate") | Reference("copulative-predicate")
	
	g["intransitive-predicate"] = WordCategoryFilter("v", ("intr",)) + Reference("adverbs") * OPTIONAL_CLOSURE + Reference("complement") * KLEENE_CLOSURE
	g["transitive-predicate"] = WordCategoryFilter("v", ("tr",)) + Reference("adverbs") * OPTIONAL_CLOSURE + Reference("direct-object") * POSITIVE_CLOSURE + Reference("complement") * KLEENE_CLOSURE
	g["copulative-predicate"] = Reference("noun-phrase") | Reference("adjectives") * OPTIONAL_CLOSURE + Reference("complement") * KLEENE_CLOSURE

	add_phrase("adjective", "en_conj")
	add_phrase("adverb", "en_conj")
	g["direct-object"] = WordFilter(build_word(w["e_sep"])) + Reference("noun-phrase")
	g["adjective"] = WordCategoryFilter("mod")
	g["adverb"] = WordCategoryFilter("mod")
	g["complement"] = WordCategoryFilter("prep") + Reference("noun-phrase") 

	g.compile()
	
	return g

def callgraph():
	import pycallgraph
	l = prepare()
	l.reset()
	lx = l.lexicon
	gr = l.grammar
	prp = l.properties
	#Lexicon Compile
	pycallgraph.start_trace()
	lx.compile(prp, True)
	pycallgraph.make_dot_graph('lexicon_compile.png')
	#Grammar Compile
	pycallgraph.start_trace()
	gr.compile(True)
	pycallgraph.make_dot_graph('grammar_compile.png')
	#Read
	pycallgraph.start_trace()
	l.read(u"mi pona e ilo")
	pycallgraph.make_dot_graph('read.png')

if __name__ == "__main__":
	run()

