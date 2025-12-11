#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

from pyexcel_ods3 import get_data    # pip install pyexcel-ods3

# on passe deux arguments
# 1) nom de fichier .ods qui doit se terminer par -bam-fra3.ods ou -bam-fra4.ods
# 2) n° de colonne où se trouve le français à prendre en compte: 3 ou 4
#    nb: le bambara, celui ésambiguïsé, est toujours en colonne 1
#
# on obtient les fichiers suivants
# bam-fra4 : un fichier se terminant en .dis.fra.txt
# s'il n'y a pas alignement un à un, on obtient un fichier se terminant en .dis.bam-fra.prl


if len(sys.argv)>1:
  fileINname=str(sys.argv[1])
else: sys.exit("svp entrer le nom du fichier -bam-fraX.ods (avec X=3 ou 4)")

colfra=3
if len(sys.argv)>2:
	colfra=int(sys.argv[2])
if colfra<3 :
	sys.exit("le français doit être en colonne 3 ou +")

if "-bam-fra3.ods" in fileINname or "-bam-fra4.ods" in fileINname : 
	fileroot=fileINname[:-13]
	filefraName=fileroot+".dis.fra.txt"
	fileprlName=fileroot+".dis.bam-fra.prl"
else:
	sys.exit("entrer un nom de fichier se terminant en -bam-fra3.ods ou en -bam-fra4.ods")

data = get_data(fileINname)

# ADD: also open .dis.html file to check that number of bam sentences is the same

nbam=-1  # index starts at 0
nfra=-1

fratext=""

prltext=""
for key,sheet in data.items():
	# print(key) - actually: only supposed to handle unique sheet in spreadsheet...
	bamlist=[]
	fralist=[]
	nl=0
	l1=True
	for elements in sheet:
		if l1 :
			l1=False
			continue  # skips 1st line
		nl+=1
		if len(elements)==colfra:
			#bam,fra=elements
			bam=elements[1].strip()
			fra=elements[colfra-1].strip()
			if bam!="": 
				nbam+=1
				# write in -bam.txt
			if fra!="": 
				nfra+=1
			# else : print(">>> fra empty") # never happens, see $$$
				# write in -fra.txt
				fratext+="<s n=\""+str(nfra)+"\">"+fra+"</s>\n"
			bamlist.append(nbam)
			fralist.append(nfra)
		else:
			if len(elements)==0:
				print("line",nl," ??? no elements (ignored) ")
			else:
				bam=elements[1].strip()
				if bam!="": nbam+=1
				# print("$$$ fra empty")
				# write in -bam.txt
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

linesprl=prltext.split("\n")
if not (len(linesprl)==2 and linesprl[1]==""):
	fileprl=open(fileprlName,"w")
	fileprl.write(prltext)
	fileprl.close()
	print(fileprlName,"est disponible")
else:
	print("textes alignés, pas besoin de fichier .prl\nprltext:\n"+prltext)

filefra=open(filefraName,"w")
filefra.write(fratext)
filefra.close()
print(filefraName,"est disponible")


# St Exupéry Le Petit prince :
#   Output matches that of Andrij's prl file - 27/06/2025

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
