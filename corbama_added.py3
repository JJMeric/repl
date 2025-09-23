#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import git
from git import Repo   # python3 -m pip install gitpython

normalizemetas=re.compile(r'<meta content="([^\"]*)" name="([^\"]*)" />',re.U|re.MULTILINE)
retitle=re.compile(r'<meta name="text:title" content="([^\"]*)" />',re.U|re.MULTILINE)
reauthor=re.compile(r'<meta name="author:name" content="([^\"]*)" />',re.U|re.MULTILINE)
rewords=re.compile(r'<meta name="_auto:words" content="([^\"]*)" />',re.U|re.MULTILINE)
reyear=re.compile(r'<meta name="source:year" content="([^\"]*)" />',re.U|re.MULTILINE)
readddate=re.compile(r'<meta name="corpus:adddate" content="([^\"]*)" />',re.U|re.MULTILINE)
global searchwords
searchwords=re.compile(r'([a-zɛɔɲŋA-ZƐƆƝŊ0-9\-́̀̌̂]+)',re.U|re.MULTILINE)


repo = Repo(".")
commits = list(repo.iter_commits("master", max_count=5000))  # no limits ???

# load a dictionnary of files with commit dates
filesdict={}
for commit in commits:
	gitnameslist=repo.git.show("--pretty=", "--name-only", commit.hexsha)
	gitnames=gitnameslist.split("\n")
	nt=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(commit.committed_date))
	for gitname in gitnames:
		if gitname in filesdict:
			if nt<filesdict[gitname]: filesdict[gitname]=nt
		else:
			filesdict[gitname]=nt

for afile,adate in filesdict.items():
	print(afile, adate)


def filesize(path):
    res = os.stat(path);
    return res.st_size

def nwords(path):
	global searchwords
	file = open(path, "r")
	touttxt=file.read()
	file.close()
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
	words="?"
	if swords :
		numwords=len(swords)
		if numwords==0:
			print("0? ",touttxt)
		words=str(numwords)
	return words

csvfile=open("corbama_added_scan.csv","w")
#csvfile.write('"Folder / File name"\t"created"\t"modified"\n')
csvfile.write("{path}\t{title}\t{earliestcommit}\t{c_stamp}\t{m_stamp}\t{addate}\t{author}\t{year}\t{words}\n")


for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: continue
	for subdirname in dirnames:
		print(os.path.join(dirname, subdirname))

	filenames=sorted(filenames) # peut-être pas nécessaire

	for filename in sorted(filenames) :
		if filename.endswith(".html"):
			path = os.path.join(dirname, filename)
			if ".git" in path: continue
	 
			ti_c = os.path.getctime(path)
			# res=os.stat(path)
			# ti_c = res.st_birthtime
			#   'os.stat_result' object has no attribute 'st_birthtime'
			ti_m = os.path.getmtime(path)
			 
			c_ti = time.ctime(ti_c)
			m_ti = time.ctime(ti_m)
			 
			# Using the timestamp string to create a
			# time object/structure
			c_obj = time.strptime(c_ti)
			m_obj = time.strptime(m_ti)
			 
			# Transforming the time object to a timestamp
			# of ISO 8601 format
			c_stamp = time.strftime("%Y-%m-%d %H:%M:%S", c_obj)
			m_stamp = time.strftime("%Y-%m-%d %H:%M:%S", m_obj)

			if m_stamp==c_stamp : m_stamp=""
			
			# path=./fakan/fakan2023_12/fakan20231209_donniya_22.html
			gitname=path[2:]
			print(gitname)

			earliestcommit=""
			if gitname in filesdict: earliestcommit=filesdict[gitname]
			

			if earliestcommit > "2023-02-22 07:00:00":  # date of the last corbama build

				fsize=filesize(path)
				nread=min(2500,fsize)
				file = open(path, "r")
				head=file.read(nread)
				file.close()

				head=normalizemetas.sub('<meta name="\g<2>" content="\g<1>" />',head)

				restitle=retitle.search(head)
				if restitle: title=restitle.group(1)
				else : title="?"

				resauthor=reauthor.search(head)
				if resauthor: author=resauthor.group(1)
				else : author="?"

				resyear=reyear.search(head)
				if resyear: year=resyear.group(1)
				else : year="?"

				reswords=rewords.search(head)
				if reswords: words=reswords.group(1)
				else :       words=nwords(path)
				if words=="" or words=="0" or words==None :
					print("words?",words)
					words=nwords(path)

				resadddate=readddate.search(head)
				if resadddate: adddate=resadddate.group(1)
				else : adddate="?"

				#print(f"{path} created {c_stamp} was last modified at {m_stamp}")
				#csvfile.write(f"{path}\t{c_stamp}\t{m_stamp}\n")
				csvfile.write(f"{path}\t{title}\t{earliestcommit}\t{c_stamp}\t{m_stamp}\t{adddate}\t{author}\t{year}\t{words}\n")


csvfile.close()
