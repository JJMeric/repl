#!/usr/bin/python
# coding=UTF-8
import os
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# get file name
nargv=len(sys.argv)
if nargv==1 : 
  print "prlcheck.py needs -at least- one argument : file name (without extention .dis.html/ .dis.fra.txt/ .dis.bam-fra.prl"
  sys.exit
if nargv>1 : filename= str(sys.argv[1])
disname=filename+".dis.html"
franame=filename+".dis.fra.txt"
prlname=filename+".dis.bam-fra.prl"
chkname=filename+".dis.bam-fra.csv"

# open files
disfile=open(disname,"rb")
frafile=open(franame,"rb")
prlfile=open(prlname,"rb")
chkfile=open(chkname,"wb")

#read files
dislines=disfile.read()
fralines=frafile.read()
prllines=prlfile.read()
prllines,prllinesnb=re.subn(u"\r\n",u"\n",prllines)
prl=prllines.split("\n")

# print what's read
# print dislines
# print
# print fralines
# print

#build tables
#dislist=re.findall(r"<span class=\"sent\">([^<]+)﻿",dislines,re.U+re.MULTILINE)
dislist=re.findall(r'sent">([^<]+)',dislines,re.U+re.MULTILINE)
fratup=re.findall(r'">(((?!</s>).)+)',fralines,re.U+re.MULTILINE)

#walk through prl lines

# build csv
# print "dislist:"
# print dislist
# print "fralist:"
# print fralist



i=0
for distxt in dislist : 
	distxt=re.sub(r"\n"," @ ",distxt)
	dislist[i]=distxt
	i=i+1
	print distxt
# print "_______________________________"
fralist=[]
for fratxt in fratup : 
	# print fratxt[0]
	fratxt0=re.sub(r"\n"," @ ",fratxt[0])
	fralist.append(fratxt0)
#print "========================="
#print fralist[1]

for prlpair in prl :
	print '"'+prlpair+'"'
	if prlpair=="" : break
	lineout=re.sub(r"\t","   ",prlpair)+" ¤ "
	bamln,fraln=prlpair.split("\t")
	if ":" in bamln:
		bamlnbegin,bamlnend=bamln.split(":")
		bambegin=int(bamlnbegin)
		bamend=int(bamlnend)
		if ":" in fraln :
			fralnbegin,fralnend=fraln.split(":")
			frabegin=int(fralnbegin)
			fraend=int(fralnend)
			if (bamend-bambegin)!=(fraend-frabegin) : 
				sys.exit("sequence problem in "+prlpair+" number of lines differ")
			lineout=lineout+bamlnbegin+" ¤ "+dislist[bambegin]+" ¤ "+fralnbegin+" ¤ "+fralist[frabegin]
			print lineout
			chkfile.write(lineout+"\n")
			j=frabegin+1
			for i in xrange(bambegin+1,bamend+1):
				lineout=" ¤ "+str(i)+" ¤ "+dislist[i]+" ¤ "+str(j)+" ¤ "+fralist[j]
				j=j+1
				print lineout
				chkfile.write(lineout+"\n")
		elif "," in fraln :
			print "skip this 1B"  # should not occur ?
		else :	print "skip this 1C"  # should not occur ?

	elif ","  in bamln:
		# do something
		bamlnbegin,bamlnend=bamln.split(",")
		bambegin=int(bamlnbegin)
		bamend=int(bamlnend)
		lineout=lineout+bamlnbegin+" ¤ "+dislist[bambegin]+" ¤ "
		if ":" in fraln :
			print "skip this 2A"
		elif "," in fraln :
			print "skip this 2B"
		else :
			fra=int(fraln)
			fratxt=""
			if fra>=0 : fratxt=fralist[fra]
			lineout=lineout+fraln+" ¤ "+fratxt
			print lineout
			chkfile.write(lineout+"\n")
			for i in xrange(bambegin+1, bamend+1):
				lineout=" ¤ "+str(i)+" ¤ "+dislist[i]+" ¤  ¤"
				print lineout
				chkfile.write(lineout+"\n")

	else:
		bam=int(bamln)
		bamtxt=""
		if bam>=0 : bamtxt=dislist[bam]
		lineout=lineout+bamln+" ¤ "+bamtxt+" ¤ "
		if ":" in fraln :
			fralnbegin,fralnend=fraln.split(":")
			frabegin=int(fralnbegin)
			fraend=int(fralnend)
			lineout=lineout+fralnbegin+" ¤ "+fralist[frabegin]
			print lineout
			chkfile.write(lineout+"\n")
			for j in xrange(frabegin+1, fraend+1) :
				lineout=" ¤ ¤ ¤ "+str(j)+" ¤ "+fralist[j]
				print lineout
				chkfile.write(lineout+"\n")
		elif "," in fraln :
			fralnbegin,fralnend=fraln.split(",")
			frabegin=int(fralnbegin)
			fraend=int(fralnend)
			lineout=lineout+fralnbegin+" ¤ "+fralist[frabegin]
			print lineout
			chkfile.write(lineout+"\n")
			for j in xrange(frabegin+1, fraend+1) :
				lineout=" ¤ ¤ ¤ "+str(j)+" ¤ "+fralist[j]
				print lineout
				chkfile.write(lineout+"\n")
		else :
			fra=int(fraln)
			fratxt=""
			if fra>=0 : fratxt=fralist[fra]
			lineout=lineout+fraln+" ¤ "+fratxt
			print lineout
			chkfile.write(lineout+"\n")
#close files
disfile.close()
frafile.close()
prlfile.close()
chkfile.close()