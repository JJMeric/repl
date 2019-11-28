#!/usr/bin/env python
# -*- coding: utf-8 -*-

# quick memo re processor number- this could be used to get one REPL-C file per processor:
# REPL-STANDARD-C-processor_1.txt, REPL-STANDARD-C-processor_2.txt ...
"""
import os
import psutil
p=psutil.Process(os.getpid())
p.cpu_num()
"""

import os
import re
#import regex # TESTS NON CONCLUANTS PAR RAPPORT A re // (((?!lemma\svar).)*)
# il faudrait pouvoir utiliser à la place Oniguruma , comme Sublime Text 2
# problème résolu maintenant mais je laisse quand même ce commentaire pour référence 2/5/16
import sys
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#import daba.formats

import psutil
pid=os.getpid()
#print "pid : ",pid
p=psutil.Process(pid)
#print "psutil.Process(pid) : p = ",p
p.cpu_num()
ncpu=p.cpu_num()
#print "p.cpu_num : ",ncpu

#import unicodedata as u
from time import gmtime, strftime, time
# print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
import time
timestart=time.time()
# directory where this script resides
scriptdir = os.path.dirname(os.path.realpath(__file__))

textscript=re.compile(ur'\<meta content\=\"([^\"]*)\" name\=\"text\:script\" \/\>',re.U)
ambiguous=re.compile(ur'\<span class\=\"w\".*lemma var.*\n\<\/span\>')

nargv=len(sys.argv)
if nargv==1 : 
  print "repl.py needs one argument : file name"
  sys.exit
if nargv>1 : filename= str(sys.argv[1])

if ".dis.fra" in filename:
  #sys.exit("repl.py does not handle .dis.fra files")
  print "WARNING repl.py does not know how to handle .dis.fra files - results unclear"
#elif ".pars.html" in filename :
if ".pars.html" in filename :
  i_pars=filename.find(".pars.html")
  filenametemp=filename[0:i_pars]
else : # nom donné sans extension (défaut recommandé)
  filenamein=filename+".pars.html"
  filenametemp=filename
filegiven=filenamein
filenameout=filenametemp+".repl.html"

fileIN = open(filenamein, "rb")
fileOUT = open (filenameout,"wb")
tonal=""

try:
    fileREPC= open ("REPL-C.txt","r")
    print "using REPL-C.txt"
except : 
  try:
    fileREPCname="REPL-STANDARD-C.txt"
    tonal="new"
    if filenametemp.endswith(".old"):
      if  filenametemp.startswith("baabu_ni_baabu") :
        fileREPCname = "REPL-STANDARD-C-ny.txt"
        tonal = "newny"
      else:
        fileREPCname = "REPL-STANDARD-C.old.txt"
        tonal = "old"
    fileREPC = open (fileREPCname,"r")
      
  except:
    try:
      fileREPCname = os.path.join(scriptdir, "REPL-STANDARD-C.txt")
      tonal="new"
      if filenametemp.endswith(".old") :
        if  filenametemp.startswith("baabu_ni_baabu") :
          fileREPCname = os.path.join(scriptdir, "REPL-STANDARD-C-ny.txt")
          tonal = "newny"
        else :
          fileREPCname = os.path.join(scriptdir, "REPL-STANDARD-C.old.txt")
          tonal="old"

      fileREPC = open (fileREPCname,"r")

    except :
      sys.exit(fileREPCname+" ? repl.py needs a REPL-C.txt file or a REPL-STANDARD-C.txt file in the current directory (or in "+scriptdir+" )")

# read all file in one go
replall=fileREPC.read()
fileREPC.close()
linereplall=replall.split("\n")

nbreplok=0
nbmodif=0
nbmots=0
nbrulesapplied=0

tout=u""
lineOUT=u""
tout=fileIN.read()
tout=tout.decode("utf-8")

txtsc=textscript.search(tout)
if txtsc!=None :   # supposedly = if txtsc :
  script=txtsc.group(1)
else :
    script="Nouvel orthographe malien"
    if filenametemp.endswith(".old"): script="Ancien orthographe malien"
    print " ! textscript not set for "+filenametemp+" !!!  ASSUMED : "+script

if script=="Ancien orthographe malien" : tonal="old"
elif script=="Nouvel orthographe malien" : tonal="new"

if  filenametemp.startswith("baabu_ni_baabu") or filenametemp.startswith("gorog_meyer-contes_bambara1974") :
  tonal="newny"

if tonal=="" : sys.exit("text:script non defini : pas de meta ou pas d'argument (tonal, bailleul)")

totalmots = tout.count("class=\"w\"")   # is needed in the final message to compute average ambiguous left and elapse time/word

# PRE : systematic global replaces  #################################################################

# normalize single quotes to avoid pop-up messages in gdisamb complaining that k' is not the same as k’
# tilted quote (word) to straight quotes (as in Bamadaba)
tout=re.sub(u"’",u"'",tout,0,re.U|re.MULTILINE)

# eliminer EMPR ex: ONI::EMPR
# see last section of bamana.gram
wsearch=ur'<span class="w" stage="[^\"]+">([A-Z\-]+)<span class="lemma">[a-z\-]+<sub class="gloss">EMPR</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # eliminer EMPR ex: ONI::EMPR
# dots in calculated lemma or lemma var cause artificial ambiguity sometimes 22/12/18 kalayali
# first dot
wsearch=ur'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=ur'<span class="\g<1>">\g<2>\g<3><'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# second dot
wsearch=ur'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=ur'<span class="\g<1>">\g<2>\g<3><'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# third dot
wsearch=ur'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=ur'<span class="\g<1>">\g<2>\g<3><'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# more dots ignored

# autres ABR possibles
wsearch=ur'<span class="w" stage="-1">([A-Z\-0-9]+)<span class="lemma">[a-zA-Z\-0-9]+</span>\n</span>'
wrepl=ur'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # autres ABR possibles

#eliminer gloss vides ex: baarakelen::
wsearch=ur'<span class="lemma var">([^<]+)</span>'
wrepl=ur''
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # gloss vides ex: baarakelen::

# ex plus difficile pour les pluriels de mots inconnus (et d'autres dérivations communes possibles ?... à surveiller!)
wsearch=ur'<span class="lemma">[^<]+<span class="lemma var">[^<]+<sub class="ps">n/adj/dtm/prn/ptcp/n\.prop/num</sub><span class="m">[^<]+<sub class="ps">n/adj/dtm/prn/ptcp/n\.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">(((?!lemma var).)+)</span>((<span class="lemma var">[^\n]+</span>)*)</span>\n</span>'
wrepl=ur'<span class="lemma">\g<1></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss vide en lemma et n/adj/dtm/prn/ptcp/n.prop/num

# éliminer les doublons dans les lemma var (pas nécessairement contigüs) NE MARCHE PAS STRUCTURE CASSEE
wsearch=ur'<span class="lemma var">(?P<stem>[^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub>(?P<stemgloss>[^\n]+)</span><span class="lemma var">(?P=stem)<sub class="ps">(?P=stemps)</sub>(?P=stemgloss)</span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub>\g<3></span>'

tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma var/lemma var

# Éliminer les doublons lemma / lemma var qui suit (même mot dans 2 dicos, 2 dérivations similaires appliquées…)
wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub><sub class="gloss">([^<]+)</sub>(?P<stemm>.+)<span class="lemma var">[^<]+<sub class="ps">(?P=stemps)</sub>(?P=stemm)</span></span>\n</span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<3></sub>\g<4></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var

# éliminer les gloses bizarres des ordinaux : <span class="lemma">39nan<span class="lemma var">39nan<
wsearch=ur'<span class="lemma">(?P<stem>[0-9]+)nan<span class="lemma var">(?P=stem)nan<sub class="ps">adj</sub><span class="m">(?P=stem)<sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span></span>\n'
wrepl=ur'<span class="lemma">\g<1>nan<sub class="ps">adj</sub><span class="m">\g<1><sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var

# remettre dans l'ordre n/v les doublons dictionnaire v/n pour les détections NORV

# CAS COMPLEXE avec sub m
wsearch=ur'<span class="w" stage="([^>]+)">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span>\n</span>'
wrepl=ur'<span class="w" stage="\g<1>">\g<2><span class="lemma">\g<6><sub class="ps">n</sub><\g<7>><span class="lemma var">\g<3><sub class="ps">v</sub><\g<4>></span></span>\n</span>'
# attention décalage $5 $6 -> $6 $7 à cause de la formule (((?!lemma var).)*)
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
# éliminer les doublons où le second choix, calculé, n'a pas de glose
wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">(?P<ps>[^<]+)</sub><sub class="gloss">(?P<gloss>[^<]+)</sub><(?P<details>((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">(?P=ps)</sub><sub class="gloss">(?P=gloss)</sub><(?P=details)></span></span>\n</span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<3></sub><\g<4>></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
#
# déterminer les noms propres, même vaguement!
#
# mot non initial commençant par une majuscule
# et ambigu :
# remarque : ça pose problème pour Waraba, Suruku, Sonsannin... pour l'instant fixés dans REPL-STANDARD

wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.CL</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.CL</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.M</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.M</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.F</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.F</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">((((?!lemma var).)+)GENT(((?!lemma var).)+))<span class="lemma var">[^\n]+</span></span>\n'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3></span>\n'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">[^<]+<span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<2><sub class="ps">n.prop</sub><sub class="gloss">NOM</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# essai avec sous-structure : (((?!<span class="lemma var">).)+)
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">(((?!<span class="lemma var">).)+)<span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
wsearch=ur"(</span>|</span>\n)<span class=\"w\" stage=\"[0-9\-]+\">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class=\"lemma\">[^<]+<span class=\"lemma var\">.+></span>\n"
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<2><sub class="ps">n.prop</sub><sub class="gloss">NOM</sub></span>\n'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)

#Added oct 2019:
# handling NUMnan type not handled well in gparser (bamana.gram rules no longer works)
prefsearch=ur'<span class="sent">([^<]*)(?P<stem>[0-9]+)(?P<stemnan>nan|NAN|n)([\s\.\;\:\?\!\)\""][^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
nextsearch=ur'<span class="w" stage="tokenizer">(?P=stem)<span class="lemma">(?P=stem)<sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span>\n</span><span class="w" stage="[^\"]">(?P=stemnan)<span class="lemma">(?:nan|ń)<sub class="ps">(?:num|pers)</sub><sub class="gloss">(?:ORD|1SG)</sub></span>\n</span>'
prefrepl=u'<span class="sent">\g<1>\g<2>\g<3>\g<4><span class="annot">\g<5>'
nextrepl=u'<span class="w" stage="0">\g<2>\g<3><span class="lemma">\g<2>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<2><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n</span>'
wsearch=prefsearch+nextsearch
wrepl=prefrepl+nextrepl
#print "\nNUMnan wsearch:",wsearch
nombre=1
while nombre>0:
  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)

# handling NUM nan types not handled well in gparser
prefsearch=ur'<span class="sent">([^<]*)(?P<stem>[0-9]+) (?P<stemnan>nan|NAN)([\s\.\;\:\?\!\)\"][^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
nextsearch=ur'<span class="w" stage="tokenizer">(?P=stem)<span class="lemma">(?P=stem)<sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span>\n</span><span class="w" stage="2">(?P=stemnan)<span class="lemma">nan<sub class="ps">num</sub><sub class="gloss">ORD</sub></span>\n</span>'
prefrepl=u'<span class="sent">\g<1>\g<2>\g<3>\g<4><span class="annot">\g<5>'
nextrepl=u'<span class="w" stage="0">\g<2>\g<3><span class="lemma">\g<2>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<2><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n</span>'
wsearch=prefsearch+nextsearch
wrepl=prefrepl+nextrepl
#print "\nNUM nan wsearch:",wsearch
nombre=1
while nombre>0:
  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)


# NOW THE BIG TASK     -go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!--

nblinerepl=0

for linerepl in linereplall:
  if "===" in linerepl :
    wsearch, wrepl = linerepl.split("===")
    wsearch=ur""+wsearch  # this ensures wsearch is an re string!!!IMPORTANT!!!
    tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # derniers parametres : count (0=no limits to number of changes), flags re.U|


# PMINF POST correction for k' and K'
wsearch=ur'<span class="w" stage="0">(k\'|K\')<span class="lemma">kà<sub class="ps">pm</sub><sub class="gloss">INF</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">\g<1><span class="lemma">k'<sub class="ps">pm</sub><sub class="gloss">INF</sub></span>\n</span>"""
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# PMSBJV POST correction for k' and K'
wsearch=ur'<span class="w" stage="0">(k\'|K\')<span class="lemma">ka<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">\g<1><span class="lemma">k'<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span>\n</span>"""
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# NICONJet POST correction for n'
wsearch=ur'<span class="w" stage="0">n\'<span class="lemma">ni<sub class="ps">conj</sub><sub class="gloss">et</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">n'<span class="lemma">n'<sub class="ps">conj</sub><sub class="gloss">et</sub></span>\n</span>"""
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  

# NICONJsi POST correction for n'
wsearch=ur'<span class="w" stage="0">n\'<span class="lemma">ní<sub class="ps">conj</sub><sub class="gloss">si</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">n'<span class="lemma">n'<sub class="ps">conj</sub><sub class="gloss">si</sub></span>\n</span>"""
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# IPFVAFF POST correction for b'
wsearch=ur'<span class="w" stage="0">b\'<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">b'<span class="lemma">b'<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>"""
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# IPFVAFF POST correction for be
wsearch=ur'<span class="w" stage="0">be<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">be<span class="lemma">be<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# IPFVAFF POST correction for bi
wsearch=ur'<span class="w" stage="0">bi<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">bi<span class="lemma">bi<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# IPFVNEG POST correction for t'
wsearch=ur'<span class="w" stage="0">t\'<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">t'<span class="lemma">t'<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>"""
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# IPFVNEG POST correction for te
wsearch=ur'<span class="w" stage="0">te<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">te<span class="lemma">te<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# IPFVNEG POST correction for ti
wsearch=ur'<span class="w" stage="0">ti<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">ti<span class="lemma">ti<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
tout=re.sub(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
# FINISH

fileOUT.write(tout)
fileIN.close()
fileOUT.close()
fileREPC.close()

ambs=ambiguous.findall(tout)
nbambs=len(ambs)
   
timeend=time.time()
timeelapsed=timeend-timestart
# en minutes, approximativement
print ncpu," ; ",filenameout+" ; ",totalmots," ; ",nbambs," ; ",int(timeelapsed)