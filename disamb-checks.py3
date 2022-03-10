#!/usr/bin/python
# -*- coding: utf8 -*-
# coding=UTF-8
# CAVEAT : éviter la méthode "replace" qui retourne une chaine en ANSI - utiliser re.sub
# xxx.py on line x, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
# LA BIBLE : http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/

import os
import re
import sys
import importlib
# importlib.reload(sys).setdefaultencoding("utf-8")  # marche mais ne résoud pas le probleme de f.read() sur les fichiers en UTF-8
                                         # seul .decode('utf8') a marché

global fileINname,fileINnameshort,fichier, disamb

# need a more generic version of listerr
#   - adapts to the number of groups in finditer matches
#   - try the extract html for each match (NG or VG could be at any place in search sequence)

# generic version of listerr thanks to match.lastindex
def listerr(re_key):
  err_msg=""
  nerr=0
  allerr=re.finditer(re_key,disamb,re.U|re.MULTILINE)
  for match in allerr: 
    #print("match in allerr, match.lastindex",match.groups,match.lastindex)
    for n in range(1,match.lastindex+1):
      #print("match.group(",n,") =", match.group(n))
      if match.group(n)!=None:
        err_match=match.group(n)
        if "<span" in err_match:
          allng=re.finditer(r'<span class="w" stage="[^"]+">([^<\n]+)<',err_match,re.U|re.MULTILINE)
          ng=""
          for ngmatch in allng:
            ng=ng+ngmatch.group(1)+"¤"
          err_match="["+ng[:-1]+"]"  

        if err_match!="": 
          err_msg=err_msg+err_match+"_"
    err_msg=err_msg+" "

  if err_msg!="":
    err_msg,nerr=re.subn(r' ',' ‖ ',err_msg.strip())
    err_msg=err_msg.replace("_"," ")
    nerr=nerr+1
    if "¤" in err_msg: err_msg=err_msg.replace("¤"," ")
    err_msg=err_msg.replace("&lt;","<")
    err_msg=err_msg.replace("&gt;",">")

  return nerr, err_msg.strip()


fileINname= str(sys.argv[1])
INext=fileINname.find(".dis.html")
fileINnameshort=fileINname[0:INext]
fichier=fileINnameshort

fileIN = open(fileINname, "r")

#if os.path.exists(fileINnameshort+"-checks.txt") : sys.exit("\n      file "+fileINnameshort+"-checks.txt ALREADY EXISTS !\n")
fileOUT = open (fileINnameshort+"-checks.txt","w")

htmlfile=fileIN.read()
head,body=htmlfile.split("<body>")
#body=body.strip('</p></body></html>')
body=body[:-18]

# check if body has strange sentence ending sequence
body=re.sub(r'\n</span></span>\n</span>','\n</span>\n</span>\n</span>',body,0,re.U|re.MULTILINE)
# also need to worry about empty lines (cleanup needed)
# <span class="sent"> <span class="annot" />
# </span>
#
# also need to get rid of special character ﻿ as in:
#         </style></head><body><p><span class="sent">﻿
# &lt;h&gt;Galajo&lt;/h&gt;<span class="annot"><span class="c">﻿</span>
#

# check if file is new format nov 2021
if '</span><span class="w"' in body or '</span><span class="c"' in body:
  body=re.sub(r'\n</span><span class="(w|c|t)"','</span>\n<span class="\g<1>"',body,0,re.U|re.MULTILINE)

sentences=body.split("</span>\n</span>\n</span>\n")  # closing tag for last w|c|t + tag for annot + tag for sent

print(len(sentences), "sentences")

# define keywords
AMBIGUOUS =r'<span class="w" stage="[^"]+">([^<\n]+)<.*lemma var.*</span>\n'
UNKNOWN   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+</span>'
UNPARSED  =r'>([^<]+)<span class="lemma">[^<]+<span class="lemma var">[^<]+<'
INCOMPLETE=r'<span class="lemma">([^<\n]+)<sub class="ps">[^<\n]+</sub><span class="m">[^<\n]+<sub class="ps">[^<\n]+</sub></span>(?:<span class="m">[^<\n]+<sub class="ps">mrph</sub><sub class="gloss">[^<\n]+</sub></span>)+</span></span>'


#validate derivations - check with bamana.gram.txt - 
BADpl     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n|adj|ptcp).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">(?:n|adj|ptcp)</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>'
BADnmlz   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:li|ni)<sub class="ps">mrph</sub><sub class="gloss">NMLZ</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
BADagprm  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:la|na)<sub class="ps">mrph</sub><sub class="gloss">AG\.PRM</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
BADagocc  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:baga|baa)<sub class="ps">mrph</sub><sub class="gloss">AG\.OCC</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
BADcom    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n|adj).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">n</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:ma)<sub class="ps">mrph</sub><sub class="gloss">COM</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
BADadj    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!adj).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">vq</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:man)<sub class="ps">mrph</sub><sub class="gloss">ADJ</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'


BADpfvintr=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!v).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:la|na|ra)<sub class="ps">mrph</sub><sub class="gloss">PFV\.INTR</sub></span></span></span>'
BADprog   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!v).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:la|na)<sub class="ps">mrph</sub><sub class="gloss">PROG</sub></span></span></span>'

BADptcp   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!ptcp).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:len|nen)<sub class="ps">mrph</sub><sub class="gloss">PTCP\.RES</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'

#... tbc ... 



VERB      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub>.*</span></span>\n'
ADJ       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">adj</sub>.*</span></span>\n'
NUM       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">num</sub>.*</span></span>\n'
NAME      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:n|n\.prop)</sub>.*</span></span>\n'
PP        =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub>.*</span></span>\n'
PM        =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub>.*</span></span>\n'
COP       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">cop</sub>.*</span></span>\n'
VQ        =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">vq</sub>.*</span></span>\n'
NONVQ     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!vq).*)</sub>.*</span></span>\n'
ADV       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">adv</sub>.*</span></span>\n'
DTM       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">dtm</sub>.*</span></span>\n'
PRN       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:prn|pers)</sub>.*</span></span>\n'
CONJ      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub>.*</span></span>\n'
# ... tbc ...

# punctuations
START     =r'\^'
END       =r'\$'
PUNCT     =r'<span class="[ct]">([^<]+)</span>\n'  # any punctuations, tags included
HPUNCT    =r'<span class="c">([\.\;\:\!\?]+)</span>\n'  # hard punctuation marking sentence end
COMMA     =r'<span class="c">,</span>\n'  

# specifics
KAINF     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">INF</sub></span></span>\n'
KASBJV    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span></span>\n'
KAnon_SBJV=r'<span class="w" stage="[^"]+">(ka|k\'|ká|kà)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">(?:(?!SBJV).*)</sub></span></span>\n'
KAPOSS    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'
KAQUAL    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">QUAL\.AFF</sub></span></span>\n'
MANQUAL   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">QUAL\.NEG</sub></span></span>\n'
NONQUAL   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">[^<\n]+</sub><sub class="gloss">(?:(?!QUAL\.AFF|QUAL\.NEG).*)</sub></span></span>\n'
YEPFV     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">PFV\.TR</sub></span></span>\n'
YEIMP     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">IMP</sub></span></span>\n'
YEEQU     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">cop</sub><sub class="gloss">EQU</sub></span></span>\n'
MAPFV     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">PFV\.NEG</sub></span></span>\n'
MAPP      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">ADR</sub></span></span>\n'
A3SG      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pers</sub><sub class="gloss">3SG</sub></span></span>\n'
VERB1     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub><sub class="gloss">(?:(?!aller|venir).*)</sub>.*</span></span>\n'
VNONPERF  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub><sub class="gloss">((?!PFV\.INTR).)*</sub>.*</span></span>\n'
COP1      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">cop</sub><sub class="gloss">(?:(?!QUOT).*)</sub>.*</span></span>\n'
NIet      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub><sub class="gloss">et</sub></span></span>\n'
NIsi      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">conj</sub><sub class="gloss">si</sub></span></span>\n'
PMnon_INF  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">(?:(?!INF).*)</sub></span></span>\n'
PPnon_PP  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">(?:(?!PP).*)</sub></span></span>\n'
PPFINAL   =PP+PUNCT
FOprep    =r'''<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">prep</sub><sub class="gloss">jusqu'à</sub></span></span>\n'''
FOconj    =r'''<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">conj</sub><sub class="gloss">jusqu'à</sub></span></span>\n'''



# forbidden sequences
VERB_PP   =VERB+PP
ADV_PP    =ADV+PP    # peut arrive si la PP est précédée d'une clause : 
#                     surtout avec kojugu, kosɛbɛ [a sunògòkan min tè bò kosèbè] kosòn, a bè kè Lamidu Soma Nyakate nyèna ko a salen don / [jarabi bonya kojugu] fè
PP_VERB   =PP+VERB
VERB_ADJ  =VERB+ADJ
ADV_VERB  =ADV+VERB
COP_VQ    =COP+VQ
ADV_ADJ   =ADV+ADJ
PM_COP    =PM+COP     # note : COP_PM allowed : bɛ ka, tɛ ka ...
# ADJ_NAME  =ADJ+NAME    # en séquence NAME ADJ NAME, possible! "yuruguyurugu misɛnninw cayali"
NAME_VQ   =NAME+VQ
PP_VQ     =PP+VQ
ADJ_VQ    =ADJ+VQ
KAINF_VQ  =KAINF+VQ
KASBJV_VQ =KASBJV+VQ
KAPOSS_VQ =KAPOSS+VQ
MAPFV_VQ  =MAPFV+VQ
COP1_VERB  =COP1+VERB   # ok avec ko QUOT : a ko na n'a ye
A3SG_YEIMP=A3SG+YEIMP
VERB1_VERB=VERB1+VERB
PP_PPnon_PP     =PP+PPnon_PP    # pas mal d'exceptions avec 2ème PP=yé comme fin d'équative
PM_PM     =PM+PM
COP1_COP1  =COP1+COP1   # nb ye ko EQU QUOT accepté et ko ko QUOT QUOT accepté
KAQUAL_NONVQ=KAQUAL+NONVQ
MANQUAL_NONVQ=MANQUAL+NONVQ
NONQUAL_VQ  =NONQUAL+VQ
CONJ_COP1 =CONJ+COP1    # ko autorisé
CONJ_PMnon_INF   =CONJ+PMnon_INF   # autorisés avec kà INF : ni ka (rare, mais...), fo ka, janko ka ... ?
CONJ_VERB =CONJ+VERB
CONJ_ADV  =CONJ+ADV
CONJ_PP   =CONJ+PP
# COP1_CONJ =COP1_CONJ    # ko autorisé - NON a kɔnnen don n'o tɛ...
PM_CONJ   =PM+CONJ
# VERB_CONJ =VERBE_CONJ   # phrases avec absence de virgule derrière le verbe
# ADV_CONJ                # phrases avec absence de virgule derrière le verbe
FOprep_KAINF=FOprep+KAINF
FOprep_NIsi =FOprep+NIsi

# ...tbc...
# implement : NG (nominal group) NAME+ADJ*+DTM*+POSS*+AND*+... see NONVERBALGROUP in replc
# example forbiddden sequence : PM_NG_PP, PM_NG_ADV, PM_NG_VQ, 

# needs same definition without a capturing group: we only capture the whole NG
ADJ_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">adj</sub>.*</span></span>\n'
NAME_     =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:n|n\.prop)</sub>.*</span></span>\n'
DTM_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">dtm</sub>.*</span></span>\n'
PRN_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:prn|pers)</sub>.*</span></span>\n'
KAPOSS_   =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'
NUM_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">num</sub>.*</span></span>\n'
NIet_     =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub><sub class="gloss">et</sub></span></span>\n'
PP_       =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">pp</sub>.*</span></span>\n'
CONJ_     =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub>.*</span></span>\n'
CONJSBJV_ =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">(?:sánì|sánnì|sànní|yànní|wálasa|sànkó|fɔ́|yálasa|yáasa)<sub class="ps">(?:conj)</sub>.*</span></span>\n'

# manque pour l'instant les groupes avec ni et etc.

NG  = r'((?:'+NAME_+r'|'+PRN_+r'|'+DTM_+r')'+r'(?:'+NAME_+r'|'+ADJ_+r'|'+DTM_+r'|'+NUM_+r'|'+PP_+NAME_+r'|'+NIet_+NAME_+r'|'+COMMA+r')*)'
NG2 = r'((?:'+NAME_+r'|'+PRN_+r'|'+DTM_+r')'+r'(?:'+NAME_+r'|'+ADJ_+r'|'+DTM_+r'|'+NUM_+r'|'+PP_+NAME_+r'|'+NIet_+NAME_+r')*)'

# print(NG)

PP1       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">(?:(?!POSS).*)</sub>.*</span></span>\n'
#   =pp sans ka POSS
PM_NG_PPFINAL  =PM+NG+PPFINAL    # difficulty with split orthography : a be dugu kɔnɔ mɔgɔw ɲɔgɔri - only ka POSS accepted in NG/NG1
PM_NG_ADV =PM+NG+ADV
PM_NG_VQ  =PM+NG+VQ
PM_NG_HPUNCT=PM+NG+HPUNCT
# print(PM_NG_PUNCT)
PM_NG_END =PM+NG+END   # only if missing final punctuation
PM_NG_PM  =PM+NG+PM
VERB1_NG_VNONPERF=VERB1+NG+VNONPERF  # VPERF peut se trouver légitimement après : i n'a fɔ... / o y'a sɔro ... et VPERF
        # taa/na sont exclus de VERB1, mais la construction peut exister avec se : mɔgɔ si kana se a filɛ yen.
FOconj_NG_MAPP=FOconj+NG+MAPP

# it would be interesting to define a VERBALGROUP, or "proposition/verbal clause"
# for instance ( NG PM NG* VNONPERF|VQ)  | ( NG VPERF )
# ignoring for now adverbs and postposition following the verb
PM_       =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">pm</sub>.*</span></span>\n'
VNONPERF_ =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">v</sub><sub class="gloss">((?!PFV\.INTR).)*</sub>.*</span></span>\n'
VQ_       =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">vq</sub>.*</span></span>\n'

VG = r'('+NG2+PM_+NG2+r'*(?:'+VNONPERF_+r'|'+VQ_+r'))'
VG2= r'('+NG2+r'*(?:'+VNONPERF_+r'))'

FOprep_VG =FOprep+VG
#print(FOprep_VG)

# larger sequences
TEST_KASBJV=r'(?:'+START+r'|'+PUNCT+r'|'+CONJSBJV_+r')'+NG2+KAnon_SBJV+VG2
#print ("TEST_KASBJV:\n",TEST_KASBJV)
nsent=0
nsenterr=0
fileOUT.write("Légende :\nGn: Groupe nominal,\nPM: Marque prédicative,\nCOP: Copule,\nPP: Postposition,\nADV: Adverbe,\nADJ: Adjectif,\nCONJ: Conjonction\n")
fileOUT.write("Ces vérifications ne sont ni toujours pertinentes, ni exhaustives...\nEn espérant que cela reste malgré tout utile !\n\n")


for sentence in sentences:
  nsent=nsent+1
  sentence=sentence+"</span>\n"   # close last lemma or punct or tag
  
  if '<span class="annot">' not in sentence: continue
  #print("\nSentence # ",nsent,"\n",sentence,"\n")
  orig,disamb=sentence.split('<span class="annot">')

  disamb="\^"+disamb+"\$"
  originalsent=re.search('<span class="sent">([^<]*)',orig,re.U|re.MULTILINE)
  original=originalsent.group(1)
  original=original.replace("&lt;","<")
  original=original.replace("&gt;",">")
  original=original.replace("\n"," ")
  original=re.sub(r' +', ' ',original)

  errors=""
  nerr=0
  nerr2=0
  nerr3=0
  nerr4=0

  nerr,err_msg=listerr(AMBIGUOUS)
  if nerr>0:
    plural="s"
    if nerr==1: plural=""
    errors=errors+"    "+str(nerr)+" mot"+plural+" ambigu"+plural+": "+err_msg+"\n"

  nerr2,err_msg=listerr(UNKNOWN)
  if nerr2>0:
    plural="s"
    if nerr2==1: plural=""
    errors=errors+"    "+str(nerr2)+" mot"+plural+" inconnu"+plural+": "+err_msg+"\n"
    nerr=nerr+nerr2

  nerr3,err_msg=listerr(UNPARSED)
  if nerr3>0:
    plural="s"
    if nerr3==1: plural=""
    errors=errors+"    "+str(nerr3)+" mot"+plural+" mal parsé (gparser) : "+err_msg+"\n"
    nerr=nerr+nerr3

  nerr4,err_msg=listerr(INCOMPLETE)
  if nerr4>0:
    plural="s"
    if nerr4==1: plural=""
    errors=errors+"    "+str(nerr4)+" mot"+plural+" incomplet (seulement une ou des dérivations) : "+err_msg+"\n"
    nerr=nerr+nerr4

  nerr5,err_msg=listerr(BADpl)
  if nerr5>0:
    plural="s"
    if nerr5==1: plural=""
    errors=errors+"    "+str(nerr5)+" mot"+plural+" :mrph:PL pluriel mais pas n, adj ou ptcp ?) : "+err_msg+"\n"
    nerr=nerr+nerr5

  nerr6,err_msg=listerr(BADnmlz)
  if nerr6>0:
    plural="s"
    if nerr6==1: plural=""
    errors=errors+"    "+str(nerr6)+" mot"+plural+" :mrph:NMLZ mais pas n ?) : "+err_msg+"\n"
    nerr=nerr+nerr6

  nerr7,err_msg=listerr(BADagprm)
  if nerr7>0:
    plural="s"
    if nerr7==1: plural=""
    errors=errors+"    "+str(nerr7)+" mot"+plural+" :mrph:AG.PRM mais pas n ?) : "+err_msg+"\n"
    nerr=nerr+nerr7

  nerr8,err_msg=listerr(BADagocc)
  if nerr8>0:
    plural="s"
    if nerr8==1: plural=""
    errors=errors+"    "+str(nerr8)+" mot"+plural+" :mrph:AG.OCC mais pas n ?) : "+err_msg+"\n"
    nerr=nerr+nerr8

  nerr9,err_msg=listerr(BADpfvintr)
  if nerr9>0:
    plural="s"
    if nerr9==1: plural=""
    errors=errors+"    "+str(nerr9)+" mot"+plural+" :mrph:PFV.INTR mais pas v ?) : "+err_msg+"\n"
    nerr=nerr+nerr8

  nerr10,err_msg=listerr(BADptcp)
  if nerr10>0:
    if err_msg in ["fɔlen","kɔrɔlen"]: nerr10=0
    else:
      plural="s"
      if nerr10==1: plural=""
      errors=errors+"    "+str(nerr10)+" mot"+plural+" :mrph:PTCP.RES mais pas ptcp ?) : "+err_msg+"\n"
      nerr=nerr+nerr10

  nerr11,err_msg=listerr(BADprog)
  if nerr11>0:
    plural="s"
    if nerr11==1: plural=""
    errors=errors+"    "+str(nerr11)+" mot"+plural+" :mrph:PROG mais pas v ?) : "+err_msg+"\n"
    nerr=nerr+nerr11

  nerr12,err_msg=listerr(BADcom)
  if nerr12>0:
    plural="s"
    if nerr12==1: plural=""
    errors=errors+"    "+str(nerr12)+" mot"+plural+" :mrph:COM mais pas n/adj ?) : "+err_msg+"\n"
    nerr=nerr+nerr12

  nerr13,err_msg=listerr(BADadj)
  if nerr13>0:
    plural="s"
    if nerr13==1: plural=""
    errors=errors+"    "+str(nerr13)+" mot"+plural+" :mrph:ADJectivateur de vq mais pas adj ?) [ ignorer si nominalisation ]: "+err_msg+"\n"
    nerr=nerr+nerr13


  # --- si une des erreurs de validations ci-dessus ne pas faire les autres tests de cohérence ---
  # --- ignore further tests if error in one of the above

  if nerr != 0 :
    errors=errors+"    j'ignore les autres tests...\n"
  else:

    nerr,err_msg=listerr(VERB1_VERB)
    if nerr>0:
      avis="(deux verbes qui se suivent) ?"
      if "se " in err_msg:
        avis=avis+" [comme pour nà ou táa (régulier), parfois possible avec sé (ignorer)]"
      errors=errors+"    "+str(nerr)+" VERBE VERBE "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(PP_PPnon_PP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PP PP (deux postpositions successives? voir adverbes ou pp composées) ? "+err_msg+"\n"

    nerr,err_msg=listerr(PM_PM)
    if nerr>0:
      avis="(deux marques prédicatives qui se suivent)"
      if "k' " in err_msg : avis=avis+" [ k'=ko QUOT ?]"
      errors=errors+"    "+str(nerr)+" PM PM "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(COP1_COP1)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" COP COP (deux copules qui se suivent) ? "+err_msg+"\n"

    nerr,err_msg=listerr(VERB_PP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" VERBE PP (verbe suivi d'une postposition - voir adverbes possibles) ? "+err_msg+"\n"
    
    nerr,err_msg=listerr(ADV_PP)
    if nerr>0:
      if "kojugu " in err_msg or "kosɛbɛ " in err_msg or "kosèbè " in err_msg : continue # ignore for now
      avis="(adverbe suivi d'une postposition) [l'adv. est un nom? la pp est un adv.?]"
      errors=errors+"    "+str(nerr)+" ADV PP "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(PP_VERB)
    if nerr>0:
      avis="(postposition avant un verbe [ignorer si impératif/ponctuation défectueuse]) ? "
      if "ma " in err_msg: avis=avis+" [peut-être est-ce ma:pm:PFV.NEG] "
      errors=errors+"    "+str(nerr)+" PP VERBE "+avis+": "+err_msg+"\n"

    nerr,err_msg=listerr(VERB_ADJ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" VERBE ADJ (verbe suivi d'un adjectif) ? "+err_msg+"\n"
    
    nerr,err_msg=listerr(ADV_VERB)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ADV VERBE (adverbe précédent un verbe mais pas adv.p) ? "+err_msg+"\n"

    nerr,err_msg=listerr(COP_VQ)
    if nerr>0:
      avis="(copule avant un verbe qualitatif)"
      if "bɛ " in err_msg or "bɛ́ " in err_msg: avis=avis+" [possible mais rare avec bɛ́:cop:être]"
      errors=errors+"    "+str(nerr)+" COP VQ "+avis+": "+err_msg+"\n"

    nerr,err_msg=listerr(ADV_ADJ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ADV ADJ (adverbe suivi d'un adjectif) ? "+err_msg+"\n"

    nerr,err_msg=listerr(PM_COP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM COP (marque prédicative suivie d'une copule) ? "+err_msg+"\n"

    nerr,err_msg=listerr(NAME_VQ)
    if nerr>0:
      avis="(nom devant un verbe qualitatif)"
      avis=avis+"[le vq peut-il être une adjectif?]"
      errors=errors+"    "+str(nerr)+" NOM VQ "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(PP_VQ)
    if nerr>0:
      avis="(postposition devant un verbe qualitatif)"
      if "ka " in err_msg: avis=avis+"[le ka pp:POSS devrait être pm:QUAL.AFF]"
      errors=errors+"    "+str(nerr)+" PP VQ "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(ADJ_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ADJ VQ (adjectif devant un verbe qualitatif) ? "+err_msg+"\n"

    nerr,err_msg=listerr(MAPFV_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ma(PFV) VQ (ma PFV devant un vq) [devrait être man:pm:QUAL.NEG] : "+err_msg+"\n"

    nerr,err_msg=listerr(KAINF_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ka(INF) VQ (kà infinitif devant un vq) [devrait être ka:pm:QUAL.AFF] : "+err_msg+"\n"

    nerr,err_msg=listerr(KASBJV_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ka(SBJV) VQ (ka subjonctif devant un vq) [devrait être ka:pm:QUAL.AFF) : "+err_msg+"\n"

    nerr,err_msg=listerr(KAPOSS_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ka(POSS) VQ (ka POSS devant un vq) [devrait être ka:pm:QUAL.AFF) : "+err_msg+"\n"

    nerr,err_msg=listerr(COP1_VERB)
    if nerr>0:
      avis="(copule devant un verbe - au lieu d'une marque prédicative) "
      if "bɛ " in err_msg : avis=avis+"[devrait être pm:IPFV.AFF]"
      if "tɛ " in err_msg : avis=avis+"[devrait être pm:IPFV.NEG]"
      errors=errors+"    "+str(nerr)+" COP VERBE "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(A3SG_YEIMP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" a(3SG) ye(IMP) (devrait être á' 2PL) : "+err_msg+"\n"

    nerr,err_msg=listerr(KAQUAL_NONVQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ka(QUAL) NONVQ (groupe qualificatif ou pas?) : "+err_msg+"\n"

    nerr,err_msg=listerr(MANQUAL_NONVQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" man(QUAL) NONVQ (groupe qualificatif ou pas?) : "+err_msg+"\n"

    nerr,err_msg=listerr(NONQUAL_VQ)
    avis="(groupe qualificatif ou pas?)"
    if " kan" in err_msg: avis=avis+" [possible mais rare avec kán:vq:égal]"
    if nerr>0:
      errors=errors+"    "+str(nerr)+" NONQUAL VQ "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(CONJ_COP1)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" CONJ COP (conjonction devant une copule) : "+err_msg+"\n"

    nerr,err_msg=listerr(CONJ_PMnon_INF)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" CONJ PM(non_INF) (conjonction devant une marque prédicative) : "+err_msg+"\n"

    nerr,err_msg=listerr(PM_CONJ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM CONJ (marque prédicative devant une conjonction) : "+err_msg+"\n"

    nerr,err_msg=listerr(CONJ_VERB)
    if nerr>0:
      avis="(conjonction devant un verbe ) "
      if "o " in err_msg or "ó " in err_msg:
        avis=avis+"[ignorer si ó:conj:DISTR]"
      else:
        avis=avis+"[ignorer si impératif]"
      if err_msg!="o mɛɛn":  # construction acceptée mɛɛn o mɛɛn avec v au lieu de conv.n ...
        errors=errors+"    "+str(nerr)+" CONJ VERBE "+avis+": "+err_msg+"\n"

    nerr,err_msg=listerr(CONJ_PP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" CONJ PP (conjonction devant une postposition) : "+err_msg+"\n"

    nerr,err_msg=listerr(FOprep_KAINF)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" fo(prep) ka(INF) (devrait être fó/fɔ́ conj) : "+err_msg+"\n"

    nerr,err_msg=listerr(FOprep_NIsi)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" fo(prep) NIsi (devrait être fó/fɔ́ conj) : "+err_msg+"\n"

    nerr,err_msg=listerr(FOprep_VG)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" fo(prep) GroupeVerbal (devrait être fó/fɔ́ conj) : "+err_msg+"\n"


#------------------- 3 terms, NG middle

    nerr,err_msg=listerr(PM_NG_PPFINAL)
    if nerr>0:
      avis="(pas de verbe avant la postposition)"
      if " ye" in err_msg and ("ye " in err_msg or "y' " in err_msg): avis=avis+" [le 1er ye devrait être cop:EQU?]"
      errors=errors+"    "+str(nerr)+" PM Gn PPfinale "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(PM_NG_ADV)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM Gn ADV (pas de verbe avant l'adverbe) : "+err_msg+"\n"

    nerr,err_msg=listerr(PM_NG_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM Gn VQ (un intru avant le VQ) : "+err_msg+"\n"

    nerr,err_msg=listerr(PM_NG_HPUNCT)
    # print(original, "PM_NG_HPUNCT", nerr, err_msg)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM Gn Ponct. (pas de verbe avant la ponctuation) : "+err_msg+"\n"

    nerr,err_msg=listerr(PM_NG_END)  # caution : END does not return a word match : not listerr
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM Gn Fin (pas de verbe avant la fin de phrase) : "+err_msg+"\n"

    nerr,err_msg=listerr(PM_NG_PM)
    if nerr>0:
      avis="(deux marques prédicatives qui se suivent)"
      if "k' " in err_msg : avis=avis+" [k'=ko QUOT ?]"
      else : avis=avis+" [verbe mal identifié?]"
      errors=errors+"    "+str(nerr)+" PM Gn PM "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(VERB1_NG_VNONPERF)
    if nerr>0:
      avis="(deux verbes successifs [ignorer si impératifs]) ? "
      if "se " in err_msg: avis=avis+" [comme pour nà ou táa (régulier), parfois possible avec sé (ignorer)]"
      errors=errors+"    "+str(nerr)+" VERBE Gn V(non PERF) "+avis+" : "+err_msg+"\n"

    nerr,err_msg=listerr(FOconj_NG_MAPP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" fo(conj) Gn ma(PP) (devrait être fó/fɔ́ prep) : "+err_msg+"\n"

    nerr,err_msg=listerr(TEST_KASBJV)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ka(non SBJV) (devrait être ka:pm:SBJV) : "+err_msg+"\n"

  if errors!="" : 
    fileOUT.write(str(nsent)+" "+original+"\n"+errors+'\n')
    nsenterr=nsenterr+1

fileOUT.close()
if nsenterr>0:
  print(nsenterr,"sentences with errors\ncheck output as "+fileINnameshort+"-checks.txt")
else :
  os.remove(fileINnameshort+"-checks.txt")
  print("no error found, "+fileINnameshort+"-checks.txt NOT created")