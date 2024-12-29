#!/usr/bin/python
# coding=UTF-8

import os
import sys
import re

filename= str(sys.argv[1])

fileIN = open(filename, "r",encoding="UTF-8")
fileOUT = open(filename+"-cleaned","w",encoding="UTF-8")
text=fileIN.read()
fileIN.close()

# global replaces

text,nbr=re.subn(r'([\u07EB])[\u07EB]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("short high tone:",nbr)

text,nbr=re.subn(r'([\u07EC])[\u07EC]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("short low tone:",nbr)

text,nbr=re.subn(r'([\u07ED])[\u07ED]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("short rising tone:",nbr)

text,nbr=re.subn(r'([\u07EE])[\u07EE]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("long descending tone:",nbr)

text,nbr=re.subn(r'([\u07EF])[\u07EF]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("long high tone:",nbr)

text,nbr=re.subn(r'([\u07F0])[\u07F0]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("long low tone:",nbr)

text,nbr=re.subn(r'([\u07F1])[\u07F1]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("long rising tone:",nbr)

text,nbr=re.subn(r'([\u07F2])[\u07F2]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("nasalisations:",nbr)

text,nbr=re.subn(r'([\u07F3])[\u07F3]+',r'\g<1>',text,0,re.U|re.MULTILINE)
print("double dot above:",nbr)

fileOUT.write(text)
fileOUT.close()
