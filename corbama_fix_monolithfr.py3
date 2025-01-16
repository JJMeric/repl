#!/usr/bin/env python
# -*- coding: utf-8 -*-


# to fix  non monolith/diacritics in gloss (dis files only)

import os
import re
import sys


subgloss=re.compile(r'<sub class="gloss">([^\<]+[\u0301\u0300\u0302\u030c\u0327\u0308][^\<]+)</sub>',re.U|re.MULTILINE)  
# note: unicode value of the 4 bamana diacritics + Combining Cedilla (ç) + Combining Diaeresis (ï)

# splitted=re.compile(r"́|̀|̌|̂|̧|̈")
splitted=re.compile(r"\u0301|\u0300|\u0302|\u030c|\u0327|\u0308")
mapping = { 'à':'à', 'â':'â', 'é':'é', 'ê':'ê', 'è':'è', 'ë':'ë', 'î':'î', 'ï':'ï', 'ô':'ô', 'û':'û', 'ù':'ù', 'ç':'ç', 'À':'À', 'Ç':'Ç', 'Ê':'Ê', 'Ô':'Ô'}
# mapping checked 12/01/2024 : had diacritics in values!!!
for k, v in mapping.items():
	if splitted.search(v): sys.exit("mapping has invalid value in : '"+k+"':'"+v+"' \nSTOPPED")

def tomonolith(m) :
	mystring=m.groups()[0]
	if splitted.search(mystring) :  # not necessary in principle
		for k, v in mapping.items():
			if k in mystring:
				mystring = mystring.replace(k, v)
	return '<sub class="gloss">'+mystring+'</sub>'

nfmod=0 # number of modified files

for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.

	filenames=sorted(filenames) # peut-être pas nécessaire, mais plus lisible

	for filename in sorted(filenames) :
		if not filename.endswith(".dis.html"):
			continue

		path = os.path.join(dirname, filename)
		if ".git" in path: 
			continue

		file = open(path, "r")
		tout=file.read()
		file.close()

		tout,n=re.subn(r'<sub class="gloss">([^\<]+[\u0301\u0300\u0302\u030c\u0327\u0308][^\<]+)</sub>',\
			tomonolith,tout,0,re.U|re.MULTILINE)
		#tout,n=re.subn(subgloss,tomonolith,tout,0,re.U|re.MULTILINE) # raises: ValueError: cannot process flags argument with a compiled pattern

		if n>0:
			#tests: file = open(path+"1", "w")
			file = open(path, "w")
			file.write(tout)
			file.close()
			print("modified {0} - \033[3m{1} glosses changed\033[0m".format(filename,n))
			nfmod+=1
				
print(nfmod,"files modified")