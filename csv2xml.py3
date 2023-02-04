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

xmlheader="""<?xml version="1.0" encoding="UTF-8"?>
       <?xml-stylesheet type="text/xsl" href="../Styles/olac3.xsl"?>
      <catalog xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:oai="http://www.openarchives.org/OAI/2.0/"
         xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
         xmlns:crdo="http://crdo.risc.cnrs.fr/schemas/"
         xmlns:dcterms="http://purl.org/dc/terms/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns:imdi="http://www.mpi.nl/IMDI/Schema/IMDI"
         xsi:schemaLocation="http://cocoon.huma-num.fr/schemas/ http://cocoon.huma-num.fr/schemas/metadata.xsd">
"""

xmlfooter="""</catalog>
"""
### <xml> tag not closed?  mmmmmmmmmmmm

xmlaudio="""   <item crdo:datestamp="" crdo:id="crdo-***fileref***_SOUND">
      <dc:publisher>Langage, Langues et Cultures d'Afrique Noire</dc:publisher>
      <dc:contributor xsi:type="olac:role" olac:code="author">***author***</dc:contributor>
      <dc:contributor xsi:type="olac:role" olac:code="speaker">***speaker***</dc:contributor>
      <dc:contributor xsi:type="olac:role" olac:code="depositor">Langage, Langues et Cultures d'Afrique Noire</dc:contributor>
      <dcterms:spatial>***place***</dcterms:spatial>
      <dcterms:spatial xsi:type="dcterms:Point">***coord***;</dcterms:spatial>
      <dcterms:spatial xsi:type="dcterms:ISO3166">***country***</dcterms:spatial>
      <dc:title xml:lang="fr">***title***</dc:title>
      <dc:description xml:lang="fr">***description***</dc:description>
      <dc:type xsi:type="olac:linguistic-type" olac:code="primary_text"/>
      <dc:type xsi:type="olac:linguistic-field"
               olac:code="anthropological_linguistics"/>
      <dc:type xsi:type="olac:discourse-type" olac:code="narrative"/>
      <dcterms:created xsi:type="dcterms:W3CDTF">***created***</dcterms:created>
      <dc:language xsi:type="olac:language" olac:code="bam">Bambara</dc:language>
      <dc:subject xsi:type="olac:language" olac:code="bam">Bambara</dc:subject>
      <dc:identifier xsi:type="dcterms:URI">https://corporan.huma-num.fr/Archives/BAM/WAV/***fileref***</dc:identifier>
      <dcterms:isRequiredBy xsi:type="dcterms:URI">https://corporan.huma-num.fr/Archives/BAM/ELAN/***fileref***</dcterms:isRequiredBy>
      <dc:format xsi:type="dcterms:IMT">audio/x-wav</dc:format>
      <dc:type xsi:type="dcterms:DCMIType">Sound</dc:type>
      <dcterms:extent>***duration***</dcterms:extent>
      <dc:rights>Copyright © ***copyright***</dc:rights>
      <dcterms:licence xsi:type="dcterms:URI">http://creativecommons.org/licenses/by-nc-nd/2.5/</dcterms:licence>
      <dcterms:accessRights>open</dcterms:accessRights>
      <crdo:collection>Llacan</crdo:collection>
   </item>
"""

xmleaf="""   <item crdo:datestamp="" crdo:id="crdo-***fileref***_SOUND">
      <dc:publisher>Langage, Langues et Cultures d'Afrique Noire</dc:publisher>
      <dc:contributor xsi:type="olac:role" olac:code="author">***author***</dc:contributor>
      <dc:contributor xsi:type="olac:role" olac:code="speaker">***speaker***</dc:contributor>
      <dc:contributor xsi:type="olac:role" olac:code="depositor">Langage, Langues et Cultures d'Afrique Noire</dc:contributor>
      <dcterms:spatial>***place***</dcterms:spatial>
      <dcterms:spatial xsi:type="dcterms:Point">***coord***</dcterms:spatial>
      <dcterms:spatial xsi:type="dcterms:ISO3166">***country***</dcterms:spatial>
      <dc:title xml:lang="fr">***title***</dc:title>
      <dc:description xml:lang="fr">***description***</dc:description>
      <dc:type xsi:type="olac:linguistic-type" olac:code="primary_text"/>
      <dc:type xsi:type="olac:linguistic-field"
               olac:code="anthropological_linguistics"/>
      <dc:type xsi:type="olac:discourse-type" olac:code="narrative"/>
      <dcterms:created xsi:type="dcterms:W3CDTF">***created***</dcterms:created>
      <dc:subject>Annotation</dc:subject>
      <dc:subject>Morphosyntax</dc:subject>
      <dc:subject>Leipzig Glossing Rules</dc:subject>
      <dc:language xsi:type="olac:language" olac:code="fr">français</dc:language>
      <dc:subject xsi:type="olac:language" olac:code="bam">Bambara</dc:subject>
      <dc:identifier xsi:type="dcterms:URI">https://corporan.huma-num.fr/Archives/BAM/ELAN/***fileref***</dc:identifier>
      <dcterms:requires xsi:type="dcterms:URI">https://corporan.huma-num.fr/Archives/BAM/WAV/***fileref***</dcterms:requires>
      <dc:format xsi:type="dcterms:IMT">text/xml</dc:format>
      <dc:type xsi:type="dcterms:DCMIType">Text</dc:type>
      <dcterms:extent>***words*** words</dcterms:extent>
      <dc:rights>Copyright © ***copyright***</dc:rights>
      <dcterms:licence xsi:type="dcterms:URI">http://creativecommons.org/licenses/by-nc-nd/2.5/</dcterms:licence>
      <dcterms:accessRights>open</dcterms:accessRights>
      <crdo:collection>Llacan</crdo:collection>
   </item>
"""
xml0=xmlaudio+xmleaf

fileIN = open(fileINname, "r")
tout=fileIN.read()
fileIN.close()
tout=re.sub(r"\n$(?![\r\n])", "",tout)  # fixes end of file extra empty line

lines=tout.split("\n")
print(fileINname,":",len(lines)-1," sentences")

lineindex=0

for line in lines:
  xml=xml0
  lineindex+=1
  if lineindex==1 : continue  # skip 1st line
  if line.strip()=="": continue  # skip empty/trailing lines

  #title,description,durationhms,words,created,author,speaker,place,coord,country,fileref,copyright=line.split("\t")
  title,description,duration,words,created,author,speaker,place,coord,country,fileref,corbamaref,copyright=line.split("\t")
  # note: corbamaref : for future use
  
  if title=="": continue

  # h,m,s=duration.split(":")
  # duration=3600*int(h)+60*int(m)+s

  xml=xml.replace("***fileref***",fileref)
  xml=xml.replace("***author***",author)
  xml=xml.replace("***speaker***",speaker)
  xml=xml.replace("***place***",place)
  xml=xml.replace("***coord***",coord)
  xml=xml.replace("***country***",country)
  xml=xml.replace("***title***",title)
  xml=xml.replace("***description***",description)
  # xml=xml.replace("***duration***",str(duration))
  xml=xml.replace("***duration***",duration)
  xml=xml.replace("***words***",words)
  xml=xml.replace("***created***",created)
  xml=xml.replace("***copyright***",copyright)

  fileOUT=open(fileref+".xml","w")
  fileOUT.write(xmlheader+xml+xmlfooter)
  fileOUT.close()
  print("created "+fileref+".xml")

print("\033[42;30;1mJob done\033[0m\n")