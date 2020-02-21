# -*- coding: utf-8 -*-

# Copyright 2013-2018, 2020 Hannu Väisänen (Hannu.Vaisanen@uef.fi)
# Program to generate old spellings and common spelling mistakes for Voikko lexicon.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# This automatic generation will generate some old
# spellings and spelling errors that do not exist in real life.

# Style- ja usage-lippujen arvot suoraan Joukahaisesta:
# grep -A1 '<style>' ../vocabulary/joukahainen.xml|grep flag|sort -u|gawk '{printf "%s,", substr($1,7,length($1)-13)}'
# grep -A1 '<usage>' ../vocabulary/joukahainen.xml|grep flag|sort -u|gawk '{printf "%s,", substr($1,7,length($1)-13)}'


import codecs
import getopt
import re
import sys
from types import *
sys.path.append("common")
import generate_lex_common

OPTIONS = generate_lex_common.get_options()

infile = codecs.open (OPTIONS["destdir"] + u"/all.lexc", "r", "UTF-8")
outfile = codecs.open (OPTIONS["destdir"] + u"/all-sukija.lexc", 'w', 'UTF-8')
sukijafile = codecs.open (OPTIONS["destdir"] + u"/poikkeavat-sukija.lexc", 'r', 'UTF-8')

C = u"[qwrtpsšdfghjklzžxcvbnm]"      # Kerakkeet.
K = u"[qwrtpsšdfghjklzžxcvbnmaiou]"  # Kerakkeet + ääntiöitä.
V = u"[aeiouüyåäö]"                  # Ääntiöt.
A = u"[aä]"
U = u"[uy]"

def makeRePattern (wordClass, word):
    u = u"^\\[%s\\](\\[I..\\])?\\[Xp\\].*%s\\[X\\]" % (wordClass, word)
    u = u.replace ('C', C)
    u = u.replace ('K', K)
    u = u.replace ('V', V)
    u = u.replace ('A', A)
    u = u.replace ('U', U)
    return u


def makeRe (wordClass, word):
    return re.compile (makeRePattern (wordClass, word), re.UNICODE)


def replace (s, old, new):
    u = s.replace (old + u":",  new + u":")
    u = u.replace (old + u" ",  new + u" ")
    u = u.replace (old + u"\t", new + u"\t")
    u = u.replace (old + u"@",  new + u"@")
    return u


def replace_and_write (line, string1, string2):
    s = replace (line, string1, string2)
    outfile.write (s)


def replace_and_write_2 (line, string1, string2):
    s = replace (line, string1, string2)
    outfile.write (s)


re_oittaa1 = makeRe (u"Lt", u".Koittaa")
re_oittaa2 = makeRe (u"Lt", u".Köittää")

re_ottaa1 = makeRe (u"Lt", u".Kottaa")
re_ottaa2 = makeRe (u"Lt", u".Köttää")

re_oitella1 = makeRe (u"Lt", u".Koitella")
re_oitella2 = makeRe (u"Lt", u".Köitellä")

re_otella1 = makeRe (u"Lt", u".Kotella")
re_otella2 = makeRe (u"Lt", u".Kötellä")

re_ottua1 = makeRe (u"Lt", u".Kottua")
re_ottua2 = makeRe (u"Lt", u".Köttyä")

re_oittua1 = makeRe (u"Lt", u".Koittua")
re_oittua2 = makeRe (u"Lt", u".Köittyä")

re_isoida = makeRe (u"Lt", u"isoida") # Organisoida => organiseerata.

re_nuolaista = re.compile (u"\\[Lt\\].* Nuolaista_", re.UNICODE)
re_rangaista = re.compile (u"\\[Lt\\].* Rangaista_", re.UNICODE)

re_Xiljoona = re.compile (u"\\A(?:\\[Bc\\]|\\[Sn\\]|@).*(b|m|tr)iljoon", re.UNICODE)

re_tautua1 = re.compile ("\\[Lt\\].*tautua.*Kaatua_", re.UNICODE)
re_tautua2 = re.compile ("\\[Lt\\].*täytyä.*Kaatua_", re.UNICODE)

re_isoida_x = re.compile (u"\\A\[Lt\]\[Xp\](dramatisoida|karakterisoida)\[X\]")

re_A = re.compile (u"[aou]")

re_oitin = makeRe (u"Ln", u".Coitin")
re_oite  = makeRe (u"Ln", u".Coite")

re_aatio = makeRe (u"Ln", u"..aatio")
re_uutio = makeRe (u"Ln", u".Cuutio")
re_tio   = makeRe (u"Ln", u"([^a]i|k|p)tio") # Traditio, funktio, mutta ei aitio.
re_uusio = makeRe (u"Ln", u"Cuusio")         # Myös fuusio.

re_mmainen = re.compile (".*mmainen\\[X\\]")
re_mmäinen = re.compile (".*mmäinen\\[X\\]")


def g2 (line, x):
    outfile.write (line.replace (x[0], x[1]))


def g4 (line, x):
    s = line.replace (x[0], x[1])
    outfile.write (s.replace (x[2], x[3]))


def g6 (line, x):
    if line.find(x[4]) > 0:
        s = line.replace (x[4], x[5])
        s = s.replace (x[0], x[1])
        s = s.replace (x[2], x[3])
        outfile.write (s)


def xprint (s, old, new):
    p = s.find(":")
#    print (s, p, old, new)
    if p >= 0:
        n = s.find (old, p)
        if n >= 0:
            outfile.write (s[:n] + new + s[n+len(old):])


def gn (line, x):
    if not line.startswith("[Ln][Xp]kuusio[X]"):
        for u in x[1]:
            xprint (line, x[0], u)
            replace_and_write_2 (line, x[0], u)
        for u in x[2]:
#            xprint (line.replace(x[3][0],x[3][1]), x[0], u)
            replace_and_write_2 (line.replace(x[3][0],x[3][1]), x[0], u)


def g10 (line, x):
    if not x[8].match(line):
        s = line.replace(x[0],x[1]).replace(x[4],x[5]).replace(x[6],x[7])
        replace_and_write (s, x[2], x[3])


list_all = [
    (re_nuolaista, g2, ("Nuolaista_", "SukijaNuolaista_")),
    (re_rangaista, g2, ("Rangaista_", "SukijaRangaista_")),
    (re_tautua1,   g2, ("Kaatua_",    "SukijaAntautua_")),
    (re_tautua2,   g2, ("Kaatua_",    "SukijaAntautua_")),
    (re_isoida,   g10, ("isoida", "iseerata", "iso", "iseer", "Kanavoida", "Saneerata", "Voida", "Saneerata", re_isoida_x)),

    (re_oitin,     g6, ("oit:", "oit:", "oit ", "ot ",  "Suodatin",   "Suodatin")),
    (re_oite,      g6, ("oit:", "oit:", "oit ", "ot ",  "Vaate",      "Vaate")),
    (re_oittaa1,   g6, ("o:",   "oit:", "o ",   "ot ",  "Kirjoittaa", "Alittaa")),
    (re_oittaa2,   g6, ("ö:",   "öit:", "ö ",   "öt ",  "Kirjoittaa", "Alittaa")),
    (re_oittaa1,   g6, ("oit:", "oit:", "oit ", "ot ",  "Alittaa",    "Alittaa")),
    (re_oittaa2,   g6, ("öit:", "öit:", "öit ", "öt ",  "Alittaa",    "Alittaa")),
    (re_ottaa1,    g6, ("ot:",  "ot:",  "ot ",  "oit ", "Alittaa",    "Alittaa")),
    (re_ottaa2,    g6, ("öt:",  "öt:",  "öt ",  "öit ", "Alittaa",    "Alittaa")),
    (re_ottaa1,    g6, ("o:",   "o:",   "o ",   "oi ",  "Ammottaa",   "Ammottaa")),
    (re_ottaa2,    g6, ("ö:",   "ö:",   "ö ",   "öi ",  "Ammottaa",   "Ammottaa")),
    (re_oitella1,  g6, ("oit:", "oit:", "oit ", "ot ",  "Aatella",    "Aatella")),
    (re_oitella2,  g6, ("öit:", "öit:", "öit ", "öt ",  "Aatella",    "Aatella")),
    (re_otella1,   g6, ("ot:",  "ot:",  "ot ",  "oit ", "Aatella",    "Aatella")),
    (re_otella2,   g6, ("öt:",  "öt:",  "öt ",  "öit ", "Aatella",    "Aatella")),
    (re_ottua1,    g6, ("ot:",  "ot:",  "ot ",  "oit ", "Asettua",    "Asettua")),
    (re_ottua2,    g6, ("öt:",  "öt:",  "öt ",  "öit ", "Asettua",    "Asettua")),
    (re_oittua1,   g6, ("oit:", "oit:", "oit ", "ot ",  "Asettua",    "Asettua")),
    (re_oittua2,   g6, ("öit:", "öit:", "öit ", "öt ",  "Asettua",    "Asettua")),

    (re_uusio,     gn, ("uusio", ("usio",),         ("usion",  "usioon"),  ("NimisanaAutio_a", "NimisanaPaperi_a"))),
    (re_tio,       gn, ("tio",   ("tsio",),         ("tsion",  "tsioon"),  ("NimisanaAutio_a", "NimisanaPaperi_a"))),
    (re_aatio,     gn, ("aatio", ("atio", "atsio"), ("atsion", "atsioon"), ("NimisanaAutio_a", "NimisanaPaperi_a"))),
    (re_uutio,     gn, ("uutio", ("utio", "utsio"), ("utsion", "utsioon"), ("NimisanaAutio_a", "NimisanaPaperi_a"))),

    (re_mmainen,   g4, ("mmai ", "mai ", "mmai\t", "mai ")),
    (re_mmäinen,   g4, ("mmäi ", "mäi ", "mmäi\t", "mäi ")),
]


def generate_all (line, pattern_list):
    for x in pattern_list:
        if x[0].match(line):
            x[1] (line, x[2])
        


def word_class (line):
    L = dict ([("[Lep]", "Paikannimi"),
               ("[Ll]",  "Laatusana"),
               ("[Ln]",  "Nimisana"),
               ("[Lnl]", "NimiLaatusana")])
    return L[line[0:line.find("]")+1]]


# Sanoja, joilla on vain muutama vanha taivutusmuoto. Generoidaan ne erikseen,
# mutta vain sanoille, jotka ovat Joukahaisessa. Sanat ovat Nykysuomen
# sanakirjan taivutuskaavojen numeroiden mukaisessa järjestyksessä.
#
# Tuomo Tuomi: Suomen kielen käänteissanakirja, 2. painos.
# Suomalaisen Kirjallisuuden Seura 1980.

def write_word (line, word, lexicon):
    prefix = line[0:line.find (u" ")]
    A = u"a" if re_A.search(word) else u"ä"
    outfile.write (u"%s %s%s_%s ;\n" % (prefix, word_class(line), lexicon, A))

def write_ahven (line, word):
    if not line.startswith (u"[Lu]"):
        write_word (line, word, u"SukijaAhven")

def write_virkkaa (line, word):
    prefix = line[0:line.find (u" ")]
    outfile.write (u"%s SukijaVirkkaa_ä ;\n" % (prefix))

def write_paistaa (line, word):
    prefix = line[0:line.find (u" ")]
    outfile.write (u"%s SukijaPaistaa_a ;\n" % (prefix))

def write_paahtaa (line, word):
    prefix = line[0:line.find (u" ")]
    outfile.write (u"%s SukijaPaahtaa_a ;\n" % (prefix))


word_list = [
    (u"tällainen",       ((u"tällai",      u"tällai", u"NimiLaatusanaNainenInen_a", u"NimiLaatusanaNainenInen_ä"),
                          (u"tällai",      u"tälläi", u"NimiLaatusanaNainenInen_a", u"NimiLaatusanaNainenInen_aä"))),

    (u"lainen",  lambda line, word: replace_and_write (line.replace(u"lai",u"läi"), u"NimiLaatusanaNainen_a", u"NimiLaatusanaNainen_ä")),

    # 38 pieni (4, 4). Juoni, moni, pieni, tyyni, (peilityyni, rasvatyyni).
    #
    # Nämä ovat tiedostossa poikkeavat-sukija.lexc
    #
##    (u"juoni", [u"[Lnl][Xp]juoni[X]juon:juon NimiLaatusanaSukijaPieni_a ;"]),
##    (u"moni",  [u"[Ln][Xp]moni[X]mon:mon NimisanaSukijaPieni_a ;"]),
##    (u"pieni", [u"[Ll][Xp]pieni[X]pien:pien LaatusanaSukijaPieni_ä ;"]),
##    (u"tyyni", [u"[Ll][Xp]tyyni[X]tyyn:tyyn LaatusanaSukijaPieni_ä ;"]),
##    (u"peilityyni", [u"[Ll][Xp]peilityyni[X]peili[Bm]tyyn:peilityyn LaatusanaSukijaPieni_ä ;"]),
##    (u"rasvatyyni", [u"[Ll][Xp]rasvatyyni[X]rasva[Bm]tyyn:rasvatyyn LaatusanaSukijaPieni_ä ;"]),

    # 39 nuori (3, 3). Tuomi, s. 182, 184.
    #
    # Nämä ovat tiedostossa poikkeavat-sukija.lexc
    #
#    (u"juuri",   [u"[Ln][Xp]juuri[X]juur[Ses][Ny]na:juurna NimisanaLiOlV_a ;",
#                  u"[Ln][Xp]juuri[X]juur[Ses][Ny]ra:juurra NimisanaLiOlV_a ;"]),
#    (u"nuori",   [u"[Lnl][Xp]nuori[X]nuor[Ses][Ny]na:nuorna NimisanaLiOlV_a ;",
#                  u"[Lnl][Xp]nuori[X]nuor[Ses][Ny]ra:nuorra NimisanaLiOlV_a ;"]),
#    (u"suuri",   [u"[Lnl][Xp]suuri[X]suur[Ses][Ny]na:suurna NimisanaLiOlV_a ;",
#                  u"[Lnl][Xp]suuri[X]suur[Ses][Ny]ra:suurra NimisanaLiOlV_a ;"]),

    # 46 hapsi (1, 1). Tuomi, s. 190. -- Vvfst tunnistaa muodot "hasten" ja "hapsien".
    # hasna, hassa, hasten, hapsien   -- Nämä ovat niin harvinaisia, että tarvitseeko näitä indeksoinnissa?
    #
#    (u"hapsi", [u"[Ln][Xp]hapsi[X]has[Ses][Ny]na:hasna NimisanaLiOlV_a ;",
#                u"[Ln][Xp]hapsi[X]has[Ses][Ny]sa:hassa NimisanaLiOlV_a ;"]),

    # 79 terve (4, 4). Tuomi s. 142, 143, 146.
    #
    # Nämä ovat tiedostossa poikkeavat-sukija.lexc
    #
#    (u"tuore", [u"[Ll][Xp]tuore[X]tuore[Ses][Ny]nna:tuorenna NimisanaLiOlV_a ;"]),
#    (u"vetre", [u"[Ll][Xp]vetre[X]vetre[Ses][Ny]nnä:vetrennä NimisanaLiOlV_ä ;"]),
#    (u"päre",  [u"[Ln][Xp]päre[X]päre[Ses][Ny]nnä:pärennä NimisanaLiOlV_ä ;"]),
#    (u"terve", [u"[Lnl][Xp]terve[X]terve[Ses][Ny]nnä:tervennä NimisanaLiOlV_ä ;"]),

##    (u"kaivu", [u"[Ln][Xp]kaivu[X]kaivu[Sill][Ny]usee:kaivuusee NimisanaLiOlN_a ;"]),
#    (u"kaivu", [u"[Ln][Xp]kaivu[X]kaivu:kaivu NimisanaPuu_a ;",
#                u"[Ln][Xp]kaivu[X]kaivu[Sill][Ny]usee:kaivuusee NimisanaLiOlN_a ;"]),
]


function_list = [
    # Herttua-tyyppisillä sanoilla on monikkomuodot, joissa ei ole o:ta (herttuilla, jne).
    #
    # 20 herttua (10, 10). Tuomi, s. 114, 116, 121, 124, 125.
    #
    (lambda line, word: outfile.write (u"[Ln][Xp]%s[X]%s:%s SukijaHerttua ;\n" %
                                       (word, word[0:len(word)-1], word[0:len(word)-1])),
     (u"aurtua",
      u"herttua",
      u"hierua",
      u"juolua",
      u"lastua",
      u"liettua",
      u"luusua",
      u"porstua",
      u"saarua",
      u"tanhua")),

# Vapaa ja tienoo ovat taivutuskaavoina SukijaVapaa.
#
    # 23 vapaa (8, 8). Tuomi, s. 1, 2.
    #
#    (write_vapaa_tienoo,
#     (u"kajaa",
#      u"vajaa",
#      u"vakaa",
#      u"suklaa",
#      u"harmaa",
#      u"vapaa",
#      u"nepaa",
#      u"hurraa")),

    # 24 tienoo (14, 14). Tuomi, s. 345. Taipuu kuten vapaa.
    #
#    (write_vapaa_tienoo,
#     (u"kabeljoo",
#      u"kalikoo",
#      u"pikoo",
#      u"talkoo",
#      u"haloo",
#      u"halloo",
#      u"tienoo",
#      u"poppoo",
#      u"bigarroo",
#      u"platoo",
#      u"ehtoo",
#      u"palttoo",
#      u"ponttoo",
#      u"nivoo")),

    # 33 lohi (2, 2). Tuomi, s. 151.
    # lohten, uuhten
    #
    (lambda line, word: outfile.write (u"[Ln][Xp]%s[X]%s:%s SukijaLohi ;\n" %
                                       (word, word[0:len(word)-1], word[0:len(word)-1])),
     (u"lohi",
      u"tyynenmerenlohi",   # On Joukahaisessa.
      u"uuhi")),

    # 34 lahti (2, 2). Tuomi, s. 193.
    # lahta (= lahtea), lahtein
    #
    (lambda line, word: write_word (line, word, "SukijaLahti"),
     (u"haahti",
      u"lahti")),

    # Ahven taipuu kuten sisar, paitsi että yksikön olento on myös ahvenna.
    #
    # 55 ahven (22, 23). Tuomi, s. 246, 247, 301, 302.
    #
    (write_ahven,
     (u"aamen",
      u"ahven",
      u"haiven",
      u"huomen",
      u"häiven",
      u"höyhen",
#      u"ien",  # On erikseen: ikene, ien.
      u"iljen",
      u"joutsen",
      u"jäsen",
      u"kymmen",
      u"kämmen",
      u"liemen",
      u"paimen",
      u"siemen",
      u"ruumen",
      u"terhen",
      u"taimen",
      u"tuumen",
      u"tyven",
      u"tyyven",
      u"uumen",
      u"vuomen")),

    # 69 kaunis (7, 6). Tuomi, s. 358.
    #
     (lambda line, word: write_word (line, word, "SukijaKaunis"),
     (u"kallis",
      u"aulis",
      u"valmis",
      u"kaunis",
#      u"altis",
      u"tiivis")),

    (lambda line, word: write_word (line, word, "SukijaAltis"), ("altis", )),

     # 11 paistaa (9, 9). Tuomi s. 1, 2, 8, 11, 12, 15, 17.
     #
     (write_virkkaa, (u"vilkkaa",
                      u"virkkaa")),
     (write_paistaa, (u"paistaa",
                      u"uppo=paistaa")),
     (write_paahtaa, (u"paahtaa",
                      u"raistaa",
                      u"saattaa",
                      u"taittaa",
                      u"palttaa",
                      u"varttaa")),
]

def convert_to_dictionary (word_list):
    l0 = map (lambda x : x[0], word_list)
    l1 = map (lambda x : x[1], word_list)
    return dict (zip (l0, l1))

sukija_dictionary = convert_to_dictionary (word_list)


def error (line):
    sys.stderr.write (line)
    sys.stderr.write ("Wrong format in sukija_dictionary.\n")
    sys.exit (1)


def write_list (line, key, data):
    for x in data:
        if type(x) == str:
            outfile.write (x + u"\n")
        else:
            error (line)


def write_tuple (line, key, g):
     if type(g[0]) == str:
         for i in range (1, len(g)):
             replace_and_write (line, g[0], g[i])
     elif type(g[0]) == tuple:
         for i in range (0, len(g)):
             if (len(g[i]) == 2):
                 replace_and_write (line, g[i][0], g[i][1])
             else:
                 s = line.replace (g[i][2], g[i][3])
                 outfile.write (replace (s, g[i][0], g[i][1]))
     else:
         error (line)


# Extract base form from a line.
#
base_form_re = re.compile (u"\\[Xp\\]([^[]+)\\[X\\]", re.UNICODE)

def generate_word (r, line, sukija_dictionary):
    try:
        g = sukija_dictionary[r.group(1)]
        if type(g) == list:
            write_list (line, r.group(1), g)
        elif type(g) == tuple:
            write_tuple (line, r.group(1), g)
        elif type(g) == LambdaType:
            g (line, r.group(1))
        else:
            error (line)
    except KeyError:  # It is not an error if a word is not in sukija_dictionary.
        pass


def generate_from_function (r, line, function_list):
    for x in function_list:
        if r.group(1) in x[1]:
            x[0] (line, r.group(1))


def generate_xiljoona (line):
    if (line.startswith ("[Sn]")):
        u = line.replace (u"miljoona@", u"miljona@")
        u = u.replace (u"miljoonat@", u"miljonat@")
        u = u.replace (u"biljoona@",  u"biljona@")
        u = u.replace (u"biljoonat@", u"biljonat@")
        u = u.replace (u"triljoona@",  u"triljona@")
        u = u.replace (u"triljoonat@", u"triljonat@")
        outfile.write (u)
    else:
        outfile.write (line.replace (u"iljoon", u"iljon"))
        if (line.startswith (u"@") and line.find (u"iljoonien:")):
            outfile.write (line.replace (u"iljoonien", u"iljoonain"))
            outfile.write (line.replace (u"iljoonien", u"iljonain"))


def write_arvaella (line):
    if line.startswith("[Lt][Xp]") and line.find ("Arvailla_") > 0:
        if not line.startswith ("[Lt][Xp]piillä[X]") and not line.startswith ("[Lt][Xp]viillä[X]"):
            line = line.replace ("il:", ":").replace("il ", " ").replace ("Arvailla_", "SukijaArvaella_")
            outfile.write (line)


ei_vertm = re.compile (u"@[PDC][.]EI_VERTM([.]ON)?@", re.UNICODE)
ei_yks = "@P.EI_YKS.ON@"


sukija_additions = {
    "LEXICON Asemosana\n":     "SukijaAsemosana ;\n",
    "LEXICON Sanasto_em\n":    "SukijaPoikkeavat_em ;\n",
    "LEXICON Sanasto_ep\n":    "SukijaPoikkeavat_ep ;\n",
    "LEXICON Sanasto_l\n":     "SukijaPoikkeavat_l ;\n",
    "LEXICON Sanasto_n\n":     "SukijaPoikkeavat_n ;\n",
    "LEXICON Sanasto_nl\n":    "SukijaPoikkeavat_nl ;\n",
    "LEXICON Sanasto_p\n":     "Sukija_p ;\n",
    "LEXICON Sanasto_t\n":     "SukijaPoikkeavat_t ;\n",
    "LEXICON Sanasto_s\n":     "SukijaPoikkeavat_s ;\n",
    "LEXICON Suhdesana\n":     "SukijaSuhdesana ;\n",
    "LEXICON LukusananErikoisjälkiliite\n": "SukijaLukusananErikoisjälkiliite ;\n",
    "LEXICON Lukusana\n":        "SukijaLukusanaSeitsemän ;\n",
    "LEXICON Omistusliite_a\n":  "[O2y]s:s Liitesana_a  ;\n",
    "LEXICON Omistusliite_ä\n":  "[O2y]s:s Liitesana_ä  ;\n",
    "LEXICON Omistusliite_aä\n": "[O2y]s:s Liitesana_aä ;\n"
#   "LEXICON Omistusliite_a\n":  "[O1y]in:in Liitesana_a  ;\n[O2y]s:s Liitesana_a  ;\n",
#   "LEXICON Omistusliite_ä\n":  "[O1y]in:in Liitesana_ä  ;\n[O2y]s:s Liitesana_ä  ;\n",
#   "LEXICON Omistusliite_aä\n": "[O1y]in:in Liitesana_aä ;\n[O2y]s:s Liitesana_aä ;\n"
}


def write_sukija_additions (line, sukija_additions):
    try:
        outfile.write (sukija_additions[line])
    except KeyError:
        pass


# Copy Voikko vocabulary and insert forms that Sukija needs.
#
while True:
    line = infile.readline()
    if line == u"":
        break
    if line.find (u"[Tn4]mi@") == 0:  # 4. nimitapa (puhu+minen) ei ole teonsanan taivutusmuoto.
        continue
    if line.find ("vihanta[X]") >= 0:
        line = line.replace ("Emäntä_", "SukijaVihanta_")
    line = re.sub (ei_vertm, "", line)
    if line.find (ei_yks) > 0 and line.startswith ("[L"):
        if not line.startswith ("[Ln][Xp]lehdes[X]"):
            line = line.replace (ei_yks, "")
    if line.find (u"=") >= 0:
        line = line.replace (u"@P.YS_EI_JATKOA.ON@", u"")
    if line.find ("lähtöinen") >= 0:
        line = line.replace ("@R.YS_ALKANUT@", "")

    if OPTIONS["sukija-ys"]:
        line = line.replace (u"@P.YS_EI_JATKOA.ON@", u"")
        line = line.replace (u"@D.YS_EI_JATKOA@", u"")
        line = line.replace (u"@C.YS_EI_JATKOA@", u"")
    outfile.write (line)
    write_sukija_additions (line, sukija_additions)

    generate_all (line, list_all)

    write_arvaella (line)

    r = base_form_re.search (line)
    if r:
        generate_word (r, line, sukija_dictionary)
        generate_from_function (r, line, function_list)
    if (re_Xiljoona.search (line)):
        generate_xiljoona (line)
infile.close()

outfile.write (u"\n\n\n")

while True:
    line = sukijafile.readline()
    if line == u"":
        break
    if u"!" in line:
        line = line[0:line.find(u"!")]
    outfile.write (line)
sukijafile.close()

outfile.close()
