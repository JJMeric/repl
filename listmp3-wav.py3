#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import pydub

def timecode(m):     # returns timecode formatted as a string "00:00:00.000"
	secs=m/1000   # float
	mns=int(secs/60)
	h=int(mns/60)
	mn=mns-h*60
	s=secs-mns*60
	return f"{h:02d}:{mn:02d}:{s:06.3f}"

# all input files in same directory, name structure XX-YY.mp3 with XX fixed and YY incremental
# resulting wav file as XX-ref-timecodes.csv (tab separated values) and XX.wav


# might run on several directories, starting from current

for dirname, dirnames, filenames in sorted(os.walk('.')):
	if '.git' in dirnames: dirnames.remove('.git') # don't go into any .git directories.

	filenames=sorted(filenames) # peut-être pas nécessaire

	tmillis=0
	end=timecode(tmillis)
	taudio=pydub.AudioSegment.empty()
	fout=open("XX-ref-timecodes.csv","w")
	fout.write("ref@B\tstart\tend\n")


	for filename in filenames :
		select=".mp3"
		
		if select in filename :
			mp3file=filename[:-4]
			audio=pydub.AudioSegment.from_mp3(filename)
			millis=len(audio)  # length in milli-seconds
			start=end
			tmillis+=millis
			end=timecode(tmillis)
			print(mp3file,start,end)
			fout.write(mp3file+"\t"+start+"\t"+end+"\n")
			taudio+=audio

	fout.close()
	if tmillis>0:
		prefix=mp3file[:2]
		taudio.export(prefix+".wav", format="wav")
		os.rename("XX-ref-timecodes.csv",prefix+"-ref-timecodes.csv")
		print("* files ready *")
	else:
		os.remove("XX-ref-timecodes.csv")
