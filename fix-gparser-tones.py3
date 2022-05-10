#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

def nodots(m):
  first=m.groups()[0]
  firstnodots=first.replace('.','')
  return '<span class="m">'+firstnodots+'<'


nargv=len(sys.argv)
if nargv==1 : 
  print("fix-gparser-tones.py needs -at least- one argument : file name complete with .dis.html")
  sys.exit
if nargv>1 : filenamein= str(sys.argv[1])

filenameout=filenamein.replace(".dis.html","-fixed.dis.html")
filenameold=filenamein.replace(".dis.html","-before-tones-fix.dis.html")

fileIN = open(filenamein, "r")   # w+ = read-write mode
fileOUT = open(filenameout, "w")

tout=fileIN.read()
#print("tout = ",len(tout)," characters")


# check strange issue with "<span class="lemma">lámɛnbaga<\n" random insertions
wsearch=r'<span class="lemma">lámɛnbaga<\n'
wrepl=r''
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i remove <lamenbaga bug> " % nombre +" for "+wsearch +"\n"
  print(msg)

# delete empty lines
wsearch=r'<p><span class="sent"> *\n*<span class="annot" />\n</span>\n</p>'
wrepl=r''
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  empty lines suppression " % nombre +" for "+wsearch +"\n"
  print(msg)
wsearch=r'<span class="sent"> *\n*<span class="annot" />\n</span>\n'
wrepl=r''
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  empty lines suppression " % nombre +" for "+wsearch +"\n"
  print(msg)
wsearch=r'<span class="sent">None<span class="annot" />\n</span>\n'
wrepl=r''
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  empty lines suppression " % nombre +" for "+wsearch +"\n"
  print(msg)

# check if file is new format nov 2021
if '</span><span class="w"' in tout or '</span><span class="c"' in tout:
  print("adapting file to nov2021 html format")
  tout,nadapt=re.subn(r'\n</span><span class="(w|c|t)"','</span>\n<span class="\g<1>"',tout,0,re.U|re.MULTILINE)
  print(nadapt,"lines adapted")

# check dabased problems
# need text:script
textscript=re.compile(r'(?:<meta content\=\"|<meta name\=\"text\:script\" content\=\")([^\"]*)(?:\" name\=\"text\:script\" \/>|\" \/>)',re.U) # as of daba 0.9.0 dec 2020 meta format order changed!

txtsc=textscript.search(tout,re.U|re.MULTILINE)
if txtsc!=None :   # supposedly = if txtsc :
  script=txtsc.group(1)
else :
  script="Nouvel orthographe malien"
  if filenamein.endswith(".old"): script="Ancien orthographe malien"
  print(" ! textscript not set for "+filenamein+" !!!  ASSUMED : "+script)

wsearch=r'>fóyì<span class="lemma">fóyì<'
wrepl=r'>foyi<span class="lemma">fóyì<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)
wsearch=r'>fósì<span class="lemma">fósì<'
wrepl=r'>fosi<span class="lemma">fósì<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>kà<span class="lemma">kà<'
wrepl=r'>ka<span class="lemma">kà<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>òlú<span class="lemma">òlú<'
wrepl=r'>olu<span class="lemma">òlú<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>òlú<span class="lemma">òlû<'
wrepl=r'>olu<span class="lemma">òlû<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

# DEPENDS on text:script

wsearch=r'>dɔ́rɔn<span class="lemma">dɔ́rɔn<'
wrepl=r'>dɔrɔn<span class="lemma">dɔ́rɔn<'
if script=="Ancien orthographe malien": wrepl=r'>dòròn<span class="lemma">dɔ́rɔn<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>wɛ́rɛ<span class="lemma">wɛ́rɛ<'
wrepl=r'>wɛrɛ<span class="lemma">wɛ́rɛ<'
if script=="Ancien orthographe malien": wrepl=r'>wèrè<span class="lemma">wɛ́rɛ<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>wɛrɛw<span class="lemma">wɛrɛw<'
wrepl=r'>wɛrɛw<span class="lemma">wɛ́rɛw<'
if script=="Ancien orthographe malien": wrepl=r'>wèrèw<span class="lemma">wɛ́rɛw<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>dɔ́wɛrɛ<span class="lemma">dɔ́wɛrɛ<'
wrepl=r'>dɔwɛrɛ<span class="lemma">dɔ́wɛrɛ<'
if script=="Ancien orthographe malien": wrepl=r'>dòwèrè<span class="lemma">dɔ́wɛrɛ<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>bɛ́<span class="lemma">bɛ́<'
wrepl=r'>bɛ<span class="lemma">bɛ́<'
if script=="Ancien orthographe malien": wrepl=r'>bè<span class="lemma">bɛ́<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  dabased-tones correction(s) " % nombre +" for "+wsearch
  print(msg)
# 

# fix double ps like prn/dtm
wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span></span><span class="m">w'
wrepl=r'>adj</sub><sub class="gloss">\g<1></sub></span></span><span class="m">w'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">w<'
wrepl=r'>adj</sub><sub class="gloss">\g<1></sub></span><span class="m">w<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">ba<'
wrepl=r'>adj</sub><sub class="gloss">\g<1></sub></span><span class="m">ba<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">nin<'
wrepl=r'>adj</sub><sub class="gloss">\g<1></sub></span><span class="m">nin<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)


wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">ya<sub class="ps">mrph</sub><sub class="gloss">DEQU<'
wrepl=r'>vq</sub><sub class="gloss">\g<1></sub></span><span class="m">ya<sub class="ps">mrph</sub><sub class="gloss">DEQU<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">baga<sub class="ps">mrph</sub><sub class="gloss">AG.OCC<'
wrepl=r'>vq/adj</sub><sub class="gloss">\g<1></sub></span><span class="m">baga<sub class="ps">mrph</sub><sub class="gloss">AG.OCC<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">man<sub class="ps">mrph</sub><sub class="gloss">ABSTR<'
wrepl=r'>vq</sub><sub class="gloss">\g<1></sub></span><span class="m">man<sub class="ps">mrph</sub><sub class="gloss">ADJ<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>vq/adj</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">man<sub class="ps">mrph</sub><sub class="gloss">ADJ<'
wrepl=r'>vq</sub><sub class="gloss">\g<1></sub></span><span class="m">man<sub class="ps">mrph</sub><sub class="gloss">ADJ<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>n</sub><sub class="gloss">([^<\n]+)</sub></span><span class="m">([^<\n]+)<sub class="ps">vq/adj<'
wrepl=r'>n</sub><sub class="gloss">\g<1></sub></span><span class="m">\g<2><sub class="ps">adj<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'<span class="m">ní*<sub class="ps">(?:conj/prep|prep/conj)</sub><sub class="gloss">et</sub></span>'
wrepl=r'<span class="m">ni<sub class="ps">conj</sub><sub class="gloss">et</sub></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>n</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">adj/n<'
wrepl=r'>n</sub>\g<1><span class="m">\g<2><sub class="ps">n<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)


wsearch=r'>dtm</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">(?:prn/dtm|dtm/prn)<'
wrepl=r'>dtm</sub>\g<1><span class="m">\g<2><sub class="ps">dtm<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>prn</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">(?:prn/dtm|dtm/prn)<'
wrepl=r'>prn</sub>\g<1><span class="m">\g<2><sub class="ps">prn<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>n</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">adv/n<'
wrepl=r'>n</sub>\g<1><span class="m">\g<2><sub class="ps">n<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>n</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">adj/n<'
wrepl=r'>n</sub>\g<1><span class="m">\g<2><sub class="ps">n<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>adj</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">adj/n<'
wrepl=r'>adj</sub>\g<1><span class="m">\g<2><sub class="ps">n<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>conj</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">(?:prep/conj|conj/prep)<'
wrepl=r'>conj</sub>\g<1><span class="m">\g<2><sub class="ps">conj<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>prep</sub>(<sub class="gloss">[^<\n]+</sub>)*<span class="m">([^<\n]+)<sub class="ps">(?:prep/conj|conj/prep)<'
wrepl=r'>prep</sub>\g<1><span class="m">\g<2><sub class="ps">prep<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>nísɔngoya<sub class="ps">v</sub><sub class="gloss">contrarier</sub><span class="m">nísɔngo<sub class="ps">adj/n<'
wrepl=r'>nísɔngoya<sub class="ps">v</sub><sub class="gloss">contrarier</sub><span class="m">nísɔngo<sub class="ps">n<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'<span class="m">dí<sub class="ps">vq/adj</sub><sub class="gloss">agréable</sub></span><span class="m">ya<sub class="ps">mrph</sub><sub class="gloss">ABSTR<'
wrepl=r'<span class="m">dí<sub class="ps">vq</sub><sub class="gloss">agréable</sub></span><span class="m">ya<sub class="ps">mrph</sub><sub class="gloss">ABSTR<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>adv.p</sub><sub class="gloss">sérieusement</sub><span class="m">sɛ̀bɛ<sub class="ps">adj/n</sub><sub class="gloss">sérieux</sub></span><span class="m">kɔ̀rɔ<sub class="ps">vq/adj<'
wrepl=r'>adv.p</sub><sub class="gloss">sérieusement</sub><span class="m">sɛ̀bɛ<sub class="ps">adj</sub><sub class="gloss">sérieux</sub></span><span class="m">kɔ̀rɔ<sub class="ps">adj<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

wsearch=r'>yàn<sub class="ps">adv/n</sub><sub class="gloss">ici</sub></span><span class="m">fàn<sub class="ps">n<'
wrepl=r'>yàn<sub class="ps">n</sub><sub class="gloss">ici</sub></span><span class="m">fàn<sub class="ps">n<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  double-ps correction(s) " % nombre +" for "+wsearch
  print(msg)

# fix remaing dots in lemmas ----------------------------------
wsearch=r'<span class="m">([^<\n\.]+\.[^<\n]+)<'
tout,nombre=re.subn(wsearch,nodots,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i lemmas with dots -> no dots" % nombre
  print(msg)

# fix NUMnan gloss missing ------------------------------------
wsearch=r'span class="lemma">([0-9]+)nan<sub class="ps">adj</sub><span class="m">([0-9]+)<sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD<'
wrepl=r'span class="lemma">\g<1>nan<sub class="ps">adj</sub><span class="m">\g<2><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  NUMnan gloss missing fixed " % nombre
  print(msg)

# -----------------------------------------------------------------------
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
  # print(lemma, ps, slemma)
  slemma_notone,ntones=re.subn(r'[́̀̌̂]','',slemma)
  if ntones==0:
    print(lemma+":"+ps+": -> no tone in ",slemma," ???")
  else:
    fixedlist.append(fixeditem)
    lemma_tones=lemma.replace(slemma_notone,slemma,1)  # only 1st occurence: avoid nànà
    # print("->",lemma_tones)
    wsearch=r'<span class="'+lemmaclass+r'">'+lemma      +r'<sub class="ps">'+ps+r'</sub><span class="m">'+slemma+r'<'
    wrepl  =r'<span class="'+lemmaclass+r'">'+lemma_tones+r'<sub class="ps">'+ps+r'</sub><span class="m">'+slemma+r'<'
    tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
    if nombre>0 :
      msg="%i  tones correction(s) " % nombre +" for "+lemma +"\n"
      #print(msg)
      
print("gparser tones fixed items: ",len(fixedlist))

fileOUT.write(tout)

fileIN.close()
fileOUT.close()

os.rename(filenamein, filenameold)
os.rename(filenameout, filenamein)
