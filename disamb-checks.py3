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
    nerr+=1
    if "¤" in err_msg: err_msg=err_msg.replace("¤"," ")
    err_msg=err_msg.replace("&lt;","<")
    err_msg=err_msg.replace("&gt;",">")

  return nerr, err_msg.strip()
disfiles=[]
if len(sys.argv)>1:
  fileINname= str(sys.argv[1])
  disfiles=[fileINname]
else:
  for dirname, dirnames, filenames in sorted(os.walk('.')):
    if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.

    filenames=sorted(filenames) # peut-être pas nécessaire, mais plus lisible

    for filename in sorted(filenames) :
      if filename.endswith(".dis.html"): disfiles.append(filename)

for fileINname in disfiles:
  INext=fileINname.find(".dis.html")
  fileINnameshort=fileINname[0:INext]
  fichier=fileINnameshort

  fileIN = open(fileINname, "r")

  fileOUTname=fileINnameshort+"-checks.txt"

  if os.path.exists(fileOUTname) : 
    #        sys.exit("\n      file "+fileINnameshort+"-checks.txt ALREADY EXISTS !\n")
    indexer=1
    while os.path.exists(fileINnameshort+"-checks"+str(indexer)+".txt") :
      indexer+=1
    fileOUTname=fileINnameshort+"-checks"+str(indexer)+".txt"


  fileOUT = open (fileOUTname,"w")

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
    body=re.sub(r'\n</span><span class="(w|c|t)"',r'</span>\n<span class="\g<1>"',body,0,re.U|re.MULTILINE)

  sentences=body.split("</span>\n</span>\n</span>\n")  # closing tag for last w|c|t + tag for annot + tag for sent

  print(fileINname,len(sentences), "sentences")

  # check if double ps dtm/prn to correct
  # psambsearch=re.compile(r'<span class="lemma">[^\<]+<sub class="ps">([^\<]+/[^\<]+)<')
  psambsearch=re.compile(r'<sub class="ps">([^\<\n]+\/[^\<\n]+)<')   # also inside compound words
  psambs = psambsearch.findall(body,re.U|re.MULTILINE)
  nbpsambs = len(psambs)
  psambslist = ""
  if nbpsambs > 0:
    for psamb in psambs:
      if psamb not in psambslist: psambslist=psambslist+psamb+" "
    print(nbpsambs, " ps ambigües / ambiguous ps ( "+psambslist+")")
    print("FIX and run disamb-checks again !\n\n")

  # check dabased problems - belongs to disamb-fix ?
  # >fóyì<span class="lemma">fóyì<
  # >fósì<span class="lemma">fósì<
  # >dɔ́rɔn<span class="lemma">dɔ́rɔn<
  # >wɛ́rɛ<span class="lemma">wɛ́rɛ<
  # 


  # define keywords
  AMBIGUOUS =r'<span class="w" stage="[^"]+">([^<\n]+)<.*lemma var.*</span>\n'
  UNKNOWN   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+</span>'
  UNPARSED  =r'>([^<]+)<span class="lemma">[^<]+<span class="lemma var">[^<]+<'
  INCOMPLETE=r'<span class="lemma">([^<\n]+)<sub class="ps">[^<\n]+</sub><span class="m">[^<\n]+<sub class="ps">[^<\n]+</sub></span>(?:<span class="m">[^<\n]+<sub class="ps">mrph</sub><sub class="gloss">[^<\n]+</sub></span>)+</span></span>'


  #validate derivations - check with bamana.gram.txt - 
  BADpl     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n|adj|ptcp).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">(?:n|adj|ptcp)</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>'
  BADnmlz   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:li|ni)<sub class="ps">mrph</sub><sub class="gloss">NMLZ</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADinstr  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:lan|nan)<sub class="ps">mrph</sub><sub class="gloss">INSTR</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADagprm  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:la|na)<sub class="ps">mrph</sub><sub class="gloss">AG\.PRM</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADagocc  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:baga|baa)<sub class="ps">mrph</sub><sub class="gloss">AG\.OCC</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADcom    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n|adj).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">n</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:ma)<sub class="ps">mrph</sub><sub class="gloss">COM</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADcom2   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">[^<\n]+</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">(?:(?!n).)</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:ma)<sub class="ps">mrph</sub><sub class="gloss">COM</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADadj    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!adj|n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">vq</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:man)<sub class="ps">mrph</sub><sub class="gloss">ADJ</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADadj2   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">[^<\n]+</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">(?:(?!vq).)</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:man)<sub class="ps">mrph</sub><sub class="gloss">ADJ</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADstat   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!adj|n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">n</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:lama|nama|rɔma)<sub class="ps">mrph</sub><sub class="gloss">STAT</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADstat2  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">[^<\n]+</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">(?:(?!n).)</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:lama|nama|rɔma)<sub class="ps">mrph</sub><sub class="gloss">STAT</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADst     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!adj|n).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">n</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:tɔ)<sub class="ps">mrph</sub><sub class="gloss">ST</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'

  BADpfvintr=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!v).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:la|na|ra)<sub class="ps">mrph</sub><sub class="gloss">PFV\.INTR</sub></span></span></span>'
  BADprog   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!v).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:la|na)<sub class="ps">mrph</sub><sub class="gloss">PROG</sub></span></span></span>'
  BADptcp   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!ptcp).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:len|nen)<sub class="ps">mrph</sub><sub class="gloss">PTCP\.RES</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADconv   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!ptcp).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:tɔ)<sub class="ps">mrph</sub><sub class="gloss">CONV</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADpot    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!ptcp).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">v</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:ta)<sub class="ps">mrph</sub><sub class="gloss">PTCP\.POT</sub></span>(?:<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span>)*</span></span>'
  BADdequ   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:(?!n|v).)</sub>(?:<sub class="gloss">[^<\n]+</sub>)*<span class="m">[^<\n]+<sub class="ps">vq</sub><sub class="gloss">[^<\n]+</sub></span><span class="m">(?:ya)<sub class="ps">mrph</sub><sub class="gloss">DEQU</sub></span></span></span>'


  BADmrphBA				=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">ba<sub class="ps">mrph</sub><sub class="gloss">(?:(?!AUGM).)+</sub></span>'
  BADmrphBALI			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">bali<sub class="ps">mrph</sub><sub class="gloss">(?:(?!PTCP\.NEG).)+</sub></span>'
  BADmrphNTAN			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">ntan<sub class="ps">mrph</sub><sub class="gloss">(?:(?!PRIV).)+</sub></span>'
  BADmrphNIN			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">nin<sub class="ps">mrph</sub><sub class="gloss">(?:(?!DIM).)+</sub></span>'
  BADmrphBAGA			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:baa|baga)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!AG\.OCC).)+</sub></span>'
  BADmrphKA				=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">(?:(?!GENT).)+</sub></span>'
  BADmrphLANA			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:la|na|n\'|l\')<sub class="ps">mrph</sub><sub class="gloss">(?:(?!AG\.PRM|LOC|MNT1|PRIX|PROG|OPT2|PFV\.INTR|à|à).)+</sub></span>'
  BADmrphRA		    =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:ra|r\')<sub class="ps">mrph</sub><sub class="gloss">(?:(?!OPT2|PFV\.INTR).)+</sub></span>'
  BADmrphLAMANAMA	=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:lama|nama)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!STAT).)+</sub></span>'
  BADmrphLATANATA	=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:lata|nata)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!MNT2).)+</sub></span>'
  BADmrphLANNAN		=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:lan|nan)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!INSTR|ORD).)+</sub></span>'
  BADmrphLENNEN		=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:len|nen)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!PTCP\.RES).)+</sub></span>'
  BADmrphLINI			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:li|ni)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!NMLZ).)+</sub></span>'
  BADmrphLUNU			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:lu|nu)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!PL2).)+</sub></span>'
  BADmrphMA				=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">ma<sub class="ps">mrph</sub><sub class="gloss">(?:(?!COM|DIR|RECP\.PRN|SUPER).)+</sub></span>'
  BADmrphMAN			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">man<sub class="ps">mrph</sub><sub class="gloss">(?:(?!ADJ|SUPER).)+</sub></span>'
  BADmrphNCI			=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">nci<sub class="ps">mrph</sub><sub class="gloss">(?:(?!AG\.EX).)+</sub></span>'
  BADmrphƝƆGƆN		=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:ɲɔgɔn|ɲwan)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!RECP).)+</sub></span>'
  BADmrphTA				=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">ta<sub class="ps">mrph</sub><sub class="gloss">(?:(?!PTCP\.POT).)+</sub></span>'
  BADmrphTƆ				=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">tɔ<sub class="ps">mrph</sub><sub class="gloss">(?:(?!CONV|ST).)+</sub></span>'
  BADmrphW				=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">w<sub class="ps">mrph</sub><sub class="gloss">(?:(?!PL).)+</sub></span>'
  BADmrphYA				=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^\n]+<span class="m">(?:ya|yɛ)<sub class="ps">mrph</sub><sub class="gloss">(?:(?!ABSTR|DEQU).)+</sub></span>'
  """ # mrph NOT IMPLEMENTED
  \\:mrph:NMLZ2
  lá:mrph:CAUS
  lán:mrph:CAUS
  mà:mrph:SUPER  <-- sans ton dans BADmrphMA : à revoir !
  màn:mrph:SUPER  <-- sans ton dans BADmrphMAN : à revoir !
  ná:mrph:CAUS
  rá:mrph:IN
  rɔ́:mrph:CAUS
  rɔ́:mrph:IN
  sɔ̀:mrph:EN
  +
  la:mrph:à   <--- dans BADmrphLANA
  l' et n':mrph:PFV.INTR  <--- dans BADmrphLANA
  r':mrph:PFV.INTR  <--- dans BADmrphRA
  nan:mrph:ORD      <--- ajouté en vitesse à LANNAN, à revoir
  """

  #... tbc ... pp ? pm ? 



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
  PRT       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">prt</sub>.*</span></span>\n'
  DTM       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">dtm</sub>.*</span></span>\n'
  PRN       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:prn|pers)</sub>.*</span></span>\n'
  CONJ      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub>.*</span></span>\n'
  # ... tbc ...
  PPpm      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">(?:y\'|yé|mà|ná)<sub class="ps">pp</sub>.*</span></span>\n'

  # punctuations
  START     =r'\^'
  END       =r'\$'
  PUNCT     =r'<span class="[ct]">([^<]+)</span>\n'  # any punctuations, tags included
  HPUNCT    =r'<span class="c">([\.\;\:\!\?]+)</span>\n'  # hard punctuation marking sentence end
  COMMA     =r'<span class="c">,</span>\n'
  LAQUO     =r'<span class="c">\«</span>\n'
  RAQUO     =r'<span class="c">\»</span>\n'
  PARO      =r'<span class="c">\(</span>\n'
  PARF      =r'<span class="c">\)</span>\n'
  GUILLEMET =r'<span class="c">\"</span>\n'
  INNGPUNCT =r'<span class="c">(?:\«|\»|\(|\)|\")</span>\n'

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
  MADES     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">(?:mà|màa|m\')<sub class="ps">pm</sub><sub class="gloss">DES</sub></span></span>\n'
  MAnon_DES =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">(?:ma[́̀]*|ma[́̀]*a|m\')<sub class="ps">pm</sub><sub class="gloss">(?:(?!DES).*)</sub></span></span>\n'
  A3SG      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pers</sub><sub class="gloss">3SG</sub></span></span>\n'
  VERB1     =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub><sub class="gloss">(?:(?!aller|venir).*)</sub>.*</span></span>\n'
  VnonPERF  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub>[^\n]*<sub class="ps">mrph</sub><sub class="gloss">((?!PFV\.INTR).)*</sub></span></span></span>\n'
  VnonOPT2  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub>[^\n]*<sub class="ps">mrph</sub><sub class="gloss">((?!OPT2).)*</sub></span></span></span>\n'
  VERBralana=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">v</sub>[^\n]*<span class="m">(?:ra|la|na|r\'|l\'|n\')<sub class="ps">mrph</sub><sub class="gloss">[^\n<]+</sub></span></span></span>\n'
  COP1      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">cop</sub><sub class="gloss">(?:(?!QUOT).*)</sub>.*</span></span>\n'
  NIet      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub><sub class="gloss">et</sub></span></span>\n'
  NIsi      =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">conj</sub><sub class="gloss">si</sub></span></span>\n'
  PMnon_INF  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pm</sub><sub class="gloss">(?:(?!INF).*)</sub></span></span>\n'
  PPnon_PP  =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">(?:(?!PP).*)</sub></span></span>\n'
  PPnon_POSS=r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">(?:(?!POSS).*)</sub></span></span>\n'
  non_2PL   =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">[^<\n]+</sub><sub class="gloss">(?:(?!2PL|2PL\.EMPH).*)</sub></span></span>\n'



  PPFINAL   =PP+HPUNCT
  ADVFINAL  =ADV+HPUNCT
  PRTFINAL  =PRT+HPUNCT
  FOprep    =r'''<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">prep</sub><sub class="gloss">jusqu'à</sub></span></span>\n'''
  FOconj    =r'''<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">conj</sub><sub class="gloss">jusqu'à</sub></span></span>\n'''
  QUOT      =r'''<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">(?:ko|kó|k')+<sub class="ps">cop</sub><sub class="gloss">QUOT</sub></span></span>\n'''
  Ala       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[aA]́la<sub class="ps">n</sub><sub class="gloss">Dieu</sub></span></span>\n'



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
  VERB_VQ   =VERB+VQ
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
  PM_ADJ   =PM+ADJ
  PM_ADV   =PM+ADV
  non_2PL_YEIMP=non_2PL+YEIMP

  # VERB_CONJ =VERBE_CONJ   # phrases avec absence de virgule derrière le verbe
  # ADV_CONJ                # phrases avec absence de virgule derrière le verbe
  FOprep_KAINF=FOprep+KAINF
  FOprep_NIsi =FOprep+NIsi
  ADV_VERB  =ADV+VERB
  ADV_PMnon_INF=ADV+PMnon_INF
  ADV_COP1   =ADV+COP1
  START_ADJ =START+ADJ
  START_VERB_PM=START+VERB+PM
  # ...tbc...
  # implement : NG (nominal group) NAME+ADJ*+DTM*+POSS*+AND*+... see NONVERBALGROUP in replc
  # example forbiddden sequence : PM_NG_PP, PM_NG_ADV, PM_NG_VQ, 

  # needs same definition without a capturing group: we only capture the whole NG
  ADJ_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">adj</sub>.*</span></span>\n'
  NAME_     =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:n|n\.prop|conv\.n)</sub>.*</span></span>\n'
  DTM_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">dtm</sub>.*</span></span>\n'
  PRN_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:prn|pers)</sub>.*</span></span>\n'
  KAPOSS_   =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'
  NUM_      =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">num</sub>.*</span></span>\n'
  NIet_     =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub><sub class="gloss">et</sub></span></span>\n'
  PP_       =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">pp</sub>.*</span></span>\n'
  CONJ_     =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">(?:conj|prep)</sub>.*</span></span>\n'
  CONJSBJV_ =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">(?:sánì|sáni|sánnì|sánni|sànní|yànní|yánni|wálasa|sànkó|sánko|fɔ́|yálasa|yáasa)<sub class="ps">(?:conj)</sub>.*</span></span>\n'
  QUOT_     =r'''<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">(?:ko|kó|k')+<sub class="ps">cop</sub><sub class="gloss">QUOT</sub></span></span>\n'''
  INNGPUNCT_ =r'<span class="c">[\«\»\(\)\"]</span>\n'

  # manque pour l'instant les groupes avec ni et etc.

  # nominal group including quotes, possessive subgroup, ni consecutive subgroup, including commas
  NG  = r'((?:'+NAME_+r'|'+INNGPUNCT_+NAME_+r'|'+PRN_+r'|'+DTM_+r'|'+INNGPUNCT_+r')'+r'(?:'+NAME_+r'|'+ADJ_+r'|'+DTM_+r'|'+NUM_+r'|'+PP_+NAME_+r'|'+PP_+INNGPUNCT_+NAME_+r'|'+NIet_+NAME_+r'|'+NIet_+INNGPUNCT_+NAME_+r'|'+INNGPUNCT_+r'|'+COMMA+r')*)'

  # nominal group including quotes, possessive subgroup, ni consecutive subgroup, BUT NOT including commas
  NG1 = r'((?:'+NAME_+r'|'+INNGPUNCT_+NAME_+r'|'+PRN_+r'|'+DTM_+r'|'+INNGPUNCT_+r')'+r'(?:'+NAME_+r'|'+ADJ_+r'|'+DTM_+r'|'+NUM_+r'|'+PP_+NAME_+r'|'+PP_+INNGPUNCT_+NAME_+r'|'+NIet_+NAME_+r'|'+NIet_+INNGPUNCT_+NAME_+r'|'+INNGPUNCT_+r')*)'

  # nominal group including possessive subgroup, ni consecutive subgroup, BUT NOT including quotes, commas
  NG2 = r'((?:'+NAME_+r'|'+PRN_+r'|'+DTM_+r')'+r'(?:'+NAME_+r'|'+ADJ_+r'|'+DTM_+r'|'+NUM_+r'|'+PP_+NAME_+r'|'+NIet_+NAME_+r')*)'

  #print(NG)

  PP1       =r'<span class="w" stage="[^"]+">([^<\n]+)<span class="lemma">[^<\n]+<sub class="ps">pp</sub><sub class="gloss">(?:(?!POSS).*)</sub>.*</span></span>\n'
  #   =pp sans ka POSS
  PM_NG_PPFINAL  =PM+NG1+PPFINAL    # difficulty with split orthography : a be dugu kɔnɔ mɔgɔw ɲɔgɔri - only ka POSS accepted in NG/NG1
  #print("\nNG1",NG1)
  #print("\nPM_NG_PPFINAL",PM_NG_PPFINAL)
  PM_NG_ADVFINAL  =PM+NG1+ADVFINAL
  PM_NG_PRTFINAL  =PM+NG1+PRTFINAL

  PM_NG_ADV =PM+NG+ADV   # not checked if another error in sentence NG_ADV_NG ???
  #print("PM_NG_ADV:\n"+PM_NG_ADV)

  PM_NG_VQ  =PM+NG+VQ
  PM_NG_HPUNCT=PM+NG+HPUNCT
  # print(PM_NG_PUNCT)
  PM_NG_END =PM+NG+END   # only if missing final punctuation
  PM_NG_PM  =PM+NG+PM
  PM_NG_PPnon_POSS  =PM+NG+PPnon_POSS
  VERB1_NG_VnonPERF=VERB1+NG+VnonPERF  # VPERF peut se trouver légitimement après : i n'a fɔ... / o y'a sɔro ... et VPERF
  VERB1_PRT_VnonPERF=VERB1+PRT+VnonPERF
          # taa/na sont exclus de VERB1, mais la construction peut exister avec se : mɔgɔ si kana se a filɛ yen.
  FOconj_NG_MAPP=FOconj+NG+MAPP
  NIsi_NG_PP1=NIsi+NG+PP1
  NG_ADV_NG =NG2+ADV+NG
  PPpm_NG_VnonPERF=PPpm+NG+VnonPERF

  # it would be interesting to define a VERBALGROUP, or "proposition/verbal clause"
  # for instance ( NG PM NG* VnonPERF|VQ)  | ( NG VPERF )
  # ignoring for now adverbs and postposition following the verb
  PM_       =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">pm</sub>.*</span></span>\n'
  VnonPERF_ =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">v</sub><sub class="gloss">((?!PFV\.INTR).)*</sub>.*</span></span>\n'
  VQ_       =r'<span class="w" stage="[^"]+">[^<\n]+<span class="lemma">[^<\n]+<sub class="ps">vq</sub>.*</span></span>\n'

  VG = r'('+NG2+PM_+NG2+r'*(?:'+VnonPERF_+r'|'+VQ_+r'))'
  VG2= r'('+NG2+r'*(?:'+VnonPERF_+r'))'

  FOprep_VG =FOprep+VG

  Ala_MAnon_DES_NG_VERBralana = Ala+MAnon_DES+NG2+"*"+VERBralana
  Ala_MADES_NG_VnonOPT2 = Ala+MADES+NG2+"*"+VnonOPT2

  # print(Ala_MAnon_DES_NG_VERB+"\n\n"+Ala_MADES_NG_VnonOPT2)

  #print(FOprep_VG)

  # larger sequences
  TEST_KASBJV=r'('+START+r'|'+PUNCT+r'|'+CONJSBJV_+r'|'+QUOT_+r')'+NG2+KAnon_SBJV+VG2
  #print ("TEST_KASBJV:\n",TEST_KASBJV)
  nsent=0
  nsenterr=0
  fileOUT.write("Légende :\nGn: Groupe nominal,\nPM: Marque prédicative,\nCOP: Copule,\nPP: Postposition,\nADV: Adverbe,\nADJ: Adjectif,\nCONJ: Conjonction\nV(non PERF): Verbe (non perfectif)\n")
  fileOUT.write("Ces vérifications ne sont ni toujours pertinentes, ni exhaustives...\nEn espérant que cela reste malgré tout utile !\n\n")

  nsentchecked=0
  totalwordschecked=0
  totalerrors=0

  for sentence in sentences:
    nsent=nsent+1
    sentence=sentence+"</span>\n"   # close last lemma or punct or tag
    
    if '<span class="annot">' not in sentence: continue
    #print("\nSentence # ",nsent,"\n",sentence,"\n")
    orig,disamb=sentence.split('<span class="annot">')

    disamb=r"\^"+disamb+r"\$"
    originalsent=re.search('<span class="sent">([^<]*)',orig,re.U|re.MULTILINE)
    original=originalsent.group(1)
    original=original.replace("&lt;","<")
    original=original.replace("&gt;",">")
    original=original.replace("\n"," ")
    original=re.sub(r' +', ' ',original)

    errors=""
    nerr=0

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
      nerr+=nerr2

    nerr3,err_msg=listerr(UNPARSED)
    if nerr3>0:
      plural="s"
      if nerr3==1: plural=""
      errors=errors+"    "+str(nerr3)+" mot"+plural+" mal parsé (gparser) : "+err_msg+"\n"
      nerr+=nerr3

    nerr4,err_msg=listerr(INCOMPLETE)
    if nerr4>0:
      plural="s"
      if nerr4==1: plural=""
      errors=errors+"    "+str(nerr4)+" mot"+plural+" incomplet (seulement une ou des dérivations) : "+err_msg+"\n"
      nerr+=nerr4

    nerr5,err_msg=listerr(BADpl)
    if nerr5>0:
      plural="s"
      if nerr5==1: plural=""
      errors=errors+"    "+str(nerr5)+" mot"+plural+" :mrph:PL pluriel mais pas n, adj ou ptcp ?) : "+err_msg+"\n"
      nerr+=nerr5

    nerr6,err_msg=listerr(BADnmlz)
    if nerr6>0:
      plural="s"
      if nerr6==1: plural=""
      errors=errors+"    "+str(nerr6)+" mot"+plural+" :mrph:NMLZ mais pas n ?) : "+err_msg+"\n"
      nerr+=nerr6

    nerr6b,err_msg=listerr(BADinstr)
    if nerr6b>0:
      plural="s"
      if nerr6b==1: plural=""
      errors=errors+"    "+str(nerr6b)+" mot"+plural+" :mrph:INSTR mais pas n ?) : "+err_msg+"\n"
      nerr+=nerr6b

    nerr7,err_msg=listerr(BADagprm)
    if nerr7>0:
      plural="s"
      if nerr7==1: plural=""
      errors=errors+"    "+str(nerr7)+" mot"+plural+" :mrph:AG.PRM mais pas n ?) : "+err_msg+"\n"
      nerr+=nerr7

    nerr8,err_msg=listerr(BADagocc)
    if nerr8>0:
      plural="s"
      if nerr8==1: plural=""
      errors=errors+"    "+str(nerr8)+" mot"+plural+" :mrph:AG.OCC mais pas n ?) : "+err_msg+"\n"
      nerr+=nerr8

    nerr9,err_msg=listerr(BADpfvintr)
    if nerr9>0:
      plural="s"
      if nerr9==1: plural=""
      errors=errors+"    "+str(nerr9)+" mot"+plural+" :mrph:PFV.INTR mais pas v ?) : "+err_msg+"\n"
      nerr+=nerr8

    nerr10,err_msg=listerr(BADptcp)
    if nerr10>0:
      if err_msg.lower() in ["fɔlen","fòlen","kɔrɔlen","kòròlen"]: nerr10=0
      else:
        plural="s"
        if nerr10==1: plural=""
        errors=errors+"    "+str(nerr10)+" mot"+plural+" :mrph:PTCP.RES mais pas ptcp ?) : "+err_msg+"\n"
        nerr+=nerr10

    nerr10b,err_msg=listerr(BADconv)
    if nerr10b>0:
      plural="s"
      if nerr10b==1: plural=""
      errors=errors+"    "+str(nerr10b)+" mot"+plural+" tɔ:mrph:CONV mais pas ptcp ?) : "+err_msg+"\n"
      nerr+=nerr10b

    nerr10c,err_msg=listerr(BADpot)
    if nerr10c>0:
      plural="s"
      if nerr10c==1: plural=""
      errors=errors+"    "+str(nerr10c)+" mot"+plural+" ta:mrph:PTCP.POT mais pas ptcp ?) : "+err_msg+"\n"
      nerr+=nerr10c


    nerr11,err_msg=listerr(BADprog)
    if nerr11>0:
      plural="s"
      if nerr11==1: plural=""
      errors=errors+"    "+str(nerr11)+" mot"+plural+" :mrph:PROG mais pas v ?) : "+err_msg+"\n"
      nerr+=nerr11

    nerr12,err_msg=listerr(BADcom)
    if nerr12>0:
      plural="s"
      if nerr12==1: plural=""
      errors=errors+"    "+str(nerr12)+" mot"+plural+" :mrph:COM dont le dérivé n'est pas n/adj ?) : "+err_msg+"\n"
      nerr+=nerr12

    nerr13,err_msg=listerr(BADadj)
    #print("BADadj err_msg: '"+err_msg.strip()+"'")
    oklst=["cɛman","cɛmanw","cèman","cèmanw","musoman","musomanw"]
    ok=False
    if "‖" in err_msg:
      err=err_msg.split("‖")
      errlst=[i.strip().lower() for i in err]
      for i in errlst:
        if i not in oklst: break
        ok=True
    else:
      ok=err_msg.strip().lower() in oklst
    if not ok  and nerr13>0:
      plural="s"
      if nerr13==1: plural=""
      errors=errors+"    "+str(nerr13)+" mot"+plural+" :mrph:ADJectivateur de vq dont le dérivé n'est pas pas adj ni n ?): "+err_msg+"\n"
      nerr+=nerr13

    nerr14,err_msg=listerr(BADstat)
    if nerr14>0:
      plural="s"
      if nerr14==1: plural=""
      errors=errors+"    "+str(nerr14)+" mot"+plural+" :mrph:STAT de n mais pas adj ni n ?) : "+err_msg+"\n"
      nerr+=nerr14

    nerr14b,err_msg=listerr(BADst)
    if nerr14b>0:
      plural="s"
      if nerr14b==1: plural=""
      errors=errors+"    "+str(nerr14b)+" mot"+plural+" tɔ:mrph:ST de n mais pas adj ni n ?) : "+err_msg+"\n"
      nerr+=nerr14b

    nerr15,err_msg=listerr(BADcom2)
    if nerr15>0:
      plural="s"
      if nerr15==1: plural=""
      errors=errors+"    "+str(nerr15)+" mot"+plural+" :mrph:COM ne dérive pas un N ?) : "+err_msg+"\n"
      nerr+=nerr15

    nerr16,err_msg=listerr(BADadj2)
    #print("BADadj2 err_msg: '"+err_msg.strip()+"'")
    oklst=["cɛman","cɛmanw","cèman","cèmanw","musoman","musomanw"]
    ok=False
    if "‖" in err_msg:
      err=err_msg.split("‖")
      errlst=[i.strip().lower() for i in err]
      for i in errlst:
        if i not in oklst: break
        ok=True
    else:
      ok=err_msg.strip().lower() in oklst
    if not ok and nerr16>0:
      plural="s"
      if nerr16==1: plural=""
      errors=errors+"    "+str(nerr16)+" mot"+plural+" :mrph:ADJectivateur de vq ne dérive pas un vq ?): "+err_msg+"\n"
      nerr+=nerr16

    nerr17,err_msg=listerr(BADstat2)
    if nerr17>0:
      plural="s"
      if nerr17==1: plural=""
      errors=errors+"    "+str(nerr17)+" mot"+plural+" :mrph:STAT de n mais ne dérive pas un n ?) : "+err_msg+"\n"
      nerr+=nerr17

    nerr18,err_msg=listerr(BADdequ)
    if nerr18>0:
      plural="s"
      if nerr18==1: plural=""
      errors=errors+"    "+str(nerr18)+" mot"+plural+" ya:mrph:DEQU de vq mais ne dérive pas un n ou un v ?) : "+err_msg+"\n"
      nerr+=nerr18

    # --- BAD MORPHEMES --->>>>>>>>>>>>>>>

    nerrm,err_msg=listerr(BADmrphBA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ba mais pas AUGM ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphBALI)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -bali mais pas PTCP.NEG ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphNTAN)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ntan mais pas PRIV ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphNIN)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -nin mais pas DIM ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphBAGA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -baga mais pas AG.OCC ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphKA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ka mais pas GENT ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphLANA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -la/-na mais pas AG.PRM|LOC|MNT1|PRIX|PROG|OPT2|PFV.INTR|à ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphRA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ra mais pas OPT2|PFV.INTR ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphLAMANAMA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -lama/-nama mais pas STAT ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphLATANATA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -lata/-nata mais pas MNT2 ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphLANNAN)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -lan/-nan mais pas INSTR ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphLENNEN)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -len/-nen mais pas PTCP.RES ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphLINI)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -li/-ni mais pas NMLZ ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphLUNU)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -lu/-nu mais pas PL2 ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphMA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ma mais pas COM|DIR|RECP.PRN|SUPER ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphMAN)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -man mais pas ADJ|SUPER ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphNCI)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -nci mais pas AG.EX ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphƝƆGƆN)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ɲɔgɔn/-ɲwan mais pas RECP ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphTA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ta mais pas PTCP.POT ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphTƆ)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -tɔ mais pas CONV|ST ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphW)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -w mais pas PL ?) : "+err_msg+"\n"
      nerr+=nerrm
    nerrm,err_msg=listerr(BADmrphYA)
    if nerrm>0:
      plural="s"
      if nerrm==1: plural=""
      errors=errors+"    "+str(nerrm)+" mot"+plural+" morphème -ya mais pas ABSTR|DEQU ?) : "+err_msg+"\n"
      nerr+=nerrm



    # --- end BAD MORPHEMES <<<<<<<<<<<<<<


    # --- si une des erreurs de validations ci-dessus ne pas faire les autres tests de cohérence ---
    # --- ignore further tests if error in one of the above

    if nerr != 0 :
      errors=errors+"    j'ignore les autres tests...\n"
    else:

      nsentchecked=nsentchecked+1
      allw=re.findall(r'<span class="w" stage="[^"]+">([^<\n]+)<',disamb,re.U|re.MULTILINE)
      totalwordschecked=totalwordschecked+len(allw)

      nerr,err_msg=listerr(VERB1_VERB)
      if nerr>0:
        avis="(deux verbes qui se suivent) ?"
        if "se " in err_msg:
          avis=avis+" [comme pour nà ou táa (régulier), parfois possible avec sé (ignorer)]"
        errors=errors+"    "+str(nerr)+" VERBE VERBE "+avis+" : "+err_msg+"\n"

      nerr,err_msg=listerr(PP_PPnon_PP)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" PP PP (deux postpositions successives? voir adverbes ou pp composées?) : "+err_msg+"\n"

      nerr,err_msg=listerr(PM_PM)
      if nerr>0:
        avis="(deux marques prédicatives qui se suivent)"
        if "k' " in err_msg : avis=avis+" [ k'=ko QUOT ? ka POSS ?]"
        elif "tɛ ka" in err_msg or "tè ka" in err_msg or "bɛ ka" in err_msg or "bè ka" in err_msg or "ye ka" in err_msg:
          avis=avis+" [les pm doubles commencent par une copule] "
        errors=errors+"    "+str(nerr)+" PM PM "+avis+" : "+err_msg+"\n"

      nerr,err_msg=listerr(COP1_COP1)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" COP COP (deux copules qui se suivent) : "+err_msg+"\n"

      nerr,err_msg=listerr(VERB_PP)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" VERBE PP (verbe suivi d'une postposition - voir adverbes possibles?) : "+err_msg+"\n"
      
      nerr,err_msg=listerr(ADV_PP)
      if nerr>0:
        if "kojugu " in err_msg or "kosɛbɛ " in err_msg or "kosèbè " in err_msg : continue # ignore for now
        avis="(adverbe suivi d'une postposition) [l'adv. est un nom? la pp est un adv.? nb: acceptable derrière un ptcp ou un nmlz]"
        errors=errors+"    "+str(nerr)+" ADV PP "+avis+" : "+err_msg+"\n"

      nerr,err_msg=listerr(PP_VERB)
      if nerr>0:
        avis="(postposition avant un verbe [ignorer si impératif/ponctuation défectueuse]) ? "
        if "ma " in err_msg: avis=avis+" [peut-être est-ce ma:pm:PFV.NEG] "
        errors=errors+"    "+str(nerr)+" PP VERBE "+avis+": "+err_msg+"\n"

      nerr,err_msg=listerr(VERB_ADJ)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" VERBE ADJ (verbe suivi d'un adjectif) : "+err_msg+"\n"
      
      nerr,err_msg=listerr(ADV_VERB)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" ADV VERBE (adverbe précédent un verbe mais pas adv.p) [OK si suit un ptcp/nmlz] : "+err_msg+"\n"

      nerr,err_msg=listerr(COP_VQ)
      if nerr>0:
        avis="(copule avant un verbe qualitatif)"
        if "bɛ " in err_msg or "bɛ́ " in err_msg: avis=avis+" [possible mais rare avec bɛ́:cop:être]"
        errors=errors+"    "+str(nerr)+" COP VQ "+avis+": "+err_msg+"\n"

      nerr,err_msg=listerr(ADV_ADJ)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" ADV ADJ (adverbe suivi d'un adjectif) : "+err_msg+"\n"

      nerr,err_msg=listerr(PM_COP)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" PM COP (marque prédicative suivie d'une copule) : "+err_msg+"\n"

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
        errors=errors+"    "+str(nerr)+" ADJ VQ (adjectif devant un verbe qualitatif) : "+err_msg+"\n"

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
      else:
        nerr,err_msg=listerr(non_2PL_YEIMP)
        if nerr>0:
          errors=errors+"    "+str(nerr)+" XXX ye(IMP) (devrait être á' 2PL) : "+err_msg+"\n"

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

      nerr,err_msg=listerr(PM_ADJ)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" PM ADJ (marque prédicative devant un adjectif) : "+err_msg+"\n"

      nerr,err_msg=listerr(PM_ADV)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" PM ADV (marque prédicative devant un adverbe) : "+err_msg+"\n"

      nerr,err_msg=listerr(CONJ_VERB)
      if nerr>0:
        avis="(conjonction devant un verbe ) "
        err_lst=err_msg.strip().split(" ")
        if "o" in err_lst or "ó" in err_lst:
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


      nerr,err_msg=listerr(ADV_PMnon_INF)
      if nerr>0:
        avis=" Adverbe avant marque prédicative ? [ok si suit un ptcp ou un nmlz]"
        if "tun" in err_msg: avis=avis+ "[ tùn:prt:PST ? ]"
        errors=errors+"    "+str(nerr)+avis+" : "+err_msg+"\n"

      nerr,err_msg=listerr(ADV_COP1)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" Adverbe avant copule? : "+err_msg+"\n"

      nerr,err_msg=listerr(VERB_VQ)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" Verbe avant Verbe qualitatif? [possible Nom+Adj?]: "+err_msg+"\n"

      nerr,err_msg=listerr(START_ADJ)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" Adjectif en début de phrase ? [les adj en -nan peuvent être convertis en n !]: "+err_msg+"\n"

      nerr,err_msg=listerr(START_VERB_PM)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" Verbe en début devant MP ? : "+err_msg+"\n"

  #------------------- 3 terms, NG middle

      nerr,err_msg=listerr(PM_NG_PPFINAL)
      if nerr>0:
        avis="(pas de verbe avant la postposition)"
        if " ye" in err_msg and ("ye " in err_msg or "y' " in err_msg): avis=avis+" [le 1er ye devrait être cop:EQU?]"
        errors=errors+"    "+str(nerr)+" PM Gn PPfinale "+avis+" : "+err_msg+"\n"
      else:
        nerr,err_msg=listerr(PM_NG_PPnon_POSS)
        if nerr>0:
          avis="(pas de Verbe avant la postposition?)"
          avis2=" [verbe mal identifié? COP au lieu de PM? Ignorer si la PP fait partie d'un groupe nominal plus large, comme un superlatif: X bɛɛ la ɲuman...]\n"
          errors=errors+"    "+str(nerr)+" PM Gn PP "+avis+" : "+err_msg+"\n"+"      "+avis2

      nerr,err_msg=listerr(PM_NG_PRTFINAL)
      if nerr>0:
        avis="(pas de verbe avant la particule finale)"
        errors=errors+"    "+str(nerr)+" PM Gn PRTfinale "+avis+" : "+err_msg+"\n"

      nerr,err_msg=listerr(PM_NG_ADV)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" PM Gn ADV (pas de verbe avant l'adverbe) [OK si l'adv. suit un ptcp ou un conv.n ou un nmlz] : "+err_msg+"\n"

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
        if "k' " in err_msg : avis=avis+" [k'=ko QUOT ? ka POSS ?]"
        else : avis=avis+" [verbe mal identifié? ignorer après \"n'ò tɛ́\"]"
        errors=errors+"    "+str(nerr)+" PM Gn PM "+avis+" : "+err_msg+"\n"



      nerr,err_msg=listerr(VERB1_NG_VnonPERF)
      if nerr>0:
        avis="(deux verbes successifs) ? "
        avis2="     [ignorer si impératifs, si le premier est nà/táa, ou si derrière conjonction comme \"k'a sɔrɔ\"]\n"
        if "se " in err_msg: avis2=avis2+"\n      [comme pour nà ou táa (régulier), parfois possible avec sé (ignorer)]\n"
        errors=errors+"    "+str(nerr)+" VERBE Gn V(non PERF) "+avis+" : "+err_msg+"\n"+avis2

      nerr,err_msg=listerr(VERB1_PRT_VnonPERF)
      if nerr>0:
        avis="(deux verbes successifs) ?"
        errors=errors+"    "+str(nerr)+" VERBE PRT V(non PERF) "+avis+" : "+err_msg+"\n"

      nerr,err_msg=listerr(FOconj_NG_MAPP)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" fo(conj) Gn ma(PP) (devrait être fó/fɔ́ prep) : "+err_msg+"\n"

      nerr,err_msg=listerr(NIsi_NG_PP1)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" ni(si) Gn PP [ devrait être ni(et) ou yé:cop:EQU ] : "+err_msg+"\n"

      nerr,err_msg=listerr(NG_ADV_NG)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" Adverbe isolé entre 2 Gn [ok si suit un ptcp ou un nmlz] : "+err_msg+"\n"

      nerr,err_msg=listerr(TEST_KASBJV)
      if nerr>0:
        print(err_msg)
        errors=errors+"    "+str(nerr)+" ka(non SBJV) (devrait être ka:pm:SBJV) [ignorer si: kà sɔ̀rɔ, ou kà fàra ... kàn, ou kà bɔ́ TOP / ignorer si suit un ptcp/nmlz : kɛ́len kà... bìlali kà...] : "+err_msg+"\n"

      nerr,err_msg=listerr(PPpm_NG_VnonPERF)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" PP Gn Vnonperf [la PP pourrait-elle être une MP?] (OK si verbe à l'impératif) : "+err_msg+"\n"

      nerr,err_msg=listerr(Ala_MAnon_DES_NG_VERBralana)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" Ala ma (non DES) ? : "+err_msg+"\n"

      nerr,err_msg=listerr(Ala_MADES_NG_VnonOPT2)
      if nerr>0:
        errors=errors+"    "+str(nerr)+" Ala ma Verbe (dérivation non OPT2) ? : "+err_msg+"\n"

    if errors!="" : 
      allerr=re.findall(r'(    [0-9])',errors,re.U|re.MULTILINE)
      totalerrors=totalerrors+len(allerr)

      original=original.replace("<br/>","¶")
      originalhi=original  # hi = highlight errors in sentence
      
      #if len(allerr)==1:

      err_msg_search=r'    [0-9][^\n]+: *([^\n\:]+) *'
      err_msg_result=re.search(err_msg_search,errors)
      if err_msg_result:
        #err_msg=err_msg_result.groups()[0]    # only handles the first error type message
        #print("err_msg :",err_msg)
        for err_msg in err_msg_result.groups():
          err_list=[]
          if " ‖ " in err_msg:
            err_list=err_msg.split(" ‖ ")
          else:
            err_list.append(err_msg)
          for err_msgclean in err_list:
            err_msgclean=err_msgclean.replace("[","")   # re.sub would give more flexibility with optional spaces before puncts
            err_msgclean=err_msgclean.replace("]","")
            err_msgclean=err_msgclean.replace("  "," ")
            err_msgclean=err_msgclean.replace(" .",".")
            err_msgclean=err_msgclean.replace("’ ","’")
            err_msgclean=err_msgclean.replace("^ ","")
            err_msgclean=err_msgclean.replace("' ","'").strip()  # 
            if err_msgclean[-2:]==" r" or err_msgclean[-2:]==" R" : err_msgclean=err_msgclean[:-2]
            
            #print("err_msgclean :",err_msgclean)
            originalhibefore=originalhi
            originalhi=originalhi.replace(err_msgclean," ⋙ "+err_msgclean+" ⋘ ")    # may repeat several times in sentence!
            if originalhi==originalhibefore:
              fileOUT.write("     -> originalhi fail : '"+err_msgclean+"'\n" )

      fileOUT.write(str(nsent)+" "+originalhi+"\n"+errors+'\n')
      nsenterr=nsenterr+1

  fileOUT.close()
  if nsenterr>0:
    print(nsenterr,"sentences with errors /",nsentchecked," sentences checked\ncheck output as "+fileOUTname)
    print(totalerrors,"errors / ",totalwordschecked," words checked")
  else :
    os.remove(fileOUTname)
    print("no error found /",totalwordschecked," words checked, "+fileOUTname+" NOT created")