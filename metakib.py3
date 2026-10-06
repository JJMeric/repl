#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import sys
import importlib
from html.parser import HTMLParser
parser = HTMLParser()
import os
import time
from datetime import datetime

def get_creation_date(file):
    stat = os.stat(file)
    try:
        return stat.st_birthtime
    except AttributeError:
        # Nous sommes probablement sous Linux. Pas de moyen pour obtenir la date de création, que la dernière date de modification.
        return stat.st_mtime

def addtheme(old,metatag,conditions) :
	global theme
	if old :
		conditions=re.sub(r"ɛɛ","èe", conditions)
		conditions=re.sub(r"ɛ","è", conditions)
		conditions=re.sub(r"ɔ","ò", conditions)
		conditions=re.sub(r"Ɛ","È", conditions)
		conditions=re.sub(r"Ɔ","Ò", conditions)
		conditions=re.sub(r"ɲ","ny", conditions)
		conditions=re.sub(r"Ɲ","Ny", conditions)
	l=0
	# conditions=re.sub(r"\|","[ \.\,\;\?\!\:]| ",conditions)   # forces exact match
	conditions=re.sub(r"\|","| ",conditions)   # words begining with
	conditions=re.sub(r"\(","( ",conditions)
	#conditions=re.sub(r"\)","[ \.\,\;\?\!\:])",conditions)
	m=re.findall(conditions,tout,re.I|re.U)
	if m!=None :
		l=len(m)
		# print metatag, l
	if l>=4 :
		if theme=="": theme=metatag
		else : 
			if metatag not in theme : theme=theme+";"+metatag

def addgenre(metatag,conditions,inwhat,nb) :
	global genre
	l=0
	# conditions=re.sub(r"\|","[ \.\,\;\?\!\:]| ",conditions)   # forces exact match
	# conditions=re.sub(r"\|","| ",conditions)   # words begining with
	# conditions=re.sub(r"\(","( ",conditions)
	# conditions=re.sub(r"\)","[ \.\,\;\?\!\:])",conditions)
	m=re.findall(conditions,inwhat,re.I|re.U)
	if m!=None :
		l=len(m)
		# print metatag, l
	if l>=nb :
		if genre=="": genre=metatag
		else : 
			if metatag not in genre : genre=genre+";"+metatag
# auteurs, exemples
# prévoir tout ça, éventuellement plus d'un auteur par content
# <meta name="author:name" content="Kane, Sumana" />
# <meta name="author:spelling" content="" />
# <meta name="author:birth_year" content="0" />
# <meta name="author:sex" content="m" />
# <meta name="author:native_lang" content="Bambara" />
# <meta name="author:dialect" content="" />
# <meta name="author:addon" content="habite Bamakɔ, Balikukalan baarada DNAFLA, EN-SUP" />
# <meta name="author:uuid" content="11aefaf1-6d5b-4ffa-84c7-24a3edb32670" />
		
# <meta name="author:name" content="Ture, Basiriki|Kante, Amadu Gaɲi" />
# <meta name="author:spelling" content="|" />
# <meta name="author:birth_year" content="0|1936" />
# <meta name="author:sex" content="m|m" />
# <meta name="author:native_lang" content="Bambara|Bambara" />
# <meta name="author:dialect" content="|Kayes" />
# <meta name="author:addon" content="éditeur de Kibaru&#10;(ou Basidiki Ture)|né à Kita. Travaille au Point G de 1955 à 1963. Puis AMAP, L'ESSOR, L'INFORMATEUR, et enfin KIBARU." />
# <meta name="author:uuid" content="60ba1311-ba33-4b5a-ab42-8fb1a6038263|797f3350-5147-480b-9ec5-4f7ccfe35139" />
import csv
dictauth={} 
with open(os.path.expanduser("~")+'/GITlab/corbama/authors.csv') as f:
    authors = csv.reader(f)
    for author in authors:
        if author[0]=="" or author[0]=='author:name' : continue
        #modèle dictauth[u"uuid"]=u"Nom, Prénom|spelling|datebirth|sex|language|native|comment"
        # ['author:name', 'author:spelling', 'author:sex', 'author:birth_year', 'author:dialect', 'author:native_lang', 'author:addon', 'author:uuid']
        uuid=author[7]
        data=author[0]+"|"+author[1]+"|"+author[3]+"|"+author[2]+"|"+author[4]+"|"+author[5]+"|"+author[6]
        # why do a join here and a split later ? inherits old code structure... get rid of this asap
        dictauth[uuid]=data
        #print uuid,data


def addauthor(authcond,uuid) :
	global auuid,aname,aspelling,abirth,asex,anative,adialect,aaddon
	if uuid not in dictauth: 
		print("auteur "+uuid+" absent de dictauth <================")
		return
	l=0
	# authcond=ur"^"+authcond   # added 15/2/18 to ensure line starts with author name candidate. prevents false positives (n bɛ fo ...). But also hinders double authors....
	# does not work
	#limit search to the last two lines
	m=re.findall(authcond,endoftext,re.U)
	if m!=None :
		l=len(m)
		adata=dictauth[uuid].split("|")	
	if l>=1 :
		#print "  author : ",m
		if auuid=="": 
			auuid=uuid
			aname=adata[0]
			aspelling=adata[1]
			abirth=adata[2]
			asex=adata[3]
			anative=adata[4]
			adialect=adata[5]
			aaddon=adata[6]
		else : 
			if uuid not in auuid : 
				auuid=auuid+"|"+uuid
				aname=aname+"|"+adata[0]
				aspelling=aspelling+"|"+adata[1]
				abirth=abirth+"|"+adata[2]
				asex=asex+"|"+adata[3]
				anative=anative+"|"+adata[4]
				adialect=adialect+"|"+adata[5]
				aaddon=aaddon+"|"+adata[6]


title=re.compile(r'<h>([^\n\<]*)</h>',re.U|re.MULTILINE)
searchwords=re.compile(r'([a-zɛɔɲŋA-ZƐƆƝŊ\-́̀̌̂]+)',re.U|re.MULTILINE)
newalphabet=re.compile(r"(ɛ|ɔ|ɲ|Ɛ|Ɔ|Ɲ)",re.U|re.MULTILINE)
oldalphabet=re.compile(r"(è|ò|è|ò|È|Ò)",re.U|re.MULTILINE)

metasstub="""<html><head><meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<meta name="corpus:sponsor" content="" />
<meta name="corpus:adddate" content="MM/JJ/AAAA" />
<meta name="source:title" content="Kibaru" />
<meta name="source:year" content="XXXX" />
<meta name="source:number" content="XXX" />
<meta name="source:pagetotal" content="XX" />
<meta name="source:editor" content="AMAP" />
<meta name="source:publisher" content="Kibarudiso" />
<meta name="source:address" content="Bamako" />
<meta name="source:type" content="Périodiques" />
<meta name="source:date" content="XX.XX.XXXX" />
<meta name="source:misc" content="" />
<meta name="source:url" content="" />
<meta name="corpus:operator" content="Jean-Jacques Meric" />
<meta name="text:title" content="XXX" />
<meta name="text:date" content="XX.XX.XXXX" />
<meta name="text:pages" content="XX" />
<meta name="text:script" content="XXX" />
<meta name="text:genre" content="XXX" />
<meta name="text:theme" content="XXX" />
<meta name="text:rubric" content="" />
<meta name="text:transcription" content="" />
<meta name="text:transldata" content="" />
<meta name="text:original_lang" content="" />
<meta name="text:medium" content="écrit" />
<meta name="text:translation" content="inconnu" />
<meta name="_auto:words" content="XX" />
</head>
"""

bi=time.strftime("%m/%d/%Y")
metasstub=re.sub(r'name="corpus:adddate" content="(MM/JJ/AAAA)" ','name="corpus:adddate" content="'+bi+'" ',metasstub)

rundir=os.getcwd()
rundirs=rundir.split("/")
ndirs=len(rundirs)
currdir=rundirs[ndirs-1]
print(currdir)

if currdir.startswith("faso_kumakan"):
	dateelems=re.search(r"faso_kumakan([0-9]+)_([0-9]+)_([0-9]+)",currdir)
	year=dateelems.group(1)
	month=dateelems.group(2)
	day=dateelems.group(3)
	datenum=day+"."+month+"."+year
	pagestotal="2"
	print(datenum, pagestotal)
	#sys.exit()
else:
	nargv=len(sys.argv)
	print("nb args=",nargv)
	if nargv==1 :  # pas d'arguments
  		#sys.exit("entrer la date et le nombre de pages du numéro de Kibaru/Jekabaara: metakib.py 01.MM.AAAA N ")
		bi=time.strftime("%d.%m.%Y")
		datenum=bi
		pagestotal="1"
		print("Date:",datenum," (ou dates de création des fichiers) Pages=",pagestotal," (pas d'arguments fournis)")
	else : 
		datenum= str(sys.argv[1])
		pagestotal= str(sys.argv[2])
		print("Date:",datenum," Pages=",pagestotal)

	ddmmaaaafind=re.search(r"([0-9][0-9])\.([0-9][0-9])\.([0-9][0-9][0-9][0-9])",datenum)
	if ddmmaaaafind:
		year=ddmmaaaafind.group(3)
		month=ddmmaaaafind.group(2)
		day=ddmmaaaafind.group(1)
		if year >= "1900" and year <= "2200":
			if month > "00" and month < "13":
				if day > "00" and day < "32":
					datenum=day+"."+month+"."+year
				else:
					sys.exit ("day "+day+" not in 01-31 range")
			else:
				sys.exit("month "+month+" not in 01-12 range")
		else:
			sys.exit("year "+year+" not in 1900-2200 range")
		
	else:
		sys.exit ("date format should be DD.MM.YYYY")

metasstub=re.sub(r'name="source:year" content="(XXXX)" ','name="source:year" content="'+year+'" ',metasstub)
metasstub=re.sub(r'name="source:pagetotal" content="(XX)" ','name="source:pagetotal" content="'+pagestotal+'" ',metasstub)
metasstub=re.sub(r'name="source:date" content="(XX.XX.XXXX)" ','name="source:date" content="'+datenum+'" ',metasstub)
metasstub=re.sub(r'name="text:date" content="(XX.XX.XXXX)" ','name="text:date" content="'+datenum+'" ',metasstub)

# possibilité de récupérer ici le n° de Kibaru via os.dirname (?)
filenames=os.listdir(".")
filenames=sorted(filenames)
for filename in filenames:
	if ".txt" in filename :
		print("\n"+filename)
		periodique=""

		filehtml=filename.replace(".txt",".html")
		if os.path.exists(filehtml) : sys.exit("\n      \033[1m Output file "+filehtml+" ALREADY EXISTS !\033[0m\n")

		noauth=False  # noautho = do not check authors in filename
		find_in_name=re.search(r"^(kibaru|kibarufb|ankaso|jekabaara|faso_kumakan|jama|irisila_kunnafoniseben|kalamene|dibifara|koteba_kura|kote|kalanso|nafarinma|ntuloma|nyetaa|saheli|sankore|fakan)([0-9\-]*[a-z]*)\_",filename)
		try:
			periodique=find_in_name.group(1)
		except:
			noauth=True
			periodique=filename[:-4]  # remove .txt
			if periodique.endswith(".old"): periodique=periodique[:-4]
			if periodique.endswith("-zup") or filenamepart.endswith("-kot"): periodique=periodique[:-4]
		print("periodique=",periodique)

		# nb: le cas kibaru est le cas par défaut
		if periodique=="jekabaara" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Jɛkabaara" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Jamana" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="ODIPAC / CMDT / ODIMO" />',metasstub)
		elif periodique=="jama" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Jama" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Klena Sanogo" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Maaya dɔnniya da" />',metasstub)
		elif periodique=="kalamene" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Kalamɛnɛ" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Seyibane Kulibali" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="CAURIS/Animare/IMRAD" />',metasstub)
		elif periodique=="dibifara" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Dibifara" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Yusufu Jalo" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="AMAP/Kibaru" />',metasstub)
		elif "*"+periodique+"*"=="*kote*" :  # * pour ne pas confondre avec koteba_kura
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Kɔtɛ" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Berehima Dunbiya" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Balikukalan soba" />',metasstub)
		elif periodique=="kalanso" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Kalanso" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Adama Berete" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Balikukalan soba" />',metasstub)
		elif periodique=="nafarinma" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Nafarima" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','',metasstub)   # inconnu
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','',metasstub)   # inconnu
		elif periodique=="ntuloma" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Ntuloma" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Ayisata Jara Dunbuya" />',metasstub)   
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Wande Sumare, Balikukalan Baarada" />',metasstub)
		elif periodique=="nyetaa" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Ɲɛtaa" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Adama Berete" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Balikukalan Ɲɛmɔgɔso" />',metasstub)
		elif periodique=="saheli" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Saheli" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Sumayila Sanba Tarawele" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="G. Munkoro" />',metasstub)
		elif periodique=="sankore" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Sankore" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Mamadu Sar" />',metasstub) 
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Institut des Sciences Humaines" />',metasstub)
		elif periodique=="kibarufb" :
			metasstub=re.sub('<meta name="source:url" content="" />','<meta name="source:url" content="https://www.facebook.com/kibaru.kibaru.31" />',metasstub)
		elif periodique=="ankaso" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="An Ka So" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="@farafinna  · Site web culture et société" />',metasstub) 
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="internet-Facebook" />',metasstub)
			metasstub=re.sub('<meta name="source:url" content="" />','<meta name="source:url" content="https://www.facebook.com/farafinna/" />',metasstub)
		elif periodique=="fakan" :
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Fakan" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Isiyaka Baalo" />',metasstub) 
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="internet" />',metasstub)
			metasstub=re.sub('<meta name="source:url" content="" />','<meta name="source:url" content="https://www.fakan.ml" />',metasstub)
		elif periodique!="kibaru" : # autres cas: supposé par un vrai périodique
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="preCorpus/'+periodique+'" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Valentin Vydrine" />',metasstub) 
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="CNRS/LLACAN" />',metasstub)
			if nargv==1:
				# date du fichier
				creation_date = datetime.fromtimestamp(get_creation_date(filename))
				# print("creationdate:",creation_date)
				find_in_bi=re.search(r'([0-9]{4})\-([0-9]{2})\-([0-9]{2})',str(creation_date))
				year=find_in_bi.group(1)
				month=find_in_bi.group(2)
				day=find_in_bi.group(3)
				newdate=day+"."+month+"."+year
				# print("newdate:",newdate)
				metasstub=re.sub(r'name="text:date" content="[^\"]*"',r'name="text:date" content="'+newdate+r'"',metasstub)
		try:
			numero=find_in_name.group(2)
		except:
			numero="0"
		
		if periodique=="faso_kumakan":
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Faso kumakan" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="L\'Essor" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="L\'Essor" />',metasstub)
			year=numero
			find_in_name=re.search(r"faso_kumakan"+year+"_([0-9]+)_([0-9]+)",filename)
			month=find_in_name.group(1)
			day=find_in_name.group(2)
			numero=year+month+day

		elif periodique=="irisila_kunnafoniseben":
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Irisila kunnafoniseben" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Azansi Nowòsiti" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Kibaru" />',metasstub)
			year=numero
			find_in_name=re.search(r"irisila_kunnafoniseben"+year+"_([0-9]+)",filename)
			month=find_in_name.group(1)
			numero=year+month

		elif periodique=="koteba_kura":
			metasstub=re.sub('<meta name="source:title" content="Kibaru" />','<meta name="source:title" content="Kɔtɛba kura" />',metasstub)
			metasstub=re.sub('<meta name="source:editor" content="AMAP" />','<meta name="source:editor" content="Yakuba Jara" />',metasstub)
			metasstub=re.sub('<meta name="source:publisher" content="Kibarudiso" />','<meta name="source:publisher" content="Gervais Mounkoro" />',metasstub)
			find_in_name=re.search(r"koteba_kura([0-9]+)",filename)
			numero=find_in_name.group(1)

		elif periodique=="kibarufb" or periodique=="fakan":
			find_in_name=re.search(r"(?:kibarufb|ankaso|fakan)([0-9]{4})([0-9]{2})([0-9]{2})",filename)
			year=find_in_name.group(1)
			month=find_in_name.group(2)
			day=find_in_name.group(3)
			# leave numero as is: YYYYMMDD
			# print("metasstub avant:",metasstub)
			# print("datenum:",datenum)
			# print("filename:",filename)
			# print("day:",day)
			# print("month:",month)
			# print("year:",year)
			newdate=day+"."+month+"."+year
			# print("newdate:",newdate)
			metasstub=re.sub(r'name="text:date" content="[^\"]*"',r'name="text:date" content="'+newdate+r'"',metasstub)
			# print("metasstub après:",metasstub)
			
		elif periodique=="ankaso":
			find_in_name=re.search(r"ankaso([0-9]{4})_([0-9]{2})",filename)
			year=find_in_name.group(1)
			month=find_in_name.group(2)
			day="01"
			newdate=day+"."+month+"."+year
			# print("newdate:",newdate)
			metasstub=re.sub(r'name="text:date" content="[^\"]*"',r'name="text:date" content="'+newdate+r'"',metasstub)

		numerosource=numero
		if "-" in numero :
			numeros=numero.split("-")
			numerosource=numeros[0]  # meta.py n'accepte pas les - dans les numéros, on en choisi un seul, le premier...
		
		try:
			page=re.search(r"[0-9\-]*\_([0-9]*)",filename).group(1)
		except:
			page="0"

		if periodique=="faso_kumakan":
			page=re.search(r"faso_kumakan"+year+"_"+month+"_"+day+"_([0-9]+)",filename).group(1)
		elif periodique=="irisila_kunnafoniseben":
			page=re.search(r"irisila_kunnafoniseben"+year+"_"+month+"_([0-9]+)",filename).group(1)
		elif periodique=="kibarufb" or periodique=="ankaso" or periodique=="fakan":
			page="1"  # no notion of page on internet facebook unique page
		
		if numero==""  :  # essayer  ex: nyetaa_kerenkerennen_02...
			numeropage=re.search(r""+periodique+r"_([a-z]*)_([0-9]+)",filename)
			numero=numeropage.group(1)
			page=numeropage.group(1)

		metas=metasstub
		metas=re.sub(r'name="source:number" content="(XXX)" ','name="source:number" content="'+numerosource+'" ',metas)
		metas=re.sub(r'name="text:pages" content="(XX)" ','name="text:pages" content="'+page+'" ',metas)
		
		fileIN = open(filename, "r")
		tout=fileIN.read()
		fileIN.close()

		# limit search of signatures to the end of the text
		# defined as : last 200 characters or last 3 lines
		ltout=len(tout)
		btout=0
		if ltout>200: btout=ltout-200
		endoftext=tout[btout:ltout]
		endoftextobj=re.search(r"([^\n]*\n\n[^\n]*\n\n[^\n]*)$(?![\r\n])",tout,re.U|re.MULTILINE)
		if endoftextobj : endoftext=endoftextobj.group(1)
		# untracked situations : last block is several lines with single \n
		# print "endoftext=",endoftext
	
		# is it "old"
		old=False
		if ".old.txt" in filename : old=True # no question asked, we trust it's old, and output file WILL be .old.html
		else:
			m=newalphabet.findall(tout)  # check if there are any of new alphabet (start here because sometime there are a few possible French è )
			if m!=None:
				l=len(m)
				if l==0 :
					m2=oldalphabet.findall(tout) # check if there are any of old alphabet (this is positive check !!!)
					if m2!=None :
						l2=len(m2)
						if l2==0 :
							print("new or old alphabet unidentifiable, assumed new <- please CHECK content")
						else: 
							old=True
							prevfilename=filename
							filename=re.sub(r".txt",".old.txt",filename)
							os.rename(prevfilename, filename)

		if old :   # replaced and by or, twas too restrictive maybe !
			metas=re.sub(r'name="text:script" content="(XXX)" ','name="text:script" content="Ancien orthographe malien" ',metas)
			tout=re.sub("è","è",tout,0,re.U|re.MULTILINE)
			tout=re.sub("ò","ò",tout,0,re.U|re.MULTILINE)
			
		else :
			metas=re.sub(r'name="text:script" content="(XXX)" ','name="text:script" content="Nouvel orthographe malien" ',metas)
		

		try:
			titl=title.search(tout).group(1)
		except:
			filenamepart=filename[:-4]
			if filenamepart.endswith(".old") : filenamepart=filenamepart[:-4]
			if filenamepart.endswith("-zup") or filenamepart.endswith("-kot"): filenamepart=filenamepart[:-4]
			titl=filenamepart.replace("_"," ")
			print("titre:",periodique," (pas de balise TITRE <h>Titre</h>)")
		titl=re.sub("\"","",titl)   # was &quot; but this is converted back to " and causes problems in build
		# print "titl="+titl
		titl=re.sub(r"\<c\>"," - ",titl)  # comments '< brackets' in metas cause problems in build mparser - 21/5/19
		titl=re.sub(r"\<\/c\>"," - ",titl)
		titl=re.sub(r"\&","-et-",titl)  # amperstand causes problem in build mparser
		titl=re.sub(r"\<","&lt;",titl)
		titl=re.sub(r"\>","&gt;",titl)

		metas=re.sub(r'name="text:title" content="(XXX)" ','name="text:title" content="'+titl+'" ',metas)
		
		tout=re.sub(r"\&","&amp;",tout,0,re.U|re.MULTILINE)  
		tout=re.sub(r"\<","&lt;",tout,0,re.U|re.MULTILINE)  
		tout=re.sub(r"\>","&gt;",tout,0,re.U|re.MULTILINE)
		
		#bis ?
		#tout=re.sub(ur"\<",u"&lt;",tout,re.U|re.MULTILINE)  
		#tout=re.sub(ur"\>",u"&gt;",tout,re.U|re.MULTILINE)

		touttxt=tout
		touttxt=re.sub(r"&lt;c&gt;.*&lt;/c&gt;"," ",touttxt,re.U|re.MULTILINE)  # enlever les séquences <c>...</c>
		touttxt=re.sub(r"&lt;n&gt;.*&lt;/n&gt;"," ",touttxt,re.U|re.MULTILINE)  # enlever les séquences <n>...</n>
		touttxt=re.sub(r"&lt;h&gt;|&lt;/h&gt;"," ",touttxt,re.U|re.MULTILINE)  # enlever les tags <h> ou </h>
		touttxt=re.sub(r"&lt;ill&gt;|&lt;/ill&gt;"," ",touttxt,re.U|re.MULTILINE)  # enlever les tags <ill> ou </ill>
		touttxt=re.sub(r"&lt;ls&gt;|&lt;/ls&gt;"," ",touttxt,re.U|re.MULTILINE)  # enlever les tags <ls> ou </ls>
		touttxt=re.sub(r"&lt;br/&gt;"," ",touttxt,re.U|re.MULTILINE)  # enlever les tags <br/>
			
		swords=searchwords.findall(touttxt)
		if swords :
			words=len(swords)
			word=str(words)
		
		# print word,"mots"
		metas=re.sub(r'name="_auto:words" content="(XX)" ','name="_auto:words" content="'+word+'" ',metas)

		# rubriques et thèmes
		# <meta name="text:genre" content="XXX" />
		genre=""
		addgenre("Litt&#233;rature orale : Th&#233;atre Koteba",r"(KOTEBA|Koteba|koteba)",titl,1)
		addgenre("Litt&#233;rature orale : Contes populaires",r"(nsiirin|Nsiirin|NSIIRIN|nsirin|Nsirin|NSIRIN|NZIRI)",titl,1)
		addgenre("Litt&#233;rature orale : Contes populaires",r"(nsiirin|Nsiirin|NSIIRIN|nsirin|Nsirin|NSIRIN|NZIRI)",tout,1)
		addgenre("Litt&#233;rature orale : Proverbes",r"(nsana|Nsana|NSANA)",titl,1)
		addgenre("Litt&#233;rature orale : &#201;pop&#233;es",r"(maana|Maana|MAANA)",titl,1)
		addgenre("Belles-Lettres : Po&#233;sie moderne",r"(Poyi|N ka kalimu|poyi|POYI|n ka kalimu)",titl,1)
		addgenre("Belles-Lettres : Po&#233;sie moderne",r"poyi_",filename,1)
		addgenre("Belles-Lettres : Po&#233;sie moderne",r"(&lt;po&gt;)",tout,1)
		addgenre("Litt&#233;rature orale : Devinettes",r"[\_\-]ntenten",filename,1)
		## trop dangereux (autres longue listes de noms) : addgenre("Belles-Lettres : Po&#233;sie moderne",ur"(&lt;br/&gt;)",tout,12)
			
		if genre=="":
			if old :
				addgenre("Litt&#233;rature orale : Chansons populaires",r"(dònkili|Dònkili)",titl,1)
				addgenre("Litt&#233;rature orale : Contes populaires",r"(nin kèra cè dò ye|nin kèra cè fila ye|nin kèra cè saba ye|nin kèra muso dò ye|nin kèra muso ye|Nin kèra cè dò ye|Nin kèra cè fila ye|Nin kèra cè saba ye|Nin kèra muso dò ye|Nin kèra muso ye)",tout,1)
				addgenre("Litt&#233;rature orale : Contes populaires",r"(nin kèra muso dò ye|nin kèra muso fila ye|nin kèra muso saba ye)",tout,1)
				#addgenre("Litt&#233;rature orale : Contes populaires",ur"(nin kèra [^\s]* dò ye|nin kèra [^\s]* fila ye|nin kèra [^\s]* saba ye)",tout,1)
				addgenre("Litt&#233;rature orale : Contes populaires",r"(juguni|suruku|nsonsanin|waraba|waraninkalan|warabilen|ntura|kami|ntori|wulu|bilisi|dononkòrò)",tout,3)
				addgenre("Litt&#233;rature orale : Devinettes",r"(Kuma kòròma|kuma kòròma|Ntèntèn|ntèntèn|ntenpari|ntènpari|NTÈNTÈN|NTENTEN)",titl,1)
				addgenre("Litt&#233;rature orale : Devinettes",r"(Kuma kòròma|kuma kòròma|Ntèntèn|ntèntèn|ntenpari|ntènpari)",tout,1)
			else :
				addgenre("Litt&#233;rature orale : Chansons populaires",r"(dɔnkili|Dɔnkili)",titl,1)
				addgenre("Litt&#233;rature orale : Contes populaires",r"(nin kɛra cɛ dɔ ye|nin kɛra cɛ fila ye|nin kɛra cɛ saba ye|nin kɛra muso dɔ ye|nin kɛra muso ye|Nin kɛra cɛ dɔ ye|Nin kɛra cɛ fila ye|Nin kɛra cɛ saba ye|Nin kɛra muso dɔ ye|Nin kɛra muso ye|Tericɛ saba)",tout,1)
				addgenre("Litt&#233;rature orale : Contes populaires",r"(nin kɛra muso dɔ ye|nin kɛra muso fila ye|nin kɛra muso saba ye)",tout,1)
				#addgenre("Litt&#233;rature orale : Contes populaires",ur"(nin kɛra [^\s]* dɔ ye|nin kɛra [^\s]* fila ye|nin kɛra [^\s]* saba ye)",tout,1)
				addgenre("Litt&#233;rature orale : Contes populaires",r"(juguni|suruku|nsonsanin|waraba|waraninkalan|warabilen|bilisi|ntura|kami|ntori|wulu|dononkɔrɔ)",tout,3)
				addgenre("Litt&#233;rature orale : Devinettes",r"(Kuma kɔrɔma|Ntɛntɛn|kuma kɔrɔma|ntɛntɛn|ntɛnpari|ntenpari|NTƐNTƐN)",titl,1)
				addgenre("Litt&#233;rature orale : Devinettes",r"(Kuma kɔrɔma|Ntɛntɛn|kuma kɔrɔma|ntɛntɛn|ntɛnpari|ntenpari)",tout,1)
		
		if genre=="":
			if len(re.findall(r"(Poyi\s*\:)",tout[0:120],re.I|re.U))>0 : genre="Belles-Lettres : Po&#233;sie moderne"
		if genre=="":
			nb_br=len(re.findall(r"(&lt;br/&gt;)",tout,re.I|re.U|re.MULTILINE))
			nb_nl=len(re.findall(r"(\n)",tout,re.I|re.U|re.MULTILINE))
			if 1.0*nb_br/nb_nl >= 0.8 :
				genre="Belles-Lettres : Po&#233;sie moderne"
			
		if genre!="" :
			metas=re.sub(r'name="text:genre" content="(XXX)" ','name="text:genre" content="'+genre+'" ',metas)
			print("  "+re.sub("&#233;","é",genre))
		else:
			if page=="01" :
				metas=re.sub(r'name="text:genre" content="(XXX)" ','name="text:genre" content="Information : Editorial" ',metas)
			else :
				metas=re.sub(r'name="text:genre" content="(XXX)" ','name="text:genre" content="Information : Nouvelles" ',metas)


		# <meta name="text:theme" content="XXX" />
		theme=""
		# appropriate spaces will be added in addtheme: all words beginning with - Case independant !
		addtheme(old,"&#201;ducation",r"(BALIKUKALAN|balikukalan|kalanso|kalanden|kalanbaliya|karamɔgɔ|lakɔli|Lakɔli|unesco|lɛkɔli|kalanjɛ)")
		addtheme(old,"Administration",r"(polisi|ciyakɛda|mɛri|komini|minisiri|Minisiri|forobakɛsu|nisɔngɔ|lɛnpo|takisi sarali|takisiw sarali|gɔfɛrɛnɛri|gɔfɛrɛnora|gɔfɛrɛnɛrɛ| kɔnsɛyi|arɔndisiman|erezɔn|sɛriwusida|baarada)")
		addtheme(old,"Agriculture",r"(FAO|fɛnɲɛnamafagalan|koperatifu|bɛnɛsɛnɛ|kabasɛnɛ|sɔsɛnɛ|fantɔrɔso|sisɛmara|kamifan|sisɛfan|ɔtiwale|forokurabɔ|jiritigɛ|kolokolo|pipiɲɛri|basikili|fantɔrɔmansin|malokisɛ|maloforo|hɛkitari|sayijirinin|Sayijirinin|jirituru|jiriden|jiribulu|jiridili|sɛnɛkɛ|Sɛnɛkɛ|cikɛko|cikɛla|Cikɛla|bagan|mɔnni|nakɔ|sanji|bulukuli|shyɛnni|turuli|saribilennin|dabakurunin|danni|jiri turu|ɲɔforo|kɔɔri|kabaforo|malosɛnɛ|saɲɔ|keninge|suman|jiginɛ|misi|shɛmara|syɛmara|sagagɛn|jɛgɛ|taari|kɔrɔshiyɛn|nɔgɔdon|Ofisidinizɛri|pɔmutɛri|tigasɛnɛ|shɛ|shɛdennin)")
		addtheme(old,"Arm&#233;e et Guerre",r"(maramafɛn|burudamɛkɛlɛ|binkanni|burudamɛ murutilenw|kɛlɛbansɛbɛn|sɔrɔdasi|marifatigi|binnkannikɛla|binkannikɛla|binnkanikɛla|Minusima|kojugubakɛla|dagayɔrɔ|basigibaliya|maramafɛn)")
		addtheme(old,"Chasse",r"(donsokɛ|donsoya|kungo sogo)")
		addtheme(old,"Christianisme", r"(kerecɛndiinɛ|kerecɛn|kereciyɛn|Kereciyɛn|mɔnsɛɲɛri|Mɔnsɛɲɛri|tubabumori|egilizi|Mishɔn|mishɔn|papu|Papu|Watikan)")
		addtheme(old,"Communication",r"(kunnafonina|kunnafonidila|kibaru|amap|jɛkabaara|arajo|tele|jabaranin|ORTM|nɛgɛjurusira|SOTƐLIMA|kabaaru|Essor|Faso Kumakan)")
		addtheme(old,"Economie et Finances",r"(PNUD|tajifeere|baarakɛnafolo|sanuɲinina|sanu bɔ|sanubɔ|damanda|yuruguyurugu|kɛmɛbiye|biye|dewaliyasɔn|Dewaliyasɔnkɔlɔnsen|CEAO|BCEAO|SUKALA|CMDT|KOMATƐKISI|SOTELMA|SEPAMA|OTER|OPAM|F\.M\.I|FMI|FARANSEFA|FARANSƐFA|FARANFARANSƐ|Faran Sefa|SEFAKO|forobakɛsu|foroba kɛsu|foroba wariko|dɔrɔmɛ|miliyɔn|miliyari|dugujukɔrɔfɛn|babili|izini|taji sɔngɔ|tajijago|tajifeere|sanbaga|nafolo|musaka|lɛnpo|wusuru|sefawari|dolari|warikodɛmɛ|sanubɔ|BNDA|banki|warimaraso|BDI|donfini|donfini|jagokɛla|koɲɛnabɔ)")
		addtheme(old,"Environnement",r"(dugukoloyɛrɛyɛ|bajiko|Bajiko|Bajoliba|Selɛnge|Manantali|dugukolonɔn|lakanani|kungodaw yiriwali ni sigiyɔrɔw lakanali|Kɔlɔnsen|pɔnpu|pɔnpekɔlɔn|Pɔnpekɔlɔn|jikodɛsɛ|jikomako|sanjiba|tasuma don kungo|sigiyɔrɔ lakana|sigida lakana|sigidaw lakana|sanjiko|jakɔngɔ|sanji hakɛ|sanji mumɛ|sigida|lamini|sanya|ɲamanton)")
		addtheme(old,"G&#233;ographie",r"(koɲɛɲinitaama|sigi cogo|sigicogo|faaba|ye dugu ye a bɛ)")
		addtheme(old,"Histoire",r"(ŋaara|kurukanfuga|mandenjamana|koɲɛɲinitaama|tubabu-bilen|tubabubilen|Fɔlɔ-fɔlɔ|Fɔlɔfɔlɔ|tariki|TARIKI|sigi cogo|sigicogo|tariku|Tariku|jɔnfeere|Jɔnfeere|Eziputi|farawona|farawuna|lawale|Lawale|tubabutile|Samori|Bakarijan|Bakari Jan|Kanku Musa|Sunjata Keyita)")
		addtheme(old,"Islam", r"(silamɛ|hiji|hijita|hijitaa|Makan|makantaa|misiri|sunkalo|sunbagatɔ|morikɛ|kuranɛ|garibu)")
		addtheme(old,"Linguistique",r"(angilekan|diɲɛ kɔnɔ kanw|Diɲɛ kɔnɔ kanw|wolokan|bamanankan|sinminkan|kanw sɛbɛnni|mabɛn|fasokan|Fasokan|mabɛnnidaɲɛ|kawaleyalan|kamankutulan|dɛmɛnan|kɔbila|sinsinnan|sɛbɛncogo|Mandenkan|kanbolofara|daɲɛgafe|siginiden|kumasen)")
		addtheme(old,"Loi",r"(OMAFES|yɛrɛwolodenyasɛbɛn|sariya|Sariya|sariyasen|Sariyasen|ɲangilisariya|sariyatigi|kiiri|kiri|kiritigɛla|kaso)")
		addtheme(old,"Loisirs", r"(fɔlikɛla|dɔnkili|EREGE|erege|arasita|cd kasɛti|«O.R.T.M» sigidoolo|gintan|filimu|FESPACO|Shɛki Umaru SISOKO|Sulɛyimani SISE|jadilala|Solomani Sise|Etalɔn Yenɛnga|folisen|jeli|dɔnkilidala|tarikitigi|siniman|Siniman|Eliwisi Pɛrɛsili|Mayikɔli Jakison|Salifu Keyita|Umu Sangare|Ali Farika Ture)")
		addtheme(old,"M&#233;decine et sant&#233;",r"(niwakini|witamini|furakɛyɔrɔ|sensabagatɔ|banabagatɔ|banabaatɔ|jibaatɔ|tinminɛ|jiginnimuso|fiyentɔ|lasiritɔ|sigarɛti|kɔnɔboli|dɔlɔmin|farigan|tɔgɔtɔgɔnin|O\.M\.S|OMS|kunfilatu|kunfilanitu|kunfilanintu|sida|kɛnɛya|bana|fura|dɔgɔtɔrɔ|dɔkɔtɔrɔ|ɲɛdimi|kɔnɔdimi|dusukundimi|boloci|pikiri|penisilini|sumaya|furakisɛ|pilili|fugula nafama|ɲɔnin|ɲɔnisan|muso kɔnɔma|bolokolo|senkolo|bolotuguda)")
		addtheme(old,"Philosophie", r"(saya|satuma|donsebaliya|limaniya|mɔnɛbɔ|miiri|faamuya)")
		addtheme(old,"Politique",r"(rewolisɔn|sosiyalisi|forobatɔn|bolonɔ bila|bolonɔbila|kelenya|kalafili|Kalafili|fangaso|jɛkakuma kunbɛn|Amadu Tumani TURE|Musa Tarawele|UDPM|UNFM|politiki|pariti|sɛkisɔn|kalata|yɛrɛta|wote|peresidan|jamanaɲɛmɔgɔ|jamanakuntigi|gɔfɛrɛnama|bɛɛya|bɛɛjɛfanga|demokarasi|forobaya|depitew|mɛriw|yɛrɛmahɔrɔnya)")
		addtheme(old,"Soci&#233;t&#233;",r"(polisi|sirabakankasaara|mɔgɔkɔrɔbabonya|danbetiɲɛ|sanuɲinina|damanda|kafoɲɔgɔnya|densɔrɔjoona|kɛrɛfɛmɔgɔ|sigiɲɔgɔn|yɛrɛsagokɛ|lamɔko|hadamaden|biden|jɔyɔrɔ|sonyali|seliba|Seliba|cɛganaya|nson|ciyɛnta|laada|funankɛ|dutigi|duden|polisi|kaso|fatɔ|Fatɔ|duguba|musocamanfuru|tungafɛtaala|Tungafɛtaala|yɛrɛwolodenya|binkanni|tungalataa|UNFM|dɔrɔgu|furujoona|furusa|furusiri|boloko|karadante|dennadon|tɔgɔladon|jɔyɔrɔ|musotɔn|jɛkulu|jɛkafɔ|jɛkabaara|jɛkakɛ|senenkunya|sinankunya|dɛsɛbagatɔ|baloko|kɔngɔ kunbɛnniko|musofuru|sigiɲɔgɔnya|denmisɛnw ka donba|denmisɛnw ka seliba|denmisɛnw tɔgɔladon|musow ka donba|musow ka seliba|musow tɔgɔladon|Musocamanfuru|musocamanfuru|furuko|denko|denladon|furu kɔnɔ|garibu|warikogɛlɛya|balokogɛlɛya|jɔnya)")
		addtheme(old,"Sport",r"(karidefinali|demifinali|finali|Karidefinali|Demifinali|Finali|penaliti|kupu tanko|bi kelen don|kurunboli|Kurunboli|balontan|ntolatan|Ntolatan|ladegebaga|farikoloɲɛnajɛ|bidonna|ziɲɔri|kade|ɲɛfɛmɔgɔ|bololantola|basikɛti|kupu|kupudafiriki|Kupudafiriki|kupudimɔndi|Kupudimɔndi|KUPUDIMƆNDI|KUPU DI MALI|kupu di Mali|baarita|bolokuru|soboli|balɔntan|samatasɛgɛ|Samatasɛgɛ)")
		addtheme(old,"Technologie", r"(tekinolozi|mansin|ɔridinatɛri|antɛni|emetɛri|analozi|dekodɛri|telewisɔn|panosolɛri|elɛkitotoniki|ekutɛri|batiri|sariziɛri|sateliti|sibɛri|tɔlikiwɔliki|ɛnfɔrɔmatiki|kilawye|kɔmandi|lozisiyɛli|numeriki|ɔndilatɛri)")
		addtheme(old,"Transport",r"(elikɔputɛri|taransipɔrɔ|gitɔrɔn|sofɛri|mɔbilibolila|sirabakankasaara|sisikurun|sisikuru|bolimafɛn|kasaara|nɛgɛsira|sira dilanni|siraba|sirantanya|Siraba|bolifɛnko|pɔn jɔra|mobilibolila|mobilitigi|kamyɔn|kamyon|Dugumabolifɛnkow|dugumabolifɛnkow|jikanta|awiyɔn|pankurun|Pankurun|taji)")
		
		if theme!="" :
			metas=re.sub(r'name="text:theme" content="(XXX)" ','name="text:theme" content="'+theme+'" ',metas)
			themeprint=re.sub("&#233;","é",theme)
			themeprint=re.sub("&#201;","É",themeprint)
			print("  "+themeprint)
		else :
			metas=re.sub(r'name="text:theme" content="(XXX)" ','name="text:theme" content="" ',metas)
		
		
		authstub="""<meta name="author:name" content="XXX" />
		<meta name="author:spelling" content="XXX" />
		<meta name="author:birth_year" content="XXX" />
		<meta name="author:sex" content="XXX" />
		<meta name="author:native_lang" content="XXX" />
		<meta name="author:dialect" content="XXX" />
		<meta name="author:addon" content="XXX" />
		<meta name="author:uuid" content="XXX" />
		"""

		aname=""
		aspelling=""
		abirth=""
		asex=""
		anative=""
		adialect=""
		aaddon=""
		auuid=""

		authshort=""
		if noauth and nargv==1:	
			fileauth=None
		else:
			filenamepart=filename[:-4] # enlever .txt
			if filenamepart.endswith(".old"):filenamepart=filenamepart[:-4]
			if filenamepart.endswith("-zup") or filenamepart.endswith("-kot"):filenamepart=filenamepart[:-4]

			fileauth=re.search(r"[0-9\-]*\_[0-9]*([a-z\_]*)\-",filenamepart)
		
			if periodique=="faso_kumakan":
				fileauth=re.search(r"faso_kumakan"+year+r"_"+month+r"_"+day+r"_"+page+r"([a-z\_]*)\-",filename)
		
		nshort=0
		if fileauth : 
			nshort=1
			shorts=fileauth.group(1)
			if "_" in shorts : 
				shortelems=shorts.split("_")
				nshort=len(shortelems)
			authshort="_"+shorts+"_"
		# pas de elif : il peut y avoir plusieurs auteurs !!!
		# LECTURE :
		# si le premier nom est dans le nom de fichier, 
		# chercher la signature dans le fichier, càd l'un des noms entre (),
		# si elle y est, ajouter l'auteur trouvé (par son uuid).

		if "_abdoulaye_" in authshort or "_abudululayi_" in authshort : 
			addauthor(r"(Ibbo Daddy Abdoulaye|Ibo Daddy Abdoulaye|Ibo Dadi Abudulayi|Ibɔ Dadi Abudulayi)","29066936-48f5-4f69-829a-dfd0c8b8f4bf")
		if "_alimuludu_" in authshort : addauthor(r"(L. Alimudu|L. ALIMULUDU|Lugayi Alimuludu|Lugeyi Alimuludu|Migayi Alimuludu|Lugeyi Alimuludu)","ce4fa3c9-af99-4928-b6ab-40d91c2c1018")
		if "_aliyu_" in authshort : addauthor(r"(Dawuda Aliyu|Dawuda ALIYU)","b473ae9e-8025-4fb3-a364-d4100131779a")
		if "_aluyu_" in authshort : addauthor(r"(Dawuda Aluyu|Dawuda ALUYU)","b473ae9e-8025-4fb3-a364-d4100131779a")
		if "_ba_" in authshort : 
			addauthor(r"(Uka Ba|Uka BA)","ce093b9a-f592-43a3-9cae-c957f4134dad")
			addauthor(r"(Alimami Ba|Alimami BA)","19139517-c6ad-4fdf-b1d1-c1e2f4424361")
		if "_badou_" in authshort : addauthor(r"(Zerɔmu Ajaku Badou|Jerome Badou|Zerɔmu Badou|Jerome Adjakou Badou)","1eed21cc-1fee-477f-b51c-433c93f117b2")
		if "_badu_" in authshort : addauthor(r"(Zerɔmu Ajaku Badu|Zerɔmi Ajaku Badu|Jerome Badu|Zerɔmu Badu|Jerome Adjaku Badu|J.A. Badu|J.A. BADU)","1eed21cc-1fee-477f-b51c-433c93f117b2")
		if "_bagayogo_" in authshort :
			addauthor(r"(M. Bagayogo|M. BAGAYOGO|Mamadu Bagayogo|Mamadu BAGAYOGO)","6e83ebc8-10bf-42f7-a6f0-3ecebd79984f")
			addauthor(r"(Kajatu Kulubali Bagayɔgɔ|Kajatu KULUBALI BAGAYƆGƆ|kajatu KULUBALI BAGAYƆGƆ)","867a08c1-23ee-42aa-8479-0e629b7349ed")
		if "_bajaga_" in authshort : addauthor(r"(Salimu Bajaga|Salimu BAJAGA|Salumu Bajaga|Salumu BAJAGA|S[\.]* Bajaga|S[\.]* BAJAGA|Salimi Bajaga|Salimi BAJAGA)","8be10a14-a980-490e-9f1c-f5ae235c9d41")
		if "_balo_" in authshort : 
			addauthor(r"(faraban balo|Faraban Balo|Faraban BALO|Faraba Balo)","596d1365-a5b5-4aad-a3ec-937a2ec44035")
			addauthor(r"(Modɛsi Balo|Modɛsi BALO)","db8fbfc7-30be-4c52-a536-300dacfb2943")
		if "_banba_" in authshort : addauthor(r"(namori banba|Namori Banba)","c4c865cb-8ccd-4ff4-9761-7186683456ef")
		if "_bangali_" in authshort : 
			addauthor(r"(Daramani Bangali|Daramani BANGALI)","e116e7c0-b8d4-445d-974b-afc33c2f45a8")
			addauthor(r"(Abudulayi Bangali|Abudulayi BANGALI)","7a8b829b-7746-4c99-8f71-7cca67af1c17")
		if "_bankali_" in authshort : addauthor(r"(Daramani Bankali|Daramani BANKALI)","e116e7c0-b8d4-445d-974b-afc33c2f45a8")
		if "_banyumanke_" in authshort:
			addauthor(r"(Baɲumankɛ|baɲumankɛ)","37fb14af-e1f9-4ba2-ba7c-5f67401f42fd")   # = TYS encore!!!
		if "_bari_" in authshort : addauthor(r"(Abdulayi Bari|Abudulayi Bari|Abdulaye Bari|A\. Bari|A Bari|A\. BARI|A BARI|Ablay Bari|Abdulayi BARI|Abdulay BARI|Abdoulaye Barry|Abdoulaye BARRY)","02fd28a2-e96c-48d3-844f-2e35b3157bfa")
		if "_beligasemu_" in authshort : addauthor(r"(Malika Bɛligasɛmu|Malika BƐLIGASƐMU)","cecaf637-40f6-4743-a6e7-20de9092d772")
		if "_belikasemu_" in authshort : addauthor(r"(Malika Bɛlikasɛmu|Malika BƐLIKASƐMU)","cecaf637-40f6-4743-a6e7-20de9092d772")
		if "_berete_" in authshort or "_berte_" in authshort : 
			addauthor(r"(Adama Berete|adama berete|Adama berete|adama Berete|Adama BERETE)","a17c29fa-9ce0-42d3-9277-2a48f07abb91")
			addauthor(r"(nanpe berete|Nanpe Berete)","4627912e-d8e0-405b-a3d2-147cc73d8533")
			addauthor(r"(Berema Berete|Burama Berete|Berema BERETE|Burama BERETE)","0c034f30-6345-4772-b9f9-981c751287e2")
			addauthor(r"(Salifu Berete|Salifu BERETE|Salifu Bɛrte|Salif Bɛrte)","d6dc8fc4-170c-435a-a44d-ea4f43e998f7")
		if "_bineta_" in authshort : addauthor(r"(Mamadu Bineta|Mamadu BINETA)","3216d238-5113-471e-abf2-037dbd3c23ec")
		if "_boli_" in authshort : 
			addauthor(r"(Pate Boli|Pate BOLI)","612ef758-857a-40f9-a2e3-89bff9f739cb")
			addauthor(r"(Musa Boli|Musa BOLI)","6c349568-0bc0-44ff-92aa-6c02e99a64ef")
			addauthor(r"(Hamadi Aturu Boli|Aturu Boli|Hamadi Aturu BOLI|Hamadi Afenu Boli|Hamadi Afuru Boli)","e2c9c835-e468-4469-98c7-7be5a2e0c10d")
			addauthor(r"(Pate Boli|Pate BOLI|Patɛ Boli|Patɛ BOLI)","612ef758-857a-40f9-a2e3-89bff9f739cb")
		if "_buware_" in authshort :
			addauthor(r"(Ŋolo A. Buware|Ŋolo Buware|Ɲolo A. Buware|Ɲolo Buware|ŋolo Buware|Ŋɔlɔ A. Buware|Ŋɔlɔ Buware|Ɲɔlɔ A. Buware|Ɲɔlɔ Buware|ŋɔlɔ Buware)","ad68f742-fa39-4cc8-bda6-db1f4a663e9f")
			addauthor(r"(Kasimu Buware|Kasimu BUWARE|Kasumu Buware|Kasumu BUWARE)","05dc4cd4-becb-4023-a500-f264479d646f")
			addauthor(r"(Mamutu Buware|Mamutu BUWARE)","04434b71-efe6-402a-b5d8-1fea037c8a71")
		if "_cero_" in authshort : addauthor(r"(Bubakari Cɛrɔ|Bubakari Cɛro|B[\.]* Cɛrɔ|b[\.]* cero|B[\.]* Cero|B[\.]* Cɛro|B[\.]* CERO|B[\.]* CƐRO)","1f5a2623-ecc3-4dd6-81cf-ea6152562a3d")
		if "_dadjo_" in authshort : addauthor(r"(Crépin Hilaire Dadjo|Crépin Hilaire DADJO)","4aeabf7f-35f1-4745-bf54-02a345b6f6f1")
		if "_damele_" in authshort : addauthor(r"(Bakaribilen Danbele|Bakari Danbele|Bakari Damele|Bakaribilen Damele)","dda27c30-a372-4cdb-884b-2ac8667a1523")
		if "_danbele_" in authshort :
			addauthor(r"(Mukutari DANBELE|Mukutari Danbele)","1f8ea9bb-43b3-4c4f-8e8d-7275175cfd05")
			addauthor(r"(Bakari Danbɛlɛ|Bakari DANBƐLƐ)","56f2b63c-53ac-405a-aa7f-e0ee4341f809")
			addauthor(r"(Yaya Danbele|Yaya DANBELE)","fbfccca8-37b1-484c-a64d-9e2e81ad2832")
			addauthor(r"(ibɛrɛhima danbele|Ibɛrɛhima Danbele|Ibèrèhima Danbele)","a337a319-000c-43d3-91cf-f3364c45194a")
			addauthor(r"(Banuhun Danbɛlɛ|Banuhun DANBƐLƐ)","bede413a-a43f-4a5d-823c-cb208a12c96e")
			addauthor(r"(Bakaribilen Danbele|Bakari Bilen Danbele|Bakari Danbele|Bakari DANBELE|Bakari Damele|Bakaribilen Damele)","dda27c30-a372-4cdb-884b-2ac8667a1523")
			addauthor(r"(Lamini Danbele|Lamini DANBELE)","3a27a011-91c6-4007-9fec-a9884e791367")
			addauthor(r"(Isa Danbɛlɛ|Isa DANBƐLƐ|Isa Danbele|Isa DANBELE)","de2efafa-1e5b-4c9b-914d-fb876b7d40ba")
			addauthor(r"(Asimi Sulemani Danbele|Asimi Danbele|Asimi Sulemani DANBELE|Asimi DANBELE)","be3ded31-1088-438d-a691-7be6a5050071")
			if len(re.findall(r"(Tɛnenkun|Tɛnɛnkun|Tɛnɛkun|Moti)",tout,re.I|re.U))>0 :
				addauthor(r"(Musa Danbɛlɛ|Musa DANBƐLƐ)","0eb31712-30da-40fd-b5d5-de0fd7206d57")
			addauthor(r"(Alu Danbele|Alu DANBELE)","a247f27e-2921-4a9a-89cb-f3d5dd62685f")
		if "_darabo_" in authshort : addauthor(r"(Gawusu Darabo|Gawusu DARABO)","127f5500-c5db-4f87-8a33-d073d8430f02")
		if "_dawo_" in authshort :
			addauthor(r"(Dawuda Mace Dawo|Dawuda M\.Dawo|Dawuda M[\.]* Dawo|Dawudi Mace Dawo)","f0c85c3c-17d5-4af6-ab3e-28b8fd906fe4")
			addauthor(r"(Mori Dawo|Mori DAWO)","f76aed26-91f2-4ada-ba3d-5675ae3089aa")
		if "_denba_" in authshort : addauthor(r"(Bankɔ Denba|Bankɔ DENBA)","d2e216a8-bb57-48f9-90cc-be217d8872ef")
		if "_derilon_" in authshort: addauthor(r"(Zan-Piyɛri Dɛrilon|Zan-Piyɛri Dɛrilɔn|Zan Piyɛri Dɛrilon|Zan Piyɛri Dɛrilɔn)","3ac58000-b537-4e67-99f4-0c2e2a8606ce")
		if "_desoleri_" in authshort : addauthor(r"(Emanuwɛli Desolɛri|Emanuyɛli Desolɛri)","019284d6-dd4c-44ae-8bcf-ccfcbf7fa69a")
		if "_drabo_" in authshort : addauthor(r"(Gawusu Drabo|Gawusu DRABO)","127f5500-c5db-4f87-8a33-d073d8430f02")
		if "_dicko_" in authshort :
			addauthor(r"(Gamɛri Dicko|Gamɛri DICKO|Gamɛri A Dicko|Gamɛri A[\.]* Dicko|Gamɛri A. DICKO|G[\.]*A[\.]* Dicko|G[\.]* A[\.]* Dicko|Gameri A[\.]* DICKO|G[\.]*A[\.]* DICKO|Gamɛri Dikɔ|Gamɛri DIKƆ|Gamɛri A[\.]* Dikɔ|Gamɛri A Dikɔ|Gamɛri A[\.]* DIKƆ|G\.A[\.]* Dikɔ|G[\.]* A[\.]* Dikɔ|Gameri A[\.]* DIKƆ|G[\.]*A[\.]* DIKƆ)","d9195f9f-890f-4a0b-9a2e-166d7ea52f03")
			addauthor(r"(Mohamɛdi Dicko|Mohamɛdi DICKO)","f9d5c2b6-6699-44ea-9a2f-1bca0aeaaa28")
		if "_diko_" in authshort :
			addauthor(r"(Gamɛri Diko|Gamɛri DIKO|Gamɛri A Diko|Gamɛri A[\.]* Diko|Gamɛri A[\.]* DIKO|G[\.]*A[\.]* Diko|G[\.]* A[\.]* Diko|Gameri A[\.]* DIKO|G[\.]*A[\.]* DIKO|Gamɛri Dikɔ|Gamɛri DIKƆ|Gamɛri A[\.]* Dikɔ|Gamɛri A[\.]* DIKƆ|G\.A[\.]* Dikɔ|G[\.]* A[\.]* Dikɔ|Gameri A[\.]* DIKƆ|G[\.]*A[\.]* DIKƆ)","d9195f9f-890f-4a0b-9a2e-166d7ea52f03")
			addauthor(r"(Mohamɛdi Diko|Mohamɛdi DIKO)","f9d5c2b6-6699-44ea-9a2f-1bca0aeaaa28")
		if "_doho_" in authshort: addauthor(r"(Sidalamini Ag Doho|Sidalamin Ag Doho|Sidalamini Ag DOHO|Sidalamin Ag DOHO|Sidalamini AG DOHO|Sidalamine AG DOHO)","cdda5baa-288b-483d-8447-35bc6c5930f5")
		if "_dolo_" in authshort : addauthor(r"(Amagire Ogobara Dolo|Amagira Ogobara Dolo|Amagire Ogobara DOLO|Amagire O. Dolo|Amagire O. DOLO|A. O. Dolo|A. O. DOLO|Amagirɛyi O. DOLO|Ameyigara O. DOLO|Amayigara Ogobara Dolo|Amayigere Ogobara Dolo|Amagirɛyi Ogobara Dolo|Amagirɛyi Ogobara DOLO|Amadu Ogobara Dolo|A[\.]* Ogobara Dolo|A\.O\.D|Amagireyi Ogobara Dolo|Amagirayi Ogobara Dolo)","70301778-a09a-4593-ade3-7586f9588d30")
		if "_dukure_" in authshort :
			addauthor(r"(badama dukure|Badama Dukure|Badama DUKURE|Dadama Dukure|Baadama Dukure|Baadame Dukure)","8929d366-cfb6-4da7-a02f-1edea162b6e5")
			addauthor(r"(Mamadu Dukure|Mamadu DUKURE|M DUKURE)","c697fbc1-053d-476f-a523-ea55eaf2f986")
		if "_dunbiya_" in authshort:
			addauthor(r"(Amadu T Dunbiya|A T Dunbiya|A T DUNBIYA)","f3dde4e4-7f6a-4cba-bf2a-06fb0e752de0")
			# addauthor(r"(Amadu Tanba DUNBIYA|Amadu Tanba Dunbiya|A T Dunbiya|A Tanba Dunbiya|AMADU TANBA DUNBIYA)","587fb4ba-1385-4a2c-ab47-d60ed68d321b")
			addauthor(r"(Ayisata Jara Dunbiya|Ayisata JARA DUNBIYA|Ayisata Jara DUNBIYA)","ea8cc8b7-3fd3-4785-a8a0-9bb2361cb68b")
			addauthor(r"(Bɛnbabilen Dunbiya|Bɛnbabilen DUNBIYA|Dɛnbabilen Dunbiya)","ab3cda13-7007-4c2e-bd4b-570594555bbe")
			addauthor(r"(Fabu Dunbiya)","b97e7e65-dfef-4b44-b7c8-d3e0d2a7d9ac")
			addauthor(r"(Fantɔ Dunbiya|Fantò Dunbiya|Fantɔ DUNBIYA|Fantò DUNBIYA)","b14c2549-2cdc-44d0-9110-72e48bf5bd03")
			addauthor(r"(Mamadu Dunbiya)","1538e51f-7535-40c0-9bd4-e1bdafdfbec0")
			addauthor(r"(Musa Dunbiya|Musa DUNBIYA)","d12fe50b-c078-4b20-81c8-ac69948d134f")
			addauthor(r"(Seriba Dunbiya|Seriba DUNBIYA|Sɛriba Dunbiya|Sɛriba DUNBIYA)","7c3721fa-23d6-41ae-ab97-5526106f8947")
			addauthor(r"(Seyidu Dunbiya|Seyidu DUNBIYA)","b173ba16-ef7c-4e5c-b712-ef8e2622bf91")
			addauthor(r"(Sidiki Dunbiya|Sidiki DUNBIYA)","f1b5d53e-87be-4d3f-a9a2-d9894b7b63b8")
			addauthor(r"(Siyaka Dunbiya|Shaka Dunbiya|ʃaka Dunbiya|Saka Dunbiya|Siyaka DUNBIYA)","d969a0c7-4102-4d7a-8783-c242365f365d")
			addauthor(r"(Solomani Dunbiya|Solomani DUNBIYA)","ee44aa6e-1a01-45c2-9add-a1dad5026d62")
			addauthor(r"(Yusufu Dunbiya|Yusu Dunbiya|Yusufu DUNBIYA|Yusu DUNBIYA)",r"da8f0ed0-5365-4dd1-93f5-3f6afc0b7643")
			if periodique == "nyetaa":
				addauthor(r"(Berehima Dunbiya|Berehima DUNBIYA|berehima dunbiya|Berehima dunbiya|berehima Dunbiya)","b6e6aefc-a069-48d9-a166-039274684f50")
				addauthor(r"(B\. Dunbiya|B\. DUNBIYA|b\. dunbiya|B\. dunbiya|b\. Dunbiya)","b6e6aefc-a069-48d9-a166-039274684f50")
			elif periodique == "kibaru":
				addauthor(r"(Berehima Dunbiya|Berehima DUNBIYA|berehima dunbiya|Berehima dunbiya|berehima Dunbiya)","b6e6aefc-a069-48d9-a166-039274684f50")
			else:
				addauthor(r"(Burama Dunbiya|Burama DUNBIYA|B[\.]* Dunbiya|B[\.]* DUNBIYA|Burema Dunbiya|Burema DUNBIYA|Berema Dunbiya|Berema Dunbiya|Berehima DUNBIYA|Ibrahima Dunbiya)","ea10bbed-a078-460c-9874-02b1126a9323")
			
			

		if "_dunbuya_" in authshort:
			addauthor(r"(Amadu Tanba DUNBUYA|Amadu Tanba Dunbuya|A Tanba Dunbuya|A T Dunbuya|AMADU TANBA DUNBUYA|Amadu T Dunbuya|A T DUNBUYA|Amadou DUNBUYA NYUMANA)","587fb4ba-1385-4a2c-ab47-d60ed68d321b")
			addauthor(r"(Yusufu Dunbuya|Yusu Dunbuya|Yusufu DUNBUYA|Yusu DUNBUYA)",r"da8f0ed0-5365-4dd1-93f5-3f6afc0b7643")			
			addauthor(r"(Fabu Dunbuya)","b97e7e65-dfef-4b44-b7c8-d3e0d2a7d9ac")
			addauthor(r"(Solomani Dunbuya|Solomani DUNBUYA)","ee44aa6e-1a01-45c2-9add-a1dad5026d62")
			addauthor(r"(Bɛnbabilen Dunbuya|Bɛnbabilen DUNBUYA|Dɛnbabilen Dunbuya)","ab3cda13-7007-4c2e-bd4b-570594555bbe")
			addauthor(r"(Ayisata Jara Dunbuya|Ayisata JARA DUNBUYA|Ayisata Jara DUNBUYA)","ea8cc8b7-3fd3-4785-a8a0-9bb2361cb68b")
			if periodique == "nyetaa":
				addauthor(r"(Berehima Dunbuya|Berehima DUNBUYA|berehima dunbuya|Berehima dunbuya|berehima Dunbuya)","b6e6aefc-a069-48d9-a166-039274684f50")
				addauthor(r"(B\. Dunbuya|B\. DUNBUYA|b\. dunbuya|B\. dunbuya|b\. Dunbuya)","b6e6aefc-a069-48d9-a166-039274684f50")
				addauthor(r"(B Dunbuya|B DUNBUYA|b dunbuya|B dunbuya|b Dunbuya)","b6e6aefc-a069-48d9-a166-039274684f50")
			elif periodique == "kibaru":
				addauthor(r"(Berehima Dunbuya|Berehima DUNBUYA|berehima dunbuya|Berehima dunbuya|berehima Dunbuya)","b6e6aefc-a069-48d9-a166-039274684f50")
			else:
				addauthor(r"(Burama Dunbuya|Burama DUNBUYA|B[\.]* Dunbuya|B[\.]* DUNBUYA|Burema Dunbuya|Burema DUNBUYA|Berema Dunbuya|Berema DUNBUYA|Ibrahima Dunbuya)","ea10bbed-a078-460c-9874-02b1126a9323")
			
		if "_dumuya_" in authshort:
			addauthor(r"(Amadu Tanba DUMUYA|Amadu Tanba Dumuya|A Tanba Dumuya|A T Dumuya|AMADU TANBA DUMUYA|Amadu T Dumuya|A T Dumuya|A T DUMUYA)","587fb4ba-1385-4a2c-ab47-d60ed68d321b")
		if "_fane_" in authshort: 
			addauthor(r"(Mamadu Fane|Mamadu FANE|Mamadu Fanɛ)","4168de2f-8c3a-49bf-afd1-219d1ed04a1b")
			addauthor(r"(Yusufu F. Fanɛ|Yusufu Famori Fanɛ|Yusuf F. Fanɛ|Yusuf Famori Fanɛ|Yusufu Fanɛ|Yusufu FANƐ|Yusufu F. Fane|Yusufu F Fane|Yusufu Famori Fane|Yusufu - Famori Fane|Yusufu Fane|Yusuf F. Fane|Yusuf Famori Fane)","458db881-6de5-4039-b450-9914355c0130")
		if "_fonba_" in authshort: 
			addauthor(r"(Dirisa Fɔnba|Dirisa FƆNBA|Dirisa Fonba)","d381c752-e40c-4c6d-9cb1-60d48bc8697d")
			addauthor(r"(Amari Fɔnba|Amari FƆNBA|Amari Fonba)","f8cab50f-1bba-4b2f-aa0e-5a4d8df8f8fe")
			addauthor(r"(Basiru Fɔnba|Basiru FƆNBA)","53ef22ce-a19a-459c-a814-84ce03706231")
			addauthor(r"(Daramani Fɔnba|Daramani FƆNBA)","ea0a1dc6-84e8-4b7c-9a6d-20749c228103")
			addauthor(r"(Zankɛ Ngolo Fɔnba|Zankɛ Ngolo FƆNBA|Zankɛ Ŋɔlɔ Fɔnba)","b4ee46bb-ec0f-417a-a5c5-397024592b62")
			addauthor(r"(Seyidu Fɔnba|Seyidu FƆNBA)","c293de22-e96c-49f2-b87a-19e4a5e3f24d")
			addauthor(r"(Dajigi Fɔnba|Dajigi FƆNBA)","24b38883-3d2d-48d5-b9a4-a15db70c919f")
		if "_fofana_" in authshort : addauthor(r"(Aoua Fofana|Aoua FOFANA|Awa Fofana|Awa FOFANA)","c870475f-30c3-4939-951f-f0e6cfc4bb90")
		if "_gindo_" in authshort :
			addauthor(r"(Usmani Gindo|usumani Gindo|Usumani Gindo|Usumani Guido)","f96014e9-6a24-4735-9ffb-c9cdda74fe65")
			addauthor(r"(Adama Gindo|Adama GINDO)","83a06f3f-1435-4265-9037-a28eb8ab2203")
		if "_hageman_" in authshort : addauthor(r"(Teyo Hageman|Teyo HAGEMAN)","5bcc051c-e2c0-4dc4-857c-f33472e2d87c")
		if "_ja_" in authshort : addauthor(r"(Sɛku Amadu Ja|Seku Amadu Ja|Sɛku Amadu JA|Sɛki Amadu Ja|Sɛki Amadu JA|Sɛku A Ja|Seku A[\.]* Ja||Sɛku A[\.]* Ja|Sɛki A Ja|Sɛku A[\.]* JA|Sɛki A[\.]* Ja|Sɛki A[\.]* JA)","30e70086-e12b-4963-8f23-0572b81775f2")
		if "_jabate_" in authshort :
			addauthor(r"(Fuseni Jabate|Fuseyini Jabate|Fuseni JABATE|Fuseyini Jabate|Fuseyini JABATE|Fuseyini Jabatɛ|Fuseyini JABATE)","76c495a4-7706-4487-92c1-27be5fb4e943")
			addauthor(r"(Mariyamu F\.* Jabate|Mariyamu F\.* JABATE)","9bb50e39-6185-4783-811d-fb58f1235171")
		if "_jaabi_" in authshort :
			addauthor(r"(Musa Jaabi|Musa JAABI)","51652320-a88e-4b50-87f2-fc1b465a20a6")
			addauthor(r"(Laji M Jaabi|Laji M JAABI|Laji M[\.]* Jaabi|Laji M[\.]* JAABI)","2caf221a-1cac-403d-bc8d-5f9eedba920e")
		if "_jabate_" in authshort : addauthor(r"(Fuseni Jabate|Fuseni Jabatɛ)","76c495a4-7706-4487-92c1-27be5fb4e943")
		if "_jabi_" in authshort : addauthor(r"(Laji M[\.]* Jabi|Laji M[\.]* JABI|L[\.]* M[\.]* Jabi)","4c8159cd-a0e7-410c-85a9-ba505666abe1")
		if "_jakite_" in authshort : 
			addauthor(r"(solomani jakite|Solomani Jakite)","33f55de3-c1d0-4365-a13f-05e6360b8ed1")
			addauthor(r"(mamadu jakite|Mamadu Jakite|Mamadu JAKITE)","0b692d2a-a0fa-4adb-869d-8249580da079")
			addauthor(r"(Siyaka Jakite|Siyaka JAKITE|Saka Jakite|Shaka Jakite)","285fddae-a8f3-4d7d-b9b2-96e446ed57b2")
			addauthor(r"(Kalifa Jakite|Kalifa JAKITE|Kafila Jakite)","d28a755e-2674-4155-868e-97252d1c1b93")
			addauthor(r"(umaru jakite|Umaru Jakite|Umaru JAKITE)","4794ba48-cf05-4f90-8b04-622980a68523")
			addauthor(r"(yɔrɔ mɛnkɔrɔ jakite|Yɔrɔ Mɛnkɔrɔ Jakite|Yòrò Mènkòrò Jakite)","62918880-44b0-416b-a3d4-41f9e3261560")
			addauthor(r"(Jibirilu Kaba Jakite|Jibirili Kaba Jakite|Jibirilu Kaba JAKITE|Jibirili Kaba JAKITE)","2f06ff7f-30b8-44e8-a557-334c92c7aa56")
		if "_jalo_" in authshort : 
			addauthor(r"(Isa Jalo|Isa JALO|ISA JALO|Isa jalo|isa jalo)","9a336ead-63bd-4bac-88a4-e63fa83c8505")
			addauthor(r"(Shɛki U. Jalo|Shɛki U. JALO|Shɛki Umaru Jalo|Sɛki U[\.]* Jalo|Sɛki U[\.]* JALO|Sɛki U Jalo|Sɛki U JALO|Sɛki Umaru Jalo)","54c07225-8068-423c-bb92-ae94fea49f42")
			addauthor(r"(Sumayila Jalo|Sumɛyila Jalo|Sumayila JALO)","2f7e2bf4-7d5e-43df-93a5-057d50e3c5d4")
			addauthor(r"(Abdulayi Jalo|Abdulayi JALO)","c3fea918-60e2-4ad4-ac13-42f6713b1603")
			addauthor(r"(Daɲɛli Jalo|Danyɛli Jalo|Daɲɛli JALO)","ee15c979-1e11-46ac-87c1-04794c3039f4")
			addauthor(r"(Solomani Jalo|Solomani JALO|Solomani jalo)","be54d4e2-6f68-4e62-8802-95385ba6564b")
			addauthor(r"(Yusufu Jalo|Yusufu JALO|Yusuf Jalo)","04e64a0f-70c8-47e7-b887-09f1c67ce911")
			addauthor(r"(Haji Jalo|Haji JALO)","48ed0991-742d-40ae-918f-89b6a872e0a4")
			addauthor(r"(Burame Jalo|Burama JALO)","23b3606e-dd0f-438c-9dd0-3b3a1c788263")
			addauthor(r"(Abudulayi Jari Jalo|Abudulayi Jari JALO)","7294c787-7930-4f11-91cf-b6c6105d98dc")
			addauthor(r"(Madi Jalo|Madi Kaman Jalo|Madi Kama Jalo|Madi JALO|Madi Kaman JALO|Madi Kama JALO)","681992e8-df83-47ac-9367-89e98d9035f7")
			addauthor(r"(Amadu Umaru Jalo|Amadu Omaru Jalo|Amadu O[\.]* Jalo|Amadu O Jalo|Amadu Umaru JALO|Amadu U. Jalo)","7a7eddca-4f02-4546-8d40-8aa8095786da")
			if len(re.findall(r"(Ŋɔnɔ|Njila)",tout,re.I|re.U))>0 :
				addauthor(r"(Birama Jalo|Birama JALO|Burama Jalo|Burama JALO)","1523946b-357e-4363-81ac-80187f54da0a")
		if "_jama_" in authshort:
			addauthor(r"(Jedone Jama|Jedone JAMA)","ed12f97e-a186-472b-9881-a3a2362c4d0c")
		if "_jane_" in authshort : addauthor(r"(Sanba Janɛ|Sanba JANƐ)","61203b39-4a38-4d09-93f2-4ae74a3bd1be")
		if "_jara_" in authshort : 
			addauthor(r"(Abudaramani Jara|Abudaramani JARA|Abuduramani Jara|Abuduramani JARA)","deebae43-7984-4c82-b092-d3573d0c34cc")
			addauthor(r"(Adama Jara|Adama JARA)","d32c72aa-3711-46d4-a1e0-ff045f797f3e")
			addauthor(r"(Alu Jɛnfa Jara|Alu Jɛnfa JARA)","26910e4a-764c-427f-84de-721a50740b5a")
			addauthor(r"(Arafayɛli Balaba Jara|Arafayɛli Balaba JARA)","a2daaa29-e118-47e5-809e-e5ddc1fb10c5")
			addauthor(r"(Bakari Bilen Jara|Bakari Bilen JARA)","a0398a7a-251b-434d-be17-91e0ee1e233e")
			addauthor(r"(Bakayi Jara|Bakayi jara|Bakayi JARA)","34eb45e6-9e92-40c3-bf3a-90c7eb231fb6")
			addauthor(r"(Balaba Arafayɛli Jara|Balaba Arafayɛli JARA)","c8759b9a-b8ce-4ae5-8722-e1b2d724b085")
			addauthor(r"(Banba Jara|Banba JARA)","933dc36f-a46c-472b-9c4e-04747c214bdc")
			addauthor(r"(Bancini Siriman Daa Jara|Bancini Siriman Daa JARA|Bancinin Siriman Daa Jara|Bancinin Siriman Daa JARA)","ef8647e3-6c42-4c45-bb08-736ce7267d4f")
			addauthor(r"(Base Jara|Base JARA)","3e30b443-d581-4a8b-8da3-2570614da3dd")
			addauthor(r"(Bukari Jara|Bukari JARA)","2ff8615c-6ede-4b04-aa8f-c55f55842eb1")
			addauthor(r"(Cɛmɔgɔ Jara|Cɛmɔgɔ JARA)","706410a5-87d1-41e2-884a-39906854347c")
			addauthor(r"(Cɛsama Jara|Cɛsama JARA)","293cd531-0f0a-4b20-8c52-757604ff52c5")
			addauthor(r"(Dirisa Bakari Jara|Dirisa Bakari JARA)","266a0781-d80f-4f93-8885-fd28c4af344e")
			addauthor(r"(Dɔkala Yusufu Jara|Dɔkala Yusufu jara|Dɔkala Jara|Dokala Yusufu Jara|Dɔkala Yusuf Jara|Dɔkala Ysufu Jara|Dɔkala Yusufu JARA|Dɔkala Y Jara|Dɔkala Y[\.]* Jara|Dɔkala Y\.Jara|Dɔkala Y[\.]* JARA|Dɔkala Yusufu Diarra|D\.Y\.D|D\.Y\.J)","b5edd814-54dd-4058-bd8c-dae51a64427d")
			addauthor(r"(Fatumata Jara|Fatumata JARA)","178d8b60-2a1f-4de8-a7dc-5a0642fccd5b")
			addauthor(r"(Fuseni Jara|Fuseni JARA|Fuseyini Jara|Fuseyini JARA)","4bc8d117-344d-48c3-974e-49c5137abd82")
			addauthor(r"(Ibarahima baba Jara|Ibarahima Baba Jara|Iburahima Baba Jara|Iburuhima Baba Jara|Ibarahima Jara|Ibarahima JARA|Ibarayima Jara|Ibarayima JARA)","3b24a2db-71cb-43db-bf14-59ad4a4dcde3")
			addauthor(r"(Karimu Jara|Karimu JARA)","c98da45a-672e-497a-897a-ca110170cb2f")
			addauthor(r"(Kolankɔrɔ Faransuwa Jara|Kolankɔrɔ Faransuwa JARA|Kolankoro Faransuwa Jara|Kolankoro Farasuwa Jara)","08992fb1-cc75-4212-952e-39a5451dd68e")
			addauthor(r"(Kɔnba Jara|Kɔnba JARA)","fc81ac64-408e-449b-85cd-8cd4ae2fab25")
			addauthor(r"(Lasina Jara|Lasina JARA)","ce8e79df-fbd6-4932-9a6a-5a827677310a")
			addauthor(r"(Madujan Jara|Madujan JARA)","bbf0dd00-77bf-4e1e-b53a-d5f59ec73680")
			addauthor(r"(Mamadu Nyama Jara|mamadu nyama jara|Mamadu Ɲama Jara)","618af8da-1f81-414c-b049-a6a38c9d6c80")
			addauthor(r"(Mami Jara|Mami JARA)","0d4c13df-70b8-4683-a1f3-0c248b9d4cc7")
			addauthor(r"(Minabɛ Jara|Minabɛ JARA|Minabè Jara|Minabè JARA)","4ae33797-b128-4b4e-b19f-22f5ada38fee")
			addauthor(r"(Shaka Jara|Shaka JARA)","c9e74689-bedd-4331-ab78-31846fc977c1")
			addauthor(r"(Siyaka Jara|Siyaka JARA)","0eb7d85a-bbf5-496a-9126-c7fd261621a9")
			addauthor(r"(Soyibajan Jara|Soyiba Jara|Soyibajan JARA)","b225860b-9538-4504-aeca-b39750f1a1ea")
			addauthor(r"(Sumayila T. Jara|Sumayila T. JARA)","83db48cf-4e76-48c9-a3d0-24d06d56c8aa")
			addauthor(r"(Sɛbajan Jara|Sɛbajan JARA)","505c14cf-0ae0-4af7-b525-36293c852291")
			addauthor(r"(Usumani Jara|Usumani JARA)","1a596b70-23c8-45d8-b31e-517d6e44d41e")
			addauthor(r"(yaya jara|Yaya Jara|Yaya JARA)","fd800f25-d6ee-4b9f-b6f9-72c129183b79")
			addauthor(r"(Zan Dosayi Jara|Zan Dosaye Jara)","8bd6f254-0f03-4822-aef7-3792ac0b07e4")
			addauthor(r"(Ɲakalen Sakiliba|Ɲagalen Sakiliba|Jara Ɲakalen Sakiliba|Jara Ɲagalen Sakiliba|Ɲakalen SAKILIBA|Ɲagalen SAKILIBA)","164e4493-d7c4-4999-87ba-17b847fd9f14")
			addauthor(r"(Ɲofan Jara|Ɲofan JARA|Ɲɔfan Jara|Ɲɔfan JARA)","661deb8b-649c-406b-9244-01d2674c003d")
			if re.findall(r"(Tomina|Sofara)",endoftext,re.I|re.U) is not None :
				addauthor(r"(Solomani Jara|Solomani JARA)","2bc06452-9b5a-461b-ae0d-2504bde57dc6")
			if re.findall(r"(Nperesibugu|NPeresibugu|Npeseribugu|NPeseribugu|Masantola)",endoftext,re.I|re.U) is not None :
				addauthor(r"(Mamadu Jara|Mamadu JARA|Mamadou Jara)","dc81e9f8-e04a-4675-b98c-3b33b4a818ea")
			if re.findall(r"(Falo|Surakabugu|Bila)",endoftext,re.I|re.U) is not None :
				addauthor(r"(Daramani Jara|Daramani JARA)","04532ac2-8cd5-4b2b-a08a-25bdc3599a96")
			addauthor(r"(Fatɔgɔma Jara|Fatɔgɔma JARA)","9e957f7e-4ab4-4bd9-a3c7-376a39d24c96")
		if "_jawara_" in authshort : 
			addauthor(r"(Sɛkina Jawara|Sɛkina JAWARA)","6cf14142-7033-41a0-be64-86ca041058c0")
			addauthor(r"(Mohamɛdi D. Jawara|Mohamɛdi D Jawara|Mohamɛdi D. JAWARA|Mohamɛdi D JAWARA)","8182a385-8bc0-4c42-8537-ee8f493bc967")
			addauthor(r"(Mohamɛdi Z. Jawara|Mohamɛdi Z Jawara|Mohamɛdi Z. JAWARA|Mohamɛdi Z JAWARA)","451b08fe-05a4-42b6-b1f8-e3b0a1f6bfae")
			addauthor(r"(Mɔhamɛdi D. Jawara|Mɔhamɛdi D Jawara|Mɔhamɛdi D. JAWARA|Mɔhamɛdi D JAWARA)","8182a385-8bc0-4c42-8537-ee8f493bc967")
			addauthor(r"(Mɔhamɛdi Z. Jawara|Mɔhamɛdi Z Jawara|Mɔhamɛdi Z. JAWARA|Mɔhamɛdi Z JAWARA)","451b08fe-05a4-42b6-b1f8-e3b0a1f6bfae")
		if "_jigifa_" in authshort : addauthor(r"(F Jigifa D|F JIGIFA D|F\. Jigifa D\.|F\. JIGIFA D\.)","2b14c7e0-71c3-4db0-b169-d0201f58f40a")
		if "_jire_" in authshort : addauthor(r"(Dusu Jire|Dusu JIRE)","d2f0a2c2-d202-47a9-877e-ec52cfc694b7")
		if "_jopu" in authshort : addauthor(r"(Sira Jɔpu|Sira JƆPU)","a7245550-4df0-4cd7-a73a-a4d2a7f36fa1")
		if "_jumide_" in authshort : addauthor(r"(Adama Jumide|Adama JUMIDE)","f756fce8-0013-4b8d-b4cb-81bbf229038f")
		if "_junide_" in authshort : addauthor(r"(Adama Junide|Adama JUNIDE)","f756fce8-0013-4b8d-b4cb-81bbf229038f")
		if "_jimide_" in authshort : addauthor(r"(Adama Jimide|Adama JIMIDE)","f756fce8-0013-4b8d-b4cb-81bbf229038f")
		if "_jimude_" in authshort : addauthor(r"(Adama Jimude|Adama JIMUDE)","f756fce8-0013-4b8d-b4cb-81bbf229038f")
		if "_kaba_" in authshort : addauthor(r"(Mamadi Kaba|Mamadu Kaba|Mamadu KABA)","45856259-2685-4d35-b650-c8db3d5ae2d8")
		if "_kalanbiri_" in authshort : addauthor(r"(Alɛkisi Kalanbiri|Alex Kalanbiri)","ccf1c399-9fa6-4ebc-8887-f99759915bab")
		if "_kamara_" in authshort : 
			addauthor(r"(Usumani Kamara|Usumani KAMARA|Gigimasa)","5bb7d097-e967-4495-ab75-b71000624bcf")
			addauthor(r"(Fuseni Kamara|Fuseni KAMARA)","402a0dec-1044-4ef0-8f35-ac5430d10465")
		if "_kaminyan_" or "_kamiyan_" in authshort : 
			addauthor(r"(Usumani Kamiyan|Usumani Kamiɲan|Usumana Kamiɲan|Usumana A[\.]* Kamiɲan|Usumani A[\.]* Kamiɲan|Asumana Kamiɲan)","c90b8eb6-c045-4afa-9389-7253de5633b6")
		if "_kamisoko_" in authshort : 
			addauthor(r"(Musa Kamisɔkɔ|Musa KAMISƆKƆ)","a67a4acf-6dbe-4bc1-8e20-d32c4b613128")
			addauthor(r"(Seyibu S\.* Kamisoko|Seyibu S\.* KAMISOKO|Seyibu S\.* Kamisɔkɔ|Seyibu S\.* KAMISƆKƆ)","dafcb94c-f309-4383-a99a-66c848bd76b8")
		if "_kane_" in authshort : 
			addauthor(r"(Sumana Kane|Sumana KANE|Sumana Kanɛ)","11aefaf1-6d5b-4ffa-84c7-24a3edb32670")
			addauthor(r"(mari kanɛ|mari kanè|Mari Kanɛ|Mari Kanè)","d43907f8-d08b-4474-8bb3-1d6a55b15f1a")
			addauthor(r"(Musa Kanɛ|Musa Sayibu Kanɛ|Musa Sayidu Kanɛ|Musa Sayidu Kane|Musa KANƐ)","9f6f459c-99c5-45c9-b946-9487921c3193")
			addauthor(r"(Kaka Kanɛ|Kakɔ Kanɛ|Kakɔ KANƐ|Kakɔ kanɛ)","be3d7843-4ab1-4dfc-aa8c-583953f819de")
			addauthor(r"(Andere Kanɛ|Andere KANƐ)","56620715-802f-47d5-8fa1-73e3d9fe4960")
		if "_kante_" in authshort : 
			addauthor(r"(amadu ganyi kante|amadu ganyi kantè|Amadu Gaɲi Kantɛ|A. GAƝI Kante|A.G. Kante|A. G. Kante|A.G. KANTE|A.G.KANTE|A. G. KANTE|Amadu GANI Kante|Amadu GAƝI Kante|Amadu GAƝi Kante|Amadu GAƝI KANTE|Amadu Gaɲi Kante|Amadou Gaɲi Kante|Amadu G. Kante|Amadu G. KANTE|Amadu GANYI Kante|Amadu GAGNY Kante|Amadu Gagny Kante|Amadu Ganyi Kante|Amadu Gagny Kante|Amadu Gaɲi KANTE|Amadu G Kantɛ|Amadu G Kante|Amadu G KANTE)","797f3350-5147-480b-9ec5-4f7ccfe35139")
			addauthor(r"(Solomani Kantɛ|Solomani kantɛ|Solomani KANTƐ|solomani kantè)","dd718913-98f3-47aa-bce2-2fbffb72e317")
			addauthor(r"(Ibarahima Kante|Ibarahima KANTE)","40310b23-7d3e-4f67-98ba-8e48cbae36da")
			addauthor(r"(Mamadu Kanute|Mamadu Lamini Kanute|Mamadu KANUTE)","690f4a15-86cc-4381-9e81-f75dd9d6616d")
			addauthor(r"(Sitan Kante|Sitan KANTE)",r"5ed900fb-aa35-44ea-b2dd-01c114a61b12")
			addauthor(r"(Bubakari Kante|Bubakari KANTE)","7b682019-edc9-4f84-a86c-b033464bc882")
		if "_kanute" in authshort:
			addauthor(r"(Mamadu Lamini Kanute|Mamadu Laminn Kanute|M L Kanute|M L Kanutɛ|M L KANUTE|M-L\. KANUTE|Mamadu Laminn KANUTE|MAMADU LAMINI KANUTE|Mamadu L\. Kanute|Mamadu L Kanute|Mamadu Lamini KANUTE|Mamadu L\. KANUTE|Mamadu L KANUTE)","690f4a15-86cc-4381-9e81-f75dd9d6616d")
		if "_katile_" in authshort :
			addauthor(r"(Ali Katile|Ali KATILE)","c8782283-cb18-4b9b-a13b-57443fa2c707")
		if "_keta_" in authshort : addauthor(r"(Kaka Keta|Kaka KETA|Kakɔ Keta)","ca803960-fb84-4ca3-b5cc-5afb5472b081")
		if "_keyita_" in authshort : 
			addauthor(r"(Ani Mari Keyita|Ani Mari KEYITA|Ani-Mari Keyita|Ani-Mari KEYITA|Anni Mari Keyita|Anni Mari KEYITA)","002efa82-7a41-492e-8d7c-9a645d775275")
			addauthor(r"(Bobo Keyita|Bobo KEYITA)","b4933759-38fd-46bd-b7f5-6c5ab6faeb1e")
			addauthor(r"(Burama Keyita|Burama KEYITA)","10ac9abb-84d2-40f7-970e-eaa691975029")
			addauthor(r"(Dawuda Moriba Keyita|Dawuda Moriba keyita|Dawuda Moriba KEYITA|Dawuda Keyita|Dawuda KEYITA)","5e81a35c-c026-408e-8680-ca4ea0d8d222")
			addauthor(r"(Fatumata Keyita|Fatumata KEYITA)","3b81d000-6833-49c5-8ab4-5c8062f8b6fc")
			addauthor(r"(Gabukɔrɔ Keyita|Gabukòrò Keyita)","84a8d118-b713-41a4-9ed5-16a51f4aba6f")
			addauthor(r"(Madiba Keyita|Madiba KEYITA)","66b29102-5b8c-4edd-81ec-888d2307faa2")
			addauthor(r"(Mamadi Keyita|Mamadi KEYITA)","cef226df-486e-4d6d-a3cb-118053c436f6")
			addauthor(r"(Maman Keyita|Maman KEYITA|Manan Keyita)","33a9e28c-37f8-47ac-ae88-b8b67b4da526")
			addauthor(r"(Sanbali Keyita|Sanbali KEYITA)","c5b0ce30-9673-49ec-8759-05c357c665ee")
			addauthor(r"(Siyaka Keyita|Siyaka KEYITA|Lawale S\. Keyita|Lawale S\. KEYITA)","c1b4b374-8939-4257-a10f-0d67b1321e68")
			if len(re.findall(r"(Kucala|Akademi|Poyi)",tout,re.I|re.U))>0 :
				addauthor(r"(Burema Keyita|Burema KEYITA|Burama Keyita|Burama KEYITA)","4dedc8fc-cc66-4982-b24b-851d31e7b315")
			
		if "_komagara_" in authshort : addauthor(r"(Jiki Komagara|Jiki KOMAGARA|Jigi Komagara|Jigi KOMAGARA)","4b4d9826-8885-4fcd-92fc-2ff651a0b23e")
		if "_komakara_" in authshort : addauthor(r"(Jiki Komakara|Jiki KOMAKARA|Jigi Komakara|Jigi KOMAKARA)","4b4d9826-8885-4fcd-92fc-2ff651a0b23e")
		if "_konare_" in authshort : 
			addauthor(r"(Sɛku Umaru Konarɛ|Sɛku Umaru KONARƐ|Sɛku Umaru Konare|Sɛku Umaru KONARE|Seku Umaru Konarɛ)","6a32364d-24d6-485e-bd70-0e352ea5c775")
			addauthor(r"(Dɛnba Konare|Dènba KONARE|Dènba Konare|Demba Konare|demba konare|Demba KONARE|Denba Konare|denba konare|Denba KONARE)","b7da1872-49a6-49e4-a6e7-3607e801d3dc")
		if "_konate_" in authshort :
			addauthor(r"(Hamidu Konate|Hamidu KONATE)","c7fa01a9-6428-4d30-bfed-426ea69618ba")
			addauthor(r"(Bafa Konate|Bafa KONATE)","810eea23-edfc-43e6-be9f-6996061f86da")
			addauthor(r"(Aba Konate|Abu Konate|Aba KONATE|Abu KONATE)","e571c226-1abd-4125-9466-ec5eea8465e7")
			addauthor(r"(Mamari Konate|Mamari KONATE|Mamari Konatɛ)","0d6ecc27-bedd-421b-ab01-24dbffa6ba58")
		if "_kone_" in authshort : 
			addauthor(r"(Alu Kɔnɛ|Alu KƆNƐ|alu kɔnɛ|alu kònè)","2246823e-f72a-48b5-b593-f215a321b963")
			addauthor(r"(Bakari Kɔnɛ|Bakari KƆNƐ)","cb16231a-ac28-474d-b82d-075d4e254e76")
			addauthor(r"(Sisela Mayimuna Kɔnɛ|Sisela Mayimuna KƆNƐ)","aa1a73cb-f9a9-497b-82a5-c33feee93bf5")
			addauthor(r"(Musa Kɔnɛ|Musa KƆNƐ)","856e0687-0fb1-4469-8a46-0fa11fa9031d")
			addauthor(r"(Mariyamu Kɔnɛ|Mariyamu KƆNƐ)","41022526-703d-417b-b547-8633f27b34fa")
			addauthor(r"(Mamadu Kɔnɛ|Mamadu KƆNƐ)","f006e0f5-2ef1-4fd5-bf0b-0d1bfc707bd1")
			if len(re.findall(r"(LPK)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Mohamɛdi Kɔnɛ|Mohamɛdi KƆNƐ)","9aa67a0a-c57a-40f2-b3ad-ff5c89579f30")
			elif len(re.findall(r"(Ɲɔrɔn)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Mohamɛdi Kɔnɛ|Mohamɛdi KƆNƐ|Mohamɛdi KONƐ|Mohamɛdi KONE|M ohamɛdi kɔnɛ|mohamɛdi kɔnɛ|mohamèdi kònè)","17e50ef6-e4ef-4373-a3bc-6b9fa536bfea")
		if "_konta_" in authshort : addauthor(r"(Mahamadu Konta|Mahamadu Kɔnta|Mahamudu Kɔnta|Mamadu Kɔnta|Mohamadu Kɔnta|Mahamadu kɔnta|Mahamaddu Kɔnta|Mahamadu KONTA|Mahamadu KƆNTA|M[\.]* Kɔnta)","c742b89a-fdfb-4d5c-9868-690d9935fa18")
		if "_koyita_" in authshort : addauthor(r"(Mamutu Koyita|Mamutu KOYITA)","28d9c899-66f1-4df4-9dc2-d4b95f4d01f2")
		if "_kulibali_" in authshort:
			addauthor(r"(Seyibane Kulibali|Seyibane KULIBALI|Sekibane Kulibali|Sekibane KULIBALI|seyibane Kulibali)","d783d9b9-fbdc-4bc8-9909-63c38db4cd16")
			addauthor(r"(Nɛgɛta Kulibali|Nɛgɛta KULIBALI|Negeta Kulibali|nègèta kulibali|Negeta KULIBALI)","c6563397-b2fb-465b-8c84-98ff0740b9ca")
			addauthor(r"(basiru kulibali|Basiru Kulibali|Basiru KULIBALI)","b3d03481-2736-4a65-ae48-446097e97c31")
			addauthor(r"(Daniyɛli Kulibali|Daniyɛli KULIBALI)","7faf5c2d-3602-4af6-b4f5-d1b8a11e0ed6")
			addauthor(r"(Fanta Kulibali|Fanta KULIBALI)","6018c6bd-cad4-4354-bcb9-6327a9d28f37")
			addauthor(r"(Kamatigi Kulibali|Kamatigi KULIBALI)","db7cdd2a-d0bf-4008-885a-e97338a91b83")
			addauthor(r"(Amidu Kulibali|Amidu KULîBALI)","383c85d5-9d08-4d6f-b5e5-fd985a317d8e")
			addauthor(r"(Nuhum Legaran Kulibali|Nuhun Legaran Kulibali|Nuhun Legaran KULIBALI)","3e8412ad-afe1-48bf-b5c6-9321452cb2f5")
			if len(re.findall(r"(Basiriki Ture|Basiriki TURE)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Bakari Kulibali|Bakari KULIBALI)","89ed90eb-b923-4513-a856-1eecab6eed52")
			if len(re.findall(r"(Mahamadu Konta|Mahamadu Kɔnta|Mamadu Kɔnta|Mohamadu Kɔnta|Mahamadu kɔnta|Mahamaddu Kɔnta|Mahamadu KONTA|Mahamadu KƆNTA|M. Kɔnta)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Bakari Kulibali|Bakari KULIBALI)","89ed90eb-b923-4513-a856-1eecab6eed52")
			addauthor(r"(A J Kulibali|J A Kulibali|J A KULIBALI|Adama Jokolo Kulibali|Jokolo Adama \(Kulibali\)|Jokolo Adama Kulibali|Jokolo Adama KULIBALI|Jokolo A.* Kulibali|Jokolo A.* KULIBALI)","d8f41ebb-bd6a-4314-af91-0494469ab6da")
		if "_kulibaly_" in authshort:
			addauthor(r"(Fanta Kulibaly|Fanta KULIBALY)","6018c6bd-cad4-4354-bcb9-6327a9d28f37")
		if periodique=="jekabaara" and "_kulubali_" in authshort:
			addauthor(r"(Bubakari Kulubali|Bubakari kulubali|Babakari Kulubali|B. Kulubali|B.Kulubali)","4c6bc903-6586-44b8-91fb-6a4764a5f20e")
		if periodique=="jekabaara" and "_kulibali_" in authshort:
			addauthor(r"(Bubakari Kulibali|Bubakari kulibali|B. Kulibali|B.Kulibali)","4c6bc903-6586-44b8-91fb-6a4764a5f20e")		
		if "_kulubali_" in authshort:
			# Bubakari : il y en a trop !
			#addauthor(ur"(mamadu kulubali|Mamadu Kulubali)",u"7389e900-8214-4516-9ba1-b8b403708d7c")
			addauthor(r"(Seyibane Kulubali|Seyibane KULUBALI|Sekibane Kulubali|Sekibane KULUBALI)","d783d9b9-fbdc-4bc8-9909-63c38db4cd16")
			addauthor(r"(Abudu Kadiri Kulubali|Abuduli Kadiri Kulubali|Abudulu  Kadiri Kulubali|Abudu Kadiri KULUBALI|Abuduli Kadiri KULUBALI)","8fbac72c-f6e8-428f-ae40-26e892371652")
			addauthor(r"(Amidu Kulubali|Amidu KULUBALI)","383c85d5-9d08-4d6f-b5e5-fd985a317d8e")
			addauthor(r"(amidu kulubali|Amidu Kulubali|Amidu kulubali|Amidu KULUBALI)","383c85d5-9d08-4d6f-b5e5-fd985a317d8e")
			addauthor(r"(basiru kulubali|Basiru Kulubali|Basiru KULUBALI)","b3d03481-2736-4a65-ae48-446097e97c31")
			addauthor(r"(Bayi Kulubali|Bayi KULUBALI)","cb438776-e9e5-45eb-b1ae-dabe13fd783d")
			addauthor(r"(Berema Kulubali|Berema KULUBALI|Berehima Kulubali|Berehima KULUBALI)","488b7942-b5fc-44a7-b11a-fca3813d6f74")
			addauthor(r"(Daniyɛli Kulubali|Daniyɛli KULUBALI|Daniyɛli kulubali)","7faf5c2d-3602-4af6-b4f5-d1b8a11e0ed6")
			addauthor(r"(dɛnba kulubali|Dɛnba Kulubali|Dɛnba KULUBALI)","6ccb4659-2010-4a22-bff8-ef8a0786264d")
			addauthor(r"(Dose KULUBALI|Dose Kulubali)","6b1e6f70-06ab-4735-a8f6-4ce52795bcc1")
			addauthor(r"(Fanta Kulubali|Fanta KULUBALI)","6018c6bd-cad4-4354-bcb9-6327a9d28f37")
			addauthor(r"(Fode Kulubali|Fode KULUBALI)","e4ff0b2e-48d8-4b8e-82b4-f097469f2a1a")
			addauthor(r"(Ishaka Kulubali|Ishaka KULUBALI)","da6c2aee-5407-414e-a5e4-55d38a3422de")
			addauthor(r"(Kamatigi Kulubali|Kamatigi KULUBALI)","db7cdd2a-d0bf-4008-885a-e97338a91b83")
			addauthor(r"(Kasumu Kulubali|Kasumu KULUBALI)","ff4425e9-b500-48aa-95e8-a07691395e72")
			addauthor(r"(mamadu kulubali|Mamadu Kulubali|M. KULUBALI|M. Kulubali)","b21d1a28-e4a2-4f91-b1d8-33cff629718e")
			addauthor(r"(mamutu kulubali|Mamutu Kulubali|Mamutu KULUBALI)","e8f27ff7-9e60-454e-ac4b-bc56bf679713")
			addauthor(r"(modibo kulubali|Modibo Kulubali)","b8c824dd-40ed-46b3-939d-0687fd3415fd")
			addauthor(r"(moriba kulubali|Moriba Kulubali|Moriba KULUBALI|Mɔriba KULUBALI)","8980ff6b-0155-40bc-88e3-0d5f2650e9d4")
			addauthor(r"(Musa Numukɛba Kulubali|Musa Numukɛba KULUBALI)","b2e1c18f-0369-49b0-8f51-610d492dd521")
			addauthor(r"(Mɔrikɛ Kulubali|Mɔrikɛ KULUBALI)","6c5e9b5e-6873-4141-9e5a-c829f4591aad")
			addauthor(r"(nɛgɛta kulubali|Nɛgɛta Kulubali|Nɛgɛta KULUBALI|Negeta Kulubali|nègèta kulubali|Negeta KULUBALI)","c6563397-b2fb-465b-8c84-98ff0740b9ca")
			addauthor(r"(Shaka Kulubali|Shaka KULUBALI|Ishaka Kulubali)","325e54ef-30c7-4710-8f60-3bed25d90df9")
			addauthor(r"(Sidiki Kulubali|Sidiki, KULUBALI)","a9493165-392c-4dd6-9b4c-1fb3d668ae68")
			addauthor(r"(Siratiki Kulubali|Siratigi Kulubali)","a664260d-90d0-4271-a109-87051896c49a")
			addauthor(r"(Sumayilakɛ Kulubali|Sumayilakɛ Majan Kulubali|Sumayilakɛ KULUBALI)","43ab5bcd-4d2d-4193-83d5-aa70499f20b2")
			addauthor(r"(Umaru Kulubali|Umaru KULUBALI)","f59418f3-ea40-42cb-a742-c128bcc2e4f6")
			addauthor(r"(Usumani Kulubali|Usumani kulubali|Usumani KULUBALI)","c8c9fe81-d9e1-4d6b-a328-39b0616c19cd")
			addauthor(r"(Wena Kulubali|Wena KULUBALI|Wana Kulubali|Wana KULUBALI)","14709b7a-9e23-4d04-891e-53b8196b4ac3")
			addauthor(r"(Zan Kulubali|Zan KULUBALI)","6bc78d41-ccf8-4c78-9ff9-ed66f5b25acd")
			addauthor(r"(Ɲankile Solomani Kulubali|Ɲankile Solomani KULUBALI)","cbf0128f-e8f4-4756-8198-d71beb940a27")
			addauthor(r"(Ibarahimu Sori Kulubali|Ibarahimu Sori KULUBALI|Iburahima Sori Kulubali|Ibarahima Sori Kulubali|Ibarahimu S[\.]* Kulubali|Ibarahimu S Kulubali|Sori Ibarahimu Kulubali|Sori Ibarahima Kulubali|Sori Iburahima Kulubali|Sori I[\.]* Kulubali|Sori I Kulubali|Sori Ibarahimu KULUBALI)","a489f1e4-c3dd-44ff-b7b0-16910e1e5708")
			addauthor(r"(Ayisata Kulubali|Ayisata KULUBALI)","20c3ff95-8ed5-44a6-82d0-ec144bba8342")
			addauthor(r"(A J Kulubali|J A Kulubali|J A KULUBALI|Adama Jokolo Kulubali|Jokolo Adama \(Kulubali\)|Jokolo Adama Kulubali|Jokolo Adama KULUBALI|Jokolo A.* Kulubali|Jokolo A.* KULUBALI)","d8f41ebb-bd6a-4314-af91-0494469ab6da")
			if len(re.findall(r"(Dɔribugu|Dɔribuguni|Dɔribugunin)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Solomani Kulubali|Solomani KULUBALI)","39c08e0e-557a-43b3-8c27-cc8a51b531d4")
			#testf=re.findall(ur"(Basiriki Ture|Basiriki TURE)",endoftext,re.I|re.U)
			#print "testf (Basiriki Ture|Basiriki TURE) : ",testf,len(testf)
			if len(re.findall(r"(Basiriki Ture|Basiriki TURE)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Bakari Kulubali|Bakari KULUBALI)","89ed90eb-b923-4513-a856-1eecab6eed52")
			if len(re.findall(r"(Mahamadu Konta|Mahamadu Kɔnta|Mamadu Kɔnta|Mohamadu Kɔnta|Mahamadu kɔnta|Mahamaddu Kɔnta|Mahamadu KONTA|Mahamadu KƆNTA|M. Kɔnta)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Bakari Kulubali|Bakari KULUBALI)","89ed90eb-b923-4513-a856-1eecab6eed52")
			if len(re.findall(r"(Basiriki Ture|Basiriki TURE)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Bubakari Kulubali|Bubakari KULUBALI)","2eaff45e-72e4-4a4f-9818-736066292cd7")
			if len(re.findall(r"(Tigina|Falo)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Musa Kulubali|Musa KULUBALI)","27e565c1-0842-4f0e-9294-b64892915a1e")
			addauthor(r"(Nuhum Legaran Kulubali|Nuhun Legaran Kulubali|Nuhun Legaran KULUBALI)","3e8412ad-afe1-48bf-b5c6-9321452cb2f5")
			if len(re.findall(r"(Dɔkala Yusufu Jara|Dɔkala Yusuf Jara|Dɔkala Yusufu JARA|Dɔkala Y. Jara|Dɔkala Y. JARA)",endoftext,re.I|re.U))>0 or len(re.findall(r"(Mahamadu Konta|Mahamadu Kɔnta|Mamadu Kɔnta|Mohamadu Kɔnta|Mahamadu kɔnta|Mahamaddu Kɔnta|Mahamadu KONTA|Mahamadu KƆNTA)",endoftext,re.I|re.U))>0:
				addauthor(r"(Bakari Kulubali|Bakari KULUBALI)","89ed90eb-b923-4513-a856-1eecab6eed52")
			if len(re.findall(r"(Marena|Fuladugu)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Abudu Kadiri Kulubali|Abudu Kadiri KULUBALI|Abudulayi Kulubali|Abuduli Kulibali|Abudulu Kulubali)","8fbac72c-f6e8-428f-ae40-26e892371652")
			if len(re.findall(r"(Moti|Ofisiri)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Daramani Kulubali|Daramani KULUBALI)","7a2a3eab-a49d-49e7-b32d-d7f7de536802")

		if "_kulubaly_" in authshort:
			addauthor(r"(Fanta Kulubaly|Fanta KULUBALY)","6018c6bd-cad4-4354-bcb9-6327a9d28f37")
		if "_kumare_" in authshort :
			addauthor(r"(Siyaka Kumarɛ|Siyaka Kumare|Siyaka kumare|Siyaka KUMARƐ)","9d1ff4e3-f4a1-4bf4-8362-cdded032939a")
			addauthor(r"(Saliya Kumare|Saliya KUMARE|Saliya Kumarɛ)","00c754da-7876-4f39-a637-104e43abe2db")
			addauthor(r"(Kɛlifa Kumarɛ|Kɛlifa KUMARƐ)","ff6cdb65-5f30-4655-be83-47b9f815c43c")
		if "_kuyate_" in authshort: 
			addauthor(r"(Seku Umaru Kuyate|Seku Umaru KUYATE)","fc1dc8e6-531e-415b-a3e0-a69ffb6f1f5d")
			addauthor(r"(Siriman Kuyatɛ|Siriman KUYATƐ)","b9cfc70d-6603-4027-bc84-75752f2327b0")
		if "_labeyi_" in authshort : addauthor(r"(Antuwani Labeyi|Antuwani Labɛyi|Antuwani LABEYI)","11d8a814-adbc-4ad6-892d-0e179d435575")
		if "_lam_" in authshort : addauthor(r"(A[\.]* Lam|A Lam|A[\.]* LAM|A LAM|Alayi Lam|Alayi LAM)","ebb0c747-5e5e-41e8-baa0-c780bab4598e")
		if "_lamu_" in authshort : addauthor(r"(A[\.]* Lamu|A Lamu|A[\.]* LAMU|A LAMU|Alayi Lamu|Alayi LAMU)","ebb0c747-5e5e-41e8-baa0-c780bab4598e")
		if "_leplaideur_" in authshort : addauthor(r"(Marie-Agnès Leplaideur|Marie Agnès Leplaideur|Marie Agnès Leplaideur)","2c0367fd-a997-4609-8806-000921e35d18")
		if "_lepilederi_" in authshort : addauthor(r"(Mari Aɲɛsi Lepiledɛri|Marie-Agnès Leplaideur|Marie Agnès Leplaideur|Marie Agnès Leplaideur)","2c0367fd-a997-4609-8806-000921e35d18")
		if "_linari_" in authshort : addauthor(r"(Andere Linari|Andere LINARI|Anderi Linari|André Linard)","c16bb794-a892-4b97-956d-f7773f125238")
		if "_linaridi_" in authshort : addauthor(r"(Andere Linaridi|Andere LINARIDI|Anderi Linaridi|André Linard)","c16bb794-a892-4b97-956d-f7773f125238")
		if "_magiraga_" in authshort : addauthor(r"(Mahamadu Magiraga|Mahamadu MAGIRAGA)","71c91448-4c9e-4a70-80e6-36b4b3f8a7e3")
		if "_mariko_" in authshort : addauthor(r"(yaya mariko|Yaya Mariko|Yaya Marikɔ|Yaya mariko|Yaya MARIKO)","b746f073-4777-465a-8ee4-0276592cfb09")
		if "_mayiga_" in authshort : 
			addauthor(r"(bulkadèri mayiga|Bulkadèri Mayiga|Bulkadɛri Mayiga)","6a1ab6fb-203c-4ef6-83a5-e020afcf9b92")
			addauthor(r"(fatumata mayiga|Fatumata Mayiga|Fatumata MAYIGA)","79a71680-67a1-44be-a693-f88bb3b5dc49")
			addauthor(r"(Mahamani A. Mayiga|Mahamane Mayiga)","24d50126-b321-4288-9bca-c670c9142825")
			addauthor(r"(Amadu B*\.* *Mayiga|Amadu B*\.* *MAYIGA)","a72cd85a-0818-41d7-ac11-b17a9944c5e3")

		if "_maajuu_" in authshort: addauthor(r"(Suleyimani Sadi Maaju|Suleyimani Sadi MAAJU)","9d65b58a-4107-49d6-9595-5c8f5387e86a")
		if "_masu_" in authshort: addauthor(r"(Suleyimani Sadi Masu|Suleyimani Sadi MASU)","9d65b58a-4107-49d6-9595-5c8f5387e86a")
		if "_maazu_" in authshort: addauthor(r"(Suleyimani Sadi Maazu|Suleyimani Sadi MAAZU)","9d65b58a-4107-49d6-9595-5c8f5387e86a")
		if "_mazu_" in authshort: addauthor(r"(Suleyimani Sadi Mazu|Suleyimani Sadi MAZU)","9d65b58a-4107-49d6-9595-5c8f5387e86a")
		if "_menta_" in authshort : addauthor(r"(Suleyimani Mɛnta|Solomani Mɛnta|solomani mɛnta|solomani mènta)","63b70297-b35e-4b1f-b5df-27fcc6dec7a5")
		if "_morilaka_" in authshort : addauthor(r"(Morilaka|MORILAKA|morilaka)","d25848f6-5f45-46f5-9a72-4d92d09b8459")
		if "_nafo_" in authshort : addauthor(r"(F[\.]* Nafo|Fatumata Nafo|Fatuma Nafo|Fatumata NAFO)","486d185e-79f1-492d-82e3-b48d12a2420a")
		if "_ndawo_" in authshort : addauthor(r"(Dawuda Mace Ndawo|Dawuda M\.Ndawo|Dawuda M[\.]* Ndawo)","f0c85c3c-17d5-4af6-ab3e-28b8fd906fe4")
		if "_nforigangi_" in authshort : addauthor(r"(Sarili Nforigangi|Sarili Nfɔrigangi|Sarali Nforigangi|Sarali Nfɔrigangi)","a8f7a213-4345-4db6-9377-a2e939f1ce8a")
		if "_nforigani_" in authshort : addauthor(r"(Sarili Nforigani|Sarili Nfɔrigani|Sarali Nforigani|Sarali Nfɔrigani)","a8f7a213-4345-4db6-9377-a2e939f1ce8a")
		if "_nguessan_" in authshort : addauthor(r"(Raphaül N'Guessan|Raphaül N'Guessan|Raphaul N'Guessan|Raphaül N'GUESSAN|Raphaül N'GUESSAN|Raphaul N'GUESSAN)","fa8b3c83-db30-4fdf-951e-b7cb058956b7")
		if "_nyani_" in authshort or "_nani_" in authshort : addauthor(r"(Umaru Nani|Umaru Ɲani|Umaru ƝANI)","e3f6c7e4-2f76-459c-a4e9-c4702b6bd970")
		if "_nyare_" in authshort : 
			addauthor(r"(Meydi Ɲare|Medi Ɲare|Meydi ƝARE|Medi ƝARE)","e6be7efc-34a4-4c76-a77a-d2ddcc10e56d")
			addauthor(r"(Dɔkɔtɔrɔ Ɲare|Dɔkɔtɔrɔ Ɲarɛ|Dɔgɔtɔrɔ Ɲare|Dɔgɔtɔrɔ Ɲarɛ|Bubakari Ɲarɛ|Bubakari ƝARƐ|Bubakari Ɲare|Bubakari ƝARE)","dd3adc4e-2fc9-49ea-8216-87834898be2b")
		if "_pero_" in authshort : addauthor(r"(Kilemansi Peti Pero|Kilemansi PETI PERO)","4f423cd1-fb18-43c7-91b7-a0b7930f5ea8")
		if "_petipero_" in authshort : addauthor(r"(Kilemansi Peti-Pero|Kilemansi Peti-pero|Kilemansi PETI-PERO)","4f423cd1-fb18-43c7-91b7-a0b7930f5ea8")
		if "_sakiliba_" in authshort : 
			# "Sakiliba, Jara Ɲakalen/Ɲagalen",,f,,,Bambara,"ka bɔ Surukun Gangaran, Tukɔtɔ komini na Kita - kib416 2006 - kib422 2007 - kib436 2008 - kib471 2011 - kib490 2012",164e4493-d7c4-4999-87ba-17b847fd9f14
			addauthor(r"(Ɲakalen Sakiliba|Ɲagalen Sakiliba|Jara Ɲakalen Sakiliba|Jara Ɲagalen Sakiliba|Ɲakalen SAKILIBA|Ɲagalen SAKILIBA)","164e4493-d7c4-4999-87ba-17b847fd9f14")
		if "_sako_" in authshort : 
			addauthor(r"(Zan Sakɔ)","06083e70-ee05-42af-ba8e-410a3ed82a76")
			addauthor(r"(Dotege Sako|Dotigi Sako|Dotege SAKO)","b213ebbb-fcaa-48ec-9fb3-0a5cb50351da")
			addauthor(r"(Bayini Sakɔ|Bayini SAKƆ|Bayeni Sakɔ|Bayeni SAKƆ)","bbe65bf3-159f-4512-846b-1fa091a53fe2")
			if len(re.findall(r"(Echos)",endoftext,re.I|re.U))>0 or len(re.findall(r"(Fane)",endoftext,re.I|re.U))>0:
				addauthor(r"(Idirisa Sakɔ|Dirisa Sakɔ|Idirisa Sako|Dirisa Sako|Idirisa Saakɔ|Dirisa Saakɔ)","40ce8d8a-1bd7-4c61-add9-270600972af8")

		if "_sali_" in authshort : addauthor(r"(Yoro Sali|Yɔrɔ Sali|Yɔrɔ SALI|Yoro SALI)","69db573b-4c1f-4962-b1f1-bdf133453214")
		if "_samake_" in authshort : 
			addauthor(r"(Nanse Samake|Nanse SAMAKE|Ɲanse SAMAKE|Ɲanze SAMAKE|Ɲanze Samake|Zanze Samake|Nanse Samakɛ|Nanse SAMAKƐ|Ɲanse SAMAKƐ|Ɲanze SAMAKƐ|Ɲanze Samakɛ|Zanze Samakɛ)","2030b450-3a6b-49ed-83b9-5799e1c97c15")
			addauthor(r"(Sidi Lamini Samake|Sidi Lamini Samakɛ)","e4cac73a-9de6-497a-b977-96a700bedf01")
			addauthor(r"(Zan Samake|Zan Samakɛ)","5851ab7f-f669-487c-9ba8-d03577181a1d")
			addauthor(r"(Dawuda Jinɛmusa Samake|Dawuda jinɛmusa Samake|Dawuda, ko jinɛmusa Samake)","2a32f60e-253f-49bf-ad87-02a261f6ed52")
			addauthor(r"(Bubakari Sangare|Bubakari SANGARE)","6db84d53-f9ac-472a-9926-2deb1fdfe0ca")
			addauthor(r"(Fasun Idirisa Samake|Fasun Samake|Fasun Idirisa SAMAKE)","9fec18a6-f4e7-43c0-b93e-fd6e43e90454")
			addauthor(r"(Dominiki Samakɛ|Dominiki SAMAKƐ)","2afd56a9-b4c1-4f2b-a34f-3c0849909f36")
		if "_sangare_" in authshort : 
			addauthor(r"(Adama Dawuda Sangare|Adama Dawuda SANGARE)","65b9b944-f1a7-4973-a52d-0c30a1ce87c1")
			addauthor(r"(Bakari Sangare|Bakari sangare|Bakari SANGARE|Bakary Sangare)","1cacb7c3-5fc9-4020-bffc-4f2f60bd30ef")
			addauthor(r"(Dirisa Sangare|Dirisa SANGARE)","292ac6e2-bf22-453e-b207-314feee81df6")
			addauthor(r"(Modibo Baru Sangare|Modibo Bawu Sangare|Modibo Baru SANGARE)","203fa76e-2dd6-45f0-abea-6ced563e62c8")
			addauthor(r"(Bubakari Sangare|Bubakari)","6db84d53-f9ac-472a-9926-2deb1fdfe0ca")
			addauthor(r"(Lasina Sangare|Lasina SANGARE)","baf2a7df-84fa-4c87-8e2b-a18d5bfe4a28")
			addauthor(r"(Barama Sangare|Barama SANGARE)","68a09d5a-cd88-408c-ac3f-7cffb26e472a")
		if "_sar_" in authshort: addauthor(r"(Mamadu Sar|Mamadu SAR)","7d7f6788-7f23-49dd-9d8c-d85f4f722a34")
		if "_sarr_" in authshort: addauthor(r"(Mamadu Sarr|Mamadu SARR)","7d7f6788-7f23-49dd-9d8c-d85f4f722a34")
		if "_saya_" in authshort : addauthor(r"(Mulayi Saya|Mulayi SAYA)","cae507d3-3764-4f88-8250-f10f65df1732")
		if "_senu_" in authshort : addauthor(r"(Idirisa Senu|Idirisa SENU|Idrisa SENU|Drisa Senu|Drisa SENU)","cd0ca0ae-0426-4ebc-bfd8-2390c291c98c")
		if "_seki_" in authshort : addauthor(r"(Sɛki Majɛngi|Sɛki MAJƐNGI)","c01f698e-c858-4d7d-ad83-837a1968c40e")
		if "_senpara_" in authshort : addauthor(r"(Eli Sɛnpara|Eli SƐNPARA)","0f05df21-972a-4d6c-a063-af3d4be6209e")
		if "_si_" in authshort : 
			addauthor(r"(bubakari si|Bubakari Si|Bubakari SI)","297f5e59-7e14-4f9f-af0e-46a8373bcfdb")
			addauthor(r"(Ti Yalam Si|Ti Yalam SI)","37fb14af-e1f9-4ba2-ba7c-5f67401f42fd")  # = TYS			
			addauthor(r"(Mamadu Si|Mamadu SI)","412b4bf9-fb06-4a02-b95d-c3dbfe74b1ba")
		if "_sidi_" in authshort : addauthor(r"(Tuya Sidi|Tu Ya Sidi|Tuya SIDI)","37fb14af-e1f9-4ba2-ba7c-5f67401f42fd")  # = TYS
		if "_sidibe_" in authshort : 
			addauthor(r"(Jitumu Bala Sidibe|Jitumu Bala SIDIBE|Jitumu bala sidibe|jitumu bala sidibe|jitumu bala Sidibe|Jitumu bala SIDIBE)","8a84b6db-d69d-4ef8-b52e-870c535417b8")
			addauthor(r"(M. Sidibe|M. SIDIBE)","d382c276-cb63-42f3-9ec8-4cc7f6e79a76")
			addauthor(r"(Masa Sidibe|Masa SIDIBE)","2ba135bb-49f6-4f69-bf72-d35cb7195c45")
			addauthor(r"(tumani yalamu sidibe|tumani yalame sidibe|Tumani Sidibe|Tuya Sidibe|Ti Yalam Si|Tumani Yalam Sidibe|Tumani Y Sidibe|Tumani yalam Sidibe|Tumani Yalam SIDIBE|Tumani Y SIDIBE|Tumani Yalamu Sidibe|Tumani Yalamu SIDIBE|Tumani Y. Sidibe|Tumani Y. SIDIBE|T. Y. Sidibe|T. Y. SIDIBE|Toumani Yalam Sidibe|Toumani Yalam SIDIBE|T.Y.S.|TuyaSidi)","37fb14af-e1f9-4ba2-ba7c-5f67401f42fd")
			addauthor(r"(Burama Sidibe|Burama SIDIBE)","7ef74ea3-7846-46f1-ba22-ff113b2a40e8")
			addauthor(r"(Isaka Sidibe|Isaka SIDIBE|Isiyaka Sidibe|Isiyaka SIDIBE)","c40b5a51-94ee-48fb-a425-1a7ac752f2f8")
			addauthor(r"(Yusufu Jime Sidibe|Yusufu Jime SIDIBE|Yusuf Jime Sidibe|Yusufu Jimɛ Sidibe|Yusufu Jimɛ SIDIBE|Yusuf Jimɛ Sidibe)","c26122ec-de4d-49a9-81b8-ce5899ae0474")
			addauthor(r"(Mansa bubu Sidibe|Mansa Bubu Sidibe|Mansa Bubu SIDIBE|Mansabubu Sidibe)","f01c1c99-95df-4532-959b-15019251675b")
			addauthor(r"(Awa Sidibe|Awa SIDIBE)","14ab1bd7-7ef8-424a-84ad-40553a6cbd41")
		if "_sise_" in authshort : 
			addauthor(r"(Amadu M[\.]* Sise|Amadu M[\.]* SISE|Amadu M Sise|Amadu M SISE|A[\.]* M[\.]* Sise|A\.M Sise|A[\.]* M[\.]* SISE|A M Sise|A M SISE)","f38c8a39-329b-4916-8c7f-5b889e87523b")
			addauthor(r"(Amara Sise|Amara SISE)","d1c5691b-f597-43fc-8812-de0973007697")
			addauthor(r"(Bakɔrɔba Sise|Bakɔrɔba SISE)","8fdb8060-3664-41f2-9b8f-036e269d8c92")
			addauthor(r"(Daramani Sise|Darammani Sise|Daramani SISE)","3a8dcd18-7ff6-40d4-ad7f-67b2ee4b8537")
			addauthor(r"(Fadi Sise|Fadi SISE)","2a5bc5a9-bb75-43b0-b8e2-63f9b1407292")
			addauthor(r"(Lamini Sise|Lamini SISE|Lamine Sise)","ac9b1cd8-7480-49ec-b9b5-314e4ee5cf85")
			addauthor(r"(Mahamadu B. Sise|Mahamadu B. SISE|M. B. SISE)", "f394dedd-9131-4b1c-8456-06b06aae98a7")
			addauthor(r"(Mahamadu Lareya Sise|Mamadu Lareya Sise|Mahamadu Lariya Sise|Mamadu Lariya Sise)","f3b91ae3-022a-4d2e-91f1-c18ada0000bc")
			addauthor(r"(mamadu yusufu sise|Mamadu Yusufu Sise|Mamadu Yusuf Sise|Mamadu Yusufu SISE)","1662fdb6-5b2b-4e20-b09e-222bbc4115e6")
			addauthor(r"(Seku Sise|Seku SISE)","5cad8db8-f718-4d77-9b00-6b98c1ba02e3")
			addauthor(r"(Ahamadu Sise|Ahamada Sise|Amadu Sise|Ahamadu SISE|Ahamada SISE|Amadu SISE)","faa6df67-3696-4010-930a-98d3c130b04a")
		if "_sisoko_" in authshort :
			addauthor(r"(mariyamumadi misoko|mariyamadi sisoko|mariyanmadi sisoko|Mariyanmadi sisoko|Mariyanmadi Sisoko|Mariyamumadi Sisoko|Mariyamadi Sisoko)","a5c6837b-e811-400b-8df4-1bd5accbaf81")
			addauthor(r"(Bande Musa Sisoko|Bande Musa SISOKO|Bande M[\.]* Sisoko|Bande M[\.]* SISOKO)","c5aa1749-fe5f-44d6-a464-89a4a0d11cc3")
			addauthor(r"(Bande Musa Sisoko|Bande Musa SISOKO|Bande Musa Sisɔkɔ|Bande Musa SISƆKƆ)","c5aa1749-fe5f-44d6-a464-89a4a0d11cc3")
			addauthor(r"(Aminata Dindi Sisɔkɔ|Aminata Dindi SISƆKƆ)","2b264ba6-b3fa-4995-b6a2-a5215472e89f")
			addauthor(r"(Aminata Dindi Sisoko|Aminata Dindi SISOKO)","2b264ba6-b3fa-4995-b6a2-a5215472e89f")
			addauthor(r"(Aminata Sindi Sisɔkɔ|Aminata Sindi SISƆKƆ|Aminata Sindi SISƆKƆ)","2b264ba6-b3fa-4995-b6a2-a5215472e89f")
			addauthor(r"(Aminata Sindi Sisoko|Aminata Sindi SISOKO)","2b264ba6-b3fa-4995-b6a2-a5215472e89f")
			addauthor(r"(Aminata Dɛndi Sisɔkɔ|Aminata Dɛndi SISƆKƆ)","2b264ba6-b3fa-4995-b6a2-a5215472e89f")
			addauthor(r"(Aminata Dɛndi Sisoko|Aminata Dɛndi SISOKO)","2b264ba6-b3fa-4995-b6a2-a5215472e89f")
			addauthor(r"(Aminata Dɛndi Sisɔko|Aminata Dɛndi SISƆKO)","2b264ba6-b3fa-4995-b6a2-a5215472e89f")
			addauthor(r"(Makan Sisɔkɔ|Makan SISƆKƆ)","82c7c683-c902-46e7-ab0b-0c5f51468aac")
			
		if "_sitenzi_" in authshort : addauthor(r"(Emanuwɛli de Sol.ri Sitɛnzi|Emanuyɛli de Sol.ri Sitɛnzi)","019284d6-dd4c-44ae-8bcf-ccfcbf7fa69a")
		if "_sitentizi_" in authshort : addauthor(r"(Emanuwɛli de Sol.ri Sitɛntizi|Emanuyɛli de Sol.ri Sitɛntizi)","019284d6-dd4c-44ae-8bcf-ccfcbf7fa69a")
		if "_sitinzi_" in authshort : addauthor(r"(Emanuwɛli de Sol.ri Sitinzi|Emanuyɛli de Sol.ri Sitinzi)","019284d6-dd4c-44ae-8bcf-ccfcbf7fa69a")
		if "_sitintizi_" in authshort : addauthor(r"(Emanuwɛli de Sol.ri Sitintizi|Emanuyɛli de Sol.ri Sitintizi)","019284d6-dd4c-44ae-8bcf-ccfcbf7fa69a")
		if "_so_" in authshort : 
			addauthor(r"(Ibarahima SO|Ibarahima SƆ|Ibarahima So|Ibarahima Sɔ|ibarahima so)","8efb9f72-1f7f-45ef-88e2-63df76aa2766")
			addauthor(r"(Shɛki Madu SO|Shɛki Madu SƆ|Shɛki Madu So|Shɛki Madu Sɔ|shɛki madu so)","33bc2e39-335a-4d95-8014-2e15b52e2357")
			addauthor(r"(Madu Sɔ|Shɛki Madu SƆ|Shɛki Madu So|Shɛki Madu Sɔ|shɛki madu so)","33bc2e39-335a-4d95-8014-2e15b52e2357")
			addauthor(r"(amadu sɔ|Amadu Sɔ|Amadu SƆ)","809f77db-59f0-4f4d-a007-a766469f913c")
		if "_sogo_" in authshort: addauthor(r"(Amadu Sogo|Amadu SOGO)","a2ad789a-16c5-4d00-95f4-8595126a411b")
		if "_sogoba_" in authshort : 
			addauthor(r"(Shaka Sogoba|ʃaka Sogoba|Siyaka Sogoba|Siyaka SOGOBA)","8c54b573-5ba9-4558-a828-354afef8ee5e")
			addauthor(r"(Bala Sogoba|Bala SOGOBA)","638507fe-69e0-40c2-ad36-8337730f927f")
		if "_soke_" in authshort: addauthor(r"(Gongoloma Soke|Gongoloma SOKE)","c3bf974e-7d29-482f-bee4-c4e3f53358c9")
		if "_songomo_" in authshort: addauthor(r"(Sanusi Sɔngomo|Sanusi SƆNGOMO)","85a08b8d-4a6e-4be2-aa82-bdd8bc4a2fc6")
		if "_sukuna_" in authshort: addauthor(r"(Mamayi Sukuna|Mamayi SUKUNA)","5ca24c05-96f6-4332-906e-8bd1f9125015")
		if "_sumare_" in authshort: addauthor(r"(Wande Sumare|Wande SUMARE)","ea09623b-b3d1-4856-9372-2b1f54338d18")
		if "_sunkara_" in authshort :addauthor(r"(Amadu SUNKARA|Amadu Sunkara|amadu sunkara)","f65af322-1fe8-4381-b65d-68758164036e")
		if "_tangara_" in authshort : 
			addauthor(r"(ya tangara|Ya Tangara)","868d316d-c084-45db-921f-966fa94724ef")
			addauthor(r"(Sedu Tangara|Sedu TANGARA)","c258f7bc-00bd-4c3a-9031-64877023871e")
			addauthor(r"(Seyidu Tangara|Seyidu TANGARA)","e17ead63-2987-4fc5-9a28-85b97276a3b4")
		if "_tase_" in authshort : addauthor(r"(Ecɛni Tase|Ecɛni TASE|Ɛcɛni Tase|Ɛcɛni TASE)","980f3ad4-5f9d-4692-8067-2009ba2b8c35")
		if "_tera_" in authshort : 
			addauthor(r"(Kalilu Tera|Kalilu TERA|kalilu tera|Kalilu tera|kalilu Tera)","7d3d3690-1795-4f7e-8cff-a18ee692d8d6")
			if periodique == "nyetaa" : addauthor(r"(k\.t\.|K\.T\.|k\. t.\|K\. t\.|K\. T\.)","7d3d3690-1795-4f7e-8cff-a18ee692d8d6")
			addauthor(r"(Jɔb Tera|Jɔb TERA)","6958bbab-7a30-4c2e-ad89-794ce71b820a")
		if "_togola_" in authshort : 
			addauthor(r"(Salimu Togola|Salimu TOGOLA|Salim Togola)","46c5aee6-a9a3-461f-b48a-a6a6aa5d4b9b")
			addauthor(r"(Lazeni Togola|Lazeni TOGOLA|Laseni Togola|Laseni TOGOLA)","781b18fc-de0a-4391-9f44-69f7ab0654f5")
		if "_trawele_" in authshort: 
			addauthor(r"(Umu Amar Trawele)","14e31872-e90f-48ae-b008-ff4e325fccee")
			addauthor(r"(Daramani Trawele|Daramane Trawele|Daraman Trawele|Daramani TRAWELE|Daramane TRAWELE|Daraman TRAWELE)","2da173f5-f2f0-4af0-a413-3ca3c6ee7a88")
			addauthor(r"(Sungalo Trawele|Sungalo TRAWELE|Sunkalo Trawele)","db99321c-0d53-4eb3-aa86-7f14d99de21f")
			addauthor(r"(Usumani Trawele|Usumani TRAWELE|Usumani Nuhun Trawele|Usumani Nuhun TRAWELE|Usumani N Trawele|Usumani N TRAWELE|Usumani N. Trawele|Usumani N. TRAWELE)","a1396798-4b28-48a1-b16d-c9679207cb7a")
		if "_tarawele_" in authshort : 
			addauthor(r"(Abubakari Tarawele|Abubakari TARAWELE)","2695bd58-bdfb-4ed5-8adb-1e09e6139683")
			addauthor(r"(Ali Tarawele|Ali TARAWELE)","d59805d4-e334-4005-86c4-5523fa59ac6e")
			addauthor(r"(Alujan Tarawele|Alujan TARAWELE)","258e2d7f-e4f4-4803-ba72-518f66f18f2d")
			addauthor(r"(Asani Tarawele|Asani TARAWELE|Alasani Tarawele|Alasani TARAWELE)","48347506-6757-4d20-b854-735f2c1e09cf")
			addauthor(r"(Bafin Tarawele|Bafin TARAWELE)","0577018c-d74d-4f68-81f9-218279f2514e")
			addauthor(r"(Basumana Tarawele|Basumana TARAWELE)","e79dde7c-1739-47fa-b50d-b2addce57ae2")
			addauthor(r"(C[\.]*M[\.]* Tarawele|C[\.]* M[\.]* Tarawele)","c9775956-e767-411b-ac4a-aacc504aa314")
			addauthor(r"(Daramani Tarawele|Daramane Tarawele|Daraman Tarawele|Daramani TARAWELE|Daramane TARAWELE|Daraman TARAWELE)","2da173f5-f2f0-4af0-a413-3ca3c6ee7a88")
			addauthor(r"(Dirisa Tarawele|Dirisa TARAWELE)","7444cb4d-45e4-4645-b597-1a06b7b789c4")
			addauthor(r"(Duguna Tarawele|Duguna TARAWELE)","44a419e9-b797-4e3a-bbbc-cde095e486ba")
			addauthor(r"(Fanta Tarawele|Fanta TARAWELE|Fanta Fula Tarawele)","41f86179-2da0-4890-91f9-4bf687788f4b")
			addauthor(r"(Fasirimɛn Mace Tarawele|Fasirimɛn Mace TARAWELE|Fasirimɛn Macɛ Tarawele|Fasirimɛn Macɛ TARAWELE)","a58afefa-86dc-495d-aff1-8e5c2698ca1e")
			addauthor(r"(Fatumata Tarawele|Fatumata TARAWELE)","3f906005-a35f-42cd-9579-e5e7b8c0c49d")
			addauthor(r"(Gɔnba Tarawele|Gɔnba TARAWELE|Gonba Tarawele|Gonba TARAWELE)","47d27d6a-73fd-4cfb-bb7e-acce3dd707d9")
			addauthor(r"(Isa Tarawele|Isa Trawele|Isa TARAWELE)","dc8c09d1-c257-4939-a2c2-c98c494800fd")
			addauthor(r"(Janginɛ Tarawele|Janginɛ TARAWELE)","9a7671d9-e6e2-4c86-99c2-abd6601d9ed7")
			addauthor(r"(Kasun Tarawele|Kasun TARAWELE)","ab30d433-20bb-4152-8885-d61c958d2517")
			addauthor(r"(Mamadu Tarawele|Mamadu TARAWELE)","1f54a676-f904-4080-af0d-5b995fbf3fea")
			addauthor(r"(Mariyamu Tarawele|Maramu Tarawele|Mariyamu tarawele|mariyamu Tarawele|mariyamu tarawele|Mariyamu TARAWELE)","6bf4708c-7081-427d-a33b-e85264b80e36")
			addauthor(r"(Mariyamu A Tarawele|Mariyamu A. Tarawele|Mariyamu A TARAWELE|Mariyamu A. TARAWELE)","dd14cfd3-bfc5-4b41-9827-07330f78032a")
			addauthor(r"(Siyaka Tarawele|Siyaka TARAWELE)","9885109d-3fdf-4cf2-8307-1ad88cd1d8ed")
			addauthor(r"(Sungalo Tarawele|Sungalo TARAWELE|Sunkalo Tarawele)","db99321c-0d53-4eb3-aa86-7f14d99de21f")
			addauthor(r"(Usumani Tarawele|Usumani TARAWELE)","a1396798-4b28-48a1-b16d-c9679207cb7a")
			addauthor(r"(Mamadu Nuhun Tarawele|Mamadu Nuhun TARAWELE|M[\.]* N[\.]* Tarawele|M[\.]* N[\.]* TARAWELE)","fee62bbd-3e79-4c9c-a209-f7c8b55b24f1")
			addauthor(r"(Modibo Nama Tarawele|Modibo Nama TARAWELE|Modibo Naman Tarawele|Modibo N[\.]* Tarawele|Modibɔ N[\.]* Tarawele|Modibo Naman TARAWELE)","8442fe4a-3c33-4aa4-86d9-38f9283aea25")
			addauthor(r"(Jibirili Tarawele|Jibirili TARAWELE)","b3ef25a8-7188-40e1-9b55-c80d2ff16440")
			addauthor(r"(Gasitan Cɛkɔrɔba Tarawele|Gasitan Cɛkɔrɔba TARAWELE|Gasitɔn Tarawele|Gasitɔn TARAWELE|Gaston Tarawele|Bagasitɔn Tarawele|Bagasitɔn TARAWELE)","9e1fe92a-f93a-4bf4-9b8d-5ed49b45392b")
			addauthor(r"(Sɛki M. Tarawele|Sɛki M. TARAWELE|Sɛki M Tarawele|Sɛki M TARAWELE|Sɛki Mukutari Tarawele|Sɛki Mukutari TARAWELE)","bf3bd4ed-3c54-4afc-a8c4-9e885675fdb6")
			addauthor(r"(Mohamɛdi Tarawele|Mohamɛdi TARAWELE|Mohamedi Tarawele)","433f9d52-4081-413a-bad8-56016c81686c")
			addauthor(r"(Sinɛ Tarawele|Sinɛ TARAWELE|Sinɛ S Tarawele|Sinɛ S TARAWELE)","69d1bd16-6add-488c-996e-05fece1f794e")
			addauthor(r"(Usumani Tarawele|Usumani TARAWELE|Usumani Nuhun Tarawele|Usumani Nuhun TARAWELE|Usumani N Tarawele|Usumani N TARAWELE|Usumani N. Tarawele|Usumani N. TARAWELE)","a1396798-4b28-48a1-b16d-c9679207cb7a")
			
			if len(re.findall(r"(Basabugu|Nciba)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Musa Tarawele|Musa TARAWELE)","b512f45e-8ac3-44de-a3b9-6f75fd3720c4")
			if len(re.findall(r"(Echos)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Aminata Tarawele|Aminata TARAWELE)","e9ba1457-375d-40ed-b2c1-0c9408563938")

			if len(re.findall(r"(Ginyan|Giɲan|Bananba)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Mama Tarawele|Mama TARAWELE)","1c559d5c-4e96-4ad9-85f8-130e4778f4fd")
			if len(re.findall(r"(Yelimane|YELIMANE)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Bakari Tarawele|Bakari TARAWELE)","1a452538-37d1-4f83-8915-42bd524e309b")
			if len(re.findall(r"(Badama Dukure|Badama DUKURE)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Mohamɛdi Tarawele|Mohamɛdi TARAWELE)","433f9d52-4081-413a-bad8-56016c81686c")
			if len(re.findall(r"(Kɔndogola|Kondogola)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Modibo Tarawele|Modibo TARAWELE)","33118b51-f727-49f4-9cd7-bf7cb9bc2859")
		if "_tarawore_" in authshort : 
			addauthor(r"(Sajo Tarawore|Sajo TARAWORE)","ab326a09-9466-457d-afbf-a15ff952a87d")
		if "_togola_" in authshort : 
			addauthor(r"(Dirisa Togola|Dirisa TOGOLA)","67ad6f80-5eb9-43f4-a293-cdbbfefd5eaa")
			addauthor(r"(Mamadu Togola|Mamadu TOGOLA)","99491b6b-e476-4c9d-8f1c-9a0e06cca324")
		if "_traore_" in authshort :
			addauthor(r"(Mariyamu A Traoré|Mariyamu A. Traoré|Mariyamu A Traore|Mariyamu A. Traore|Mariyamu A TRAORE|Mariyamu A. TRAORE)","dd14cfd3-bfc5-4b41-9827-07330f78032a")
			
		if "_tulema_" in authshort : addauthor(r"(Hamidu Tulema|Hamidu TULEMA)","b5864f72-0d3d-4428-a2a3-13cca538f6e1")
		if "_tunkara_" in authshort : 
			addauthor(r"(S[\.]* B[\.]* Tunkara|Solomani Bobo Tunkara|Suleyimani Bobo Tunkara|Solomani B Tunkara|Solomani Bobo TUNKARA|Solomani B[\.]* Tunkara)","cd5292c9-93cc-494f-abd0-0a834bb677a2")
			addauthor(r"(Manbi Sama Tunkara|Manbi Tunkara|Manbi Sama TUNKARA|Manbi TUNKARA)","f3737dc6-4d4d-42d7-bb68-53797cab5152")
		if "_ture_" in authshort : 
			addauthor(r"(Abudurahamani Ture|Abudurahamani TURE)","39e14c2e-4536-4264-a03c-52897a6956c6")
			addauthor(r"(B. Ture|B. TURE|Basiriki Ture|Basiriki TURE|BASIRIKI TURE|Basidiki Ture|Basidiki TURE)","60ba1311-ba33-4b5a-ab42-8fb1a6038263")
			addauthor(r"(sedu ture|sedu turè|seyidu ture|Seyidu Ture)","72559003-6529-4e84-b9c5-ef681d1b01dd")
			addauthor(r"(Berema Ture|Berema TURE)","51d73647-d28e-45cb-96b1-52c86a597f72")
			addauthor(r"(Berehima Ture|Berehima TURE)","c61a1d96-f14d-43dd-9d70-35b435a73bc8")
			addauthor(r"(Madu Ture|Madu TURE)","eca51900-8a0c-410b-a48b-8ce752447d1a")
			addauthor(r"(Mohamɛdi Ture|Mohamɛdi TURE)","84b159ce-4760-4109-be6f-c2df333a8c52")
			addauthor(r"(Wahabu Ture|Wahabu TURE)","2db462c3-517c-43ad-9eb7-00275c5545ef")
			if len(re.findall(r"(Balikukalan nyèmògòso|balikukalan nyèmògòso|baliku kalan nyèmògòso|balikukalan Nyèmògòso|Balikukalan Nyèmògòso)",endoftext,re.I|re.U))>0 :
				addauthor(r"(Musa Ture|Musa TURE|musa ture|Musa ture|musa Ture)","baa8e6f2-7ff3-48e8-8e45-bb0ff4a3372f")
		if "_wage_" in authshort : addauthor(r"(Sidi Yaya Wage|Sidi Yaya WAGE|Sidi Y Wage|Sidi Y[\.]* Wage|Sidi Y[\.]* WAGE)","83dac3cc-d749-4758-88eb-e927dfe204ec")
		if "_watara_" in authshort or "_ouattara_" in authshort :
			addauthor(r"(Suleyimani Watara|Suleyimani WATARA|Sulɛyimani WATARA|Suleyimani Ouattara|Suleymane Watara|Sulemani Watara)","4086d40b-cb3a-4b04-9688-b9e4f4a3e8c5")
		if "_williams_" in authshort : addauthor(r"(Denise Williams|Denise WILLIAMS)","fae54512-72ee-45fe-8b00-4dbabb6bc6d4")
		if "_wiliamu_" in authshort : addauthor(r"(Denisi Wiliyamu|Denisi WILIAMU)","fae54512-72ee-45fe-8b00-4dbabb6bc6d4")
		if "_wulale_" in authshort : addauthor(r"(Berehima Wulale|Berehima WULALE|Berema Wulale|Berema WULALE)","bee6913c-c8f8-424a-9804-3cce1f8c45b1")

		naname=0
		if  aname!="": 
			naname=1
			print("  "+re.sub(r"\|"," + ",aname))
		
		if "|" in aname:
			anames=aname.split("|")
			naname=len(anames)
		if naname!=nshort:
			if nshort<naname:
				ndiff=naname-nshort
				print("  -> in excess by "+str(ndiff)+" author(s)    <+++++++++++++++++++++++++++++++++++++++++\n")
			else:
				ndiff=nshort-naname
				if ndiff==1: print("  -> missing "+str(ndiff)+" author(s)    <-----------------------------------------\n")
				elif ndiff==2: print("  -> missing "+str(ndiff)+" author(s)    <========================\n")
				elif ndiff==3: print("  -> missing "+str(ndiff)+" author(s)    <≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠\n")
				else : 	print("  -> missing "+str(ndiff)+" author(s)    <########################\n")

		authmetas=""
		if auuid!="" :
			authmetas=re.sub(r'name="author:uuid" content="(XXX)" ','name="author:uuid" content="'+auuid+'" ',authstub)
			authmetas=re.sub(r'name="author:name" content="(XXX)" ','name="author:name" content="'+aname+'" ',authmetas)
			authmetas=re.sub(r'name="author:spelling" content="(XXX)" ','name="author:spelling" content="'+aspelling+'" ',authmetas)
			authmetas=re.sub(r'name="author:birth_year" content="(XXX)" ','name="author:birth_year" content="'+abirth+'" ',authmetas)
			authmetas=re.sub(r'name="author:sex" content="(XXX)" ','name="author:sex" content="'+asex+'" ',authmetas)
			authmetas=re.sub(r'name="author:native_lang" content="(XXX)" ','name="author:native_lang" content="'+anative+'" ',authmetas)
			authmetas=re.sub(r'name="author:dialect" content="(XXX)" ','name="author:dialect" content="'+adialect+'" ',authmetas)
			authmetas=re.sub(r'name="author:addon" content="(XXX)" ','name="author:addon" content="'+aaddon+'" ',authmetas)
		# print metas
		# sys.exit("---stop tests---")
		filenameout=re.sub(r"\.txt",".html",filename)   # filename can be *.txt or *.old.txt -> *.html, *.old.html
		outf=open(filenameout,"w")
		if authmetas!="" :
			metas=re.sub("</head>",authmetas+"\n</head>",metas)
			# added 27/8/2020
		metas=re.sub(r"\n","",metas)
		metas=re.sub(r"\t","",metas)
		# touched 27/8/2020 outf.write(metas+u"\n<body><p>"+tout+u"</p></body>\n</html>\n")
		outf.write(metas+"<body><p>"+tout+"</p></body></html>")
		outf.close()
		fileIN.close()
print("\n##################################################################################\n")