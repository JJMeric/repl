#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

log =  open ("collation-align-errors.log","w")
nerr=0

nargv=len(sys.argv)
argument=""
if nargv>1 : argument= str(sys.argv[1])
old=False
if argument=="old" or argument=="-old": old=True

for dirname, dirnames, filenames in sorted(os.walk('.')):
		if '.git' in dirnames: dirnames.remove('.git')  # don't go into any .git directories.

		for filename in filenames:
			if " " in filename: # spaces in filename cause no end problems
				filename1=re.sub(r" ","",filename)
				os.rename(os.path.join(dirname, filename),os.path.join(dirname, filename1))

for dirname, dirnames, filenames in sorted(os.walk('.')):
		if '.git' in dirnames: dirnames.remove('.git')  # don't go into any .git directories.

		for filename in sorted(filenames):

			if filename.endswith("-doz.txt") or filename.endswith("-zup.txt") or filename.endswith("-kot.txt")  or filename.endswith("-gedz.txt") :
				print(os.path.join(dirname, filename))
				"""
				if u" " in filename:  # spaces in filename cause no end problems in Corpus build
					nameparts=filename.split(".")
					nameitself=nameparts[0].strip()  # strip  extra spaces both ends (happens often at the end)
					if u" " in nameitself : 
						nameitself=re.sub(u" ",u"$",nameitself)   # space inside ?
					print  u"file '"+filename+u"' renamed as '"+nameitself+u".txt'"
					os.rename(os.path.join(dirname, filename),os.path.join(dirname, nameitself+u".txt"))
					filename=nameitself+u".txt"
				"""
				try : 
					fileIN = open(os.path.join(dirname, filename), "rb")  # rb : to get the Windows \r\n EOL
				except :
					log.write("filename? "+os.path.join(dirname, filename)+"\n")
					nerr=nerr+1
					continue
				#tout=fileIN.readlines()
				tout=u""
				# actually readlines() should be OK
				line = fileIN.readline()
				nline=1
				while line:
					try :
						tout=tout+line.decode("utf-8")
					except :
						log.write("character? "+os.path.join(dirname, filename)+" line:"+str(nline)+" :\n"+line+"\n")
						print "character? "+os.path.join(dirname, filename)+" line:"+str(nline)+" :\n"+line+"\n"
						nerr=nerr+1
						pass
					nline=nline+1
					line = fileIN.readline()

				fileIN.close()

				# handle Windows EOL
				tout=re.sub(u"\r\n",u"\n",tout,0,re.U|re.MULTILINE)

				# rectify doz strange typos (ru keyboard hazards)
				tout=re.sub(u"ɑ",u"a",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"а",u"a",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"А",u"A",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"В",u"B",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"с",u"c",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"С",u"C",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"е",u"e",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Е",u"E",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɒ",u"ɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ə",u"ɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɣ",u"g",tout,0,re.U|re.MULTILINE)				
				tout=re.sub(u"Н",u"H",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"í",u"i",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɩ",u"i",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\|",u"l",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"к",u"k",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"т",u"m",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"М",u"M",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"п",u"n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"щ",u"o",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ш",u"m",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"о",u"o",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"О",u"O",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Р",u"P",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"р",u"p",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"г",u"r",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Т",u"T",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"и",u"u",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ц",u"u",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"у",u"y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɪ",u"y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"л",u"n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"á",u"a",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ý",u"y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ú",u"u",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"№",u"N°",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ï",u"i",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"˚",u"°",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"З",u"3",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"j̀",u"j",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Л",u"Ɲ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"∫",u"ʃ",tout,0,re.U|re.MULTILINE)

				# utilisation de majuscules accent grave par zup
				tout=re.sub(u"È",u"È",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Ò",u"Ò",tout,0,re.U|re.MULTILINE)

				# enforce space between the ° of N° and the number that follows
				tout=re.sub(u"°([0-9])",u"° \g<1>",tout,0,re.U|re.MULTILINE)

				#align …  and ...
				tout=re.sub(u"\.\.\.\.\.\.",u"…",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"\.\.\.",u"…",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"……",u"…",tout,0,re.U|re.MULTILINE)

				# align braquets
				tout=re.sub(u"’",u"'",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\’",u"'",tout,0,re.U|re.MULTILINE) # problème en suspens avec les quotes simples
				tout=re.sub(u"‘",u"'",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"“",u"«",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"”",u"»",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"<<",u"«",tout,0,re.U|re.MULTILINE) # erreur fréquente chez kot
				tout=re.sub(u">>",u"»",tout,0,re.U|re.MULTILINE) 
				tout=re.sub(u"<h>»",u"<h>«",tout,0,re.U|re.MULTILINE) # erreur fréquente chez zup
				tout=re.sub(u"<ill>»",u"<ill>«",tout,0,re.U|re.MULTILINE) # erreur fréquente chez zup
				tout=re.sub(u"»([^\"]+)\"",u"«\g<1>»",tout,0,re.U|re.MULTILINE) # erreur fréquente chez doz: ”URSS"
				
				deuxmajs=re.findall(ur"[ \«\"]([A-ZƐƆƝŊ][A-ZƐƆƝŊ][a-zɛɔɲŋ]+)[ \,\;\.\:\!\?\'\»\"]",tout,re.U|re.MULTILINE)
				for deuxmaj in deuxmajs:
					deuxmajcorr=deuxmaj.capitalize()
					tout=re.sub(deuxmaj,deuxmajcorr,tout,0,re.U|re.MULTILINE)

				# frequent typos
				tout=re.sub(u"aia",u"ala",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"aie",u"ale",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"aio",u"alo",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"eie",u"ele",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"eii",u"eli",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"([^b])iii",u"\g<1>ili",tout,0,re.U|re.MULTILINE)  # kɔnɔ bɛ biii fɔ !
				tout=re.sub(u"oio",u"olo",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"oiu",u"olu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"uiu",u"ulu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"uia",u"ula",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"uii",u"uli",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"iia",u"ila",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"iie",u"ile",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"oia",u"ola",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"aii",u"ali",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"oii ",u"oli ",tout,0,re.U|re.MULTILINE)
				if not old :
					tout=re.sub(u"ɛiɛ",u"ɛlɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(u"ɔiɔ",u"ɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(u"ɔii",u"ɔli",tout,0,re.U|re.MULTILINE)
				
				if old:
					tout=re.sub(u"̀̀",u"̀",tout,0,re.U|re.MULTILINE)

				tout=re.sub(ur"all([\s\.\,\;\:\!\?])",u"ali\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"aua",u"aya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ia([\s\.\,\;\:\!\?])",u" la\g<1>",tout,0,re.U|re.MULTILINE)
				# 1 instead of l
				tout=re.sub(ur" 1a([\s\.\,\;\:\!\?])",u" la\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" 1a([a-z])",u" la\g<1>",tout,0,re.U|re.MULTILINE)      # en début de mot : lajɛlen
				# I instead of l
				tout=re.sub(ur" Ia([\s\.\,\;\:\!\?])",u" la\g<1>",tout,0,re.U|re.MULTILINE)
				
				
				# enforce dɔrɔmɛ "d." attached to numbers
				tout=re.sub(ur"([^a-zɛɔA-Z])d\s*\.\s+([0-9]+)",u"\g<1>d.\g<2>",tout,0,re.U|re.MULTILINE)
				
				# enforce NO SPACE at beginning of paragraphs
				tout=re.sub(ur"\n[ ]+([^\s])",u"\n\g<1>",tout,0,re.U|re.MULTILINE)
				
				# enforce a' 2PL followed by space
				tout=re.sub(ur" a\'([^\s])",u" a' \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\'a\'([^\s])",u"'a' \g<1>",tout,0,re.U|re.MULTILINE)
				# same for leading A' 2PL ex.  imparative A' ye
				tout=re.sub(ur"A\'([^\s])",u"A' \g<1>",tout,0,re.U|re.MULTILINE)

				# correct usual errors
				# tout=re.sub(ur"eɛ([\s\,\.])",u"ɛ\g<1>",tout,0,re.U|re.MULTILINE)
				# tout=re.sub(ur"oɔ([\s\,\.])",u"ɔ\g<1>",tout,0,re.U|re.MULTILINE)

				if old :
					# l instead of i (doz!)
					tout=re.sub(ur"([aeiouèòyAEIOUÈÒ\s][^aeiouèò])l([^aeiouèò][aeiouèòy])",u"\g<1>i\g<2>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"([aeiouèòyAEIOUÈÒ\s][^aeiouèò])l([^aeiouèò])l",u"\g<1>i\g<2>i",tout,0,re.U|re.MULTILINE)
					
					# titres
					tout=re.sub(ur"KA BO ",u"KA BÒ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" SORO ",u" SÒRÒ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" SORO<",u" SÒRÒ<",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"NYEMOGO",u"NYÈMÒGÒ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"MOGO",u"MÒGÒ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"KORO",u"KÒRÒ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" KONO<",u" KÒNÒ<",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"YORO",u"YÒRÒ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"YEREDON",u"YÈRÈDÒN",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"YERE",u"YÈRÈ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"YELEMA",u"YÈLÈMA",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"BAMAKO ",u"BAMAKÒ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"BAMAKO<",u"BAMAKÒ<",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" DOW ",u" DÒW ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"JEKULU",u"JÈKULU ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"KE ",u"KÈ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"KE<",u"KÈ<",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" BE ",u" BÈ ",tout,0,re.U|re.MULTILINE)
					
					# abbreviations
					tout=re.sub(ur" L P K",u" LPK",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" U D P M",u" UDPM",tout,0,re.U|re.MULTILINE)
					
					# texte
					tout=re.sub(ur"òa([ \,\.\;])",u"ba\g<1>",tout,0,re.U|re.MULTILINE) # doz typo fréquente
					tout=re.sub(ur"òaya([ \,\.\;])",u"baya\g<1>",tout,0,re.U|re.MULTILINE) # doz typo fréquente
					tout=re.sub(ur" b ([ao])",u" b'\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" k ([ao])",u" k'\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" t ([ao])",u" t'\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" n ([ao])",u" n'\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" y ([ao])",u" y'\g<1>",tout,0,re.U|re.MULTILINE)

					tout=re.sub(ur"ò",u"ò",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur"è",u"è",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur"ê",u"è",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur"ë",u"è",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur"èè",u"èe",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur"eè",u"èe",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur"òò",u"òo",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur"oò",u"òo",tout,0,re.U|re.MULTILINE) # doz typo
					tout=re.sub(ur" konò([ \,\.\;])",u" kònò\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" kòno([ \,\.\;])",u" kònò\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" nyèmogo([^̀])",u" nyèmògò\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" nyèmògo([^̀])",u" nyèmògò\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" wòoro ",u" wòorò ",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" bolonɔ̀",u" bolonò",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" bolonɔw",u" bolonòw",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur"ɔ([^̀])",u"ò\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur"ɛ([^̀])",u"è\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" dantigecogo",u" dantigècogo",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" baarakela",u" baarakèla",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur"Baarakela",u"Baarakèla",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" kɛ",u" kè",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" kɛcogo",u" kècogo",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur"(o|O)kutòburu",u"\g<1>̀kutòburu",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" nyògon",u" nyògòn",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" nyogòn",u" nyògòn",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" nyogon",u" nyògòn",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur"nyògon([ \,\.\;])",u"nyògòn\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur"nyogòn([ \,\.\;])",u"nyògòn\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur"nyogon([ \,\.\;])",u"nyògòn\g<1>",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" depitèw",u" depitew",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" kèle ",u" kèlè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kelè ",u" kèlè ",tout,0,re.U|re.MULTILINE)
					# tout=re.sub(ur" kele ",u" kèlè ",tout,0,re.U|re.MULTILINE)   # dangereux avec kèle envieux, jaloux
					tout=re.sub(ur" kèlew ",u" kèlèw ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tèmen",u" tèmèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sekisòn",u" sèkisòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" siratige ",u" siratigè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fe([ \,\.\;])",u" fè\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kewale",u" kèwale",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" minenw",u" minènw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nyògònyè",u" nyògònye",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Nyògònyè",u"Nyògònye",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" laben",u" labèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sèn fɛ̀",u" sen fɛ̀",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dògòtòròse ",u"  dògòtòròso ",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" bògo ",u" bògò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bee ",u" bèe ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" beè ",u" bèe ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bènkansebèn",u" bènkansèbèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bènkansèben",u" bènkansèbèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dukòki",u" dulòki",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Dukòki",u" Dulòki",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fen ",u" fèn ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fòyi",u" foyi",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gèlen",u" gèlèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" korò([ \,\.\;])",u" kòrò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kosebè",u" kosèbè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòsòn",u" kosòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kosèbe ",u" kosèbè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòro([ \,\.\;])",u" kòrò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòsèbè",u" kosèbè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòɲuman",u" koɲuman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòɲè",u" koɲè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèle ",u" kèlè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"mogo([ \,\.\;])",u"mògò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"mògo([ \,\.\;])",u"mògò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"mogò([ \,\.\;])",u"mògò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"mògɔ̀([ \,\.\;])",u"mògò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲèmògo ",u" ɲèmògò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲemògò",u" ɲèmògò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sebèn",u" sèbèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sorò([ \,\.\;])",u" sòrò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sòro([ \,\.\;])",u" sòrò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sèben",u" sèbèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sèn kan",u" sen kan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sènfè",u" senfè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bolono ",u"bolonò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bè sèn na",u"bè sen na",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bè sènna",u"bè senna",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"fòlo ",u"fòlò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Fòlo ",u"Fòlò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gofèrenaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"goferènaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"goferenaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gòfèrenaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gòferènaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gòferenaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gòfèrènaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gòfènaman",u"gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gofèrenaman",u"Gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Goferènaman",u"Gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Goferenaman",u"Gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gòfèrenaman",u"Gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gòferènaman",u"Gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gòferenaman",u"Gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gòfèrènaman",u"Gofèrènaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nnèn([\s\,\.])",u"nnen\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nnènw ",u"nnenw ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"oò",u"ò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"sòmògò",u"somògò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tonò",u" tònò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nyògòŋ",u"nyògòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"ɲògòŋ",u"ɲògòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tògòdala",u" togodala",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tògòdaw",u" togodaw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fèn ɲènama",u" fènɲènama",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fèn nyènama",u" fènnyènama",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jira kò ",u"jira ko ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jirala kò ",u"jirala ko ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jatèminè",u"jateminè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Jatèminè",u"Jateminè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" wèlè ",u" wele ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bèè layèlen",u" bèè lajèlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"sènèkelaw",u"sènèkèlaw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gèleya",u"gèlèya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gelèya",u"gèlèya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòlògirin",u" kologirin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" siyakèda",u" ciyakèda",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dògoya",u" dògòya",tout,0,re.U|re.MULTILINE)
					#tout=re.sub(ur" dòonin",u" dòònin",tout,0,re.U|re.MULTILINE)
					#tout=re.sub(ur"-dòonin",u"-dòònin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" doonin",u" dòonin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dòòin",u" dòonin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"-dòòin",u"-dòonin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dòònin",u" dòonin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"-dòònin",u"-dòonin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" wòòro ",u" wòorò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sègère ",u" sègèrè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nògònna",u" ɲògònna",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" selekè",u" seleke",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nisòngòya",u" nisòngoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" poroze ",u" porozè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" jòsèn",u" jòsen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Sèmudetè",u" Sèmudete",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Sèmudète",u" Sèmudete",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" waleɲumandon",u" waleɲumandòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲògòya",u" nògòya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nogòya",u" nògòya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nògoya",u" nògòya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲògòntanya",u" nògòntanya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲògòlen",u" nògòlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fèère ",u" fèèrè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tiɲenen",u" tiɲènen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kècògò",u" kècogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fòɲògònko ",u" fòɲògònkò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dògòtòro ",u" dògòtòrò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dògòtorò",u" dògòtòrò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dògotòrò",u" dògòtòrò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dogòtòrò",u" dògòtòrò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ke ",u" kè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bòlo([\s\.\,])",u" bolo$1",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bolò([\s\.\,])",u" bolo$1",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kera ",u" kèra ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tèmenèn ",u" tèmènen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" temènèn ",u" tèmènen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tèmènèn ",u" tèmènen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tèmenen ",u" tèmènen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" temènen ",u" tèmènen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sòjòla",u" sojòla",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" folò",u" fòlò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mogò",u" mògò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Mogò",u"Mògò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèlèn ",u" kèlen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ani,",u" ani",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sorodasi",u" sòròdasi",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sorodasi",u"Sòròdasi",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sònya",u" sonya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gafè",u" gafe",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" walè",u" wale",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bugo ",u" bugò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dungo ",u" dungò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" batòn",u" baton",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Lamèrikèn",u"Lamerikèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lamèrikèn",u" lamerikèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sènègali",u"Senegali",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" jòre ",u" jòrè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gòferènèr",u" gòfèrènèr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gòfèrenèr",u" gòfèrènèr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gòfèrèner",u" gòfèrènèr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gofèrènèr",u" gòfèrènèr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" labatò",u" labato",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lajèlèn",u" lajèlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòmitèrè",u" komitèrè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòmitèri",u" komitèri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ziwèn",u" zuwèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Ziwèn",u" Zuwèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kafòɲògònya",u" kafoɲògònya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kafòɲògòya",u" kafoɲògònya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dowèrè",u" dòwèrè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" werèw",u" wèrèw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòròbòro ",u" kòròbòrò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sòngo ",u" sòngò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" koorisènè",u" kòòrisènè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Koorisènè",u"Kòòrisènè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ka bo ([A-ZƝŊƐƆ][^\s\n\,\.]+)",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" laɲisèbèn",u" laɲinisèbèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tò tò ",u" tò to ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲènabo ",u" ɲènabò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" negebo ",u" negebò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nsònsan",u" nsonsan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"yòro([ \,\.\;])",u"yòrò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" komasegin",u" kòmasegin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" cogòya",u" cogoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Kèrènkèren",u"Kèrènkèrèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Kèrenkèrèn",u"Kèrènkèrèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèrènkèren",u" kèrènkèrèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèrenkèrèn",u" kèrènkèrèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèrèkèrèn",u" kèrènkèrèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèrènkènnenya",u" kèrènkèrènnenya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" diyagòya",u" diyagoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Diyagòya",u"Diyagoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mangòya",u" mangoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nsòn ",u" nson ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nsònw",u" nsonw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Fòɲògònko ",u"Fòɲògònkò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fòɲògònko ",u" fòɲògònkò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dogòya",u" dògòya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sògò dun",u" sogo dun",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sògò jeni",u" sogo jeni",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sògò tòlò",u" sogo tòlò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sògoma",u" sògòma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sogòma",u" sògòma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sogoma",u" sògòma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sògoma",u"Sògòma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sogoma",u"Sògòma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntòlatan",u" ntolatan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musòya",u" musoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Musòya",u"Musoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musòw",u" musow",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musònin",u" musonin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Musòntolatan",u"Musontolatan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musòntolatan",u" musontolatan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bòlen ko yen",u" bòlen kò yen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòlòlo ",u" kòlòlò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" seko ni donko",u" seko ni dònko",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sekò ni dònkò",u" seko ni dònko",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sekò ni dònko",u" seko ni dònko",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nafolò",u" nafolo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nafolò ",u"nafolo ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" koɲènabo ",u" koɲènabò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tògoladon",u" tògòladon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nosòndiya",u" nisòndiya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" yòro ",u" yòrò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòlòsii",u" kòlòsili",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntènendon",u" ntènèndon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntenèndon",u" ntènèndon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Lamerikèjamana",u" Lamerikènjamana",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" senèkè",u" sènèkè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tògòladòn",u" tògòladon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nògòn ",u" ɲògòn ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" wulakòno ",u" wulakònò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mgòw",u" mògòw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mgò ",u" mògò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòlòkò",u" kòlòlò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntòla",u" ntola",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòmiteri",u" kòmitèri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" komiteri",u" komitèri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bòro ",u"bòrò ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" jènsen",u" jènsèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bayèlèmè",u" bayèlèma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòronfèla",u" kòrònfèla",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòròfèla",u" kòrònfèla",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" yèn([ \,\.\;])",u" yen\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sòro([ \,\.\;])",u" sòrò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sorò([ \,\.\;])",u" sòrò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tògo([ \,\.]\;)",u" tògò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" togò([ \,\.\;])",u" tògò\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sekèretèri",u" sekeretèri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ma dògò mògò si la",u" ma dogo mògò si la",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" diɲe ",u" diɲè ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòrolen",u" kòròlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" koròlen",u" kòròlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèmesarada",u" kèmèsarada",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dògò mògòw la",u" dogo mògòw la",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kecogo",u" kècogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòròyanfan",u" kòrònyanfan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" keɲeka",u" kèɲèka",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" keɲèka",u" kèɲèka",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Keɲeka",u"Kèɲèka",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fariloloɲènajè",u" farikoloɲènajè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" miliyon",u" miliyòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" zuyènkalo",u" zuwènkalo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sèsògò",u" sèsogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sisèsògò",u" sisèsogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sisefan",u" sisèfan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nkalòn",u" nkalon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Ahelihòku",u"Agelihòku",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Agèlihòki",u"Agèlihòku",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" magen",u" magèn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lakòdòn",u" lakodòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" simamatòn",u" sinamatòn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"lèn don ",u"len don ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nèn don ",u"nen don ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kèrefè",u" kèrèfè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lyè",u" Iyè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tòpòna",u" tòɲòna",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kiirititigè",u" kiiritigè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dèsèrè ",u" dèsèra ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" danbè ",u" danbe ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"ɲègònya ",u"ɲògònya ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jekulu ",u"jèkulu ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" watiyèlèma",u" waatiyèlèma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kòlòlòlò",u" kòlòlò",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sòrocogo",u" sòròcogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nyèsinnnen",u"  nyèsinnen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sèrèkili",u"  sèrikili",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sabau kè",u"  sababu kè",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nofè",u"  nòfè",tout,0,re.U|re.MULTILINE)
					
				else:
					# l instead of i (doz!)
					tout=re.sub(ur"([aeiouɛɔyAEIOUƐƆ\s][^aeiouɛɔ])l([^aeiouɛɔ][aeiouɛɔy])",u"\g<1>i\g<2>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"([aeiouɛɔyAEIOUƐƆ\s][^aeiouɛɔ])l([^aeiouɛɔ])l",u"\g<1>i\g<2>i",tout,0,re.U|re.MULTILINE)
					
					tout=re.sub(ur" bɔgo ",u" bɔgɔ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bɛe ",u" bɛɛ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bɛnkansebɛn",u" bɛnkansɛbɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bɛnkansɛben",u" bɛnkansɛbɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dukɔki",u" dulɔki",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Dukɔki",u" Dulɔki",tout,0,re.U|re.MULTILINE)
					#tout=re.sub(ur" dɔgokun",u" dɔgɔkun",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fen ",u" fɛn ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fɔyi",u" foyi",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gɛlen",u" gɛlɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" konɔ",u" kɔnɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" korɔ([\s\,\.])",u" kɔrɔ\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kosebɛ",u" kosɛbɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔsɔn",u" kosɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kosɛbe",u" kosɛbɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔro([\s\,\.])",u" kɔrɔ\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔsɛbɛ",u" kosɛbɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔɲuman",u" koɲuman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔɲɛ",u" koɲɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛle ",u" kɛlɛ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛnyɛrɛyw",u" kɛnyɛrɛyew",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛnyɛrɛyɛw",u" kɛnyɛrɛyew",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mogo",u" mɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mɔgo",u" mɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲɛmɔgo",u" ɲɛmɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲemɔgɔ",u" ɲɛmɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sebɛn",u" sɛbɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sorɔ",u" sɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔro",u" sɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔngo ",u" sɔngɔ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" songɔ ",u" sɔngɔ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɛben",u" sɛbɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɛn kan",u" sen kan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɛnfɛ",u" senfɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲɛmogo",u" ɲɛmɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bolono",u"bolonɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bɛ sɛn na",u"bɛ sen na",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bɛ sɛnna",u"bɛ senna",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"eɛ",u"ɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"fɔlo",u"fɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Fɔlo",u"Fɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gofɛrenaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"goferɛnaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"goferenaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gɔfɛrenaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gɔferɛnaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gɔferenaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gɔfɛrɛnaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gɔfɛnaman",u"gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gofɛrenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Goferɛnaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Goferenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gɔfɛrenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gɔferɛnaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gɔferenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Gɔfɛrɛnaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nnɛn([\s\,\.])",u"nnen\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nnɛnw ",u"nnenw ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"oɔ",u"ɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"sɔmɔgɔ",u"somɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tonɔ",u" tɔnɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"ɲogon",u"ɲɔgɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"ɲogɔn",u"ɲɔgɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"ɲɔgon",u"ɲɔgɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"ɲɔgɔŋ",u"ɲɔgɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɔgɔdala",u" togodala",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɔgɔdaw",u" togodaw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fɛn ɲɛnama",u" fɛnɲɛnama",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jira kɔ ",u"jira ko ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jirala kɔ ",u"jirala ko ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jatɛminɛ",u"jateminɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Jatɛminɛ",u"Jateminɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" wɛlɛ ",u" wele ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bɛɛ layɛlen",u" bɛɛ lajɛlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"sɛnɛkelaw",u"sɛnɛkɛlaw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gɛleya",u"gɛlɛya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"gelɛya",u"gɛlɛya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔlɔgirin",u" kologirin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" siyakɛda",u" ciyakɛda",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔgoya",u" dɔgɔya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔonin",u" dɔɔnin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"-dɔonin",u"-dɔɔnin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔɔin",u" dɔɔnin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"-dɔɔin",u"-dɔɔnin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" wɔɔro",u" wɔɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɛgɛre",u" sɛgɛrɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nɔgɔnna",u" ɲɔgɔnna",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" selekɛ",u" seleke",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nisɔngɔya",u" nisɔngoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" poroze",u" porozɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" jɔsɛn",u" jɔsen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Sɛmudetɛ",u" Sɛmudete",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Sɛmudɛte",u" Sɛmudete",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" waleɲumandon",u" waleɲumandɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲɔgɔya",u" nɔgɔya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nogɔya",u" nɔgɔya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nɔgoya",u" nɔgɔya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲɔgɔntanya",u" nɔgɔntanya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲɔgɔlen",u" nɔgɔlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fɛɛre",u" fɛɛrɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tiɲenen",u" tiɲɛnen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛcɔgɔ",u" kɛcogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fɔɲɔgɔnko",u" fɔɲɔgɔnkɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔgɔtɔro",u" dɔgɔtɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔgɔtorɔ",u" dɔgɔtɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔgotɔrɔ",u" dɔgɔtɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dogɔtɔrɔ",u" dɔgɔtɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ke ",u" kɛ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bɔlo([\s\.\,])",u" bolo$1",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bolɔ([\s\.\,])",u" bolo$1",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kera ",u" kɛra ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɛmenɛn ",u" tɛmɛnen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" temɛnɛn ",u" tɛmɛnen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɛmɛnɛn ",u" tɛmɛnen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɛmenen ",u" tɛmɛnen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" temɛnen ",u" tɛmɛnen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔjɔla",u" sojɔla",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" folɔ",u" fɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mogɔ",u" mɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Mogɔ",u"Mɔgɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛlɛn ",u" kɛlen ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ani,",u" ani",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sorodasi",u" sɔrɔdasi",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sorodasi",u"Sɔrɔdasi",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔnya",u" sonya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gafɛ",u" gafe",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" walɛ",u" wale",tout,0,re.U|re.MULTILINE)
					#tout=re.sub(ur" bugo",u" bugɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dungo",u" dungɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" batɔn",u" baton",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Lamɛrikɛn",u"Lamerikɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lamɛrikɛn",u" lamerikɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sɛnɛgali",u"Senegali",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" jɔre",u" jɔrɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gɔferɛnɛr",u" gɔfɛrɛnɛr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gɔfɛrenɛr",u" gɔfɛrɛnɛr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gɔfɛrɛner",u" gɔfɛrɛnɛr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gofɛrɛnɛr",u" gɔfɛrɛnɛr",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" labatɔ",u" labato",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lajɛlɛn",u" lajɛlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔmitɛrɛ",u" komitɛrɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔmitɛri",u" komitɛri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ziwɛn",u" zuwɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Ziwɛn",u" Zuwɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kafɔɲɔgɔnya",u" kafoɲɔgɔnya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kafɔɲɔgɔya",u" kafoɲɔgɔnya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dowɛrɛ",u" dɔwɛrɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" werɛw",u" wɛrɛw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔrɔbɔro",u" kɔrɔbɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔngo ",u" sɔngɔ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" koorisɛnɛ",u" kɔɔrisɛnɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Koorisɛnɛ",u"Kɔɔrisɛnɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" (?:k|K)a bo ([A-ZƝŊƐƆ][^\s\n\,\.]+)",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" laɲisɛbɛn",u" laɲinisɛbɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɔ tɔ ",u" tɔ to ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲɛnabo",u" ɲɛnabɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" negebo",u" negebɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nsɔnsan",u" nsonsan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" jɔyɔro",u" jɔyɔrɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" komasegin",u" kɔmasegin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" cogɔya",u" cogoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Kɛrɛnkɛren",u"Kɛrɛnkɛrɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Kɛrenkɛrɛn",u"Kɛrɛnkɛrɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛrɛnkɛren",u" kɛrɛnkɛrɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛrenkɛrɛn",u" kɛrɛnkɛrɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛrɛkɛrɛn",u" kɛrɛnkɛrɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛrɛnkɛnnenya",u" kɛrɛnkɛrɛnnenya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛrɛnkɛnneya",u" kɛrɛnkɛrɛnnenya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" diyagɔya",u" diyagoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Diyagɔya",u"Diyagoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mangɔya",u" mangoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nsɔn ",u" nson ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nsɔnw",u" nsonw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Fɔɲɔgɔnko",u"Fɔɲɔgɔnkɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fɔɲɔgɔnko",u" fɔɲɔgɔnkɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dogɔya",u" dɔgɔya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔgɔ dun",u" sogo dun",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔgɔ jeni",u" sogo jeni",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔgɔ tɔlɔ",u" sogo tɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔgoma",u" sɔgɔma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sogoma",u" sɔgɔma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sɔgoma",u"Sɔgɔma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Sogoma",u"Sɔgɔma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntɔlatan",u" ntolatan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musɔya",u" musoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Musɔya",u"Musoya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musɔw",u" musow",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musɔnin",u" musonin",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Musɔntolatan",u"Musontolatan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" musɔntolatan",u" musontolatan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bɔlen ko yen",u" bɔlen kɔ yen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔlɔlo",u" kɔlɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" seko ni donko",u" seko ni dɔnko",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sekɔ ni dɔnkɔ",u" seko ni dɔnko",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sekɔ ni dɔnko",u" seko ni dɔnko",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nafolɔ",u" nafolo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nafolɔ ",u"nafolo ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" koɲɛnabo",u" koɲɛnabɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɔgoladon",u" tɔgɔladon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nosɔndiya",u" nisɔndiya",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" yɔro ",u" yɔrɔ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔlɔsii",u" kɔlɔsili",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntɛnendon",u" ntɛnɛndon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntenɛndon",u" ntɛnɛndon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Lamerikɛjamana",u" Lamerikɛnjamana",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" senɛkɛ",u" sɛnɛkɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɔgɔladɔn",u" tɔgɔladon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nɔgɔn ",u" ɲɔgɔn ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" wulakɔno",u" wulakɔnɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mgɔw",u" mɔgɔw",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" mgɔ ",u" mɔgɔ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔlɔkɔ",u" kɔlɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ntɔla",u" ntola",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔmiteri",u" kɔmitɛri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" komiteri",u" komitɛri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"bɔro ",u"bɔrɔ ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" jɛnsen",u" jɛnsɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" bayɛlɛmɛ",u" bayɛlɛma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔronfɛla",u" kɔrɔnfɛla",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔrɔfɛla",u" kɔrɔnfɛla",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" yɛn([ \,\.\;])",u" yen\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔro([ \,\.\;])",u" sɔrɔ\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sorɔ([ \,\.\;])",u" sɔrɔ\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɔgo([ \,\.]\;)",u" tɔgɔ\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" togɔ([ \,\.\;])",u" tɔgɔ\g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sekɛretɛri",u" sekeretɛri",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ma dɔgɔ mɔgɔ si la",u" ma dogo mɔgɔ si la",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" diɲe",u" diɲɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔrolen",u" kɔrɔlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" korɔlen",u" kɔrɔlen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛmesarada",u" kɛmɛsarada",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔgɔ mɔgɔw la",u" dogo mɔgɔw la",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kecogo",u" kɛcogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔrɔyanfan",u" kɔrɔnyanfan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" keɲeka",u" kɛɲɛka",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" keɲɛka",u" kɛɲɛka",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Keɲeka",u"Kɛɲɛka",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" fariloloɲɛnajɛ",u" farikoloɲɛnajɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" miliyon",u" miliyɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" zuyɛnkalo",u" zuwɛnkalo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɛsɔgɔ",u" sɛsogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sisɛsɔgɔ",u" sisɛsogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sisefan",u" sisɛfan",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nkalɔn",u" nkalon",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Ahelihɔku",u"Agelihɔku",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Agɛlihɔki",u"Agɛlihɔku",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" magen",u" magɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lakɔdɔn",u" lakodɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" simamatɔn",u" sinamatɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"lɛn don ",u"len don ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"nɛn don ",u"nen don ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɛrefɛ",u" kɛrɛfɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lyɛ",u" Iyɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɔpɔna",u" tɔɲɔna",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kiirititigɛ",u" kiiritigɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɛsɛrɛ ",u" dɛsɛra ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" danbɛ ",u" danbe ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"ɲɛgɔnya ",u"ɲɔgɔnya ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"jekulu ",u"jɛkulu ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" watiyɛlɛma",u" waatiyɛlɛma",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" kɔlɔlɔlɔ",u" kɔlɔlɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɔrocogo",u" sɔrɔcogo",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" gelen",u" gɛlɛn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔron",u" dɔrɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" politimɔgɔw",u" politikimɔgɔw",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
					tout=re.sub(ur" ɲɛsinnnen",u" ɲɛsinnen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" ɲɛsinen",u" ɲɛsinnen",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sɛrɛkili",u" sɛrikili",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" sabau kɛ",u" sababu kɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Pɔtirigali",u" Pɔritigali",tout,0,re.U|re.MULTILINE) 
					tout=re.sub(ur" jɛkafo",u" jɛkafɔ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" lakɔlidɛn",u" lakɔliden",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" nofɛ",u" nɔfɛ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" Faranɛi",u" Faransi",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" desantalizasɔn",u" desantaralizasɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"Desantalizasɔn",u"Desantaralizasɔn",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔkɔtɔrɔsɔ",u" dɔkɔtɔrɔso",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" dɔgɔtɔrɔsɔ",u" dɔgɔtɔrɔso",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"cɔgɔ ",u"cogo ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" tɛriya",u" teriya",tout,0,re.U|re.MULTILINE)
					
					# erreurs de raccourcis ;e=ɛ ;o=ɔ
					tout=re.sub(ur"([A-ZƝƐƆŊ][a-zɛɔɲŋ])\;e([a-zɛɔɲŋ])",u"\g<1>ɛ\g<2>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"([A-ZƝƐƆŊ][a-zɛɔɲŋ])\;o([a-zɛɔɲŋ])",u"\g<1>ɔ\g<2>",tout,0,re.U|re.MULTILINE)
				
				
				# common to .old. and new orthography:
				tout=re.sub(ur" musomannnin",u"  musomannin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sinsinnnen",u"  sinsinnen",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sinsisn",u"  sinsin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lyemowa",u"  Iyemowa",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Misirijamana",u"  Misirajamana",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Misiri jamana",u"  Misira jamana",tout,0,re.U|re.MULTILINE)	
				tout=re.sub(ur" amadaden",u" adamaden",tout,0,re.U|re.MULTILINE)	
				tout=re.sub(ur" hamadaden",u" hadamaden",tout,0,re.U|re.MULTILINE)	
				tout=re.sub(ur" polotiki",u" politiki",tout,0,re.U|re.MULTILINE)	
				tout=re.sub(ur" Polotiki",u" Politiki",tout,0,re.U|re.MULTILINE)	
				tout=re.sub(ur" tie ",u" tle ",tout,0,re.U|re.MULTILINE)	
				tout=re.sub(ur" jamama ",u" jamana ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" tasumaden",u" tasumadon",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" miisiri",u" minisiri",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minisirise ",u"  minisiriso ",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" depitese ",u"  depiteso ",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" fangase ",u"  fangaso ",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" fase ",u"  faso ",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" kalanse ",u"  kalanso ",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" Burukina Fase ",u"  Burukina Faso",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" parity",u" pariti",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" politikow",u" politikikow",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" hamadaden",u" hadamaden",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" janana",u" jamana",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur"Musa TARAWEL[^E]",u"Musa TARAWELE",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur"Musa TARAW[^E]LE",u"Musa TARAWELE",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur"Musa TARAW[^E]L[^E]",u"Musa TARAWELE",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur"Musa TARAWE[^L]E",u"Musa TARAWELE",tout,0,re.U|re.MULTILINE)  # zup confuses sometimes
				tout=re.sub(ur" UDMP ",u" UDPM ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" UDPN ",u" UDPM ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lagisiden ",u" lasigiden ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ian ",u" jan ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" iira ",u" jira ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" anl ",u" ani ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" fill",u" fili",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minriu",u" minnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"'I ",u"'i ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"jiriwali",u"yiriwali",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"rn",u"m",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kubaru ",u" kibaru ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Kubaru ",u" Kibaru ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" poliki",u" politiki",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Minsiri",u"Minisiri",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minsiri",u" minisiri",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sinɛinni",u" sinsinni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Yufusu",u" Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" yusufu",u" Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" fanntan",u" faantan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kulubali",u" Kulubali",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ntolalatan",u" ntolatan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" faruta",u" fatura",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kaasara ",u" kasaara ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"misenw",u"misɛnw",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" denmisen",u" denmisɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲiɲini",u" ɲinini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɛnini",u" ɲɛɲini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Ɲiɲini",u"Ɲinini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afirik ",u"Afiriki ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afriki ",u"Afiriki ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afirki ",u"Afiriki ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" denmsuo",u" denmuso",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lakodon",u" lakodɔn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"D[^ɔ]kala",u"Dɔkala",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Dɔk[^a]la",u"Dɔkala",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Dɔkal[^a]",u"Dɔkala",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Dɔk[^a]l[^a] Y",u"Dɔkala Y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Yusuf[^u]",u"Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Yus[^u]fu",u"Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Y[^u]sufu",u"Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Yusiifui",u"Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Yusiifu",u"Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kurinafoni",u" kunnafoni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" dugukolono",u" dugukolonɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Kɔsiwari",u"Kɔdiwari",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" koɲyman",u" koɲuman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afirirki",u"Afiriki",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kuɲudimɔni",u" kupudimɔni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Kuɲudimɔni",u"Kupudimɔni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Mail ",u"Mali ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Mlai ",u"Mali ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Malli ",u"Mali ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minu ",u" minnu ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" jamankuntigi",u" jamanakuntigi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Jamankuntigi",u"Jamanakuntigi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minisri",u" minisiri",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Minisri",u"Minisiri",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" muturi",u" muruti",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" mututi",u" muruti",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lyadi",u" Iyadi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lburah",u" Iburah",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lbarah",u" Ibarah",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kidali",u" Kidali",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" hi ",u" ni ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" muosw",u" musow",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" turisumu",u" turisimu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lakuruya",u" lakuraya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Ola ",u"O la ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" wati ",u" waati ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" koronawisi",u" koronawirisi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Kotuba",u"Kɔtuba",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" halikila",u" hakilila",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kokronawirisi",u" koronawirisi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" koronawisi",u" koronawirisi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Kokronawirisi",u"Koronawirisi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" is ",u" si ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"YusufuJara",u"Yusufu Jara",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(ur"([A-ZƝƐƆŊ][a-zɛɔɲŋ]*)\-([A-ZƝƐƆŊ][a-zɛɔɲŋ]*) sira",u"\g<1> - \g<2> sira",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([sS])an([12][0-9]{3})",u" \g<1>an \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([sS])na ([12][0-9]{3})",u" \g<1>an \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([sS])n ([12][0-9]{3})",u" \g<1>an \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kg([0-9])",u" kg \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" km([0-9])",u" km \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ha([0-9])",u" ha \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" d([0-9])",u" d \g<1>",tout,0,re.U|re.MULTILINE)
				# numéros
				tout=re.sub(ur" no ([0-9])",u" n° \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" No ([0-9])",u" N° \g<1>",tout,0,re.U|re.MULTILINE)
				# températures
				tout=re.sub(ur" ([0-9]+)oC ",u" \g<1>°C ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([0-9]+)o ",u" \g<1>° ",tout,0,re.U|re.MULTILINE)
				
				# repeated consonants at beginning or end of word - handles only pairs: ddugu denww
				tout=re.sub(ur"w[w]+([ \s\.\,\;\:\!\?\n]) ",u"w\g<1>",tout,0,re.U|re.MULTILINE)
				# what about trailing vowels ? eg. kɔnɔɔɔ , baaraa ... mais maa !
				tout=re.sub(ur" (?P<char>[bcdfghjklmnprstwyzɲŋ])((?P=char)+)",u" \g<1>",tout,0,re.U|re.MULTILINE)
				
				# what about duplicates inside words : eg arajjo ???
				# feasible except for n : balannin - exceptions for k,l,m are in proper names
				# may break inside French word like "ville, attendre" though... aaargh
				# may break inside compound words???
				# l anyway dangerous : can hide mising wovels : dellla = delila, not dela
				tout=re.sub(ur"([aeiouɛɔ][n]*)(?P<char>[bcdfghjkmprstwyzɲŋ])((?P=char)+)([aeiouɛɔ])",u"\g<1>\g<2>\g<4>",tout,0,re.U|re.MULTILINE)
				
				# special cases with l or n
				tout=re.sub(ur" mil(l+)iyɔn",u" miliyɔn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kil(l+)o",u" kilo",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɛwal(l+)e",u" kɛwale",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɛnɛkɛl(l+)a",u" sɛnɛkɛla",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" hakilil(l+)a",u" hakilila",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" wul(l+)i",u" wuli",tout,0,re.U|re.MULTILINE)
				

				tout=re.sub(ur" nowan(n+)buru",u" nowanburu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" denmisɛn(n+)nin",u" denmisɛnnin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" komin(n+)i",u" komini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɛbɛnn(n+)i",u" sɛbɛnni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔn(n+)ɔ",u" kɔnɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minn(n+)u",u" minnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Minn(n+)u",u"Minnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɔgɔn(n+)na",u" ɲɔgɔnna",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɛrɛnkɛrɛn(n+)nen",u" kɛrɛnkɛrɛnnen",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɛrɛnkɛrɛnen",u" kɛrɛnkɛrɛnnen",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" labɛn(n+)nen",u" labɛnnen",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kun(n+)nafoni",u" kunnafoni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nin(n+)nu",u" ninnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Nin(n+)nu",u"Ninnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" dun(n+)nen",u" dunnen",tout,0,re.U|re.MULTILINE)
				
				# what about wovels extra repetition?
				tout=re.sub(ur" fɛɛ(ɛ+)rɛ",u" fɛɛrɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nɛgɛ(ɛ+)",u" nɛgɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([ '])a(a+) ",u"\g<1>a ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" tu(u+)n ",u" tun ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ni(i+) ",u" ni ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ani(i+) ",u" ani ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minisiri(i+) ",u" minisiri ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" litiri(i+) ",u" litiri ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ti(i+)le ",u" tile ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ti(i+)gi",u" tigi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"ti(i+)gi ",u"tigi ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afiri(i+)ki",u"Afiriki",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afi(i+)riki",u"Afiriki",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" yiriwali(i+) ",u" yiriwali ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Si(i+)ra ",u" Sira ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sifi(i+)lɛ",u" sifilɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kibaru(u+)",u" kibaru",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Nɔ(ɔ+)nni",u" Nɔnni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nɔ(ɔ+)nni",u" nɔnni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"yɔ(ɔ+)rɔ ",u"yɔrɔ ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɔ(ɔ+)gɔn",u" ɲɔgɔn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"ɲɔ(ɔ+)gɔn ",u"ɲɔgɔn ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" baa(a+)ra",u" baara",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" taa(a+)ri",u" taari",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɛtaa(a+)",u" ɲɛtaa",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" waa(a+)ti",u" waati",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" taa(a+)ra",u" taara",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" cogo(o+)",u" cogo",tout,0,re.U|re.MULTILINE)
				
				# second letter is CApital (problem with Zup texts sometimes)
				tout=re.sub(ur"NKa ",u"Nka ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"NKa,",u"Nka,",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"NK'a,",u"Nk'a,",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ALe ",u" Ale ",tout,0,re.U|re.MULTILINE)
				
				# unsolved : "x" on one side and «x» on the other : all with " ?
				# try with caution :
				# - space before first " : missing " cause havoc (frequent fault, all the rest is inverted)
				tout=re.sub(ur'\s"([^\n\"]+)"',u" «\g<1>»",tout,0,re.U|re.MULTILINE)
				# - or beginning of line
				tout=re.sub(ur'\n"([^\n\"]+)"',u"\n«\g<1>»",tout,0,re.U|re.MULTILINE)
				# - or beginning of <h>
				tout=re.sub(ur'\<h\>"([^\n\"]+)"',u"<h>«\g<1>»",tout,0,re.U|re.MULTILINE)
				# - or beginning of <ill>
				tout=re.sub(ur'\<ill\>"([^\n\"]+)"',u"<ill>«\g<1>»",tout,0,re.U|re.MULTILINE)
				# - or beginning of <ls>
				tout=re.sub(ur'\<ls\>"([^\n\"]+)"',u"<ls>«\g<1>»",tout,0,re.U|re.MULTILINE)

				# replace leading dot by bullet as this would cause empty sentence with dot (cf. nyè kènèya)
				tout=re.sub(ur'\n([ ]*)\. ',u"\n\g<1>• ",tout,0,re.U|re.MULTILINE)

				# remove extra spaces before </h> or after <h>
				tout=re.sub(ur'[\s]+\<\/h\>',u"</h>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur'\<h\>[\s]+',u"<h>",tout,0,re.U|re.MULTILINE)

				# - or beginning of ( parenthesis
				tout=re.sub(ur'\("([^\n\"]+)"',u"(«\g<1>»",tout,0,re.U|re.MULTILINE)
				# - or beginning just after : column
				tout=re.sub(ur'\:"([^\n\"]+)"',u":«\g<1>»",tout,0,re.U|re.MULTILINE)
				# around acronyms in capitals
				tout=re.sub(ur'"([A-ZƝŊƐƆ][A-ZƝŊƐƆ]+)"',u":«\g<1>»",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur'\'([A-ZƝŊƐƆ][A-ZƝŊƐƆ]+)\'',u":«\g<1>»",tout,0,re.U|re.MULTILINE)
				
				# spaces required after « and before »
				tout=re.sub(ur'«([^\s])',u"« \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur'([^\s])»',u"\g<1> »",tout,0,re.U|re.MULTILINE)
				
				# suppress wrong use of <st> to end mark of paragraph  (zup)
				tout=re.sub(ur"<st>\n\n",u".\n\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<st>$(?![\r\n])",u".",tout,0,re.U|re.MULTILINE)
				
				# align hyphens
				tout=re.sub(u"–",u"-",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"-",u"-",tout,0,re.U|re.MULTILINE)

				# ellipsis …
				tout=re.sub(u"\.\.\.\n",u"…\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"\.\.\. ",u"… ",tout,0,re.U|re.MULTILINE)

				# numéros
				tout=re.sub(u"°",u"°",tout,0,re.U|re.MULTILINE)

				# suppress "french style" space before double-sign puncts
				tout=re.sub(u" :",u":",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" ;",u";",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" \!",u"!",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" \?",u"?",tout,0,re.U|re.MULTILINE)

				# suppress space after assimilation quote
				tout=re.sub(u"([cdfgjklmnprstwyz])' ([aeiouɛɔ])",u"\g<1>'\g<2>",tout,0,re.U|re.MULTILINE)

				# correct incomplete tags
				tout=re.sub(ur"([^\<\/])h>",u"\g<1><h>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([^\<])/h>",u"\g<1></h>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<h([^\>])",u"<h>\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"</h([^\>])",u"</h>\g<1>",tout,0,re.U|re.MULTILINE)
				
				# correct tag mismatches (on same line)
				tout=re.sub(ur"<ill>([^<\n]+)</h>",u"<ill>\g<1></ill>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<ill>([^<\n]+)<ill>",u"<ill>\g<1></ill>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<h>([^<\n]+)<h>",u"<h>\g<1></h>",tout,0,re.U|re.MULTILINE)
				
				# enforce space after comma, 
				tout=re.sub(u"\,([^\s])",u", \g<1>",tout,0,re.U|re.MULTILINE)
				# suppress space(s) before comma,
				tout=re.sub(u"\s+\,",u",",tout,0,re.U|re.MULTILINE)
				# except in numbers (with decimals)
				tout=re.sub(u" ([0-9\.]+), ([0-9]+)",u" \g<1>,\g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" ([0-9\.]+)\. ([0-9]+)",u" \g<1>.\g<2>",tout,0,re.U|re.MULTILINE)

				# suppress space(s) before final dot, at end of paragraph
				tout=re.sub(u"\s+\.\n",u".\n",tout,0,re.U|re.MULTILINE)
				
				# suppress space(s) before final dot, at end of sentence
				tout=re.sub(u"\s+\.\s+([a-zA-ZɛɔɲŋƐƆƝŊ«])",u". \g<1>",tout,0,re.U|re.MULTILINE)
				
				# dɔrɔmɛ monetary and other units
				tout=re.sub(u" d([0-9\.\,]+)",u" d \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" d\.([0-9\.\,]+)",u" d \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" d\. ([0-9\.\,]+)",u" d \g<1>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(u" m([0-9\.\,]+)",u" m \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" m\.([0-9\.\,]+)",u" m \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" m\. ([0-9\.\,]+)",u" m \g<1>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(u" km([0-9\.\,]+)",u" km \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" km\.([0-9\.\,]+)",u" km \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" km\. ([0-9\.\,]+)",u" km \g<1>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(u" n°([0-9\.\,]+)",u" n° \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" n°\.([0-9\.\,]+)",u" n° \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" n°\. ([0-9\.\,]+)",u" n° \g<1>",tout,0,re.U|re.MULTILINE)
				
				# suppress spaces and tabs after end of line
				tout=re.sub(ur"[ \t]+\n",u"\n",tout,0,re.U|re.MULTILINE)

				# suppress extra empty lines
				tout=re.sub(ur"^\n\n",u"\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^\n\n",u"\n",tout,0,re.U|re.MULTILINE)

				# suppress remaining tabs and double spaces
				tout=re.sub(ur"\t",u" ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"  ",u" ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"  ",u" ",tout,0,re.U|re.MULTILINE)

				# unsolved : doz abuse of <ls>... <br/> ... <br/> ... </ls> 
				tout=re.sub(ur"</br>",u"<br/>",tout,0,re.U|re.MULTILINE)
				
				# poems end of para
				tout=re.sub(ur"<br/>\n\n",u"\n\n",tout,0,re.U|re.MULTILINE)
				
				# enforce punctuation before closing tags => (re)changed to AFTER! -> forces Gparser to separate this line from the next
				#tout=re.sub(ur"\.</h>\n",u"</h>.\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([^\.\;\:\!\?])[\.]*</h>\n",u"\g<1></h>.\n",tout,0,re.U|re.MULTILINE)
				#tout=re.sub(ur"\.</ill>\n",u"</ill>.\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([^\.\;\:\!\?])[\.]*</ill>\n",u"\g<1></ill>.\n",tout,0,re.U|re.MULTILINE)
				
				# numbers with dots between numgroups 281 350 -> 281.350
				tout=re.sub(ur"([0-9]+)\s([0-9]+)\s([0-9]+)",u"\g<1>.\g<2>.\g<3>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([0-9]+)\s([0-9]+)",u"\g<1>.\g<2>",tout,0,re.U|re.MULTILINE)
				
				# enforce -nan ordinal to be attached to number
				tout=re.sub(ur"([0-9])\snan",u"\g<1>nan",tout,0,re.U|re.MULTILINE)  

				# enforce nospace before percent
				tout=re.sub(ur"([0-9])\s\%",u"\g<1>%",tout,0,re.U|re.MULTILINE)  

				# enforce no space around hyphens in year sequences eg ; 1999 - 2001 kanpaɲi
				tout=re.sub(ur"([0-9]+)\s\-\s([0-9]+)",u"\g<1>-\g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Kalan - Mali",u"Kalan-Mali",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"KALAN - MALI",u"KALAN-MALI",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"CALAN - MALI",u"CALAN-MALI",tout,0,re.U|re.MULTILINE)
				
				# enforce simple list if only 2 or 3 items in list
				# to be fixed : if line already starts with - 
				tout=re.sub(ur"<ls>([^<]*)<br/>\n([^<]*)</ls>",u"- \g<1>\n\n- \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<ls>([^<]*)<br/>\n([^<]*)<br/>\n([^<]*)</ls>",u"- \g<1>\n- \g<2>\n- \g<3>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<ls>([^<]*)<br/>\n([^<]*)<br/>\n([^<]*)<br/>\n([^<]*)</ls>",u"- \g<1>\n- \g<2>\n- \g<3>\n- \g<4>",tout,0,re.U|re.MULTILINE)
				# dirty fix
				tout=re.sub(ur"\n- - ","\n- ",tout,0,re.U|re.MULTILINE)
				# suppress extra line between list items
				tout=re.sub(ur"\n- ([^\n]*)\n\n- ([^\n]*)",u"\n- \g<1>\n- \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\n- ([^\n]*)\n\n- ([^\n]*)",u"\n- \g<1>\n- \g<2>",tout,0,re.U|re.MULTILINE)
				

				# no punctuation at end of line ?
				# ([^\>\.\;\:\!\?])\n\n
				# \g<1>.\n\n
				# --------- may be problematic in some cases (eg doz tends to break para)
				tout=re.sub(ur"([^\>\.\;\:\!\?\,])\n\n",u"\g<1>.\n\n",tout,0,re.U|re.MULTILINE)

				# no line break in a middle of  a sentence (frequent in doz texts)
				tout=re.sub(ur"([^\>\n])\n([a-zA-Z0-9ɛɔɲŋƐƆƝŊ«])",u"\g<1> \g<2>",tout,0,re.U|re.MULTILINE)

				# no paragraph break after a comma
				tout=re.sub(ur"\,\n\n",u", ",tout,0,re.U|re.MULTILINE)

				# eliminate extra empty lines before EOF
				tout=re.sub(ur"(\s*\n)*\s*[\.]*$(?![\r\n])",u"",tout,0,re.U|re.MULTILINE)

				# do not allow region names after signatures (end of text)
				# to be attached
				tout=re.sub(ur"-Bamakɔ(\.*)$(?![\r\n])",u" - Bamakɔ\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Bamako(\.*)$(?![\r\n])",u" - Bamako\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Kati(\.*)$(?![\r\n])",u" - Kati\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Kita(\.*)$(?![\r\n])",u" - Kita\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Kayi(\.*)$(?![\r\n])",u" - Kayi\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Segu(\.*)$(?![\r\n])",u" - Segu\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Kulukɔrɔ(\.*)$(?![\r\n])",u" - Kulukɔrɔ\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Kolokani(\.*)$(?![\r\n])",u" - Kolokani\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Kɔlɔkani(\.*)$(?![\r\n])",u" - Kɔlɔkani\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Joyila(\.*)$(?![\r\n])",u" - Joyila\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Bananba(\.*)$(?![\r\n])",u" - Bananba\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Ɲamina(\.*)$(?![\r\n])",u" - Ɲamina\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Buguni(\.*)$(?![\r\n])",u" - Buguni\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Kucala(\.*)$(?![\r\n])",u" - Kucala\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-Sikaso(\.*)$(?![\r\n])",u" - Sikaso\g<1>",tout,0,re.U|re.MULTILINE)

				# don't leave places as separate line (Town, Region)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nKati mara la[\.]*$(?![\r\n])",u"\g<1>, Kati mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nKita mara la[\.]*$(?![\r\n])",u"\g<1>, Kita mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nSegu mara la[\.]*$(?![\r\n])",u"\g<1>, Segu mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nKayi mara la[\.]*$(?![\r\n])",u"\g<1>, Kayi mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nSikaso mara la[\.]*$(?![\r\n])",u"\g<1>, Sikaso mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nKɔlɔkani mara la[\.]*$(?![\r\n])",u"\g<1>, Kɔlɔkani mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nKangaba[\.]*$(?![\r\n])",u"\g<1>, Kangaba",tout,0,re.U|re.MULTILINE)  # TYS le plus souvent
				
				tout=re.sub(ur" ([ln]a)\.\n\nKati mara la[\.]*$(?![\r\n])",u"\g<1>, Kati mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nKita mara la[\.]*$(?![\r\n])",u"\g<1>, Kita mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nSegu mara la[\.]*$(?![\r\n])",u"\g<1>, Segu mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nKayi mara la[\.]*$(?![\r\n])",u"\g<1>, Kayi mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nSikaso mara la[\.]*$(?![\r\n])",u"\g<1>, Sikaso mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nKɔlɔkani mara la[\.]*$(?![\r\n])",u"\g<1>, Kɔlɔkani mara la",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nkomini[\.]*\n na ([^\n])$(?![\r\n])",u"\g<1> komini na \g<2>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nmara la[\.]*$(?![\r\n])",u"\g<1> mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nkomini na[\.]*$(?![\r\n])",u"\g<1> komini na",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nkomini na ([^\n]*)[\.]*$(?![\r\n])",u"\g<1> komini na \g<2>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([^\n]+) mara la[\.]*$(?![\r\n])",u"\g<1>, \g<2> mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([^\n]+) komini na[\.]*$(?![\r\n])",u"\g<1>, \g<2> komini na",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([^\n]+) komini na ([^\n]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2> komini na \g<3>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(ur" (?:k|K)a\.\n\nbɔ ([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?:k|K)a bɔ\.\n\n([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?:k|K)a\.\n\nbò ([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?:k|K)a bò\.\n\n([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)

				tout=re.sub(ur"\n(?:k|K)a\.\n\nbɔ ([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\n(?:k|K)a bɔ\.\n\n([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\n(?:k|K)a\.\n\nbò ([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\n(?:k|K)a bò\.\n\n([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)

				# animatɛri don, dugutigi don, ...
				tout=re.sub(ur"\.\n\ndon ([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" don \g<1>",tout,0,re.U|re.MULTILINE)

				tout=re.sub(ur"\.\nKucala Aka([^\n]+)$(?![\r\n])",u", Kucala Aka\g<1>",tout,0,re.U|re.MULTILINE)
				
				#remove dots at end of place in signature
				tout=re.sub(ur" (?:k|K)a bɔ ([A-ZƝŊƐƆ][^\.]*)[\.]$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?:k|K)a bò ([A-ZƝŊƐƆ][^\.]*)[\.]$(?![\r\n])",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" komini na ([^\n]*)[\.]$(?![\r\n])",u" komini na \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" mara la ([^\n]*)[\.]$(?![\r\n])",u" mara la \g<1>",tout,0,re.U|re.MULTILINE)
				
				
				# dont leave names on separate lines
				tout=re.sub(ur"Alayi Lamu\.\n\nBadama Dukure$(?![\r\n])",u"Alayi Lamu, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"A\. Lamu\.\n\nBadama Dukure$(?![\r\n])",u"A. Lamu, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Adama Jimide\.\n\nBadama Dukure$(?![\r\n])",u"Adama Jimide, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«UNESCO»\.\n\nBadama Dukure$(?![\r\n])",u"«UNESCO», Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«AFP»\.\n\nBadama Dukure$(?![\r\n])",u"«AFP», Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«OMS»\.\n\nBadama Dukure$(?![\r\n])",u"«OMS», Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Bakari Kulubali\.\n\nBadama Dukure$(?![\r\n])",u"Bakari Kulubali, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Amagirɛyi Ogobara Dolo\.\n\nBadama Dukure$(?![\r\n])",u"Amagirɛyi Ogobara Dolo, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Solomani Bobo Tunkara\.\n\nBadama Dukure$(?![\r\n])",u"Solomani Bobo Tunkara, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Amagirɛyi Ogobara Dolo\.\n\nBadama DUKURE$(?![\r\n])",u"Amagirɛyi Ogobara Dolo, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Solomani Bobo Tunkara\.\n\nBadama DUKURE$(?![\r\n])",u"Solomani Bobo Tunkara, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				#
				tout=re.sub(ur"Adama Jimide\.\n\nBasiriki Ture$(?![\r\n])",u"Adama Jimide, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Yusufu DUNBIYA\.\n\nBasiriki Ture$(?![\r\n])",u"Yusufu DUNBIYA, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				#
				tout=re.sub(ur"Alayi Lamu\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Alayi Lamu,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Alayi LAMU\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Alayi LAMU,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"A\. Lamu\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"A. Lamu,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Adama Jimide\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Adama Jimide,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Adama Jimide\.\n\n Dɔkala Yusufu Jara$(?![\r\n])",u"Adama Jimide,  Dɔkala Yusufu Jara",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Adama JIMIDE\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Adama JIMIDE,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«UNESCO»\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"«UNESCO»,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«AFP»\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"«AFP»,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«OMS»\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"«OMS»,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Bakari Kulubali\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Bakari Kulubali,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Bakari Kulubali\.\n\n Dɔkala Yusufu Jara$(?![\r\n])",u"Bakari Kulubali,  Dɔkala Yusufu Jara",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Yusufu DUNBIYA\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Yusufu DUNBIYA,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Amagirɛyi Ogobara Dolo\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Amagirɛyi Ogobara Dolo,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Solomani Bobo Tunkara\.\n\n Dɔkala Yusufu JARA$(?![\r\n])",u"Solomani Bobo Tunkara,  Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Amagirɛyi Ogobara Dolo\.\n\n Dɔkala Yusufu Jara$(?![\r\n])",u"Amagirɛyi Ogobara Dolo,  Dɔkala Yusufu Jara",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Solomani Bobo Tunkara\.\n\n Dɔkala Yusufu Jara$(?![\r\n])",u"Solomani Bobo Tunkara,  Dɔkala Yusufu Jara",tout,0,re.U|re.MULTILINE)
				# more general, 2 parts name
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama Dukure[\.]*$(?![\r\n])",u"\g<1>, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki Ture[\.]*$(?![\r\n])",u"\g<1>, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama DUKURE[\.]*$(?![\r\n])",u"\g<1>, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki TURE[\.]*$(?![\r\n])",u"\g<1>, Basiriki TURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Kɔnta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Kɔnta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KƆNTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KƆNTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Konta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Konta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KONTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KONTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nDɔkala Yusufu Jara[\.]*$(?![\r\n])",u"\g<1>, Dɔkala Yusufu Jara",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nDɔkala Yusufu JARA[\.]*$(?![\r\n])",u"\g<1>, Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nDɔkala Y\. Jara[\.]*$(?![\r\n])",u"\g<1>, Dɔkala Yusufu Jara",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nDɔkala Y\. JARA[\.]*$(?![\r\n])",u"\g<1>, Dɔkala Yusufu JARA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				
				#avec ni
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nni ([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1> ni \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nni ([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1> ni \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nni ([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1> ni \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nni ([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1> ni \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nni ([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1> ni \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nni ([A-ZƝŊƐƆ][^\.\s]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1> ni \g<2>",tout,0,re.U|re.MULTILINE)
				
				#
				#Tumani Yalamu Sidibe./Zafukuntigi./Kangaba
				tout=re.sub(ur"Tumani Yalamu Sidibe\.\n\nZafukuntigi\.\n\nKangaba$(?![\r\n])",u"Tumani Yalamu Sidibe, Zafukuntigi, Kangaba",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Tumani Y Sidibe\.\n\nZafukuntigi\.\n\nKangaba$(?![\r\n])",u"Tumani Y Sidibe, Zafukuntigi, Kangaba",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Tumani Y\. Sidibe\.\n\nZafukuntigi\.\n\nKangaba$(?![\r\n])",u"Tumani Y\. Sidibe, Zafukuntigi, Kangaba",tout,0,re.U|re.MULTILINE)
				

				# Madu Konare./Kalifabugu./Kati.
				# -> Madu Konare, Kalifabugu, Kati
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\.\s]*)[\.]*\n\n([A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>, \g<3>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*\n\n([A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>, \g<3>",tout,0,re.U|re.MULTILINE)
				# Madu Konare./Kalifabugu./(Kati).
				# -> Madu Konare, Kalifabugu (Kati)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\.\s]*)[\.]*\n\n\(([A-ZƝŊƐƆ][^\.\s]*)\)[\.]*$(?![\r\n])",u"\g<1>, \g<2> (\g<3>)",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*\n\n\(([A-ZƝŊƐƆ][^\.\s]*)\)[\.]*$(?![\r\n])",u"\g<1>, \g<2> (\g<3>)",tout,0,re.U|re.MULTILINE)
				

				# more general, 3 parts name
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama Dukure[\.]*$(?![\r\n])",u"\g<1>, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki Ture[\.]*$(?![\r\n])",u"\g<1>, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama DUKURE[\.]*$(?![\r\n])",u"\g<1>, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki TURE[\.]*$(?![\r\n])",u"\g<1>, Basiriki TURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Kɔnta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Kɔnta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KƆNTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KƆNTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Konta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Konta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KONTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KONTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				#print "pass BEFORE even more general"
				# even more general
				# REMOVED 16/10/2018 : causes hang on kibaru489_08kani2013_kuluw-doz.txt
				#        tout=re.sub(ur"^((([A-ZƝŊƐƆ][^\s\n]+)*[ ,\/]*)*)\.\n\n((([A-ZƝŊƐƆ][^\s\n]+)*[ ,\/]*)*)$(?![\r\n])",u"\g<1>, \g<4>",tout,0,re.U|re.MULTILINE)
				#print "pass even more general"
				# remove final dot after signatures - two names required - risk: possible end of legitimate sentence
				tout=re.sub(ur"([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]$(?![\r\n])",u"\g<1>",tout,0,re.U|re.MULTILINE)
				
				# force comma before known signatures
				tout=re.sub(ur"([a-zɛɔ]) Dɔkala Yusufu (Jara|JARA)",u"\g<1>, Dɔkala Yusufu \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Dɔkala Y\. (Jara|JARA)",u"\g<1>, Dɔkala Y. \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Mahamadu (Kɔnta|KƆNTA|Konta|KONTA)",u"\g<1>, Mahamadu \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Basiriki (Ture|TURE)",u"\g<1>, Basiriki \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Badama (Dukure|DUKURE)",u"\g<1>, Badama \g<2>",tout,0,re.U|re.MULTILINE)

				# dots in names (abbreviations for names) : eliminate dot (!) otherwise gparser will break sentence
				tout=re.sub(ur"([ \n])([A-ZƝŊƐƆ])\.[ ]*([A-ZƝŊƐƆ][^\.\s\n]*)",u"\g<1>\g<2> \g<3>",tout,0,re.U|re.MULTILINE)
				# need to repeat (up to 4 such cases in signatures)
				tout=re.sub(ur"([ \n])([A-ZƝŊƐƆ])\.[ ]*([A-ZƝŊƐƆ][^\.\s\n]*)",u"\g<1>\g<2> \g<3>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([ \n])([A-ZƝŊƐƆ])\.[ ]*([A-ZƝŊƐƆ][^\.\s\n]*)",u"\g<1>\g<2> \g<3>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([ \n])([A-ZƝŊƐƆ])\.[ ]*([A-ZƝŊƐƆ][^\.\s\n]*)",u"\g<1>\g<2> \g<3>",tout,0,re.U|re.MULTILINE)
				
				# isolated words in signatures
				tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(B|b)alikukalankalanden\.\n\n",u"\g<1>, \g<2>alikukalankalanden, ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(B|b)alikukalan([^\.]*)\.\n\n",u"\g<1>, \g<2>alikukalan\g<3>.\n\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(B|b)alikukalan([^\.]*)$(?![\r\n])",u"\g<1>, \g<2>alikukalan\g<3>.",tout,0,re.U|re.MULTILINE)
				
				if old:
					tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(B|b)alikukalankaramògò\.\n\n",u"\g<1>, \g<2>alikukalankaramògò, ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(L|l)akòlikaramògò\.\n\n",u"\g<1>, \g<2>akòlikaramògò, ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(A|a)nimate ̀ri\.\n\n",u"\g<1>, \g<2>nimate ̀ri, ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" (?:k|K)a bò\.\n\n([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" (?:k|K)a bò\.\n\n([A-ZƝŊƐƆ][^\.])[\.]*$(?![\r\n])",u" ka bò \g<1>.",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"\.\n\n(?:k|K)a bò ([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bò \g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"\.\n\n(?:k|K)a bò ([A-ZƝŊƐƆ][^\.\s]*\.)",u" ka bò \g<1>.",tout,0,re.U|re.MULTILINE)
				else:
					tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(B|b)alikukalankaramɔgɔ\.\n\n",u"\g<1>, \g<2>alikukalankaramɔgɔ, ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(L|l)akɔlikaramɔgɔ\.\n\n",u"\g<1>, \g<2>akɔlikaramɔgɔ, ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(A|a)nimatɛri\.\n\n",u"\g<1>, \g<2>nimatɛri, ",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" (?:k|K)a bɔ\.\n\n([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur" (?:k|K)a bɔ\.\n\n([A-ZƝŊƐƆ][^\.])[\.]*$(?![\r\n])",u" ka bɔ \g<1>.",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"\.\n\n(?:k|K)a bɔ ([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
					tout=re.sub(ur"\.\n\n(?:k|K)a bɔ ([A-ZƝŊƐƆ][^\.\s]*\.)",u" ka bɔ \g<1>.",tout,0,re.U|re.MULTILINE)
				
				
				# in signatures, replace " / " by ", "  (attention aux tags fermant type </ill>: ajouter non-<)
				tout=re.sub(ur"\n([^\n<]+)[ ]*/[ ]*([^\n>]+)$(?![\r\n])",u"\n\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\n([^\n<]+)[ ]*/[ ]*([^\n>]+)$(?![\r\n])",u"\n\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\n([^\n<]+)[ ]*/[ ]*([^\n>]+)$(?![\r\n])",u"\n\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				

				# force duplicates to stick together
				tout=re.sub(ur" (?P<stem>.+)[\s]+\-[\s]+(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?P<stem>.+)\-[\s]+(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?P<stem>.+)[\s]+\-(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)

				# fix tulon-doz presentation
				if filename.endswith("tulon-doz.txt") or filename.endswith("tulon-gedz.txt"):
					tout=re.sub(ur'(<ls>|</ls>)',u'',tout)
					tout=re.sub(ur'<br/>[\n]*',u' ',tout)
					tout=re.sub(ur'<h>Jaabi.</h>',u'Jaabi.',tout)
				
				# re-enforce NO SPACE at beginning of paragraphs
				tout=re.sub(u"\n[ ]+([^\s])",u"\n\g<1>",tout,0,re.U|re.MULTILINE)
				
				#log.write("tout:'"+tout+"'\n")
				try : 
					fileOUT = open(os.path.join(dirname, filename), "w")
				except :
					log.write("filename? "+os.path.join(dirname, filename)+"\n")
					continue

				fileOUT.write(tout)
				fileOUT.close()
log.close()
if nerr==0 : os.remove("collation-align-errors.log")
