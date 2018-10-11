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


for dirname, dirnames, filenames in sorted(os.walk('.')):
		if '.git' in dirnames: dirnames.remove('.git')  # don't go into any .git directories.

		# print path to all filenames.
		for filename in sorted(filenames):
			
			if '.txt' in filename :
				print(os.path.join(dirname, filename))
				if u" " in filename:  # spaces in filename cause no end problems in Corpus build
					nameparts=filename.split(".")
					nameitself=nameparts[0].strip()  # strip  extra spaces both ends (happens often at the end)
					if u" " in nameitself : 
						nameitself=re.sub(u" ",u"$",nameitself)   # space inside ?
					print  u"file '"+filename+u"' renamed as '"+nameitself+u".txt'"
					os.rename(os.path.join(dirname, filename),os.path.join(dirname, nameitself+u".txt"))
					filename=nameitself+u".txt"
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
				while line:
					try :
						tout=tout+line.decode("utf-8")
					except :
						log.write("character? "+os.path.join(dirname, filename)+" line:"+str(nline)+" :\n"+line+"\n")
						nerr=nerr+1
						pass
					line = fileIN.readline()

				fileIN.close()

				# handle Windows EOL
				tout=re.sub(u"\r\n",u"\n",tout,0,re.U|re.MULTILINE)

				# rectify doz strange typos (ru keyboard hazards)
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

				# enforce space between the ° of N° and the number that follows
				tout=re.sub(u"°([0-9])",u"° \g<1>",tout,0,re.U|re.MULTILINE)

				#align …  and ...
				tout=re.sub(u"…",u"...",tout,0,re.U|re.MULTILINE)

				# align braquets
				tout=re.sub(u"’",u"'",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"’",u"'",tout,0,re.U|re.MULTILINE) # problème en suspens avec les quotes simples
				tout=re.sub(u"‘",u"'",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"“",u"«",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"”",u"»",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"<<",u"«",tout,0,re.U|re.MULTILINE) # erreur fréquente chez kot
				tout=re.sub(u">>",u"»",tout,0,re.U|re.MULTILINE) 
				tout=re.sub(u"<h>»",u"<h>«",tout,0,re.U|re.MULTILINE) # erreur fréquente chez zup
				tout=re.sub(u"<ill>»",u"<ill>«",tout,0,re.U|re.MULTILINE) # erreur fréquente chez zup

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
				tout=re.sub(u"ɛiɛ",u"ɛlɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɔiɔ",u"ɔlɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɔii",u"ɔli",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"iia",u"ila",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"iie",u"ile",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"oia",u"ola",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"aii",u"ali",tout,0,re.U|re.MULTILINE)

				tout=re.sub(u"oii ",u"oli ",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(u"all([\s\.\,\;\:\!\?])",u"ali\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"aua",u"aya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" ia([\s\.\,\;\:\!\?])",u" la\g<1>",tout,0,re.U|re.MULTILINE)
				
				# enforce dɔrɔmɛ "d." attached to numbers
				tout=re.sub(u" d\. ([0-9\.]+)",u" d.\g<1>",tout,0,re.U|re.MULTILINE)
				
				
				# enforce a' 2PL followed by space
				tout=re.sub(u" a\'([^\s])",u" a' \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"\'a\'([^\s])",u"'a' \g<1>",tout,0,re.U|re.MULTILINE)
				# same for leading A' 2PL ex.  imparative A' ye
				tout=re.sub(u"A\'([^\s])",u"A' \g<1>",tout,0,re.U|re.MULTILINE)

				# correct usual errors
				# tout=re.sub(ur"eɛ([\s\,\.])",u"ɛ\g<1>",tout,0,re.U|re.MULTILINE)
				# tout=re.sub(ur"oɔ([\s\,\.])",u"ɔ\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" anl ",u" ani ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bugo ",u" bugɔ ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bɔgo ",u" bɔgɔ ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bɛe ",u" bɛɛ ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bɛnkansebɛn",u" bɛnkansɛbɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bɛnkansɛben",u" bɛnkansɛbɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" dukɔki",u" dulɔki",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Dukɔki",u" Dulɔki",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" fen ",u" fɛn ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" fill",u" fili",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur" minriu",u" minnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" mogo",u" mɔgɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" mɔgo",u" mɔgɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɛmɔgo",u" ɲɛmɔgɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲemɔgɔ",u" ɲɛmɔgɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sebɛn",u" sɛbɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sorɔ",u" sɔrɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɔro;",u" sɔrɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɛben",u" sɛbɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɛn kan",u" sen kan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɛnfɛ",u" senfɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɛmogo",u" ɲɛmɔgɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"'I ",u"'i ",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur"Gofɛrenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Goferɛnaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Goferenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Gɔfɛrenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Gɔferɛnaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Gɔferenaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Gɔfɛrɛnaman",u"Gofɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"jiriwali",u"yiriwali",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"nnɛn([\s\,\.])",u"nnen\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"nnɛnw ",u"nnenw ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"oɔ",u"ɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"rn",u"m",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur" wɛlɛ ",u" wele ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kubaru ",u" kibaru ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Kubaru ",u" Kibaru ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bɛɛ layɛlen",u" bɛɛ lajɛlen",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"sɛnɛkelaw",u"sɛnɛkɛlaw",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"gɛleya",u"gɛlɛya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"gelɛya",u"gɛlɛya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔlɔgirin",u" kologirin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" siyakɛda",u" ciyakɛda",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" dɔgoya",u" dɔgɔya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" dɔonin",u" dɔɔnin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"-dɔonin",u"-dɔɔnin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" wɔɔro",u" wɔɔrɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɛgɛre",u" sɛgɛrɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nɔgɔnna",u" ɲɔgɔnna",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" selekɛ",u" seleke",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nisɔngɔya",u" nisɔngoya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" poroze",u" porozɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" jɔsɛn",u" jɔsen",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Minsiri",u"Minisiri",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minsiri",u" minisiri",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Sɛmudetɛ",u" Sɛmudete",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" Sɛmudɛte",u" Sɛmudete",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sinɛinni",u" sinsinni",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur" kɛlɛn ",u" kɛlen ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ani,",u" ani",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sorodasi",u" sɔrɔdasi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Sorodasi",u"Sɔrɔdasi",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɔnya",u" sonya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" gafɛ",u" gafe",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" walɛ",u" wale",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bugo",u" bugɔ",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur" Yufusu",u" Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" yusufu",u" Yusufu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" fanntan",u" faantan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kafɔɲɔgɔnya",u" kafoɲɔgɔnya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kafɔɲɔgɔya",u" kafoɲɔgɔnya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" dowɛrɛ",u" dɔwɛrɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" werɛw",u" wɛrɛw",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔrɔbɔro",u" kɔrɔbɔrɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɔngo ",u" sɔngɔ ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" koorisɛnɛ",u" kɔɔrisɛnɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Koorisɛnɛ",u"Kɔɔrisɛnɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ka bo ([A-ZƝŊƐƆ][^\s\n\,\.]+)",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" laɲisɛbɛn",u" laɲinisɛbɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kulubali",u" Kulubali",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" tɔ tɔ ",u" tɔ to ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɛnabo",u" ɲɛnabɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" negebo",u" negebɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nsɔnsan",u" nsonsan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" jɔyɔro",u" jɔyɔrɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" komasegin",u" kɔmasegin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" cogɔya",u" cogoya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Kɛrɛnkɛren",u"Kɛrɛnkɛrɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɛrɛnkɛren",u" kɛrɛnkɛrɛn",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur" ntolalatan",u" ntolatan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ntɔlatan",u" ntolatan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" musɔya",u" musoya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Musɔya",u"Musoya",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" musɔw",u" musow",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" musɔnin",u" musonin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Musɔntolatan",u"Musontolatan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" musɔntolatan",u" musontolatan",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" bɔlen ko yen",u" bɔlen kɔ yen",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔlɔlo",u" kɔlɔlɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" faruta",u" fatura",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" seko ni donko",u" seko ni dɔnko",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sekɔ ni dɔnkɔ",u" seko ni dɔnko",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sekɔ ni dɔnko",u" seko ni dɔnko",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nafolɔ",u" nafolo",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"nafolɔ ",u"nafolo ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" koɲɛnabo",u" koɲɛnabɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kaasara ",u" kasaara ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"misenw",u"misɛnw",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" denmisen",u" denmisɛn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲiɲini",u" ɲinini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɛnini",u" ɲɛɲini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Ɲiɲini",u"Ɲinini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afirik ",u"Afiriki ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afriki ",u"Afiriki ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Afirki ",u"Afiriki ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" tɔgoladon",u" tɔgɔladon",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" denmsuo",u" denmuso",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" lakodon",u" lakodɔn",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur" nowan(n+)buru",u" nowanburu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" denmisɛn(n+)nin",u" denmisɛnnin",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" komin(n+)i",u" komini",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" sɛbɛnn(n+)i",u" sɛbɛnni",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔn(n+)ɔ",u" kɔnɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minn(n+)u",u" minnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ɲɔgɔn(n+)na",u" ɲɔgɔnna",tout,0,re.U|re.MULTILINE)
				
				# what abour wovels extra repetition?
				tout=re.sub(ur" fɛɛ(ɛ+)rɛ",u" fɛɛrɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" nɛgɛ(ɛ+)",u" nɛgɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([ '])a(a+) ",u"\g<1>a ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" tu(u+)n ",u" tun ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ni(i+) ",u" ni ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ani(i+) ",u" ani ",tout,0,re.U|re.MULTILINE)
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
				
				# - or beginning of ( parenthesis
				tout=re.sub(ur'\("([^\n\"]+)"',u"(«\g<1>»",tout,0,re.U|re.MULTILINE)
				# - or beginning just after : column
				tout=re.sub(ur'\:"([^\n\"]+)"',u":«\g<1>»",tout,0,re.U|re.MULTILINE)
				# around acronyms in capitals
				tout=re.sub(ur'"([A-ZƝŊƐƆ][A-ZƝŊƐƆ]+)"',u":«\g<1>»",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur'\'([A-ZƝŊƐƆ][A-ZƝŊƐƆ]+)\'',u":«\g<1>»",tout,0,re.U|re.MULTILINE)
				

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

				# correct tag mismatches (on same line)
				tout=re.sub(ur"<ill>([^<\n]+)</h>",u"<ill>\g<1></ill>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<ill>([^<\n]+)<ill>",u"<ill>\g<1></ill>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<h>([^<\n]+)<h>",u"<h>\g<1></h>",tout,0,re.U|re.MULTILINE)
				
				# enforce space after comma, 
				tout=re.sub(u"\,([^\s])",u", \g<1>",tout,0,re.U|re.MULTILINE)
				# suppress space(s) before comma,
				tout=re.sub(u"([\s]+)\,",u",",tout,0,re.U|re.MULTILINE)
				# except in numbers (with decimals)
				tout=re.sub(u" ([0-9\.]+), ([0-9]+)",u" \g<1>,\g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" ([0-9\.]+)\. ([0-9]+)",u" \g<1>.\g<2>",tout,0,re.U|re.MULTILINE)

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
				tout=re.sub(ur"<ls>(.*)<br/>\n(.*)</ls>",u"- \g<1>\n\n- \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"<ls>(.*)<br/>\n(.*)<br/>\n(.*)</ls>",u"- \g<1>\n\n- \g<2>\n\n- \g<3>",tout,0,re.U|re.MULTILINE)
				# dirty fix
				tout=re.sub(ur"\n- - ","\n- ",tout,0,re.U|re.MULTILINE)

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
				
				tout=re.sub(ur" ([ln]a)\.\n\nKati mara la[\.]*$(?![\r\n])",u"\g<1>, Kati mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nKita mara la[\.]*$(?![\r\n])",u"\g<1>, Kita mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nSegu mara la[\.]*$(?![\r\n])",u"\g<1>, Segu mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nKayi mara la[\.]*$(?![\r\n])",u"\g<1>, Kayi mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nSikaso mara la[\.]*$(?![\r\n])",u"\g<1>, Sikaso mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ([ln]a)\.\n\nKɔlɔkani mara la[\.]*$(?![\r\n])",u"\g<1>, Kɔlɔkani mara la",tout,0,re.U|re.MULTILINE)
			
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nmara la[\.]*$(?![\r\n])",u"\g<1> mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nkomini na[\.]*$(?![\r\n])",u"\g<1> komini na",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\nkomini na ([^\n]*)[\.]*$(?![\r\n])",u"\g<1> komini na \g<2>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([^\n]+) mara la[\.]*$(?![\r\n])",u"\g<1>, \g<2> mara la",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([^\n]+) komini na[\.]*$(?![\r\n])",u"\g<1>, \g<2> komini na",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"( [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([^\n]+) komini na ([^\n]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2> komini na \g<3>",tout,0,re.U|re.MULTILINE)
				
				tout=re.sub(ur" ka\.\n\nbɔ ([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ka bɔ\.\n\n([A-ZƝŊƐƆ][^\.]*)[\.]*$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				
				#remove dots at end of place in signature
				tout=re.sub(ur" ka bɔ ([A-ZƝŊƐƆ][^\.]*)[\.]$(?![\r\n])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*\, [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
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
				# even more general
				tout=re.sub(ur"^((([A-ZƝŊƐƆ][^\s\n]+)*[ ,\/]*)*)\.\n\n((([A-ZƝŊƐƆ][^\s\n]+)*[ ,\/]*)*)$(?![\r\n])",u"\g<1>, \g<4>",tout,0,re.U|re.MULTILINE)
				
				# remove final dot after signatures - two names required - risk: possible end of legitimate sentence
				tout=re.sub(ur"([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]$(?![\r\n])",u"\g<1>",tout,0,re.U|re.MULTILINE)
				
				# force comma before known signatures
				tout=re.sub(ur"([a-zɛɔ]) Dɔkala Yusufu (Jara|JARA)",u"\g<1>, Dɔkala Yusufu \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Dɔkala Y\. (Jara|JARA)",u"\g<1>, Dɔkala Y. \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Mahamadu (Kɔnta|KƆNTA|Konta|KONTA)",u"\g<1>, Mahamadu \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Basiriki (Ture|TURE)",u"\g<1>, Basiriki \g<2>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([a-zɛɔ]) Badama (Dukure|DUKURE)",u"\g<1>, Badama \g<2>",tout,0,re.U|re.MULTILINE)


				# isolated words in signatures
				tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(B|b)alikukalankaramɔgɔ\.\n\n",u"\g<1>, \g<2>alikukalankaramɔgɔ, ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ka bɔ\.\n\n([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ka bɔ\.\n\n([A-ZƝŊƐƆ][^\.])[\.]*$(?![\r\n])",u" ka bɔ \g<1>.",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\.\n\nka bɔ ([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\.\n\nka bɔ ([A-ZƝŊƐƆ][^\.\s]*\.)",u" ka bɔ \g<1>.",tout,0,re.U|re.MULTILINE)
				

								# force duplicates to stick together
				tout=re.sub(ur" (?P<stem>.+)[\s]+\-[\s]+(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?P<stem>.+)\-[\s]+(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?P<stem>.+)[\s]+\-(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)

				# fix tulon-doz presentation
				if filename.endswith("tulon-doz.txt") or filename.endswith("tulon-gedz.txt"):
					tout=re.sub(ur'(<ls>|</ls>)',u'',tout)
					tout=re.sub(ur'<br/>[\n]*',u' ',tout)
					tout=re.sub(ur'<h>Jaabi.</h>',u'Jaabi.',tout)

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
