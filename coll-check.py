#!/usr/bin/env python
# -*- coding: utf-8 -*-

# checks that files in *this* directory have a collationed version in ../colldone
#
# for collation work, the recommended directory structure is
# /collations         (download place for rar, zip, pdf files
# /collations/colltodo    (pairs of directories of pre-collated texts, there is always one -zup), for instance
# /collations/colltodo/kibaru570-doz
# /collations/colltodo/kibaru570-zup
# /collations/colldone   (directories of collated texts - result of collation work) for instance
# /collations/colldone/kibaru570        (this will later on sent to VV, be placed on GIT, /corbama/kibaru/kibaru570, then archived...)
# /collations/archives   (this is were the pre-collated texts move when work is finished), for instance
# /collations/archives/kibaru569-doz
# /collations/archives/kibaru569-zup
# /collations/archives/kibaru569
#
# this program : checks that all files in colltodo/xxx-zup exist with same name in colldone/xxx
#                          then moves collated texts in colltodo/xxx-zup & xxx-doz to archives/xxx-zup & xxx-doz
#
# use:
#     cd collations/colltodo
#     python ~/GIT/repl/coll-check.py kibaruXXX
#

import os
import re
import shutil
import sys
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os

nargv=len(sys.argv)
if nargv==1 : 
  sys.exit("coll-check.py needs -at least- one argument : directory name, as in\n coll-check.py KibaruXXX")
  
if nargv>1 : dirtocheck= str(sys.argv[1])

if "-zup" in dirtocheck: sys.exit("please give directory name without -zup at the end")
rundir=os.getcwd()
if not rundir.endswith("colltodo") : sys.exit("here is not colltodo? "+rundir)

refdone=dirtocheck
refcurr=dirtocheck+"-zup"
refdir=rundir+"/"+refcurr

nerr=0
dirdone=[]

print "=== checking if there are missing files ==="
missing=0
# refdir=os.getcwd()
# refdirels=refdir.split("/")
# refcurr=refdirels[len(refdirels)-1]
# refdone=re.sub(r"\-zup","",refcurr)
donedir="../colldone/"+refdone
print refcurr," VS ",donedir,"\n"
# reflist=os.listdir(".")
reflist=os.listdir(refcurr)
donelist=os.listdir(donedir)

for ref in reflist :
                        donelookup=re.sub(r"-zup\.txt",".txt",ref)
                        donelookupold=re.sub(r"-zup\.txt",".old.txt",ref)
                        if donelookup not in donelist and donelookupold not in donelist:
                              missing=missing+1
                              print donelookup
if missing>0 : print "\n",missing," files missing in ",donedir ,"\n"
else : 
	print "\nOK"
	# os.chdir("../../")
	topdir="../"
	archdir=topdir+"archives"+"/"+refcurr
	if not os.path.isdir(archdir): 
		os.mkdir(archdir)
		# print archdir," created"
	# print "moving to ? ",archdir
	for node in os.listdir(refdir):
		reffile=os.path.join(refdir, node)
		archfile=os.path.join(archdir, node)
		shutil.move(reffile , archfile)
      	# check if refdir empty
      	if len(os.listdir(refdir))==0 :
      		os.rmdir(refdir)
      		print refcurr," moved to ",archdir
      	extdoz="-doz"
      	# refdoz=topdir+"/colltodo/"+refdone+extdoz
      	refdoz=refdone+extdoz
      	if not os.path.isdir(refdoz):
      		extdoz="-gedz"
      		#refdoz=topdir+"colltodo/"+refdone+extdoz
      		refdoz=refdone+extdoz
      	if not os.path.isdir(refdoz):
       		extdoz="-kot"
      		#refdoz=topdir+"colltodo/"+refdone+extdoz
      		refdoz=refdone+extdoz
      	if not os.path.isdir(refdoz):
      		sys.exit("other typist dir "+refdoz+"not found, tried -doz, -gedz, -kot: "+refdone+"-xxx ?")	
      	archdir=topdir+"archives"+"/"+refdone+extdoz
	if not os.path.isdir(archdir): 
		os.mkdir(archdir)
		# print archdir," created"
	# print "moving to ? ",archdir
	for node in os.listdir(refdoz):
		reffile=os.path.join(refdoz, node)
		archfile=os.path.join(archdir, node)
		shutil.move(reffile , archfile)
      	# check if refdir empty
      	if len(os.listdir(refdoz))==0 :
      		os.rmdir(refdoz)
      		print refdoz," moved to ",archdir
      	
      	#os.chroot(topdir+"/colltodo")
