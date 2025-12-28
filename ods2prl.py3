#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from pyexcel_ods3 import get_data    # pip install pyexcel-ods3

# makes a summary of the parallel spreadsheet, saved in a .prl file
#   where each bamanankan sentence is associated with one or many french translation sentences
#   associating each bam sentence n° with a corresponding fra sentence n°
#   see attached (end of this file) for explanations.


# on passe un argument:
# 1) nom de fichier .ods qui doit se terminer par -bam-fra3.ods ou -bam-fra4.ods
# 2) argument optionnel : n° de colonne où se trouve le français à prendre en compte: 3 (défaut) ou 4
#    nb: le bambara, celui ésambiguïsé, est toujours en colonne 1
#
# on obtient les fichiers suivants
# bam.fra bam.fra2, bam-fra3 : un fichier se terminant en .dis.fra.txt
# bam-fra3 : en supplément un fichier se terminant en .dis.fra2.txt ("aligné")
# bam-fra4 : seulement un fichier se terminant en .dis.fra2.txt
# s'il n'y a pas alignement un à un, on obtient un fichier se terminant en .dis.bam-fra.prl
#
# 3) argument optionnel : -c
# on obtient un fichier se terminant en -check.csv qui reconstitue le fichier de départ à partir du fichier .prl 
# NB : fichier csv séparé par des tabulations



if len(sys.argv)>1:
  fileINname=str(sys.argv[1])
else: sys.exit("svp entrer le nom du fichier -bam-fraX.ods (avec X=3 ou 4)")

if not os.path.exists(fileINname):
	sys.exit(fileINname+" n'existe pas dans ce répertoire, vérifier svp")

colfra=3
checks=False
if len(sys.argv)>2:
	if sys.argv[2].isdigit():
		colfra=int(sys.argv[2])
		if colfra<3 :
			sys.exit("le français doit être en colonne 3 ou +")
	elif sys.argv[2]=="-c":
		checks=True
	else:
		print("argument ignoré:",sys.argv[2])

endswith=fileINname[-13:]

if endswith[1:]=="-bam-fra.ods" :  # no dis file, only bam text and fra text
	filebamrequired=True
	fileroot=fileINname[:-12]
	filebamName=fileroot+".bam.txt"
	filefraName=fileroot+".fra.txt"
	fileprlName=fileroot+".bam-fra.prl"
elif endswith in ["-bam-fra2.ods","-bam-fra3.ods","-bam-fra4.ods"] : 
	filebamrequired=False  # bambara is in dis file
	fileroot=fileINname[:-13]
	fileprlName=fileroot+".dis.bam-fra.prl"
	filefraName=fileroot+".dis.fra.txt"
	if endswith=="-bam-fra4.ods" : 
		filefraName=fileroot+".dis.fra2.txt"
	elif endswith=="-bam-fra3.ods" :
		filefra2Name=fileroot+".dis.fra2.txt"	
else:
	sys.exit("entrer un nom de fichier se terminant en -bam-fra?.ods ou ? est vide ou =2 ou 3 ou 4")

data = get_data(fileINname)

# ADD: also open .dis.html file to check that number of bam sentences is the same

nbam=-1  # index starts at 0
nfra=-1

fratext=""
bamtext=""

prltext=""
bamdict={}
fradict={}
for key,sheet in data.items():
	# print(key) - actually: only supposed to handle unique sheet in spreadsheet...
	nbamlist=[]
	nfralist=[]
	nl=0
	l1=True
	for elements in sheet:
		if l1 :
			l1=False
			continue  # skips 1st line
		nl+=1
		if len(elements)>=colfra: # nb ; les cellules à droite de colfra sont ignorées
			
			#print(nl,elements)
			if type(elements[1]) is str: bam=elements[1].strip()
			else: 
				bam=str(elements[1])
				print("!!!Attention: éviter les lignes ne contenant que des chiffres, voir ligne",nl,":",bam)
			
			if type(elements[colfra-1]) is str: fra=elements[colfra-1].strip()
			else:	
				fra=str(elements[colfra-1])
				print("!!!Attention: éviter les lignes ne contenant que des chiffres, voir ligne",nl,":",fra)
				
			NA=False
			#print("bam:",nl,bam)
			if bam!="":
				if bam!="-NA-":
					nbam+=1
					# write in -bam.txt
					# print("bam:","<s n=\""+str(nbam)+"\">"+bam+"</s>")
					bamdict[nbam]=bam
					if filebamrequired: bamtext+="<s n=\""+str(nbam)+"\">"+bam+"</s>\n"
				else:
					NA=True
					if fra=="": sys.exit("un -NA- ne peut pas être en face d'une cellule vide de continuation, voir ligne"+str(nl))
			if fra!="":
				if fra!="-NA-":
					nfra+=1
				# else : print(">>> fra empty") # never happens, see $$$
					# write in -fra.txt
					fradict[nfra]=fra
					fratext+="<s n=\""+str(nfra)+"\">"+fra+"</s>\n"
				else:
					NA=True
					if bam=="": sys.exit("un -NA- ne peut pas être en face d'une cellule vide de continuation, voir ligne"+str(nl))
			if not NA :
				nbamlist.append(nbam)
				nfralist.append(nfra)
			else:
				if bam=="-NA-": 
					nbamlist.append(-1)
					nfralist.append(nfra)
				if fra=="-NA-":
					nbamlist.append(nbam)
					nfralist.append(-1)
		else:
			if len(elements)==0:
				print("line",nl," ??? no elements (to be ignored if lines closing table) ")
			else:
				bam=elements[1].strip()
				if bam!="": nbam+=1
				# print("$$$ fra empty")
				# write in -bam.txt
				bamdict[nbam]=bam
				if filebamrequired: bamtext+="<s n=\""+str(nbam)+"\">"+bam+"</s>\n"
				nbamlist.append(nbam)
				nfralist.append(nfra)

	if endswith=="-bam-fra3.ods" :   # type 3 : loop again on aligned translation
		fra2dict={}
		fra2text=""
		l1=True
		for elements in sheet:
			if l1 :
				l1=False
				continue  # skips 1st line
			if len(elements)==0: continue    # skip empty lines at the end
			nl+=1
			fra=elements[colfra].strip()  # last column (2d of French, aligned)
			fra2dict[nfra]=fra
			fra2text+="<s n=\""+str(nfra)+"\">"+fra+"</s>\n"


nbamlist.append(-1) # to close the lists
nfralist.append(-1)

nlmax=len(nbamlist)-1

prltext=""     # writes only occur on alignment breaks (ruptures)
nlseq=False   # opens a sequence one2many or many2one
nlseqNAbam=False # same for "not available" but need to treat bam and fra separately
nlseqNAfra=False # same for "not available"

nlstart=-22    # start of a new sequence summary
seqlist=[]
lastseqbam=-22
#lastseqfra=0
nbam_in_seq=[]
nfra_in_seq=[]

for nl in range(0, nlmax) :
	if nlstart==-22: nlstart=nl
	nbam=nbamlist[nl]
	nfra=nfralist[nl]
	# print(nl,nbam,nfra)

	if nbam==-1:
		if nbam==nfra: sys.exit("cannot have -NA- in both columns, check line ",nl)
		if not nlseqNAbam:
			# save  previous sequence summary 
			if nl>0:
				nbam1=nbamlist[nl-1]
				nfra1=nfralist[nl-1]
				if lastseqbam!=nbam1: # or: nbma1 in nbam_in_seq  (already in stored sequences)
					seqlist.append((nbamlist[nlstart],nbam1,nfralist[nlstart],nfra1))
					#print("cas A-NAbam",nl,nbam,nfra,"+",(nbamlist[nlstart],nbam1,nfralist[nlstart],nfra1))
					lastseqbam=nbam1
					for i in range(nbamlist[nlstart],nbam1+1): 
						if i!=-1:nbam_in_seq.append(i)
					for i in range(nfralist[nlstart],nfra1+1): 
						if i!=-1:nfra_in_seq.append(i)
					#lastseqfra=nfra1
			nlstart=nl
			nlseqNAbam=True
			nlseqNAfra=False
			nlseq=False

	elif nfra==-1:
		if nbam==nfra: sys.exit("cannot have -NA- in both columns, check line ",nl)
		if not nlseqNAfra:
			# save  previous sequence summary 
			if nl>0:
				nbam1=nbamlist[nl-1]
				nfra1=nfralist[nl-1]
				if lastseqbam!=nbam1: # or: nbma1 in nbam_in_seq  (already in stored sequences)
					seqlist.append((nbamlist[nlstart],nbam1,nfralist[nlstart],nfra1))
					#print("cas A-NAfra",nl,nbam,nfra,"+",(nbamlist[nlstart],nbam1,nfralist[nlstart],nfra1))
					lastseqbam=nbam1
					for i in range(nbamlist[nlstart],nbam1+1): 
						if i!=-1:nbam_in_seq.append(i)
					for i in range(nfralist[nlstart],nfra1+1): 
						if i!=-1:nfra_in_seq.append(i)
					#lastseqfra=nfra1
			nlstart=nl
			nlseqNAfra=True
			nlseqNAbam=False
			nlseq=False

	elif nbam==nbamlist[nl+1] or nfra==nfralist[nl+1]:
		if nbam==nbamlist[nl+1] and nfra==nfralist[nl+1]: sys.exit("cannot have [empty space] in both columns, check line ",nl)
		if not nlseq:
			# save  previous sequence summary 
			if nl>0:
				nbam1=nbamlist[nl-1]
				nfra1=nfralist[nl-1]
				if lastseqbam!=nbam1:
					seqlist.append((nbamlist[nlstart],nbam1,nfralist[nlstart],nfra1))
					#print("cas A",nl,nbam,nfra,"+",(nbamlist[nlstart],nbam1,nfralist[nlstart],nfra1))
					lastseqbam=nbam1
					for i in range(nbamlist[nlstart],nbam1+1): 
						if i!=-1:nbam_in_seq.append(i)
					for i in range(nfralist[nlstart],nfra1+1): 
						if i!=-1:nfra_in_seq.append(i)
			nlstart=nl
			nlseq=True
			nlseqNAbam=False
			nlseqNAfra=False
			
	else:
		if nlseqNAbam:
			nlseqNAbam=False
			if nl>0:
				if lastseqbam!=nbam:
					seqlist.append((nbamlist[nlstart],nbamlist[nl-1],nfralist[nlstart],nfralist[nl-1]))
					#print("cas B-NAbam",nl,nbam,nfra,"+",(nbamlist[nlstart],nbamlist[nl-1],nfralist[nlstart],nfralist[nl-1]))
					lastseqbam=nbamlist[nl-1]
					for i in range(nbamlist[nlstart],nbamlist[nl-1]+1): 
						if i!=-1:nbam_in_seq.append(i)
					for i in range(nfralist[nlstart],nfralist[nl-1]+1): 
						if i!=-1:nfra_in_seq.append(i)		
			nlstart=nl
		elif nlseqNAfra:
			nlseqNAfra=False
			if nl>0:
				if lastseqbam!=nbam:
					seqlist.append((nbamlist[nlstart],nbamlist[nl-1],nfralist[nlstart],nfralist[nl-1]))
					#print("cas B-NAfra",nl,nbam,nfra,"+",(nbamlist[nlstart],nbamlist[nl-1],nfralist[nlstart],nfralist[nl-1]))
					lastseqbam=nbamlist[nl-1]
					for i in range(nbamlist[nlstart],nbamlist[nl-1]+1): 
						if i!=-1:nbam_in_seq.append(i)
					for i in range(nfralist[nlstart],nfralist[nl-1]+1): 
						if i!=-1:nfra_in_seq.append(i)		
			nlstart=nl
		elif nlseq:   # note : at this step next ligne number nbam is different from current
			nlseq=False
			#print("cas B, lastseqbam=",lastseqbam,"nbam=",nbam)
			if lastseqbam!=nbam:
				seqlist.append((nbamlist[nlstart],nbam,nfralist[nlstart],nfra))
				#print("cas B",nl,nbam,nfra,"+",(nbamlist[nlstart],nbam,nfralist[nlstart],nfra))
				lastseqbam=nbam
				for i in range(nbamlist[nlstart],nbam+1): 
					if i!=-1:nbam_in_seq.append(i)
				for i in range(nfralist[nlstart],nfra+1): 
					if i!=-1:nfra_in_seq.append(i)		
			nlstart=-22
		else:
			#print("RAF",nl,nbam,nfra)
			continue # dummy end of loop (because dummy else)

# loop finished
seqlist.append((nbamlist[nlstart],nbam,nfralist[nlstart],nfra))
for i in range(nbamlist[nlstart],nbam+1): 
	if i!=-1:nbam_in_seq.append(i)
for i in range(nfralist[nlstart],nfra+1): 
	if i!=-1:nfra_in_seq.append(i)

if len(nbam_in_seq)!=len(bamdict): 
	print("problème de logique interne nbam_in_seq",len(nbam_in_seq)," not = bamdict",len(bamdict))
	#print(nbam_in_seq)
	nbam=0
	for i in nbam_in_seq:
		if i!=nbam:
			print("->problème de séquence ? i,nbam",i,nbam)
			break
		nbam+=1
if len(nfra_in_seq)!=len(fradict): 
	print("problème de logique interne nfra_in_seq",len(nfra_in_seq)," not = fradict",len(fradict))
	#print(nfra_in_seq)
	nfra=0
	for i in nfra_in_seq:
		if i!=nfra:
			print("->problème de séquence ? i,nfra",i,nfra)
			break
		nfra+=1

#print("seqlist")
#for x in seqlist:print(x)
#sys.exit("fin temporaire")


lenlinesprl=len(seqlist)
if endswith=="-bam-fra4.ods" and lenlinesprl>1: print("Type 4 mais fichier non aligné ?\n",prltext)
else :
	prltext=""
	if lenlinesprl==1: print("NB: bambara et français sont alignés lignes à ligne, considérer un type 4 si le style de traduction est également \"aligné\"")
	for x in seqlist:
		nbam1,nbam2,nfra1,nfra2=x
		bamsep=":"
		if nbam2==nbam1+1 : bamsep=","
		frasep=":"
		if nfra2==nfra1+1 : frasep=","
		if nbam2>nbam1:	prltext+=str(nbam1)+bamsep+str(nbam2)+"\t"
		elif nbam2==nbam1: prltext+=str(nbam1)+"\t"
		#elif nbam2==-1: prltext+=str(nbam)+"\t"
		if nfra2>nfra1: prltext+=str(nfra1)+frasep+str(nfra2)+"\n"
		elif nfra2==nfra1: prltext+=str(nfra1)+"\n"
		#elif nfra==-1: prltext+=str(nfra)+"\n"

	fileprl=open(fileprlName,"w")
	fileprl.write(prltext)
	fileprl.close()
	print(fileprlName,"est disponible")

filefra=open(filefraName,"w")
filefra.write(fratext)
filefra.close()
print(filefraName,"est disponible")

if endswith=="-bam-fra3.ods" :
	filefra=open(filefra2Name,"w")
	filefra.write(fra2text)
	filefra.close()
	print(filefra2Name,"est disponible")


if filebamrequired:
	filebam=open(filebamName,"w")
	filebam.write(bamtext)
	filebam.close()
	print(filebamName,"est disponible")

if checks:
	filecheckName=fileroot+"-check.csv"
	checktext=""
	nl=0
	for x in seqlist:
		nbam1,nbam2,nfra1,nfra2=x
		if nbam2==nbam1:
			for i in range(nfra1,nfra2+1):
				#print("nbam1=nbam2",nbam1,"nfra",i)
				nl+=1
				bamtext=""
				if i==nfra1:
					if nbam1==-1: bamtext="-NA-"
					else: bamtext=bamdict[nbam1]
				fratext=""
				if i==-1: fratext="-NA-"
				else: fratext=fradict[i]
				checktext+=str(nl)+"\t"+str(nbam1)+"\t"+bamtext+"\t"+str(i)+"\t"+fratext+"\n"
		elif nfra2==nfra1:
			for i in range(nbam1,nbam2+1):
				nl+=1
				fratext=""
				if i==nbam1:
					if nfra1==-1: fratext="-NA-"
					else: fratext=fradict[nfra1]
				checktext+=str(nl)+"\t"+str(i)+"\t"+bamdict[i]+"\t"+str(nfra1)+"\t"+fratext+"\n"
		else:
			j=nfra1
			for i in range(nbam1,nbam2+1):
				nl+=1
				if i==-1: bamtext="-NA-"
				else: bamtext=bamdict[i]
				checktext+=str(nl)+"\t"+str(i)+"\t"+bamtext+"\t"+str(j)+"\t"+fradict[j]+"\n"
				j+=1
				if j>=len(fradict):break   # why does this happen sometimes???

	filecheck=open(filecheckName,"w")
	filecheck.write(checktext)
	filecheck.close()
	print(filecheckName,"est disponible")

# statistics
# sentences
bamsent=len(bamdict)
frasent=len(fradict)
# words
# get text
bamtext=""
for key,value in bamdict.items():
	bamtext+=value+"\n"
fratext=""
for key,value in fradict.items():
	fratext+=value+"\n"

import re
# eliminate comments sections <c>...</c> - see stats.py3
comments=re.compile(r'&lt;c&gt;[^¤/]*&lt;/c&gt;|<c>[^>\n]+</c>',re.U|re.MULTILINE)
bamtext=comments.sub('',bamtext,0)
fratext=comments.sub('',fratext,0)
# eliminate tags in bamanankan: <h> <ill> <sp> <br> etc.
bmtags=re.compile(r'&lt;[^\&\n]+&gt;|<[^>\n]+>',re.U|re.MULTILINE)
bamtext=bmtags.sub('',bamtext,0)

# finally count words
w_matches = re.findall(r"[\w]+", bamtext)
bamwords=len(w_matches)
w_matches = re.findall(r"[\w]+", fratext)
frawords=len(w_matches)

# doublecheck bamsent and bamwords from dis file if available - see stats.py3
disfileName=fileroot+".dis.html"
if os.path.exists(disfileName):
	disfile=open(disfileName,"r")
	distext=disfile.read()
	disfile.close()
	metasentences=re.compile(r'(?:\<meta content\=\"|\<meta name\=\"\_auto\:sentences\" content\=\")([0-9]*)(?:\" name\=\"\_auto\:sentences\" \/\>|\" \/\>)',re.U)
	metawords=re.compile(r'(?:\<meta content\=\"|\<meta name\=\"\_auto\:words\" content\=\")([0-9]*)(?:\" name\=\"\_auto\:words\" \/\>|\" \/\>)',re.U)
	metasent=metasentences.search(distext)
	if metasent :
		nsent=int(metasent.group(1))
	else:
		nsent=0
	s_matches = re.findall(r'<span class="sent">', distext)
	nsent_real=len(s_matches)
	if bamsent!=nsent: 
		if nsent!=nsent_real:
			print("Warning: number of sentences in dis file (real)",nsent_real,"does not match number reported in meta:",nsent)
			if bamsent!=nsent_real:
				print("!!!IMPORTANT!!! not the same number of sentences in dis file (real):",nsent_real,"and in ods file",bamsent," !!!")
		else:
			print("!!!IMPORTANT!!! not the same number of sentences in dis file (meta=real):",nsent,"and in ods file",bamsent," !!!")
	metaw=metawords.search(distext)
	if metaw :
		nwords=int(metaw.group(1))
	else:
		nwords=0
	if bamwords!=nwords:
		print(disfileName,"reports",nwords,"words\n<> text in ods file seems to be",bamwords,"words (disambiguated)")
else: print("could not check bamanankan stats with",disfileName,": file not available")


# report on stats:
print("bamanankan: ",bamsent,"sentences -",bamwords,"words")
print("français :  ",frasent,"sentences -",frawords,"words")



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

# CAVEAT : the following situation is not handled
# many2many inversions : where two or more sentences in Bam is not in the same sentence order as in the same number of sentences in French
#     how is this handled today ? colors!  how to signal in ods ?

# some information about the prl format by Andrij Rovenchak
# Dear Colleagues,
# 
# I am sending an excerpt from the Fasokan blog (May 2012).
# the alignment files (*.prl) have the following structure:
# 0:3 0:3 -- first four sentences in Bamana correspond to the same in French
# 4 4,5 -- the fifth sentence in Bamana corresponds to two subsequent sentences in French
# 5:7 6:8
# 8 -1 -- no French equivalent for the ninth Bamana sentence
# 9:18 9:18.
# 
# Please, do not hesitate and ask me if you need more explanation about file formats.
# 
# Best greetings from,
# Andrij
