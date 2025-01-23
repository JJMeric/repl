#!/usr/bin/env python
# -*- coding: utf-8 -*-


# to fix  non monolith/diacritics in gloss (dis files only)

import os
import re
import sys

c_reversed	=re.compile(r'<meta content="([^\"]+)" name="([^\"]+)" />',re.U|re.MULTILINE)
c_jjm		=re.compile(r'<meta name="corpus:operator" content="Jean Jacques Meric" />',re.U|re.MULTILINE)  
c_adddate	=re.compile(r'<meta name="corpus:adddate" content="([^\"]+)" />',re.U|re.MULTILINE)  
c_texscript	=re.compile(r'<meta name="text:date" content="([^\"]+)" />',re.U|re.MULTILINE)  
c_textscript=re.compile(r'<meta name="text:script" content="([^\"]+)" />',re.U|re.MULTILINE)  
c_sourcedate=re.compile(r'<meta name="source:date" content="([^\"]+)" />',re.U|re.MULTILINE)
c_mmjjaaaa	=re.compile(r'([0-9]{2})/([0-9]{2})/([0-9]{4})')
c_mmjjaa	=re.compile(r'([0-9]{2})/([0-9]{2})/([0-9]{2})')
c_jjmmaaaa	=re.compile(r'([0-9]{2})\.([0-9]{2})\.([0-9]{4})')

nfmod=0 # number of modified files

for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.

	filenames=sorted(filenames) # peut-être pas nécessaire, mais plus lisible

	for filename in sorted(filenames) :
		if not filename.endswith(".html"):
			continue
		elif filename.endswith(".dis.html"):
			continue

		path = os.path.join(dirname, filename)
		if ".git" in path: 
			continue

		file = open(path, "r",encoding='utf-8')
		tout=file.read()
		file.close()

		n=0

		tout,nc=re.subn(r'<meta content="([^\"]+)" name="([^\"]+)" />','<meta name="\g<2>" content="\g<1>" />',tout,0,re.U|re.MULTILINE)
		#was: tout,nc=re.subn(c_reversed,'<meta name="\g<2>" content="\g<1>" />',tout,0,re.U|re.MULTILINE)
		if nc>0: n=n+nc

		s_textscript=re.search(c_textscript,tout)
		if s_textscript:
			t_textscript=s_textscript.group(1)
		else:
			print("no textsscript? in",path)

		if t_textscript=="Ancien orthographe malien" and not filename.endswith(".old.html"):
			print("change filename to.old.html OR change textscript :",path)


		