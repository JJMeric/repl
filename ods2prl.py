#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

from pyexcel_ods3 import get_data    # pip install pyexcel-ods3

data = get_data("sen_tegiziperi-masadennin-bam-fra.ods")

# ADD: also open .dis.html file to check that number of bam sentences is the same

nbam=-1  # index starts at 0
nfra=-1

prltext=""
for key,sheet in data.items():
	# print(key) - actually: only supposed to handle unique sheet in spreadsheet...
	bamlist=[]
	fralist=[]
	nl=0
	for elements in sheet:
		nl+=1
		if len(elements)==2:
			#bam,fra=elements
			bam=elements[0].strip()
			fra=elements[1].strip()
			if bam!="": 
				nbam+=1
			if fra!="": 
				nfra+=1
			# else : print(">>> fra empty") # never happens, see $$$
			# write in -bam.txt
			# write in -fra.txt
			bamlist.append(nbam)
			fralist.append(nfra)
		else:
			if len(elements)==0:
				print("line",nl," ??? no elements (ignored) ")
			else:
				bam=elements[0].strip()
				if bam!="": nbam+=1
				# print("$$$ fra empty")
				# write in -bam.txt
				# write in -fra.txt
				bamlist.append(nbam)
				fralist.append(nfra)

nbamstart=-1   # start of alignment sequence one-one one2many many2one
nfrastart=-1

bamlist.append(-1) # to close the lists
fralist.append(-1)

nlmax=len(bamlist)-1

prltext=""     # writes only occur on alignment breaks (ruptures)
bamseq=False   # opens a sequence one2many
fraseq=False   # opens a sequence many2one

for nl in range(0, nlmax) :
	nbam=bamlist[nl]
	nfra=fralist[nl]
	if nbamstart==-1 : nbamstart=nbam 
	if nfrastart==-1 : nfrastart=nfra
	if nbam==bamlist[nl+1]:
		if not bamseq:
			bamsep=":"
			if nbam-1==nbamstart+1 : bamsep=","
			frasep=":"
			if nfra-1==nfrastart+1 : frasep=","
			prltext+=str(nbamstart)+bamsep+str(nbam-1)+"\t"+str(nfrastart)+frasep+str(nfra-1)+"\n"
			nbamstart=nbam
			nfrastart=nfra
			bamseq=True
		
	elif nfra==fralist[nl+1]:
		if not fraseq:
			bamsep=":"
			if nbam-1==nbamstart+1 : bamsep=","
			frasep=":"
			if nfra-1==nfrastart+1 : frasep=","
			prltext+=str(nbamstart)+bamsep+str(nbam-1)+"\t"+str(nfrastart)+frasep+str(nfra-1)+"\n"
			nbamstart=nbam
			nfrastart=nfra
			fraseq=True
		
	else:
		if bamseq:
			bamseq=False
			frasep=":"
			if nfra==nfrastart+1 : frasep=","
			prltext+=str(nbamstart)+"\t"+str(nfrastart)+frasep+str(nfra)+"\n"
			nbamstart=-1
			nfrastart=-1
		elif fraseq:
			fraseq=False
			bamsep=":"
			if nbam==nbamstart+1 : bamsep=","
			prltext+=str(nbamstart)+bamsep+str(nbam)+"\t"+str(nfrastart)+"\n"
			nbamstart=-1
			nfrastart=-1
# loop finished
if bamseq:
	frasep=":"
	if nfra==nfrastart+1 : frasep=","
	prltext+=str(nbamstart)+"\t"+str(nfrastart)+frasep+str(nfra)+"\n"

elif fraseq:
	bamsep=":"
	if nbam==nbamstart+1 : bamsep=","
	prltext+=str(nbamstart)+bamsep+str(nbam)+"\t"+str(nfrastart)+"\n"

else:
	bamsep=":"
	if nbam==nbamstart+1 : bamsep=","
	frasep=":"
	if nfra==nfrastart+1 : frasep=","
	prltext+=str(nbamstart)+bamsep+str(nbam)+"\t"+str(nfrastart)+frasep+str(nfra)+"\n"

print("prltext:\n"+prltext)
# write to .prl file


# Output matches that of Andrij's prl file - 27/06/2025

#   0:511	0:511
#   512,513	512
#   514:570	513:569
#   571,572	570
#   573:616	571:614
#   617,618	615
#   619:657	616:654
#   658,659	655
#   660:814	656:810
#   815,816	811
#   817:896	812:891
#   897,898	892
#   899:932	893:926
#   933,934	927
#   935:1191	928:1184
#   1192	1185,1186
#   1193:1531	1187:1525

# CAVEAT : the following situations are not handled
# noop : not part of translation (translation missing or comment)
#     could be signaled by someting like -NA- in .ods
# many2many : where two or more sentences in Bam is not in the same sentence order as in the same number of sentences in French
#     how is this handled today ? how to signal in ods ?
