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

global fileINname,fileINnameshort,fichier

fileINname= str(sys.argv[1])
INext=fileINname.find(".dis.html")
fileINnameshort=fileINname[0:INext]
fichier=fileINnameshort

fileIN = open(fileINname, "r")

if os.path.exists(fileINnameshort+"-bam-fra2.csv") : sys.exit("\n      file "+fileINnameshort+"-bam-fra2.csv ALREADY EXISTS !\n")
fileOUT = open (fileINnameshort+"-bam-fra2.csv","w")
fileOUT.write('"BM ORIGINAL","BM DÉSAMB","FR ORIGINAL","FR AJUSTÉ"\n')

tout=fileIN.read()
#tout=tout.decode("utf-8")

sent1=tout.find('<span class="sent"')
tout1=tout[sent1:]
endoffile=tout1.find('</p></body></html>')-1
tout2=tout1[:endoffile]

# protect against possible nl suppression in manual edits (sentence splits/joins)
tout2,n2=re.subn(r'</span></span>\n</span>\n<span class="sent">','</span>\n</span>\n</span>\n<span class="sent">',tout2,0,re.U|re.MULTILINE)
if n2==0:
  print("pas de changement fin de phrase (w)")
else:
  print(n2,"changements fin de phrase (w)")

sentences=tout2.split("</span>\n</span>\n</span>\n")  # closing tag for last w|c|t + tag for annot + tag for sent

print(len(sentences), "sentences")

nsent=0
for sentence in sentences:
  nsent=nsent+1
  #print nsent,"---",sentence
  sentence=sentence+"</span>"   # close last lemma or punct or tag
  
  originalsent=re.search('<span class="sent">([^<]*)',sentence,re.U|re.MULTILINE)
  original=originalsent.group(1)
  original=original.replace("&lt;","<")
  original=original.replace("&gt;",">")

  lemmaspuncts=re.findall('<span class="(?:lemma|c|t)">([^<]*)',sentence,re.U|re.MULTILINE)
  #print len(lemmaspuncts),"lemma ou c"
  disamb=""
  itemprec=" "
  nitem=0
  for item in lemmaspuncts:
    nitem=nitem+1
    item=re.sub(r"́|̀|̌|̂","",item)
    item=item.replace("&lt;","<")
    item=item.replace("&gt;",">")
    if nitem==1:
      if item[:1]!="<":
        item=item.title()
    elif nitem==2:
      if itemprec[:1]=="<":
        item=item.title()
    if item==";" or item=="?" or item==":" or item=="!": item=" "+item+" "
    elif item=="," or item=="." : item=item
    elif itemprec[-1:]!="'" and item[:1]!="<" and itemprec[:1]!="<" : item=" "+item
    elif item=="<br/>": item=item+"\n"
    disamb=disamb+item
    itemprec=item
  disamb=disamb.strip()
  original=original.strip()
  disamb=disamb.replace('"','""')
  original=original.replace('"','""')
  #print original,"¤",disamb

  fileOUT.write('"'+original+'","'+disamb+'",,\n')

print("done, check output as "+fileINnameshort+"-bam-fra2.csv")