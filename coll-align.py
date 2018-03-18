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
		for filename in filenames:
			
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

				# rectify doz strange typos
				tout=re.sub(u"а",u"a",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"А",u"A",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"В",u"B",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"с",u"c",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"С",u"C",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"е",u"e",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Е",u"E",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɒ",u"ɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɣ",u"g",tout,0,re.U|re.MULTILINE)				
				tout=re.sub(u"Н",u"H",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"í",u"i",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɩ",u"i",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"к",u"k",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"т",u"m",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"М",u"M",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"п",u"n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"щ",u"o",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"о",u"o",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"О",u"O",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Р",u"P",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"р",u"p",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"г",u"r",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"Т",u"T",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"и",u"u",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"у",u"y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ɪ",u"y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"л",u"n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"á",u"a",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ý",u"y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ú",u"u",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"№",u"N°",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ï",u"i",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"˚",u"°",tout,0,re.U|re.MULTILINE)

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

				# numéros
				tout=re.sub(u"°",u"°",tout,0,re.U|re.MULTILINE)

				# suppress "french style" space before double-sign puncts
				tout=re.sub(u" :",u":",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u" ;",u";",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" \!",u"!",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" \?",u"?",tout,0,re.U|re.MULTILINE)

				# enforce space after comma, 
				tout=re.sub(u"\,([^\s])",u", \g<1>",tout,0,re.U|re.MULTILINE)
				# suppress space(s) before comma,
				tout=re.sub(u"([\s]+)\,",u",",tout,0,re.U|re.MULTILINE)
				# except in numbers (with decimals)
				tout=re.sub(u" ([0-9\.]+), ([0-9]+)",u" \g<1>,\g<2>",tout,0,re.U|re.MULTILINE)

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
				
				# enforce punctuation before closing tags
				#tout=re.sub(ur"\.</h>\n",u"</h>.\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([^\.\;\:\!\?])</h>\n",u"\g<1>.</h>\n",tout,0,re.U|re.MULTILINE)
				#tout=re.sub(ur"\.</ill>\n",u"</ill>.\n",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([^\.\;\:\!\?])</ill>\n",u"\g<1>.</ill>\n",tout,0,re.U|re.MULTILINE)
				
				# numbers with dots between numgroups 281 350 -> 281.350
				tout=re.sub(ur"([0-9]+)\s([0-9]+)\s([0-9]+)",u"\g<1>.\g<2>.\g<3>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"([0-9]+)\s([0-9]+)",u"\g<1>.\g<2>",tout,0,re.U|re.MULTILINE)
				
				# enforce -nan ordinal to be attached to number
				tout=re.sub(ur"([0-9])\snan",u"\g<1>nan",tout,0,re.U|re.MULTILINE)  

				# enforce nospace before percent
				tout=re.sub(ur"([0-9])\s\%",u"\g<1>%",tout,0,re.U|re.MULTILINE)  

				# enforce no space aound hyphens in year sequences eg ; 1999 - 2001 kanpaɲi
				tout=re.sub(ur"([0-9]+)\s\-\s([0-9]+)",u"\g<1>-\g<2>",tout,0,re.U|re.MULTILINE)
				
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
				tout=re.sub(ur"(\s*\n)*\s*$(?![\r\n])",u"",tout,0,re.U|re.MULTILINE)

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
				
				# dont leave names on separate lines
				tout=re.sub(ur"Alayi Lamu\.\n\nBadama Dukure$(?![\r\n])",u"Alayi Lamu, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"A\. Lamu\.\n\nBadama Dukure$(?![\r\n])",u"A. Lamu, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Adama Jimide\.\n\nBadama Dukure$(?![\r\n])",u"Adama Jimide, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Adama Jimide\.\n\nBasiriki Ture$(?![\r\n])",u"Adama Jimide, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«UNESCO»\.\n\nBadama Dukure$(?![\r\n])",u"«UNESCO», Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«AFP»\.\n\nBadama Dukure$(?![\r\n])",u"«AFP», Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"«OMS»\.\n\nBadama Dukure$(?![\r\n])",u"«OMS», Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Bakari Kulubali\.\n\nBadama Dukure$(?![\r\n])",u"Bakari Kulubali, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Yusufu DUNBIYA\.\n\nBasiriki Ture$(?![\r\n])",u"Yusufu DUNBIYA, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Amagirɛyi Ogobara Dolo\.\n\nBadama Dukure$(?![\r\n])",u"Amagirɛyi Ogobara Dolo, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Solomani Bobo Tunkara\.\n\nBadama Dukure$(?![\r\n])",u"Solomani Bobo Tunkara, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Amagirɛyi Ogobara Dolo\.\n\nBadama DUKURE$(?![\r\n])",u"Amagirɛyi Ogobara Dolo, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"Solomani Bobo Tunkara\.\n\nBadama DUKURE$(?![\r\n])",u"Solomani Bobo Tunkara, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				# more general, 2 parts name
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama Dukure[\.]*$(?![\r\n])",u"\g<1>, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki Ture[\.]*$(?![\r\n])",u"\g<1>, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama DUKURE[\.]*$(?![\r\n])",u"\g<1>, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki TURE[\.]*$(?![\r\n])",u"\g<1>, Basiriki TURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Kɔnta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Kɔnta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KƆNTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KƆNTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Konta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Konta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KONTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KONTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				# more general, 3 parts name
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama Dukure[\.]*$(?![\r\n])",u"\g<1>, Badama Dukure",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki Ture[\.]*$(?![\r\n])",u"\g<1>, Basiriki Ture",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBadama DUKURE[\.]*$(?![\r\n])",u"\g<1>, Badama DUKURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nBasiriki TURE[\.]*$(?![\r\n])",u"\g<1>, Basiriki TURE",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Kɔnta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Kɔnta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KƆNTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KƆNTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu Konta[\.]*$(?![\r\n])",u"\g<1>, Mahamadu Konta",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\nMahamadu KONTA[\.]*$(?![\r\n])",u"\g<1>, Mahamadu KONTA",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"^([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)\.\n\n([A-ZƝŊƐƆ][^\s]*[\.]* [A-ZƝŊƐƆ][^\.\s]*)[\.]*$(?![\r\n])",u"\g<1>, \g<2>",tout,0,re.U|re.MULTILINE)
				
				# isolated words in signatures
				tout=re.sub(ur"([A-ZƝŊƐƆ][^\.\s]*)\.\n\n(B|b)alikukalankaramɔgɔ\.\n\n",u"\g<1>, \g<2>alikukalankaramɔgɔ, ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ka bɔ\.\n\n([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" ka bɔ\.\n\n([A-ZƝŊƐƆ][^\.\s]*\.)",u" ka bɔ \g<1>.",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\.\n\nka bɔ ([A-ZƝŊƐƆ][^\.\s]*\s[A-ZƝŊƐƆ\-])",u" ka bɔ \g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"\.\n\nka bɔ ([A-ZƝŊƐƆ][^\.\s]*\.)",u" ka bɔ \g<1>.",tout,0,re.U|re.MULTILINE)
				

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
				tout=re.sub(ur" kosɔn",u" kɔsɔn",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kosɛbe",u" kosɛbɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔro([\s\,\.])",u" kɔrɔ\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔsɛbɛ",u" kosɛbɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔɲuman",u" koɲuman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɔɲɛ",u" koɲɛ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" kɛle ",u" kɛlɛ ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" minriu",u" minnu",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" mogo",u" mɔgɔ",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" mɔgo",u" mɔgɔ",tout,0,re.U|re.MULTILINE)
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
				tout=re.sub(ur"gɔfɛrenaman",u"gɔfɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"gɔferɛnaman",u"gɔfɛrɛnaman",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur"gɔferenaman",u"gɔfɛrɛnaman",tout,0,re.U|re.MULTILINE)
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
				
				# force duplicates to stick together
				tout=re.sub(ur" (?P<stem>.+)[\s]+\-[\s]+(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?P<stem>.+)\-[\s]+(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)
				tout=re.sub(ur" (?P<stem>.+)[\s]+\-(?P=stem)", u" \g<1>-\g<1>",tout,0,re.U|re.MULTILINE)

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
