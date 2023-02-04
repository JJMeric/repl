#!/usr/bin/python
# -*- coding: utf8 -*-
# coding=UTF-8

import os
import re
import sys

global fileINname,fileINnameshort,fichier

fileINname= str(sys.argv[1])
INext=fileINname.find(".csv")
fileINnameshort=fileINname[0:INext]
fichier=fileINnameshort

has_dis=False
fileDISname=fileINnameshort+".dis.html"
if os.path.exists(fileDISname) : 
  
  fileDIS = open(fileDISname,"r")
  tout=fileDIS.read()
  fileDIS.close()
  has_dis=True

  # (from disambextract.py3)
  sent1=tout.find('<span class="sent"')
  tout1=tout[sent1:]
  endoffile=tout1.find('</p></body></html>')-1
  tout2=tout1[:endoffile]

  # protect against possible nl suppression in manual edits (sentence splits/joins)
  tout2,n2=re.subn(r'</span></span>\n</span>\n<span class="sent">','</span>\n</span>\n</span>\n<span class="sent">',tout2,0,re.U|re.MULTILINE)
  if n2!=0:
    print(fileDISname,":",n2,"changements fin de phrase (w) Ancien format .dis -> nouveau format")

  sentences=tout2.split("</span>\n</span>\n</span>\n")  # closing tag for last w|c|t + tag for annot + tag for sent

  print(fileDISname,":",len(sentences), "sentences")
else:
  print("\nno file named "+fileDISname+" -> generating EAF with tx and ft only...")

eaf_header="""<?xml version="1.0" encoding="UTF-8"?>
<ANNOTATION_DOCUMENT AUTHOR="ELAN-Tools" DATE="2022-12-11T20:14:32+01:00" FORMAT="3.0" VERSION="3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/EAFv3.0.xsd">
    <HEADER MEDIA_FILE="***WAV***" TIME_UNITS="milliseconds">
        <MEDIA_DESCRIPTOR MEDIA_URL="file://***WAV***"/>
        <PROPERTY NAME="URN">urn:nl-mpi-tools-elan-eaf:cf1df908-4025-49bd-a547-079aaa40b8d0</PROPERTY>
        <PROPERTY NAME="lastUsedAnnotationId">***annotationindex***</PROPERTY>
    </HEADER>
"""
#             question what about URN : is it important - if yes, how to generate?

eaf_footer="""    <LINGUISTIC_TYPE GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="ref" TIME_ALIGNABLE="true"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="tx" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="ps" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="ge" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="cf" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="rx" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="ft" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="lit" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="not" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="wt" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="wps" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Subdivision" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="mot" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Subdivision" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="mb" TIME_ALIGNABLE="false"/>
    <LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="ftf" TIME_ALIGNABLE="false"/>
    <LOCALE COUNTRY_CODE="FR" LANGUAGE_CODE="fr"/>
    <LANGUAGE LANG_DEF="http://cdb.iso.org/lg/CDB-00138512-001" LANG_ID="fra" LANG_LABEL="French (fra)"/>
    <LANGUAGE LANG_DEF="http://cdb.iso.org/lg/CDB-00138482-001" LANG_ID="bam" LANG_LABEL="Bambara (bam)"/>
    <CONSTRAINT DESCRIPTION="Time subdivision of parent annotation's time interval, no time gaps allowed within this interval" STEREOTYPE="Time_Subdivision"/>
    <CONSTRAINT DESCRIPTION="Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered" STEREOTYPE="Symbolic_Subdivision"/>
    <CONSTRAINT DESCRIPTION="1-1 association with a parent annotation" STEREOTYPE="Symbolic_Association"/>
    <CONSTRAINT DESCRIPTION="Time alignable annotations within the parent annotation's time interval, gaps are allowed" STEREOTYPE="Included_In"/>
</ANNOTATION_DOCUMENT>
"""
fileIN = open(fileINname, "r")
tout=fileIN.read()
fileIN.close()
tout=re.sub(r"\n$(?![\r\n])", "",tout)  # fixes end of file extra empty line

lines=tout.split("\n")
print(fileINname,":",len(lines)-1," sentences")
if has_dis:
  if len(sentences)!=len(lines)-1:
    sys.exit("\n      \033[1m.csv and .dis.html do not have the same number of sentences ?\033[0m\n")
  else:
    print("\nWarning: .csv and .dis.html sentences are supposed to be aligned but this is not checked here!\n      Please check manually if problems arise")

lineindex=0
tsindex=0
annotindex=0
msprevstart=0
tslines=""
nlines_dict={}
reflines_dict={}
reflines_global=""
msendprev_dict={}
txlines_dict={}
ftlines_dict={}
tx_dict={}  # nested
ft_dict={}  # nested
speaker_list=[]
if has_dis:
  mot_dict={}
  motps_dict={}
  motgloss_dict={}
  motspans_dict={}

nsent=-1  # index in tab of sentences
for line in lines:
  lineindex+=1
  if lineindex==1 : continue
  if line.strip()=="": continue

  nsent+=1
  ntabs=line.count("\t")
  if ntabs >= 5:
    speaker,ref,start,end,tx,ft=line.split("\t",5)
  else: sys.exit("\033[1mtab missing ("+str(ntabs)+"/5) on line "+str(lineindex)+" :\033[0m"+line)

  if speaker not in speaker_list: 
    speaker_list.append(speaker)
    reflines_dict[speaker]=""
    txlines_dict[speaker]=""
    ftlines_dict[speaker]=""
    msendprev_dict[speaker]={"ms":0, "ts":"00:00:00.000"}
    tx_dict[speaker]={}
    ft_dict[speaker]={}
    if has_dis:
      mot_dict[speaker]={}
      motps_dict[speaker]={}
      motgloss_dict[speaker]={}
      motspans_dict[speaker]={}

  # timecodes
  ncol=start.count(":")
  if ncol==2:
    starth,startm,starts_ms=start.split(":")
  else:
    sys.exit("\033[1mnot the right number of ':' ("+str(ncol)+"/2) on line "+str(lineindex)+" :\033[0m"+line)
  
  if "." in starts_ms:
    starts,startms=starts_ms.split(".")
  else:
    sys.exit("\033[1mstart: no dot before milliseconds on line "+str(lineindex)+" :\033[0m"+line)
  
  if int(startm)>59: sys.exit("\033[1mstart: minutes > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(starts)>59: sys.exit("\033[1mstart: seconds > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(startms)>999: sys.exit("\033[1mstart: milliseconds > 999 ??? "+str(lineindex)+" :\033[0m"+line)
  ms=int(startms)+int(starts)*1000+int(startm)*60000+int(starth)*3600000

  # start time must be >= previous end timecode
  msprev=msendprev_dict[speaker]['ms']
  msprevcode=msendprev_dict[speaker]['ts']
  #print("line ",lineindex, ":",msendprev_dict)
  if ms < msprev : sys.exit("\033[1mstart timecode before previous one - line "+str(lineindex)+" :\033[0m"+start+" < "+msprevcode)
  msstart=ms
  tsindex+=1
  tslines+='\t\t<TIME_SLOT TIME_SLOT_ID="ts'+str(tsindex)+'" TIME_VALUE="'+str(ms)+'"/>\n'
  tsstart=tsindex
  
  ncol=end.count(":")
  if ncol==2:
    endh,endm,ends_ms=end.split(":")
  else:
    sys.exit("\033[1mnot the right number of ':' ("+str(ncol)+"/2) on line "+str(lineindex)+" :\033[0m"+line)

  if "." in ends_ms:
    ends,endms=ends_ms.split(".")
  else:
    sys.exit("\033[1mend: no dot before milliseconds on line "+str(lineindex)+" :\033[0m"+line)
  if int(endm)>59: sys.exit("\033[1mend: minutes > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(ends)>59: sys.exit("\033[1mend: seconds > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(endms)>999: sys.exit("\033[1mend: milliseconds > 999 ??? "+str(lineindex)+" :\033[0m"+line)
  ms=int(endms)+int(ends)*1000+int(endm)*60000+int(endh)*3600000
  if ms < msstart : sys.exit("\033[1mend timecode before start - line "+str(lineindex)+" :\033[0m"+end+" < "+start)
  
  msendprev_dict[speaker]={"ms":ms,"ts":end}

  tsindex+=1
  tslines+='\t\t<TIME_SLOT TIME_SLOT_ID="ts'+str(tsindex)+'" TIME_VALUE="'+str(ms)+'"/>\n'
  tsend=tsindex

  annotindex+=1
  refline='\t\t\t<ALIGNABLE_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" TIME_SLOT_REF1="ts'+str(tsstart)+'" TIME_SLOT_REF2="ts'+str(tsend)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+ref+'</ANNOTATION_VALUE>\n\t\t\t</ALIGNABLE_ANNOTATION>\n'
  reflines_dict[speaker]+='\t\t<ANNOTATION>\n'+refline+'\t\t</ANNOTATION>\n'
  reflines_global+='\t\t<ANNOTATION>\n'+refline+'\t\t</ANNOTATION>\n'

  nlines_dict[annotindex]=nsent # must start at 0 to index in sentences
  # possible check here : this sentence has the same speaker id in the dis file <sp></sp>

  tx_dict[speaker][annotindex]=tx
  ft_dict[speaker][annotindex]=ft

#-------------------

for speaker in speaker_list:
  for refid,ft in ft_dict[speaker].items():
    annotindex+=1
    ftline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(refid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+ft+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>'
    ftlines_dict[speaker]+='\t\t<ANNOTATION>\n'+ftline+'\t\t</ANNOTATION>\n'

for speaker in speaker_list:
  for refid,tx in tx_dict[speaker].items():
    annotindex+=1
    txline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(refid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+tx+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>'
    txlines_dict[speaker]+='\t\t<ANNOTATION>\n'+txline+'\t\t</ANNOTATION>\n'

    if has_dis:
      # ici, pour chacune de ces phrases, alimenter le dictionnaire des mots premier niveau
      dis_sent=nlines_dict[refid]
      #print(tx," =\n",sentences[dis_sent])
      lemmas=re.findall(r'<span class="lemma">([^\<]+)<sub class="ps">([^\<]+)</sub>(?:<sub class="gloss">([^\<]+)</sub>)*(?:(<span class="m">[^\n]+</span>)*)*</span>',sentences[dis_sent])
      #print("lemmas:\n",lemmas)
      mot_list=[]
      motps_list=[]
      motgloss_list=[]
      motspans_list=[]
      for lx in lemmas:
        mot_list.append(lx[0])
        motps_list.append(lx[1])
        gloss=lx[2]
        if lx[2]=='':  # case where gloss is empty, try catch from sub spans
          # I do not even test that lx[3] exists!
          subglosses=re.findall(r'<sub class="gloss">([^\<]+)</sub>',lx[3])
          gloss="-".join(subglosses)

        motgloss_list.append(gloss)
        motspans_list.append(lx[3])

      mot_dict[speaker][annotindex]=mot_list
      motps_dict[speaker][annotindex]=motps_list
      motgloss_dict[speaker][annotindex]=motgloss_list
      motspans_dict[speaker][annotindex]=motspans_list

if has_dis:
  # traiter les mots
  wps_dict={}
  wt_dict={}
  spans_dict={}
  motlines_dict={}

  for speaker in speaker_list:
    wps_dict[speaker]={}
    wt_dict[speaker]={}
    spans_dict[speaker]={}
    motlines_dict[speaker]=""

    for txid,mots in mot_dict[speaker].items():
      prevannot=0
      motid=-1
      listps=motps_dict[speaker][txid]
      listgloss=motgloss_dict[speaker][txid]
      listspans=motspans_dict[speaker][txid]

      for mot in mots:
        annotindex+=1
        motid+=1

        if prevannot==0:
          motline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(txid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+mot+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'  
        else:
          motline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(txid)+'" PREVIOUS_ANNOTATION="a'+str(prevannot)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+mot+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'
        prevannot=annotindex

        motlines_dict[speaker]+='\t\t<ANNOTATION>\n'+motline+'\t\t</ANNOTATION>\n'

        wps_dict[speaker][annotindex] = listps[motid]
        wt_dict[speaker][annotindex]  = listgloss[motid]
        spans_dict[speaker][annotindex]  = listspans[motid]

  wpslines_dict={}
  wtlines_dict={}
  mblines_dict={}
  pslines_dict={}
  gelines_dict={}
  ps_dict={}
  ge_dict={}

  for speaker in speaker_list:
    # ici pour chacun de ces mots, alimenter les dictionnaires des wps, wt, mb
    # print("wps_dict:\n",wps_dict)
    wpslines_dict[speaker]=""
    for motid,ps in wps_dict[speaker].items():
      annotindex+=1
      wpsline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(motid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+ps+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'
      wpslines_dict[speaker]+='\t\t<ANNOTATION>\n'+wpsline+'\t\t</ANNOTATION>\n'

    wtlines_dict[speaker]=""
    for motid,gloss in wt_dict[speaker].items():
      annotindex+=1
      wtline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(motid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+gloss+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'
      wtlines_dict[speaker]+='\t\t<ANNOTATION>\n'+wtline+'\t\t</ANNOTATION>\n'

    mblines_dict[speaker]=""
    ps_dict[speaker]={}
    ge_dict[speaker]={}
    for motid,span in spans_dict[speaker].items():
      subs=re.findall(r'<span class="m">([^\<]+)<sub class="ps">([^\<]+)</sub>(?:<sub class="gloss">([^\<]+)</sub>)*</span>',span)
      prevannot=0
      for sub in subs:
        lx=sub[0]
        ps=sub[1]
        gloss=sub[2]
        annotindex+=1
        if prevannot==0:
          mbline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(motid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+lx+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'  
        else:
          mbline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(motid)+'" PREVIOUS_ANNOTATION="a'+str(prevannot)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+lx+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'
        prevannot=annotindex
     
        mblines_dict[speaker]+='\t\t<ANNOTATION>\n'+mbline+'\t\t</ANNOTATION>\n'
        ps_dict[speaker][annotindex]=ps
        ge_dict[speaker][annotindex]=gloss

    pslines_dict[speaker]=""
    for mbid,ps in ps_dict[speaker].items():
      annotindex+=1
      psline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(mbid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+ps+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'
      pslines_dict[speaker]+='\t\t<ANNOTATION>\n'+psline+'\t\t</ANNOTATION>\n'

    gelines_dict[speaker]=""
    for mbid,ge in ge_dict[speaker].items():
      annotindex+=1
      geline='\t\t\t<REF_ANNOTATION ANNOTATION_ID="a'+str(annotindex)+'" ANNOTATION_REF="a'+str(mbid)+'">\n\t\t\t\t<ANNOTATION_VALUE>'+ge+'</ANNOTATION_VALUE>\n\t\t\t</REF_ANNOTATION>\n'
      gelines_dict[speaker]+='\t\t<ANNOTATION>\n'+geline+'\t\t</ANNOTATION>\n'



if os.path.exists(fileINnameshort+".wav") :
  eaf_header=eaf_header.replace("***WAV***",fileINnameshort+".wav")
elif os.path.exists(fileINnameshort+".mp3") :
  print("\033[1mWarning\033[0m, "+fileINnameshort+".mp3"+" found here, but is not a good format for Elan and vtt file : time codes ms not compatible")
else:
  print("\033[1mWarning\033[0m, "+fileINnameshort+".wav"+" not found here, check eaf MEDIA_URL")
eaf_header=eaf_header.replace("***annotationindex***",str(annotindex))

# enrobage des différents bspeakerks
eaf_body=""

eaf_body+="\t<TIME_ORDER>\n"+tslines+"\t</TIME_ORDER>\n"
if len(speaker_list)>1:
  eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="ref" TIER_ID="ref@global">\n'+reflines_global+'\t</TIER>\n'
for speaker in speaker_list:
  eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="ref" TIER_ID="ref@'+speaker+'">\n'+reflines_dict[speaker]+'\t</TIER>\n'
  eaf_body+='\t<TIER DEFAULT_LOCALE="fr" LANG_REF="bam" LINGUISTIC_TYPE_REF="tx" PARENT_REF="ref@'+speaker+'" TIER_ID="tx@'+speaker+'">\n'+txlines_dict[speaker]+'\t</TIER>\n'
  eaf_body+='\t<TIER LANG_REF="fra" LINGUISTIC_TYPE_REF="ftf" PARENT_REF="ref@'+speaker+'" TIER_ID="ft@'+speaker+'">\n'+ftlines_dict[speaker]+'\t</TIER>\n'
  if has_dis:
    eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="mot" PARENT_REF="tx@'+speaker+'" TIER_ID="mot@'+speaker+'">\n'+motlines_dict[speaker]+'\t</TIER>\n'
    eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="wps" PARENT_REF="mot@'+speaker+'" TIER_ID="wps@'+speaker+'">\n'+wpslines_dict[speaker]+'\t</TIER>\n'
    eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="wt" PARENT_REF="mot@'+speaker+'" TIER_ID="wt@'+speaker+'">\n'+wtlines_dict[speaker]+'\t</TIER>\n'
    eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="mb" PARENT_REF="mot@'+speaker+'" TIER_ID="mb@'+speaker+'">\n'+mblines_dict[speaker]+'\t</TIER>\n'
    eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="rx" PARENT_REF="mb@'+speaker+'" TIER_ID="ps@'+speaker+'">\n'+pslines_dict[speaker]+'\t</TIER>\n'
    eaf_body+='\t<TIER LINGUISTIC_TYPE_REF="ge" PARENT_REF="mb@'+speaker+'" TIER_ID="ge@'+speaker+'">\n'+gelines_dict[speaker]+'\t</TIER>\n'




pre_footer=""
if not has_dis:
  for speaker in speaker_list:
    pre_footer+='\t<TIER LINGUISTIC_TYPE_REF="mot" PARENT_REF="tx@'+speaker+'" TIER_ID="mot@'+speaker+'"/>\n\t<TIER LINGUISTIC_TYPE_REF="mb" PARENT_REF="mot@'+speaker+'" TIER_ID="mb@'+speaker+'"/>\n\t<TIER LINGUISTIC_TYPE_REF="wt" PARENT_REF="mot@'+speaker+'" TIER_ID="wt@'+speaker+'"/>\n\t<TIER LINGUISTIC_TYPE_REF="wps" PARENT_REF="mot@'+speaker+'" TIER_ID="wps@'+speaker+'"/>\n\t<TIER LINGUISTIC_TYPE_REF="ge" PARENT_REF="mb@'+speaker+'" TIER_ID="ge@'+speaker+'"/>\n\t<TIER LINGUISTIC_TYPE_REF="rx" PARENT_REF="mb@'+speaker+'" TIER_ID="ps@'+speaker+'"/>\n'
eaf_footer=pre_footer+eaf_footer

fileOUT = open (fileINnameshort+".eaf","w")

fileOUT.write(eaf_header)
fileOUT.write(eaf_body)
fileOUT.write(eaf_footer)

fileOUT.close()

print("\033[42;30;1mJob done, check output as "+fileINnameshort+".eaf\033[0m\n")