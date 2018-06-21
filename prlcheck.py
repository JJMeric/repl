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
dislist=re.findall(ur'sent">([^<]*)',dislines,re.U+re.MULTILINE)
fratup=re.findall(ur'[0-9"]>(((?!</s>)[^¤])*)',fralines,re.U+re.MULTILINE)

#walk through prl lines

# build csv
# print "dislist:"
# print dislist
# print "fralist:"
# print fralist



i=0
for distxt in dislist : 
	distxt=re.sub(ur"\n",u" ␤ ",distxt,re.U+re.MULTILINE)
	dislist[i]=distxt
	i=i+1
	# print distxt
# print "_______________________________"
fralist=[]
for fratxt in fratup : 
	# print fratxt[0]
	fratxt0=re.sub(ur"\n",u" ␤ ",fratxt[0],re.U+re.MULTILINE)
	fralist.append(fratxt0)
#print "========================="
#print fralist[1]

ldislist=len(dislist)
lfralist=len(fralist)
print "dis: "+str(ldislist)+" sentences, fra: "+str(lfralist)+" sentences"
for prlpair in prl :
	# print '"'+prlpair+'"'
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
			# print lineout
			chkfile.write(lineout+"\n")
			j=frabegin+1
			for i in xrange(bambegin+1,bamend+1):
				fraout=fralist[j].strip()
				if fraout=="": 
					fraout="(void)"
					print "problem at prl "+prlpair+" : fra line empty :"+str(j)
				lineout=" ¤ "+str(i)+" ¤ "+dislist[i]+" ¤ "+str(j)+" ¤ "+fraout
				j=j+1
				# print lineout
				chkfile.write(lineout+"\n")
		elif "," in fraln :
			print prlpair+" : skip this 1B"  # should not occur ?
		else :	print prlpair+" : skip this 1C"  # should not occur ?

	elif ","  in bamln:
		# do something
		bamlnbegin,bamlnend=bamln.split(",")
		bambegin=int(bamlnbegin)
		bamend=int(bamlnend)
		lineout=lineout+bamlnbegin+" ¤ "+dislist[bambegin]+" ¤ "
		if ":" in fraln :
			print prlpair+" : skip this 2A"
		elif "," in fraln :
			print prlpair+" : skip this 2B"
		else :
			fra=int(fraln)
			fratxt=""
			if fra>=0 : fratxt=fralist[fra].strip()
			if fratxt=="": 
				fratxt="(void)"
				print "problem at prl "+prlpair+" : fra line empty :"+fraln
			lineout=lineout+fraln+" ¤ "+fratxt
			# print lineout
			chkfile.write(lineout+"\n")
			for i in xrange(bambegin+1, bamend+1):
				lineout=" ¤ "+str(i)+" ¤ "+dislist[i]+" ¤  ¤ ↆ"
				# print lineout
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
			# print lineout
			chkfile.write(lineout+"\n")
			for j in xrange(frabegin+1, fraend+1) :
				fraout=fralist[j].strip()
				if fraout=="":
					fraout="(void)"
					print "problem at prl "+prlpair+" : fra line empty :"+str(j)
				lineout=" ¤ ¤ ¤ "+str(j)+" ¤ "+fraout
				# print lineout
				chkfile.write(lineout+"\n")
		elif "," in fraln :
			fralnbegin,fralnend=fraln.split(",")
			frabegin=int(fralnbegin)
			fraend=int(fralnend)
			lineout=lineout+fralnbegin+" ¤ "+fralist[frabegin]
			# print lineout
			chkfile.write(lineout+"\n")
			for j in xrange(frabegin+1, fraend+1) :
				fraout=fralist[j].strip()
				if fraout=="":
					fraout="(void)"
					print "problem at prl "+prlpair+" : fra line empty :"+str(j)
				lineout=" ¤ ¤ ¤ "+str(j)+" ¤ "+fraout
				# print lineout
				chkfile.write(lineout+"\n")
		else :
			fra=int(fraln)
			fratxt=""
			if fra>=0 :
				fratxt=fralist[fra].strip()
			if fratxt=="":
				fratxt="(void)"
				print "problem at prl "+prlpair+" : fra line empty :"+fraln
			lineout=lineout+fraln+" ¤ "+fratxt
			# print lineout
			chkfile.write(lineout+"\n")
#close files
disfile.close()
frafile.close()
prlfile.close()
chkfile.close()
print chkname+ " is available "