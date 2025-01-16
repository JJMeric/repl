#!/usr/bin/env python
# -*- coding: utf-8 -*-


# to fix  non monolith/diacritics in gloss (dis files only)

import os
import re
import sys

c_reversed	=re.compile(r'<meta content="([^\"]+)" name="([^\"]+)" />',re.U|re.MULTILINE)
c_jjm		=re.compile(r'<meta name="corpus:operator" content="Jean Jacques Meric" />',re.U|re.MULTILINE)  
c_adddate	=re.compile(r'<meta name="corpus:adddate" content="([^\"]+)" />',re.U|re.MULTILINE)  
c_textdate	=re.compile(r'<meta name="text:date" content="([^\"]+)" />',re.U|re.MULTILINE)  
c_sourcedate=re.compile(r'<meta name="source:date" content="([^\"]+)" />',re.U|re.MULTILINE)
c_mmjjaaaa	=re.compile(r'([0-9]{2})/([0-9]{2})/([0-9]{4})')
c_mmjjaa	=re.compile(r'([0-9]{2})/([0-9]{2})/([0-9]{2})')
c_jjmmaaaa	=re.compile(r'([0-9]{2})\.([0-9]{2})\.([0-9]{4})')

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

		n=0

		tout,nc=re.subn(r'<meta content="([^\"]+)" name="([^\"]+)" />','<meta name="\g<2>" content="\g<1>" />',tout,0,re.U|re.MULTILINE)
		#was: tout,nc=re.subn(c_reversed,'<meta name="\g<2>" content="\g<1>" />',tout,0,re.U|re.MULTILINE)
		if nc>0: n=n+nc

		tout,nc=re.subn(r'<meta name="corpus:operator" content="Jean Jacques Meric" />','<meta name="corpus:operator" content="Jean-Jacques Méric" />',tout,0,re.U|re.MULTILINE)
		if nc>0: n=n+nc

		s_adddate=re.search(c_adddate,tout)
		# print("s_adddate:",s_adddate)
		if s_adddate:
			t_adddate=s_adddate.group(1)
			t_adddatem=t_adddate
			# print("   t_adddate:",t_adddate)
			if "/" in t_adddate:
				s_mmjjaaaa=re.search(c_mmjjaaaa,t_adddate)
				# print("      s_mmjjaaaa:",s_mmjjaaaa)
				if s_mmjjaaaa:
					mm=s_mmjjaaaa.group(1)
					jj=s_mmjjaaaa.group(2)
					aaaa=s_mmjjaaaa.group(3)
					t_adddatem=jj+'.'+mm+'.'+aaaa
					tout,nc=re.subn(r'<meta name="corpus:adddate" content="'+t_adddate+r'" />',\
									'<meta name="corpus:adddate" content="'+t_adddatem+'" />',tout,0,re.U|re.MULTILINE)
					if nc>0: n=n+nc
				else:
					s_mmjjaa=re.search(c_mmjjaa,t_adddate)
					# print("      s_mmjjaa:",s_mmjjaa)
					if s_mmjjaa:
						mm=s_mmjjaa.group(1)
						jj=s_mmjjaa.group(2)
						aa=s_mmjjaa.group(3)
						n_aa=int(aa)+2000
						aaaa=str(n_aa)
						t_adddatem=jj+'.'+mm+'.'+aaaa
						# print("      jj,mm,aaaa",jj,mm,aaaa)
						tout,nc=re.subn(r'<meta name="corpus:adddate" content="'+t_adddate+r'" />',\
										'<meta name="corpus:adddate" content="'+t_adddatem+'" />',tout,0,re.U|re.MULTILINE)
						if nc>0: n=n+nc
					else:
						s_jjmmaaaa=re.search(c_jjmmaaaa,t_adddate)
						if s_jjmmaaaa:
							jj=s_mmjjaaaa.group(1)
							mm=s_mmjjaaaa.group(2)
							aaaa=s_mmjjaaaa.group(3)
							n_aa=int(aaaa)
							if n_aa>2000:
								n_aa=n_aa+2000
								aaaa=str(n_aa)
							t_adddatem=jj+'.'+mm+'.'+aaaa
							tout,nc=re.subn(r'<meta name="corpus:adddate" content="'+t_adddate+r'" />',\
											'<meta name="corpus:adddate" content="'+t_adddatem+'" />',tout,0,re.U|re.MULTILINE)
							if nc>0: n=n+nc
						else:
							print("\033[1mValeur non attendue de t_adddate:\033[0m",t_adddate)

		t_textdate="\033[1m?\033[0m"
		t_sourcedate="\033[1m?\033[0m"

		s_textdate=re.search(c_textdate,tout)
		if s_textdate:
			t_textdate=s_textdate.group(1)
			if t_textdate != "  .  .    ":
				t_textdate1=""
				if "1 " in t_textdate:
					t_textdate1=t_textdate.replace("1 ","01")
				if "  ." in t_textdate:
					t_textdate1=t_textdate.replace("  .","01.")
				if t_textdate1!="":
					tout,nc=re.subn(r'<meta name="text:date" content="'+t_textdate+r'" />',\
									'<meta name="text:date" content="'+t_textdate1+'" />',tout,0,re.U|re.MULTILINE)
					if nc>0: n=n+nc
					t_textdate=t_textdate1

		s_sourcedate=re.search(c_sourcedate,tout)
		if s_sourcedate:
			t_sourcedate=s_sourcedate.group(1)
			if t_sourcedate != "  .  .    ":
				t_sourcedate1=""
				if "1 " in t_sourcedate:
					t_sourcedate1=t_sourcedate.replace("1 ","01")
				if "  ." in t_sourcedate:
					t_sourcedate1=t_sourcedate.replace("  .","01.")
				if t_sourcedate1!="":
					tout,nc=re.subn(r'<meta name="source:date" content="'+t_sourcedate+'" />',\
									'<meta name="source:date" content="'+t_sourcedate1+'" />',tout,0,re.U|re.MULTILINE)
					if nc>0: n=n+nc
					t_sourcedate=t_sourcedate1
					
		if t_textdate != "  .  .    ":
			if t_sourcedate=="  .  .    ":
					t_sourcedate=t_textdate
					tout,nc=re.subn(r'<meta name="source:date" content="  .  .    " />',\
									'<meta name="source:date" content="'+t_sourcedate+'" />',tout,0,re.U|re.MULTILINE)
					if nc>0: n=n+nc						
		elif t_sourcedate != "  .  .    ":
			t_textdate=t_sourcedate
			tout,nc=re.subn(r'<meta name="text:date" content="  .  .    " />',\
									'<meta name="text:date" content="'+t_textdate+'" />',tout,0,re.U|re.MULTILINE)
			if nc>0: n=n+nc

		if n>0:
			# tests : file = open(path+"1", "w")
			file = open(path, "w")
			file.write(tout)
			file.close()
			print("modified {0} - \033[3m{1} changes\033[0m dates: add {2} source {3} text {4}".format(filename,n,t_adddatem,t_sourcedate,t_textdate))
			nfmod+=1

print(nfmod,"files modified")	
