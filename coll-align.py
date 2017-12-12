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
				tout=re.sub(u"á",u"a",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ý",u"y",tout,0,re.U|re.MULTILINE)
				tout=re.sub(u"ú",u"u",tout,0,re.U|re.MULTILINE)

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
