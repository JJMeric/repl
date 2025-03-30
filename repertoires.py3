#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import sys
#from html.parser import HTMLParser
#parser = HTMLParser()
import html

normalizemetas=re.compile(r'<meta content="([^\"]*)" name="([^\"]*)" />',re.U|re.MULTILINE)

ambiguous=re.compile(r'\<span class\=\"w\".*lemma var.*\<\/span\>')
unknown=re.compile(r'<span class="w" stage="-1">[^<]+<span class="lemma">[^<]+</span>')

sentence=re.compile(r'\<span class\=\"sent\"\>([^<]*)\<')
title=re.compile(r'<meta name="text:title" content="([^\"]*)" />',re.U|re.MULTILINE)
author=re.compile(r'<meta name="author:name" content="([^\"]*)" />',re.U|re.MULTILINE)
wordssearch=re.compile(r'<meta name="_auto:words" content="([^\"]*)" />',re.U|re.MULTILINE)

parsedwords=re.compile(r'\<span class\=\"w\"',re.U)
extraittxt=re.compile(r'<body><p>([^£]*)</p></body>',re.U|re.MULTILINE)   #  ^< ne marche plus ?
searchwords=re.compile(r'([a-zɛɔɲŋA-ZƐƆƝŊ0-9\-́̀̌̂]+)',re.U|re.MULTILINE)
medianame=re.compile(r'^([a-zA-Z\-\_]+)[0-9]*[a-z]*\_',re.U)
medianumber=re.compile(r'^[a-zA-Z\-\_]+([0-9]*[a-z]*)\_',re.U)
date=re.compile(r'<meta name="text:date" content="([^\"]*)" />',re.U|re.MULTILINE)
datesource=re.compile(r'<meta name="source:date" content="([^\"]*)" />',re.U|re.MULTILINE)
textscript=re.compile(r'<meta name="text:script" content="([^\"]*)" />',re.U|re.MULTILINE)
sourceurl=re.compile(r'<meta name="source:url" content="([^\"]*)" />',re.U|re.MULTILINE)
sourcepagetotal=re.compile(r'<meta name="source:pagetotal" content="([^\"]*)" />',re.U|re.MULTILINE)
sourceyear=re.compile(r'<meta name="source:year" content="([^\"]*)" />',re.U|re.MULTILINE)



import os
# log=open("repertoire.log","w")


outf =  open ("repertoires.csv","w")
grandtotal=0
nbrep=0
nfiles=0

for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.
		# print path to all subdirectories first.
	#for subdirname in dirnames:
	#	print(os.path.join(dirname, subdirname))

	if dirname.endswith("/run"): continue  # ignore gparser run directory
	print(dirname)
	#break
	#if select=="" : break #sys.exit("no relevant file (.dis.html, .pars.html, .html) in current directory")
	# filenames=os.listdir(".")
	toutout=""
	toutwords=0
	toutmedianame=""
	toutmedianumber=""
	toutdate=""

	filenames=sorted(filenames) # peut-être pas nécessaire
	
	htmlfiles=[]
	disfiles=[]
	selectfiles=[]

	# 1st pass
	for filename in filenames :
		if not filename.endswith(".html"): continue
		if filename.endswith(".pars.html"): continue
		elif filename.endswith("repl.html"): continue
		if filename.endswith(".dis.html"):
			disfiles.append(filename[:-9])
		else:
			htmlfiles.append(filename[:-5])
	if len(disfiles)>0: 
		select=".dis.html"
		selectedfiles=disfiles
	elif len(htmlfiles)>0: 
		select=".html"
		selectedfiles=htmlfiles
	else: 
		sys.exit("!!! no .html and no .dis.html files")
		#print("!!! no .html and no .dis.html files")
	# missing disamb ?
	nerrfiles=0
	for fname in htmlfiles:
		if fname not in disfiles:
			print(fname,"missing in .dis.html files")
			nerrfiles+=1
	# disamb file not same name ?
	for fname in disfiles:
		if fname not in htmlfiles:
			print(fname,"missing in .html files")
			nerrfiles+=1
	if nerrfiles>0:
		sys.exit("!!! file names mismatch")
		#print("!!! file names mismatch")

	nfiles+=len(selectedfiles)

	# 2d pass
	for filename in selectedfiles :
		filename=filename+select
		print(os.path.join(dirname, filename))
		fileIN = open(os.path.join(dirname, filename), "r")
		if toutmedianame=="":
			mn=medianame.search(filename)
			if mn :
				toutmedianame=mn.group(1)
				ismedianumber=medianumber.search(filename)
				if ismedianumber!=[] :
					toutmedianumber=ismedianumber.group(1)
		"""
		#tout=fileIN.readlines()
		line = fileIN.readline()
		tout=""
		while line:
			tout=tout+line     # py2: .decode("utf-8")
			line = fileIN.readline()
		"""
		tout=fileIN.read()
		fileIN.close()

		tout=normalizemetas.sub(r'<meta name="\g<2>" content="\g<1>" />',tout)

		if toutdate=="":
			toutdatesearch=date.search(tout)
			if toutdatesearch :
				toutdate=toutdatesearch.group(1)
			else:
				toutdatesearch=datesource.search(tout)
				if toutdatesearch :
					toutdate=toutdatesearch.group(1)
				else:
					toutdate="23.09.2016"
		scriptok=False
		scriptsearch=textscript.search(tout)
		if scriptsearch:
			#print("scriptsearch.group(0):", scriptsearch.group(0))
			#print("scriptsearch.group(1):'"+scriptsearch.group(1)+"'")
			script=scriptsearch.group(1)
			if script!="": scriptok=True
		scriptpb=""
		if not scriptok:
			scriptpb="- ATTENTION PAS DE TEXT-SCRIPT"
			print(scriptpb)
		
		titlefound=title.search(tout)
		titl=""
		if titlefound:
			titl=titlefound.group(1)
		else: print("      no tile")
		#print title.search(tout).group(2)
		# log.write("\n"+filename+"\ntitle-1: "+titl+"\n")
		if titl!="":
			titl=re.sub(r"\"","",titl)
			titl=re.sub(r"\;",",",titl)  # dangereux pour un comma-separated-values
			titl=html.unescape(titl)
		
		auth=""
		authors=author.search(tout)
		if authors :
			auth=authors.group(1)
		if   select==".dis.html"  :
			word=wordssearch.search(tout).group(1)
			words=int(word)
		#elif select==".pars.html" :
		#	words=len(parsedwords.findall(tout))
		#	word=str(words)
		elif select==".html"      : 
			touttxt=tout
			touttxt=re.sub(r"&lt;c&gt;.*&lt;/c&gt;"," ",touttxt,0,re.U|re.MULTILINE)  # enlever les <c>...</c>
			touttxt=re.sub(r"&lt;n&gt;.*&lt;/n&gt;"," ",touttxt,0,re.U|re.MULTILINE)  # enlever les <n>...</n>
			touttxt=re.sub(r"&lt;h&gt;|&lt;/h&gt;"," ",touttxt,0,re.U|re.MULTILINE)  # enlever les <h> ou </h>
			touttxt=re.sub(r"&lt;ill&gt;|&lt;/ill&gt;"," ",touttxt,0,re.U|re.MULTILINE)  # enlever les <ill> ou </ill>
			touttxt=re.sub(r"&lt;ls&gt;|&lt;/ls&gt;"," ",touttxt,0,re.U|re.MULTILINE)  # enlever les <ls> ou </ls>
			touttxt=re.sub(r"&lt;br/&gt;"," ",touttxt,0,re.U|re.MULTILINE)  # enlever les <br/>
			touttxt=re.sub(r"<p>|</p>","",touttxt,0,re.U|re.MULTILINE) # enlever les marques de paragraphes
			touttxt=re.sub(r"^ *- ","",touttxt,0,re.U|re.MULTILINE)       # enlever les tirets
			touttxt=re.sub(r" - ","",touttxt,0,re.U|re.MULTILINE)       # enlever les tirets isolés
			touttxt=re.sub(r"<head>[^¤]*</head>","",touttxt,0,re.U|re.MULTILINE)       # enlever la section header
			touttxt=re.sub(r"</*body>|</*html>","",touttxt,0,re.U|re.MULTILINE) # enlever les tags bidy et html
			
			swords=searchwords.findall(touttxt)
			# rappel : searchwords=re.compile(ur'([a-zɛɔɲŋA-ZƐƆƝŊ0-9\-́̀̌̂]+)',re.U)
			if swords :
				words=len(swords)
				word=str(words)
				#for iword in swords :
				#	outf.write(": "+iword+"\n")
		url=""
		pagetotal=""
		year=""
		if select==".dis.html": 
			ambs=len(ambiguous.findall(tout))
			unkn=len(unknown.findall(tout))
			
			nambigus=""
			if ambs!=0 : 
				nambigus="ambigus: "+str(ambs)+" "
				print("      ambigus:",ambs)
			ninconnus=""
			if unkn!=0 : 
				ninconnus="inconnus: "+str(unkn)
				print("      inconnus:",unkn)
			toutout=toutout+titl+"; ; "+filename+"; ; "+word+"; "+auth+"; "+nambigus+ninconnus+scriptpb+"\n"
		else:
			diffauth=""
			nauth_fn=0
			fileauth=re.search(r"[0-9\-]*\_[0-9]*([a-z\_]*)\-",filename)
			if fileauth :
				authshort=fileauth.group(1)
				nauth_fn=1
				if "_" in authshort:
					spauthshort=authshort.split("_")
					nauth_fn=len(spauthshort)
			nauth_meta=0
			if auth!="":
				nauth_meta=1
				if "|" in auth:
					spauth=auth.split("|")
					nauth_meta=len(spauth)
			if nauth_fn!=nauth_meta :
				diffauth=" "+str(nauth_fn)+"/"+str(nauth_meta)+" ?"

			result=sourceurl.search(tout)
			if result: url=str(result.group(1))
			result=sourcepagetotal.search(tout)
			if result: pagetotal=str(result.group(1))
			result=sourceyear.search(tout)
			if result: year=str(result.group(1))


			toutout=toutout+titl+"; ; "+filename+"; ; "+word+"; "+auth+"; "+year+"; "+pagetotal+"; "+url+"; "+diffauth+scriptpb+"\n"
		
		toutwords=toutwords+words

	if toutout!="" :
		toutout=toutmedianame+" "+toutmedianumber+" "+toutdate+"; ; ; ; "+str(toutwords)+"; ;\n" +toutout+"\n\n"
		outf.write(toutout)
		grandtotal=grandtotal+toutwords
		nbrep=nbrep+1

outf.write("TOTAL for "+str(nbrep)+" issues ; ; ; ; "+str(grandtotal)+"; ;\n")
outf.close()
print("\n",nfiles," files")
print("TOTAL for "+str(nbrep)+" issue(s) "+str(grandtotal)+" words\n")