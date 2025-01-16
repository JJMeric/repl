#!/usr/bin/env python
# -*- coding: utf-8 -*-

# to check authors references in files against authors.csv
# and use of authors.csv references

import os
import re
import sys
import csv

dictauth_uuid={} 
dictauth_name={}   # nb pas uniques

with open('/home/corpus-team/GITlab/corbama/authors.csv') as f:
    authors = csv.reader(f)
    for author in authors:
        if author[0]=="" or author[0]=='author:name' : continue
        uuid=author[7]
        data=author[0]
        dictauth_uuid[uuid]=data
        if data in dictauth_name:   # il y a plusieurs Traoré, Moussa, tous différents!
        	dictauth_name[data].append(uuid)
        else:
        	dictauth_name[data]=[uuid]

c_reversed	=re.compile(r'<meta content="([^\"]+)" name="([^\"]+)" />',re.U|re.MULTILINE)
c_uuid		=re.compile(r'<meta name="author:uuid" content="([^\"]+)" />',re.U|re.MULTILINE)
c_auth_name	=re.compile(r'<meta name="author:name" content="([^\"]+)" />',re.U|re.MULTILINE)
c_textscript=re.compile(r'<meta name="text:script" content="([^\"]+)" />',re.U|re.MULTILINE)
valid_textscripts=('Nouvel orthographe malien','Ancien orthographe malien', 'N&#8217;Ko', 'N’Ko', 'Orthographe coloniale', 'Autres orthographes latines', 'Adjami')

lold=('è','ò')
lnew=('ɛ','ɔ')

htmldec2char={'&#603;':'ɛ', '&#596;':'ɔ', '&#626;':'ɲ', '&#331;':'ŋ', '&#400;':'Ɛ', '&#390;':'Ɔ', \
			'&#413;':'Ɲ', '&#330;':'Ŋ', '&#233;':'é', '&#232;':'è', '&#231;':'ç', '&#224;':'à', '&#249;':'ù', \
			'&#228;':'ä', '&#235;':'ë', '&#239;':'ï', '&#246;':'ö', '&#252;':'ü', '&#226;':'â', '&#234;':'ê', \
			'&#238;':'î', '&#244;':'ô', '&#251;':'û', '&#201;':'É', '&#171;':'«', '&#187;':'»', '&#180;':'´', \
			'&#8220;':'“', '&#8221;':'”', '&#242;':'ò', 'o&#768;':'ò', 'e&#768;':'è', 'e&#769;':'é', 'e&#769;':'É',\
			'c&#184;':'ç', 'a&#768;':'à', 'u&#768;':'ù', '&#8217;':'’'}

auth_in_files={}

for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.

	filenames=sorted(filenames) # peut-être pas nécessaire, mais plus lisible

	for filename in sorted(filenames) :
		# run 1 if not filename.endswith(".dis.html"):
		# run 2 :
		if not filename.endswith(".html"):
			continue

		path = os.path.join(dirname, filename)
		if ".git" in path: 
			continue

		file = open(path, "r")
		tout=file.read()
		file.close()

		# normalize meta presentation as name, content

		tout,nc=re.subn(r'<meta content="([^\"]*)" name="([^\"]+)" />','<meta name="\g<2>" content="\g<1>" />',tout,0,re.U|re.MULTILINE)
		
		# take this occasion to spot strange missing textscript

		t_textscript="?"
		s_textscript=c_textscript.search(tout)
		if s_textscript:
			t_textscript=s_textscript.group(1)
		if t_textscript not in valid_textscripts:
			print("$ ",path," problème de textscript=",t_textscript)
			t_textscript2=t_textscript
			if t_textscript=="Nouveau orthographe malien":
				t_textscript2="Nouvel orthographe malien"
			elif ".old" in filename:
				t_textscript2="Ancien orthographe malien"
			else: # try to determine
				tout2=tout
				if ".dis."in filename:
					# extract sentences. Caution : Sentences may have attributes after "sent"
					s_sent=re.findall(r'<span class="sent"[^\>]*>([^\<]*)<span class="annot"',tout,re.U|re.MULTILINE)
					if s_sent:
						tout2=' '.join(s_sent)

				nold=0
				for i in lold: nold+=tout2.count(i)
				nnew=0
				for i in lnew: nnew+=tout2.count(i)
				if nnew > nold:
					t_textscript2="Nouvel orthographe malien"

			if t_textscript2 != t_textscript:
				# update file
				if t_textscript=="?": t_textscript=""
				tout,nc=re.subn('<meta name="text:script" content="'+t_textscript+'" />',\
								'<meta name="text:script" content="'+t_textscript2+'" />',\
								tout,0,re.U|re.MULTILINE)
				if nc>0:
					file = open(path, "w")
					file.write(tout)
					file.close()
					print("@ modifié ",path,"(new text:script) : ",t_textscript2)	

		# take this occasion to transform html decimal notation in html files

		if ('&#603;' in tout ) or ('&#596;' in tout) or ('&#233;' in tout) or ('&#242;' in tout) or ('&#8217;' in tout) :
			ncp=0
			for k,v in htmldec2char.items() :
				if k in tout: 
					tout,nc=re.subn(k,v,tout,0,re.U|re.MULTILINE)
					ncp+=nc
			if ncp>0:
				file = open(path, "w")
				file.write(tout)
				file.close()
				print("¹ modifié ",path,"(htmldec2char) : ")				



		# clean-up void entries like:
		"""
		<meta content="Bambara||||" name="author:native_lang" />
		<meta content="0|0|0|0|0" name="author:birth_year" />
		<meta content="m|m|m||" name="author:sex" />
		<meta content="||||" name="author:dialect" />
		<meta content="||||" name="author:spelling" />
		<meta content="éditeur de Kibaru||||" name="author:addon" />
		<meta content="Ture, Basiriki|Togola, Sunkalo|Tarawele, Modibo Nama||" name="author:name" />
		"""

		s_metas=re.findall(r'<meta name="author:([^\"]+)" content="([^\"]*)" />',tout,re.U|re.MULTILINE)
		if len(s_metas)>0:  # some files don't even have meta author
			metas={}
			for k,v in s_metas: metas[k]=v
			if 'name' in metas :
				if '|' in metas['name']:
					oklist=[]
					names=metas["name"].split('|')
					do_suppress=False
					for name in names:
						if name=='' : 
							oklist.append(False)
							do_suppress=True
						else: oklist.append(True)

					if do_suppress:
						for k,v in metas.items(): 
							newv=[]
							oklist_index=0
							for velement in v.split('|'):
								if oklist_index>len(oklist)-1:
									print("µ ",path,"author:"+k,"plus long sur author:name ?")
								else:
									if oklist[oklist_index]: newv.append(velement)
								oklist_index+=1
							t_newv='|'.join(newv)
							metas[k]=t_newv

						nct=0
						for k,v in metas.items():
							tout,nc=re.subn(r'<meta name="author:'+k+r'" content="[^\"]*" />',\
											'<meta name="author:'+k+r'" content="'+v+'" />',tout,0,re.U|re.MULTILINE)
							nct+=nc

						if nct>0:
							file = open(path, "w")
							file.write(tout)
							file.close()
							print("@ auteurs vides supprimés, fichier modifié : ",path)
			else:
				print("% no 'name' in metas? ",path, metas)
				# 114 cas répertoriés
				if metas in [{'native_lang': 'Bambara', 'sex': 'inconnu', 'dialect': 'inconnu'},\
							{'native_lang': 'Bambara'},\
							{'native_lang': 'inconnu', 'sex': 'inconnu', 'dialect': 'inconnu'},\
							{'native_lang': 'inconnu', 'sex': 'inconnu'},\
							{'native_lang': 'inconnu', 'sex': 'm', 'dialect': 'inconnu'},\
							{'sex': 'inconnu'} ]:
					tout,nc=re.subn(r'<meta name="author:[^\"]+" content="[^\"]+" />','',tout,0,re.U|re.MULTILINE)
					if nc>0:
						file = open(path, "w")
						file.write(tout)
						file.close()
						print("@ metas author: isolées supprimées, fichier modifié : ",path)
					else:
						print("  fichier non corrigé:",path)



		else:
			print("% no meta data author: ",path)

		#caution: treat all author elements as lists
		uuids=[]
		auth_names=[]

		s_uuid=re.search(c_uuid,tout)
		if s_uuid:
			t_uuid=s_uuid.group(1)
			if "|" in t_uuid:
				uuids=t_uuid.split("|")
			else:
				uuids=[t_uuid]

		s_auth_name=re.search(c_auth_name,tout)
		if s_auth_name:
			t_auth_name=s_auth_name.group(1)
			if "|" in t_auth_name:
				auth_names=t_auth_name.split("|")
			else:
				auth_names=[t_auth_name]
		
		#print(path,"\nuuids, auth_names:",uuids, auth_names)

		uuid_index=0

		luuids=len(uuids)
		lnames=len(auth_names)
		
		if luuids>0:

			for uuid in uuids:

				if uuid not in dictauth_uuid:
					if lnames>0:
						print("?",path,"uuid inconnue:",uuid,auth_names[uuid_index])
					else:
						print("*",path,"uuid inconnue:",uuid,"author:name VIDE")
						# parasites causés par l'ancienne version de meta (cf auteurs à vide dans authors.csv)
						tout,nc=re.subn(r'<meta name="author:[^\"]+" content="[^\"]+" />','',tout,0,re.U|re.MULTILINE)
						if nc>0:
							file = open(path, "w")
							file.write(tout)
							file.close()
							print("@ auteur vide supprimé: ",path)
							# ne supprime que les champs avec content non vide comme uuid -pour les supprimer tous il aurait fallu content="[^\"]*"

				if uuid in auth_in_files:
					auth_in_files[uuid].append(path)
				else:
					auth_in_files[uuid]=[path]

				uuid_index+=1
		
		elif lnames>0:

			uuids=[]

			for auth_name in auth_names:
				
				if auth_name in dictauth_name:
					print("+ ",path,"uuid manquante:",dictauth_name[auth_name],auth_name)
					if len(dictauth_name[auth_name])==1 :
						uuids.append(dictauth_name[auth_name][0])
					else:
						uuids.append("")  # not safe but should be the same uuids length as auth_names
						print("¤ ",path,"name multiple in authors.csv",auth_name,len(dictauth_name[auth_name]))
				else:
					uuids.append("")  
					print("€ ",path,"name absent in authors.csv",auth_name)
			
			if len(uuids) == lnames:
				t_uuids="|".join(uuids)
				if t_uuids!="":  # ! doublons meta uuid!!! ou bien non, on le fait quand même : il faut une mate uuid (à remplir!)
					tout,nc=re.subn(r'<meta name="author:name" content="([^\"]+)" />',\
					'<meta name="author:name" content="\g<1>" /><meta name="author:uuid" content="'+t_uuids+'" />',\
						tout,0,re.U|re.MULTILINE)
					if nc>0:
						file = open(path, "w")
						file.write(tout)
						file.close()
						print("@ modifié: ",path,"ajout des uuids, t_uuids: ",t_uuids)

		else:
			print("no author in "+path)

		# check differences in authors.csv names and file names	:

		if luuids>0 and luuids==lnames:
			uuid_index=0
			t_auth_name2=t_auth_name

			for uuid in uuids:
				if uuid in dictauth_uuid:
					if dictauth_uuid[uuid] != auth_names[uuid_index]:
						print("² ",path,"author names differ:",uuid,dictauth_uuid[uuid],"<?>",auth_names[uuid_index])
						t_auth_name2=t_auth_name2.replace(auth_names[uuid_index],dictauth_uuid[uuid])
				uuid_index+=1

			if t_auth_name2 != t_auth_name:
				if "|" in t_auth_name: 
					t_auth_name=t_auth_name.replace("|","\|")
				if ("(" in t_auth_name) or (")" in t_auth_name):
					t_auth_name=t_auth_name.replace("(","\(")
					t_auth_name=t_auth_name.replace(")","\)")
				tout,nc=re.subn('<meta name="author:name" content="'+t_auth_name+'" />',\
								'<meta name="author:name" content="'+t_auth_name2+'" />',\
								tout,0,re.U|re.MULTILINE)
				if nc>0:
					file = open(path, "w")
					file.write(tout)
					file.close()
					print("@ modifié (auteurs normalisés) : ",path)	

#reverse check
nauth=len(auth_in_files)

if nauth<20: sys.exit("nauth ?"+str(nauth))
print("\nChecking authors.csv")
for uuid,data in dictauth_uuid.items():
	if uuid in auth_in_files:
		nfiles=len(auth_in_files[uuid])
		print("=",uuid,data,"utilisé dans ",nfiles,"fichiers")
	else:
		print("! uuid non utilisée dans les fichiers dis:",uuid,data)

	
