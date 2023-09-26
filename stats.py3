#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import sys
#from html.parser import HTMLParser
#parser = HTMLParser()
import html
# import htmlentitydefs
import urllib.request


ambiguous=re.compile(r'\<span class\=\"w\".*lemma var.*\n\<\/span\>')
unknown=re.compile(r'<span class="w" stage="-1">[^<]+<span class="lemma">[^<]+</span>')
sentence=re.compile(r'\<span class\=\"sent\"\>([^<]*)\<')
# title=re.compile(ur'\<meta content\=\"([^\"]*)\" name\=\"text\:title\" \/\>|\<meta name\=\"text\:title\" content\=\"([^\"]*)\" \/\>',re.U)  # as of daba 0.9.0 dec 2020 meta format order changed!
title=re.compile(r'(?:\<meta content\=\"|\<meta name\=\"text\:title\" content\=\")([^\"]*)(?:\" name\=\"text\:title\" \/\>|\" \/\>)',re.U)
author=re.compile(r'(?:\<meta content\=\"|\<meta name\=\"author\:name\" content\=\")([^\"]*)(?:\" name\=\"author\:name\" \/\>|\" \/\>)',re.U)

metawords=re.compile(r'(?:\<meta content\=\"|\<meta name\=\"\_auto\:words\" content\=\")([0-9]*)(?:\" name\=\"\_auto\:words\" \/\>|\" \/\>)',re.U)
metasentences=re.compile(r'(?:\<meta content\=\"|\<meta name\=\"\_auto\:sentences\" content\=\")([0-9]*)(?:\" name\=\"\_auto\:sentences\" \/\>|\" \/\>)',re.U)

parsedwords=re.compile(r'\<span class\=\"w\"',re.U)
extraittxt=re.compile(r'<body><p>([^£]*)</p></body>',re.U)   #  ^< ne marche plus ?
searchwords=re.compile(r'([a-zɛɔɲŋA-ZƐƆƝŊ0-9\-́̀̌̂]+)',re.U)
medianame=re.compile(r'^([a-zA-Z\-\_]+)[0-9]*\_',re.U)
medianumber=re.compile(r'^[a-zA-Z\-\_]+([0-9]*)\_',re.U)
#date=re.compile(ur'\<meta content\=\"[0-9]+\.([0-9\.]*)\" name\=\"text\:date\" \/\>|\<meta name\=\"text\:date\" content\=\"[0-9]+\.([0-9\.]*)\" \/\>',re.U)
date=re.compile(r'(?:\<meta content\=\"[0-9]+\.|\<meta name\=\"text\:date\" content\=\"[0-9]+\.)([0-9\.]*)(?:\" name\=\"text\:date\" \/\>|\" \/\>)',re.U)

#datesource=re.compile(ur'\<meta content\=\"[0-9]+\.([0-9\.]*)\" name\=\"source\:date\" \/\>|\<meta name\=\"source\:date\" content\=\"[0-9]+\.([0-9\.]*)\" \/\>',re.U)
datesource=re.compile(r'(?:\<meta content\=\"[0-9]+\.|\<meta name\=\"source\:date\" content\=\"[0-9]+\.)([0-9\.]*)(?:\" name\=\"source\:date\" \/\>|\" \/\>)',re.U)

bamtags=re.compile(r'<s n="[0-9]+">',re.U|re.MULTILINE)
fratags=re.compile(r'<s n="[0-9]+">',re.U|re.MULTILINE)
fragroups=re.compile(r'[a-zA-ZɛɔɲŋéèàçùâêîôûœäëïöüÉÈÀÇÙÂÊÎÔÛŒÄËÏÖÜƐƆƝŊ̀́̂̌\-0-9]+',re.U|re.MULTILINE)
sntags=re.compile(r'<s n="[0-9]+">|</s>',re.U|re.MULTILINE)
comments=re.compile(r'&lt;c&gt;[^¤/]*&lt;/c&gt;|<c>[^>\n]+</c>',re.U|re.MULTILINE)
bmtags=re.compile(r'&lt;[^\&\n]+&gt;|<[^>\n]+>',re.U|re.MULTILINE)
isolatedhyphen=re.compile(r'[-_–\s\.,;:?!\[\)]*-[-_–\s\.,;:?!\[\)]|[-_–\s\.,;:?!\[\)]-[-_–\s\.,;:?!\[\)]*',re.U|re.MULTILINE)

import os
# log=open("repertoire.log","w")


nfiles=0
tsize=0
tsent=0
twords=0
tfrasentn=0
tfrawords=0
tfrasentn2=0
tfrawords2=0
nwarn=0
npub=0

def frastat(frafilename) :
	fraIN=open(os.path.join(dirname, frafilename),'r')
	fratxt=fraIN.read()
	fraIN.close()
	frasent=fratags.findall(fratxt)
	frasentn=len(frasent)
	# words is more tricky
	# eliminate sn tags
	fratxt=sntags.sub('',fratxt,0)
	# eliminate comments
	fratxt=comments.sub('',fratxt,0)
	# eliminate possible tags imitated from bm tags
	fratxt=bmtags.sub('',fratxt,0)
	# eliminate isolated, trailing, or leading hyphens
	fratxt=isolatedhyphen.sub(' ',fratxt,0)
	# count valid groups of alphabetical letters (including internal - hyphen like "celui-ci" )
	#     this is meant to eliminate punctuations, tabs, new lines, hard spaces
	fraword=fragroups.findall(fratxt)
	frawords=len(fraword)
	"""
	test=open(frafilename+"-words-fragroups.txt","w")
	for x in fraword: test.write(x+"\n")
	test.close()

	test=open(frafilename+"-stats-text.txt","w")
	test.write(fratxt)
	test.close()

	# ERROR was in flags passed: fraword=fragroups.findall(fratxt,re.U|re.MULTILINE)
	# those flags duplicate those in compile and have another side effect which I do not understand : 7 words missing, 1 extra word on 18.300 words
	>>> fraword=fragroups.findall(text,re.U|re.MULTILINE)
	>>> len(fraword)
	18295
	>>> fraword=fragroups.findall(text)
	>>> len(fraword)
	18301
	>>> 


	"""

	return frasentn,frawords

csvfile=open("/home/corpus-team/corpus_parallele/corbama_parallel_scan.csv","w")
csvfile.write('"Folder / File name","T","online","bam_s","bam_w","fra_s","fra_w","fra2_s","fra2_w","warnings"\n')

# open corbamafara list of files in parallel corpus
# http://cormande.huma-num.fr/corbama/run.cgi/wordlist?corpname=corbamafara;wlmaxitems=1000;wlattr=doc.id;wlminfreq=1;include_nonwords=1;wlsort=f;wlnums=docf

# old Sketch Engine url = 'http://cormande.huma-num.fr/corbama/run.cgi/wordlist?corpname=corbamafara;wlmaxitems=5000;wlattr=doc.id;wlminfreq=1;include_nonwords=1;wlsort=f;wlnums=docf&async=0'
# new Sketch Engine:
# returns empty jQuery page url = "http://cormande.huma-num.fr/corbama/#text-type-analysis?corpname=corbamafara&tab=basic&filter=containing&wlattr=doc.id&wlminfreq=1&include_nonwords=1&itemsPerPage=1000&showresults=1&cols=%5B%22frq%22%5D&wlsort=frq"
url = "http://cormande.huma-num.fr/bonito/run.cgi/attr_vals?corpname=corbamafara&avattr=doc.id&avmaxitems=5000"
response = urllib.request.urlopen(url)
the_page = response.read().decode("utf-8")


for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.
	for subdirname in dirnames:
		print(os.path.join(dirname, subdirname))

	filenames=sorted(filenames) # peut-être pas nécessaire



	#for filename in sorted(os.listdir()) :
	for filename in sorted(filenames) :
		warning=""
		sentn=0
		frasentn=0
		frasentn2=0
		nwords=0
		frawords=0
		frawords2=0
		bamsentn=0
		ftype=0
		nsent=0
		pub=""

		if filename.endswith(".dis.html"): 

			filesize=os.path.getsize(os.path.join(dirname, filename))
			fsizek=int(filesize/1024)

			fileIN = open(os.path.join(dirname, filename), "r")
			htmlfile=fileIN.read()
			fileIN.close()

			metasent=metasentences.search(htmlfile)
			if metasent :
				nsent=int(metasent.group(1))
			else:
				nsent=0

			metaw=metawords.search(htmlfile)
			if metaw :
				nwords=int(metaw.group(1))
			else:
				nwords=0

			# check if this is coherent with file content (sentence count not updated live by sentence split/joins)
			sent=sentence.findall(htmlfile,re.U|re.MULTILINE)
			sentn=len(sent)
			pw=parsedwords.findall(htmlfile,re.U|re.MULTILINE)
			pwords=len(pw)

			if nsent!=sentn or nwords!=pwords:
				print("check totals:",filename, fsizek,"K, meta : ", nsent, "sentences, ",nwords,"words, = total tags sent,w:",sentn,", ",pwords)
				warning=warning+"! check totals:"+filename+str(fsizek)+" K, meta : "+str(nsent)+" sentences, "+str(nwords)+" words, = total tags sent,w:"+str(sentn)+", "+str(pwords)
				nwarn+=1
			else:
				print(filename, fsizek,"K, ", nsent, "sentences, ",nwords,"words")

			filerootname=filename[:filename.find(".dis.html")]

			# check if sentence # coherent with that in dis.bam.txt
			bamfilename=filerootname+".dis.bam.txt"
			if os.path.exists(os.path.join(dirname, bamfilename)):
				bamIN=open(os.path.join(dirname, bamfilename),'r')
				bamtxt=bamIN.read()
				bamIN.close()
				bamsent=bamtags.findall(bamtxt, re.U|re.MULTILINE)
				bamsentn=len(bamsent)
				if bamsent!=sentn:
					#print ("check : sentences in bam.txt:",bamsentn," differ from sentences in dis.html: " ,sentn, " ???")
					warning=warning+"! check : sentences in bam.txt:"+str(bamsentn)+" differ from sentences in dis.html: "+str(sentn)+" ???"
					nwarn+=1

			frafilename=filerootname+".dis.fra.txt"
			if os.path.exists(os.path.join(dirname, frafilename)):
				frasentn,frawords=frastat(frafilename)
				print("     ",frafilename,":",frasentn,"sentences, ", frawords,"words")

				prlfilename=filerootname+".dis.bam-fra.prl"
				if not os.path.exists(os.path.join(dirname, prlfilename)):
					#print("check : missing prl file ",prlfilename)
					warning=warning+"! check : missing prl file "+prlfilename+" "
					nwarn+=1

			frafilename=filerootname+".dis.fra2.txt"
			if os.path.exists(os.path.join(dirname, frafilename)):
				frasentn2,frawords2=frastat(frafilename)
				print("     ",frafilename,":",frasentn2,"sentences, ", frawords2,"words")
				if frasentn2!=sentn:
					#print("check : not the same number of sentences in dis.html:",sentn," and in fra2.txt:",frasentn2)
					warning=warning+"! check : not the same number of sentences in dis.html:"+str(sentn)+" and in fra2.txt:"+str(frasentn2)+" "
					nwarn+=1

			ods3filename=filerootname+".bam-fra3.ods"
			if os.path.exists(os.path.join(dirname,ods3filename)):
				frafilename=filerootname+".dis.fra2.txt"
				if not os.path.exists(os.path.join(dirname,frafilename)):
					print("      ",ods3filename," exists but no ",frafilename," ?")
					warning=warning+"! check : "+ods3filename+" but missing "+frafilename+"? "
					nwarn+=1

			if nsent>0: 
				if frasentn>0 and frasentn2==0:
					ftype=2
				elif frasentn>0 and frasentn2>0:
					ftype=3
				elif frasentn==0 and frasentn2>0:
					ftype=4

				if frasentn>0 or frasentn2>0: # check if published
					if filename in the_page:
						pub="pub"
						npub+=1



		elif filename.endswith(".html"):   # undisambiguated files
			filerootname=filename[:filename.find(".html")]
			filesize=os.path.getsize(os.path.join(dirname, filename))
			fsizek=int(filesize/1024)

			bamfilename=filerootname+".bam.txt"
			if os.path.exists(os.path.join(dirname, bamfilename)):
				nsent,nwords=frastat(bamfilename)

			frafilename=filerootname+".fra.txt"
			if os.path.exists(os.path.join(dirname, frafilename)):
				frasentn,frawords=frastat(frafilename)
				prlfilename=filerootname+".bam-fra.prl"
				if not os.path.exists(os.path.join(dirname, prlfilename)):
					#print("check : missing prl file ",prlfilename)
					warning=warning+"! check : missing prl file "+prlfilename+" "
					nwarn+=1

			if nsent>0 : 
				ftype=1

				# check if published
				filetocheck=filerootname+".pars.html"
				if filetocheck in the_page:
					pub="pub"
					npub+=1
				

		elif filename.endswith(".bam.txt"):   # undisambiguated files
			filerootname=filename[:filename.find(".bam.txt")]
			if not os.path.exists(os.path.join(dirname, filerootname+".dis.html")) and not os.path.exists(os.path.join(dirname, filerootname+".html")): # do not redo above work
				filesize=os.path.getsize(os.path.join(dirname, filename))
				fsizek=int(filesize/1024)

				nsent,nwords=frastat(filename)

				frafilename=filerootname+".fra.txt"
				if os.path.exists(os.path.join(dirname, frafilename)):
					frasentn,frawords=frastat(frafilename)
					prlfilename=filerootname+".bam-fra.prl"
					if not os.path.exists(os.path.join(dirname, prlfilename)):
						#print("check : missing prl file ",prlfilename)
						warning=warning+"! check : missing prl file "+prlfilename+" "
						nwarn+=1

				if nsent>0 : 
					ftype=1

					# check if published
					filetocheck=filerootname+".pars.html"
					if filetocheck in the_page:
						pub="pub"
						npub+=1

		if ftype!=0 :

			# print(dirname+"/"+filerootname,",",ftype,",",nsent,",",nwords,",",frasentn,",",frawords,",",frasentn2,",",frawords2,'"'+warning+'"')
			csvfile.write(dirname+"/"+filerootname+","+str(ftype)+","+pub+","+str(nsent)+","+str(nwords)+","+str(frasentn)+","+str(frawords)+","+str(frasentn2)+","+str(frawords2)+', "'+warning+'"\n')
			
			nfiles+=1
			tsize+=fsizek
			tsent+=nsent
			twords+=nwords
			tfrasentn+=frasentn
			tfrawords+=frawords
			tfrasentn2+=frasentn2
			tfrawords2+=frawords2

		# end loop all filenames


print(nfiles,"files, ",tsize,"K, ", tsent, "bam sentences, ",twords,"bam words")
print("     FRA :",tfrasentn,"sentences, ",tfrawords,"words")
print("     FRA2 :",tfrasentn2,"sentences, ",tfrawords2,"words")
csvfile.write('\n"Totals for '+str(nfiles)+' files ('+str(tsize)+' k)",,'+str(npub)+","+str(tsent)+","+str(twords)+","+str(tfrasentn)+","+str(tfrawords)+","+str(tfrasentn2)+","+str(tfrawords2)+", "+str(nwarn)+" warnings\n")
csvfile.close()
