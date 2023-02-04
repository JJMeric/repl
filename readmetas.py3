#!/usr/bin/python
# -*- coding: utf8 -*-
# coding=UTF-8

import os
import re
import sys
import daba.formats1

fileINname= str(sys.argv[1])
if fileINname.endswith(".dis.html"): fileDISname=fileINname
else: fileDISname=fileINname+".dis.html"

if os.path.exists(fileDISname) : 
  
  print("processing ",fileDISname)
else:
  sys.exit("\n\033[1mno file named "+fileDISname+"\033[0m\n")


freader = daba.formats1.HtmlReader(fileDISname)
metadata = freader.metadata

#print(metadata)
#print("--------------")
metas={}
items=[]
authors=False
for x,y in metadata.items():
  item,subitem=x.split(":")

  if item in items:
    if item=="author" and authors:
      vy=y.split("|")
      authindex=0
      for v in vy:
        authindex+=1
        metas[item][authindex][subitem]=v
    else:
      metas[item][subitem]=y
  else: 
    items.append(item)
    if item=="author":
      if "|" in y:
        vy=y.split("|")
        authors=True
        authindex=0
        for v in vy:
          authindex+=1
          if authindex==1: 
                  metas[item]={authindex: {subitem:v}}
          else :  metas[item][authindex]={subitem:v}
      else:
        metas[item]={subitem:y}
      #print("\n",metas,"\n")
    else:
      metas[item]={subitem:y}
  
#print(metas)
#print("--------------")
print("\033[42;30;1mMETA \033[0m\n")
for x,y in sorted(metas.items()):
  print(x)
  for w,z in sorted(y.items()):
    if x=="author" and authors:
      print("\t",w,":")
      for wn,zn in sorted(z.items()):
        print("\t\t",wn,":\t",zn)

    else: print("\t",w,":\t",z)