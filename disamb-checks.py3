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

def listerr(re_key):
  err_msg=""
  nerr=0
  allerr=re.finditer(re_key,disamb,re.U|re.MULTILINE)
  for match in allerr: 
    err_match=match.group(1)
    if err_match!="":
      err_msg=err_msg+err_match+" "
  if err_msg!="":
    err_msg,nerr=re.subn(r' ',', ',err_msg.strip())
    nerr=nerr+1
  return nerr, err_msg

def listerr2(re_key):
  err_msg=""
  nerr=0
  allerr=re.finditer(re_key,disamb,re.U|re.MULTILINE)
  for match in allerr: 
    err_match=match.group(1)
    err_match2=match.group(2)
    if err_match!="": 
      err_msg=err_msg+err_match+"_"+err_match2+" "
  if err_msg!="":
    err_msg,nerr=re.subn(r' ',', ',err_msg.strip())
    err_msg=err_msg.replace("_"," ")
    nerr=nerr+1
  return nerr, err_msg

def listerr3(re_key):
  err_msg=""
  nerr=0
  allerr=re.finditer(re_key,disamb,re.U|re.MULTILINE)
  for match in allerr: 
    err_match=match.group(1)
    #print("listerr3 (1)", err_match)
    err_match2=match.group(2)  # if NG there is html<> and there are spaces - oops ?
    if "<span" in err_match2:
      allng=re.finditer(r'<span class="w" stage="[^"]+">([^<\n]+)<',err_match2,re.U|re.MULTILINE)
      ng=""
      for ngmatch in allng:
        ng=ng+ngmatch.group(1)+"¤"
      err_match2="{"+ng[:-1]+"}"  

    err_match3=match.group(3)
    if err_match!="": 
      err_msg=err_msg+err_match+"_"+err_match2+"_"+err_match3+" "
  if err_msg!="":
    err_msg,nerr=re.subn(r' ',', ',err_msg.strip())
    err_msg=err_msg.replace("_"," ")
    if "¤" in err_msg: err_msg=err_msg.replace("¤"," ")
    nerr=nerr+1
  return nerr, err_msg

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

# check if file is new format nov 2021
if '</span><span class="w"' in body or '</span><span class="c"' in body:
  body=re.sub(r'\n</span><span class="(w|c|t)"','</span>\n<span class="\g<1>"',body,0,re.U|re.MULTILINE)

sentences=body.split("</span>\n</span>\n</span>\n")  # closing tag for last w|c|t + tag for annot + tag for sent

print(len(sentences), "sentences")

# define keywords
AMBIGUOUS =r'<span class="w" stage="[^"]+">([^<\n]+)<.*lemma var.*</span>\n'
UNKNOWN   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+</span>'
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
START     =r'^'
END       =r'$'
PUNCT     =r'<span class="[ct]">([^<]+)</span>\n'  # any punctuations, tags included
HPUNCT    =r'<span class="[c]">([\.\;\:\!\?]+)</span>\n'  # hard punctuation marking sentence end

# specifics
KAINF     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">INF</sub></span></span>\n'
KASBJV    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span></span>\n'
KAPOSS    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'
KAQUAL    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">QUAL\.AFF</sub></span></span>\n'
MANQUAL   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">QUAL\.NEG</sub></span></span>\n'
NONQUAL   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">[^<\n]+</sub><sub class="gloss">(?:(?!QUAL\.AFF|QUAL\.NEG).*)</sub></span></span>\n'
YEPFV     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">PFV\.TR</sub></span></span>\n'
YEIMP     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">IMP</sub></span></span>\n'
YEEQU     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">cop</sub><sub class="gloss">EQU</sub></span></span>\n'
MAPFV     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">PFV\.NEG</sub></span></span>\n'
A3SG      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pers</sub><sub class="gloss">3SG</sub></span></span>\n'
VERB1     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub><sub class="gloss">(?:(?!aller|venir).*)</sub>.*</span></span>\n'
COP1       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">cop</sub><sub class="gloss">(?:(?!QUOT).*)</sub>.*</span></span>\n'


# forbidden sequences
VERB_PP   =VERB+PP
ADV_PP    =ADV+PP
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
COP_VERB  =COP+VERB
A3SG_YEIMP=A3SG+YEIMP
VERB1_VERB=VERB1+VERB
PP_PP     =PP+PP
PM_PM     =PM+PM
COP1_COP1  =COP1+COP1   # nb ye ko EQU QUOT accepté et ko ko QUOT QUOT accepté
KAQUAL_NONVQ=KAQUAL+NONVQ
MANQUAL_NONVQ=MANQUAL+NONVQ
NONQUAL_VQ  =NONQUAL+VQ

# ...tbc...
# implement : NG (nominal group) NAME+ADJ*+DTM*+POSS*+AND*+... see NONVERBALGROUP in replc
# example forbiddden sequence : PM_NG_PP, PM_NG_ADV, PM_NG_VQ, 

# needs same definition withour a capturing group, we only capture the whole NG
ADJ_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">adj</sub>.*</span></span>\n'
NAME_     =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:n|n\.prop)</sub>.*</span></span>\n'
DTM_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">dtm</sub>.*</span></span>\n'
PRN_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:prn|pers)</sub>.*</span></span>\n'
KAPOSS_   =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'
NUM_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">num</sub>.*</span></span>\n'

# manque pour l'instant les groupes avec ni et etc.

NG  = r'((?:'+NAME_+r'|'+PRN_+r'|'+DTM_+r')'+r'(?:'+NAME_+r'|'+ADJ_+r'|'+DTM_+r'|'+NUM_+r'|'+KAPOSS_+r')*)'
# print(NG)

PP1       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">(?:(?!POSS).*)</sub>.*</span></span>\n'
#   =pp sans ka POSS
PM_NG_PP  =PM+NG+PP1
PM_NG_ADV =PM+NG+ADV
PM_NG_VQ  =PM+NG+VQ
PM_NG_HPUNCT=PM+NG+HPUNCT
# print(PM_NG_PUNCT)
PM_NG_END =PM+NG+END   # only if missing final punctuation

nsent=0
nsenterr=0

for sentence in sentences:
  nsent=nsent+1
  #print nsent,"---",sentence
  sentence=sentence+"</span>\n"   # close last lemma or punct or tag
  
  if '<span class="annot">' not in sentence: continue
  orig,disamb=sentence.split('<span class="annot">')
  originalsent=re.search('<span class="sent">([^<]*)',orig,re.U|re.MULTILINE)
  original=originalsent.group(1)
  original=original.replace("&lt;","<")
  original=original.replace("&gt;",">")
  original=original.replace("\n"," ")
  original=re.sub(r' +', ' ',original)

  errors=""

  nerr,err_msg=listerr(AMBIGUOUS)
  if nerr>0:
    plural="s"
    if nerr==1: plural=""
    errors=errors+"    "+str(nerr)+" ambiguous word"+plural+": "+err_msg+"\n"

  nerr2,err_msg=listerr(UNKNOWN)
  if nerr2>0:
    plural="s"
    if nerr2==1: plural=""
    errors=errors+"    "+str(nerr2)+" unknown word"+plural+": "+err_msg+"\n"

  if nerr+nerr2!=0 :
    errors=errors+"    skipping other checks...\n"
  else:

    nerr,err_msg=listerr2(VERB1_VERB)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" VERB VERB ? "+err_msg+"\n"

    nerr,err_msg=listerr2(PP_PP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PP PP ? "+err_msg+"\n"

    nerr,err_msg=listerr2(PM_PM)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM PM ? "+err_msg+"\n"

    nerr,err_msg=listerr2(COP1_COP1)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" COP COP ? "+err_msg+"\n"

    nerr,err_msg=listerr2(VERB_PP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" VERB PP ? "+err_msg+"\n"
    
    nerr,err_msg=listerr2(ADV_PP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ADV PP ? "+err_msg+"\n"

    nerr,err_msg=listerr2(PP_VERB)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PP VERB ? "+err_msg+"\n"

    nerr,err_msg=listerr2(VERB_ADJ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" VERB ADJ ? "+err_msg+"\n"
    
    nerr,err_msg=listerr2(ADV_VERB)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ADV VERB ? "+err_msg+"\n"

    nerr,err_msg=listerr2(COP_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" COP VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(ADV_ADJ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ADV ADJ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(PM_COP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM_COP ? "+err_msg+"\n"

    nerr,err_msg=listerr2(NAME_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" NAME VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(PP_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PP VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(ADJ_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" ADJ VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(MAPFV_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" MAPFV VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(KAINF_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" KAINF VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(KASBJV_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" KASBJV VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(KAPOSS_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" KAPOSS VQ ? "+err_msg+"\n"

    nerr,err_msg=listerr2(COP_VERB)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" COP VERB ? "+err_msg+"\n"

    nerr,err_msg=listerr2(A3SG_YEIMP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" A3SG YEIMP (devrait être á' 2PL) ? "+err_msg+"\n"

    nerr,err_msg=listerr2(KAQUAL_NONVQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" KAQUAL NONVQ (groupe qualificatif ou pas?) ? "+err_msg+"\n"

    nerr,err_msg=listerr2(MANQUAL_NONVQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" MANQUAL NONVQ (groupe qualificatif ou pas?) ? "+err_msg+"\n"

    nerr,err_msg=listerr2(NONQUAL_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" NONQUAL VQ (groupe qualificatif ou pas?) ? "+err_msg+"\n"

    nerr,err_msg=listerr3(PM_NG_PP)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM_NG_PP (pas de verbe avant la postposition) ? "+err_msg+"\n"

    nerr,err_msg=listerr3(PM_NG_ADV)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM_NG_ADV (pas de verbe avant l'adverbe) ? "+err_msg+"\n"

    nerr,err_msg=listerr3(PM_NG_VQ)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM_NG_VQ (pas de verbe avant le VQ) ? "+err_msg+"\n"

    nerr,err_msg=listerr3(PM_NG_HPUNCT)
    # print(original, "PM_NG_HPUNCT", nerr, err_msg)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM_NG_PUNCT (pas de verbe avant la ponctuation) ? "+err_msg+"\n"

    nerr,err_msg=listerr3(PM_NG_END)
    if nerr>0:
      errors=errors+"    "+str(nerr)+" PM_NG_END (pas de verbe avant la fin de phrase) ? "+err_msg+"\n"

  if errors!="" : 
    fileOUT.write(str(nsent)+" "+original+"\n"+errors+'\n')
    nsenterr=nsenterr+1

fileOUT.close()
if nsenterr>0:
  print(nsenterr,"sentences with errors\ncheck output as "+fileINnameshort+"-checks.txt")
else :
  os.remove(fileINnameshort+"-checks.txt")
  print("no error found, "+fileINnameshort+"-checks.txt NOT created")