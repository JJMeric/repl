#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from HTMLParser import HTMLParser
parser = HTMLParser()

ambiguous=re.compile(ur'\<span class\=\"w\".*lemma var.*\n\<\/span\>')
unknown=re.compile(ur'\<span class\=\"w\ stage\=\"\-1\"')
sentence=re.compile(ur'\<span class\=\"sent\"\>([^<]*)\<')
title=re.compile(ur'\<meta content\=\"([^\"]*)\" name\=\"text\:title\" \/\>',re.U)
author=re.compile(ur'\<meta content\=\"([^\"]*)\" name\=\"author\:name\" \/\>',re.U)
wordssearch=re.compile(ur'\<meta content\=\"([0-9]*)\" name\=\"\_auto\:words\" \/\>',re.U)
parsedwords=re.compile(ur'\<span class\=\"w\"',re.U)
extraittxt=re.compile(ur'<body><p>([^£]*)</p></body>',re.U)   #  ^< ne marche plus ?
searchwords=re.compile(ur'([a-zɛɔɲŋA-ZƐƆƝŊ\-́̀̌̂]+)',re.U)
medianame=re.compile(ur'^([a-zA-Z\-\_]+)[0-9]*\_',re.U)
medianumber=re.compile(ur'^[a-zA-Z\-\_]+([0-9]*)\_',re.U)
date=re.compile(ur'\<meta content\=\"[0-9]+\.([0-9\.]*)\" name\=\"text\:date\" \/\>',re.U)
datesource=re.compile(ur'\<meta content\=\"[0-9]+\.([0-9\.]*)\" name\=\"source\:date\" \/\>',re.U)

import os
# log=open("repertoire.log","w")


outf =  open ("repertoires.csv","w")
grandtotal=0
nbrep=0

for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.
		# print path to all subdirectories first.
	#for subdirname in dirnames:
	#	print(os.path.join(dirname, subdirname))

	#break
	#if select=="" : break #sys.exit("no relevant file (.dis.html, .pars.html, .html) in current directory")
	# filenames=os.listdir(".")
	toutout=u""
	toutwords=0
	toutmedianame=""
	toutmedianumber=""
	toutdate=""

	filenames=sorted(filenames) # peut-être pas nécessaire
	for filename in filenames :
		select=".html"
		if '.dis.html' in filename :
			select=".dis.html"
		elif '.pars.html' in filename :
			select=".pars.html"
		
		if select in filename :
			print os.path.join(dirname, filename)
			fileIN = open(os.path.join(dirname, filename), "r")
			if toutmedianame=="":
				toutmedianame=medianame.search(filename).group(1)
				ismedianumber=medianumber.search(filename)
				if ismedianumber!=[] :
					toutmedianumber=ismedianumber.group(1)
			#tout=fileIN.readlines()
			line = fileIN.readline()
			tout=u""
			while line:
				tout=tout+line.decode("utf-8")
				line = fileIN.readline()
			fileIN.close()

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

			
			titl=title.search(tout).group(1)
			# log.write("\n"+filename+"\ntitle-1: "+titl+"\n")
			titl=re.sub(ur"\"","",titl)
			# log.write("title-2: "+titl+"\n")
			titl=re.sub(ur"\;",",",titl)  # dangereux pour un comma-separated-values
			# log.write("title-3: "+titl+"\n")
			titl=parser.unescape(titl)
			# log.write("title-4: "+titl+"\n")
			auth=""
			authors=author.search(tout)
			if authors :
				auth=authors.group(1)
			if   select==".dis.html"  :
				word=wordssearch.search(tout).group(1)
				words=int(word)
			elif select==".pars.html" :
				words=len(parsedwords.findall(tout))
				word=str(words)
			elif select==".html"      : 
				touttxt=extraittxt.search(tout).group(1)

				touttxt=re.sub(r"&lt;c&gt;.*&lt;/c&gt;"," ",touttxt,re.U)  # enlever les <c>...</c>
				touttxt=re.sub(r"&lt;n&gt;.*&lt;/n&gt;"," ",touttxt,re.U)  # enlever les <n>...</n>
				touttxt=re.sub(r"&lt;h&gt;|&lt;/h&gt;"," ",touttxt,re.U)  # enlever les <h> ou </h>
				touttxt=re.sub(r"&lt;ill&gt;|&lt;/ill&gt;"," ",touttxt,re.U)  # enlever les <ill> ou </ill>
				touttxt=re.sub(r"&lt;ls&gt;|&lt;/ls&gt;"," ",touttxt,re.U)  # enlever les <ls> ou </ls>
				touttxt=re.sub(r"&lt;br/&gt;"," ",touttxt,re.U)  # enlever les <br/>
			
				swords=searchwords.findall(touttxt)
				if swords :
					words=len(swords)
					word=str(words)
					#for iword in swords :
					#	outf.write(": "+iword+"\n")

			if select!=".html": 
				ambs=len(ambiguous.findall(tout))
				unkn=len(unknown.findall(tout))
				nambigus=u""
				if ambs!=0 : nambigus="ambigus: "+str(ambs)+" "
				ninconnus=u""
				if unkn!=0 : ninconnus="inconnus: "+str(unkn)
				toutout=toutout+titl+"; ; "+filename+"; ; "+word+"; "+auth+"; "+nambigus+ninconnus+"\n"
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

				toutout=toutout+titl+"; ; "+filename+"; ; "+word+"; "+auth+"; "+diffauth+"\n"
			toutwords=toutwords+words

	if toutout!="" :
		toutout=toutmedianame+" "+toutmedianumber+" "+toutdate+"; ; ; ; "+str(toutwords)+"; ;\n" +toutout+"\n\n"
		outf.write(toutout)
		grandtotal=grandtotal+toutwords
		nbrep=nbrep+1

outf.write("TOTAL for "+str(nbrep)+" issues ; ; ; ; "+str(grandtotal)+"; ;\n")
outf.close()