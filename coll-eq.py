#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

nerr=0
dirdone=[]

def valign(t1,t2):   # aligns paragraphs breaks in text1 with paragraphs break styles in text2 - aka "vertical alignment"
	paras1=re.findall("([^\n]{5,15}\n\n[^\n]{5,15})",t1,re.U|re.MULTILINE)
	#print len(paras1), paras1
	if paras1 is not None:
		for para in paras1:
			# protect against invalid expression due to imbalanced parenthesis (+?)
			para=para.replace(")","\)")
			para=para.replace("(","\(")
			paranl=re.sub(u"\n\n",u"\n",para,0,re.U|re.MULTILINE)
			parasp=re.sub(u"\n\n",u" ",para,0,re.U|re.MULTILINE)
			#print parasp
			if re.search(u""+para+u"",t2,re.U|re.MULTILINE) is None:
				if re.search(u""+paranl+u"",t2,re.U|re.MULTILINE) is not None:
					paranl2=paranl.replace("\)",")")
					paranl2=paranl2.replace("\(","(")
					t1=re.sub(u""+para+u"",paranl2,t1)
				elif re.search(u""+parasp+u"",t2,re.U|re.MULTILINE) is not None:
					parasp2=parasp.replace("\)",")")
					parasp2=parasp2.replace("\(","(")
					t1=re.sub(u""+para+u"",parasp2,t1)
				# else : unknown situation
	return t1
print "================================================================="
for dirname, dirnames, files in os.walk('.'):
	if '.git' in dirnames: dirnames.remove('.git')  # don't go into any .git directories.
	for dir in sorted(dirnames):
		print "\n",dir
		if dir in dirdone  : continue
		else:
			dirdone.append(dir)
			dirkib,dirtypist=dir.split("-")
			if dirtypist=="zup" : 
				print "    (skip)","\n"
				continue
			else:
				dirzup=dirkib+"-zup"
				dirdone.append(dirzup)
				print "- ",dirzup,"\n"

				# print path to all filenames.
				folder_path='./'+dir
				for path, dirs, filenames in os.walk(folder_path):
					for filename in sorted(filenames):
						#print filename
						iroot=filename.find("-"+dirtypist+".txt")
						fileroot=filename[0:iroot]
						filezup=fileroot+"-zup.txt"
						print filename+" - "+filezup
						file1=open(os.path.join(path, filename), "rb")
						try:
							file2=open(os.path.join("./"+dirzup, filezup), "rb")
						# attention il va falloir traiter (skip) les cas où les noms diffèrent
						except: 
							file1.close()
							print " !!! file missing or name different :",filezup
							continue
						# tout1=file1.read()
						tout1=u""
						line = file1.readline()
						nline=0
						while line:
							nline=nline+1
							try :
								tout1=tout1+line.decode("utf-8")
							except :
								print "tout1 character? line:"+str(nline)+" :\n"+line+"\n"
								nerr=nerr+1
								pass
							line = file1.readline()
						# handle Windows EOL
						tout1=re.sub(u"\r\n",u"\n",tout1,0,re.U|re.MULTILINE)

						# tout2=file2.read()
						tout2=u""
						line = file2.readline()
						nline=0
						while line:
							nline=nline+1
							try :
								tout2=tout2+line.decode("utf-8")
							except :
								print "tout2 character? line:"+str(nline)+" :\n"+line+"\n"
								nerr=nerr+1
								pass
							line = file2.readline()
						# handle Windows EOL
						tout2=re.sub(u"\r\n",u"\n",tout2,0,re.U|re.MULTILINE)

						file1.close()
						file2.close()
						if tout1==tout2:
							print "    =égalité="
							pathdone="../colldone/"+dirkib
							if not os.path.exists(pathdone):
								os.mkdir(pathdone)
								print " * ",pathdone
							filedone=open(os.path.join(pathdone+"/"+fileroot+".txt"),"wb")
							filedone.write(tout1)
							filedone.close()
							print " => ",fileroot+".txt"
							os.remove(os.path.join(path, filename))
							os.remove(os.path.join("./"+dirzup, filezup))
						else:
							# check if it's only a question of paragraphs
							tout1flat=re.sub("\n\n"," ",tout1,0,re.U|re.MULTILINE)
							tout2flat=re.sub("\n\n"," ",tout2,0,re.U|re.MULTILINE)
							if tout1flat==tout2flat:
								print "   =-- égalité --="
								# il faudrait peut-être valider la structure  \n<h>...<:h>\n ?
								pathdone="../colldone/"+dirkib
								if not os.path.exists(pathdone):
									os.mkdir(pathdone)
									print " * ",pathdone
								filedone=open(os.path.join(pathdone+"/"+fileroot+".txt"),"wb")
								if len(tout1)<len(tout2) :
									filedone.write(tout1)
								else :
									filedone.write(tout2)
								filedone.close()
								print " =--> ",fileroot+".txt"
								os.remove(os.path.join(path, filename))
								os.remove(os.path.join("./"+dirzup, filezup))
							else:
								# align paragraphs as much as possible:
								tout1n=tout1
								tout2n=tout2
								tout1n=valign(tout1n,tout2n)
								tout2n=valign(tout2n,tout1n)
								if tout1n!=tout1:
									file1=open(os.path.join("./"+dir, filename), "wb")
									file1.write(tout1n)
									file1.close
									tout1=tout1n
									print "   ! ",filename," paragraphs aligned on", filezup
								if tout2n!=tout2:
									file2=open(os.path.join("./"+dirzup, filezup), "wb")
									file2.write(tout2n)
									file2.close
									tout2=tout2n
									print "   ! ",filezup," paragraphs aligned on", filename
								# for the following checks, we assume tou1 and tout2 are vertically aligned
								
								
								# missing <ill> (zup often ignores ill for Faraban Jalo and others...)
								# only one <ill> in file! (this is why it's important to ignore "< il rest of text)
								match1=re.search(ur"(\n<h>[^<]+</h>\.\n\n)(<ill>[^<]+</ill>\.\n\n)([^¤<]*)$(?![\r\n])",tout1,re.U|re.MULTILINE)
								match2=re.search(ur"(\n<h>[^<]+</h>\.\n\n)(<ill>[^<]+</ill>\.\n\n)([^¤<]*)$(?![\r\n])",tout2,re.U|re.MULTILINE)
								# but we may have above title mentions, and pre-title ...
								# more general :  ([^¤]*\n[^¤]*<h>[^<]+</h>\.\n\n)(<ill>[^<]+</ill>\.\n\n)([^¤<]*)$(?![\r\n])
								# and                    ([^¤]*\n[^¤]*<h>[^<]+</h>\.\n\n)([^¤<]*)$(?![\r\n])
								if  match1 is not None:
									if  match2 is None:
										ill=match1.group(2)
										tout2n=re.sub(ur"(\n<h>[^<]+</h>\.\n\n)([^¤<]*)$(?![\r\n])",u"\g<1>"+ill+u"\g<2>",tout2,0,re.U|re.MULTILINE)
										if tout2n!=tout2:
											file2=open(os.path.join("./"+dirzup, filezup), "wb")
											file2.write(tout2n)
											file2.close
											tout2=tout2n
											print "  !! ", filezup, "<ill> missing fixed"
										tout2flat=re.sub("\n\n"," ",tout2,0,re.U|re.MULTILINE)
										if tout1flat==tout2flat:
											print "   =<< égalité >>="
											pathdone="../colldone/"+dirkib
											if not os.path.exists(pathdone):
												os.mkdir(pathdone)
												print " * ",pathdone
											filedone=open(os.path.join(pathdone+"/"+fileroot+".txt"),"wb")
											if len(tout1)<len(tout2) :
												filedone.write(tout1)
											else :
												filedone.write(tout2)
											filedone.close()
											print " =++> ",fileroot+".txt"
											os.remove(os.path.join(path, filename))
											os.remove(os.path.join("./"+dirzup, filezup))
								# only an inversion of <ill> ?
								elif re.search(ur"(\n<h>[^<]+</h>\.\n\n)([^¤]*)(<ill>[^<]+</ill>\.\n\n)([^¤]*)$(?![\r\n])",tout2,re.U) is not None:
									tout2=re.sub(ur"(\n<h>[^<]+</h>\.\n\n)([^¤]*)(<ill>[^<]+</ill>\.\n\n)([^\n]*)$(?![\r\n])","\g<1>\g<3>\g<2>\g<4>",tout2,0,re.U|re.MULTILINE)
									file2=open(os.path.join("./"+dirzup, filezup), "wb")
									file2.write(tout2)
									file2.close
									print "<ill> aligned to top"
									tout2flat=re.sub("\n\n"," ",tout2,0,re.U|re.MULTILINE)
									if tout1flat==tout2flat:
										print "   =++ égalité ++="
										pathdone="../colldone/"+dirkib
										if not os.path.exists(pathdone):
											os.mkdir(pathdone)
											print " * ",pathdone
										filedone=open(os.path.join(pathdone+"/"+fileroot+".txt"),"wb")
										if len(tout1)<len(tout2) :
											filedone.write(tout1)
										else :
											filedone.write(tout2)
										filedone.close()
										print " =++> ",fileroot+".txt"
										os.remove(os.path.join(path, filename))
										os.remove(os.path.join("./"+dirzup, filezup))
								elif re.search(ur"(\n<h>[^<]+</h>\.\n\n)([^¤]+)(<ill>[^<]+</ill>\.)[\n]*$(?![\r\n])",tout2,re.U) is not None:
									tout2=re.sub(ur"(\n<h>[^<]+</h>\.\n\n)([^¤]+)(<ill>[^<]+</ill>\.)[\n]*$(?![\r\n])","\g<1>\g<3>\n\n\g<2>",tout2,0,re.U|re.MULTILINE)
									file2=open(os.path.join("./"+dirzup, filezup), "wb")
									file2.write(tout2)
									file2.close
									print "<ill> aligned to bottom"
									tout2flat=re.sub("\n\n"," ",tout2,0,re.U|re.MULTILINE)
									if tout1flat==tout2flat:
										print "   =++ égalité ++="
										pathdone="../colldone/"+dirkib
										if not os.path.exists(pathdone):
											os.mkdir(pathdone)
											print " * ",pathdone
										filedone=open(os.path.join(pathdone+"/"+fileroot+".txt"),"wb")
										if len(tout1)<len(tout2) :
											filedone.write(tout1)
										else :
											filedone.write(tout2)
										filedone.close()
										print " =++> ",fileroot+".txt"
										os.remove(os.path.join(path, filename))
										os.remove(os.path.join("./"+dirzup, filezup))