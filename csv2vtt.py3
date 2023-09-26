#!/usr/bin/python
# -*- coding: utf8 -*-
# coding=UTF-8

import os
import re
import sys

fileCSVname= str(sys.argv[1])
if not fileCSVname.endswith(".csv"):
  fileCSVname=fileCSVname+".csv"

filename=fileCSVname[:-4]

if os.path.exists(fileCSVname) : 
  
  fileCSV = open(fileCSVname,"r")
  tout=fileCSV.read()
  fileCSV.close()

first,body=tout.split("\n",1)

vtt=re.sub(r'^[A-Za-z0-9]+\t[A-Z\_\-]*([0-9])','@@\g<1>',body,0,re.U|re.MULTILINE)
vtt=re.sub(r'\.([0-9]{3})\t([0-9])','.\g<1> --> \g<2>',vtt,0,re.U|re.MULTILINE)
vtt=re.sub(r'\t','\n',vtt,0,re.U|re.MULTILINE)
vtt=re.sub(r'@@','\n',vtt,0,re.U|re.MULTILINE)
vtt=re.sub(r'<h>','<b>',vtt,0,re.U|re.MULTILINE)
vtt=re.sub(r'</h>','</b>',vtt,0,re.U|re.MULTILINE)
vtt=vtt+"\n\n"
vtt=re.sub(r'\n([^\n]+)\n\n','\n<i>\g<1></i>\n\n',vtt,0,re.U|re.MULTILINE)

vtt="WEBVTT - Jean-Jacques Méric <jjmeric@free.fr> - 2023\n"+vtt

fileOUTname=filename+".vtt"
fileOUT=open(fileOUTname,"w")
fileOUT.write(vtt)
fileOUT.close()

vttbam=re.sub(r'\n<i>[^\n]+</i>\n\n','\n\n',vtt,0,re.U|re.MULTILINE)

fileOUTname=filename+"-bam.vtt"
fileOUT=open(fileOUTname,"w")
fileOUT.write(vttbam)
fileOUT.close()

vttfra=re.sub(r'\n[^\n]+\n<i>','\n<i>',vtt,0,re.U|re.MULTILINE)

fileOUTname=filename+"-fra.vtt"
fileOUT=open(fileOUTname,"w")
fileOUT.write(vttfra)
fileOUT.close()

print("\033[42;30;1mJob done, check output as "+filename+".vtt -bam.vtt & -fra.vtt\033[0m\n")