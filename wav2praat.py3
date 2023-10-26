#!/usr/bin/env python
# -*- coding: utf-8 -*-

# the purpose of this program is to handle a web link like:
# praat:https://mali-pense.net/IMG/wav/rfi20230210-kone-burukina_damandinge-ELAN.wav#t=19.948,22.389 
# - download the wav file (if not already in Downloads)
# - extract the audio segment and save it to a (smaller) wav file (if not already found in Downloads)
# - pass (send) this extracted audio to the Praat program and open it in View&Edit windows to show the Pitch blue line
#    These two actions are in a praat script (praatopen.praat) created by this program.

# in order for the praat:link to be handled (all browsers)
# the Windows installation must run praat.reg in order top update the Windows registry (regedit)
# The content of praat.reg is as follows
#     Windows Registry Editor Version 5.00
#     
#     [HKEY_CLASSES_ROOT\praat]
#     "URL Protocol"=""
#     
#     [HKEY_CLASSES_ROOT\praat\shell]
#     
#     [HKEY_CLASSES_ROOT\praat\shell\open]
#     
#     [HKEY_CLASSES_ROOT\praat\shell\open\command]
#     @="C:\\Praat\\wav2praat\\wav2praat.exe \"%1\""
#     
#  alternatively, this last line can be
#     @="\"C:\\Program Files\\Python38\\python.exe\" C:\\Praat\\wav2praat.py3 \"%1\""
# but it is dependent on the version of Python actually installed
# and %PYTHONPATH% is not available ...
# Option : distribute various .reg files: praat.reg, praat-python38.reg, praat-python39.reg, ...
#
# note : wav2praat.exe (for Windows) is created using (on Windows): pyinstaller --onefile wav2praat.py3
# which results in a 6MB file containing pythonXX.dll (this version python38), libraries, dll and pyd files.

# Installation instructions
# Installation package content : 
#    wav2praat.py3, wav2praat.exe, praat.reg, praat-python37.reg, praat-python38.reg, praat-python39.reg
# 1) if not done, install Praat in c:\Praat - normally only Praat.exe
# 2a) if Python is not installed : 
#   2a1) copy wav2praat.exe in c:\Praat
#   2a2) copy praat.reg in c:\Praat
#   2a3) run cmd with option "run as Administrator"
#   2a4) run praat.reg
#   2a5) exit - installation done!
# 2b) if Python is installed
#   2b0) check which version : in cmd : python --version
#   2b1) install pydub and praat-pythonXX.reg (if version is 3.8 XX=38) : 
#     2b1.1) copy preg-pythonXX.reg, wav2praat.py3 in c:\Praat
#     2b1.2) run cmd with option "run as Administrator"
#     2b1.3) run praat-pythonXX.reg
#     2b1.4) to install pydub, run : pip install pydub
#     2b1.5) exit - installation done!

# Security note : on 1st use, your browser will ask your permission.
# Firefox & Edge have an additional checkbox : don't ask again, allow this site permanently
# Chrome will only show this textbox if the site is trusted : 
#     Chrome Settings / Confidentiality & Security / Site parameters / Non secure content - add sites like mali-pense.net here

# ways to do the same on other platforms:
# MacOS/OSX : ?
# Linux : see https://askubuntu.com/questions/330937/is-it-possible-to-open-an-ubuntu-app-from-html

import os
import re
import sys
import pydub
import subprocess
from urllib.request import urlretrieve

Downloads=os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"\\Downloads\\"
logfile=open(Downloads+"wav2praat.log","w")

# exampge argv
# praat:https://mali-pense.net/IMG/wav/rfi20230210-kone-burukina_damandinge-ELAN.wav#t=19.948,22.389 

logfile.write("len(sys.argv)="+str(len(sys.argv))+"\n")
if len(sys.argv)>1: 
	logfile.write("sys.argv[1]="+sys.argv[1]+"\n")
else:
	logfile.write("no argument passed\n")
	sys.exit("no argument passed")

# note: not checking length or argv[1] !
praatarg=sys.argv[1][6:]   # [6:] is to remove prefix praat:
logfile.write(praatarg+" is the praatarg\n")

# note: not checking presence of #t= information !
fileurl,startend=praatarg.split("#t=")
logfile.write(fileurl+" is the file url\n")

filename=fileurl[fileurl.rfind("/")+1:]
logfile.write(filename+" is the filename\n")

# note: not checking presence of , and format of start/end times !
# caution, number formats not fixed, number of decimals may vary
tstart,tend=startend.split(",")

# start,end in milliseconds for pydub
start=int(float(tstart)*1000)
end=int(float(tend)*1000)
# restate tstart,tend in milliseconds for filename
tstart=str(start)
tend=str(end)

treename=Downloads+filename
logfile.write(treename+" is the treename to check\n")

# is file already downloaded
if os.path.exists(treename):
	logfile.write(filename+" already downloaded\n")
else:
	path, headers=urlretrieve(fileurl,treename)
	logfile.write(path+" downloaded from "+fileurl+"\n")

print(filename, start, end)
logfile.write(filename+" "+tstart+" "+tend+"\n")

selectedtreename=Downloads+filename[:-4]+"-"+tstart+"-"+tend+".wav"

if os.path.exists(selectedtreename):
	logfile.write(selectedtreename+" already exists\n")
else:
	audio=pydub.AudioSegment.from_wav(treename)
	logfile.write("audio ok\n")

	selectedaudio=audio[start:end]
	logfile.write("selected audio ok\n")

	selectedaudio.export(selectedtreename, format="wav")
	logfile.write("export "+selectedtreename+" ok\n")

# launch Praat - call or run, that is The Question

# try to launch with script file
#subprocess.run(os.environ['HOMEDRIVE']+"\\Praat\\Praat.exe --open "+selectedtreename+" ViewEdit.praat")
#   does not work 1) .praat script file needs complete treename  2) it's only open for reading, not run

# try to launch the 2 commands?
#subprocess.run(os.environ['HOMEDRIVE']+"\\Praat\\Praat.exe --open "+selectedtreename+" ; "+os.environ['HOMEDRIVE']+"\\Praat\\sendpraat.exe praat \"View & Edit\"")
#  does not work : Praat tries to load rest of line as additional files...

# try this to load file and then directly display the Pitch blue line (tone)
#subprocess.run(os.environ['HOMEDRIVE']+"\\Praat\\Praat.exe --open "+selectedtreename)
#   it does not work because 1st subprocess does not return
#subprocess.run(os.environ['HOMEDRIVE']+"\\Praat\\sendpraat.exe praat \"View & Edit\"")

# the only valid option seems to create the script file here with two lines
# as in example : https://fon.hum.uva.nl/praat/manual/Scripting_7_1__Scripting_an_editor_from_a_shell_script.html
#  sound = Read from file: "(selectedtreename)"
#  View & Edit
# and then use --new-send 
#   as mentionned in § 6 of https://fon.hum.uva.nl/praat/manual/Scripting_6_9__Calling_from_the_command_line.html
scriptfilename=Downloads+"openpraat.praat"
scriptf=open(scriptfilename,"w")
scriptf.write("sound = Read from file: \""+selectedtreename+"\"\nView & Edit\n")
scriptf.close()
logfile.write("script "+scriptfilename+" created\n")

logfile.write("Now launching Praat.exe\n")
subprocess.run(os.environ['HOMEDRIVE']+"\\Praat\\Praat.exe --new-send "+scriptfilename)

logfile.write("Praat ok, finished\n")
logfile.close()
# opportunity here to clean/delete treename and selectedtreename ?