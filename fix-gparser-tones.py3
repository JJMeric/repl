#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

nargv=len(sys.argv)
if nargv==1 : 
  print("repl.py needs -at least- one argument : file name")
  sys.exit
if nargv>1 : filename= str(sys.argv[1])

fileIN = open(filename, "r")   # w+ = read-write mode
fileOUT = open(filename.replace(".dis.html","-fixed.dis.html"), "w")

tout=fileIN.read()
#print("tout = ",len(tout)," characters")

# tones on gparser generated derivations and flexions lacking tones
# example : sinsinnen:ptcp: [sínsin:v:appuyer nen:mrph:PTCP.RES]
fixsearch=re.compile(r'<span class="(lemma|lemma var)">([^<́̀̌̂]+)<sub class="ps">([^<]+)</sub><span class="m">([^<]+)<')
# captures lemma sinsinnen ptcp and sínsi
# extract all similar constructs 
# 
fixtones=fixsearch.finditer(tout,re.U|re.MULTILINE)
fixedlist=[]
for match in fixtones:
  lemmaclass=match.group(1)
  lemma=match.group(2)
  ps=match.group(3)
  slemma=match.group(4)
  fixeditem=lemmaclass+':'+lemma+':'+ps+':'+slemma
  if fixeditem in fixedlist: continue
  print(lemma, ps, slemma)
  slemma_notone,ntones=re.subn(r'[́̀̌̂]','',slemma)
  if ntones==0:
    print(lemma+":"+ps+": -> no tone in ",slemma," ???")
  else:
    fixedlist.append(fixeditem)
    lemma_tones=lemma.replace(slemma_notone,slemma)
    print("->",lemma_tones)
    wsearch=r'<span class="'+lemmaclass+r'">'+lemma      +r'<sub class="ps">'+ps+r'</sub><span class="m">'+slemma+r'<'
    wrepl  =r'<span class="'+lemmaclass+r'">'+lemma_tones+r'<sub class="ps">'+ps+r'</sub><span class="m">'+slemma+r'<'
    tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
    if nombre>0 :
      msg="%i  tones correction(s) " % nombre +" for "+lemma +"\n"
      print(msg)
      
print("gparser tones fixed items: ",len(fixedlist))

fileOUT.write(tout)

fileIN.close()
fileOUT.close()