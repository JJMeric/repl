#!/usr/bin/python
# -*- coding: utf8 -*-
# coding=UTF-8

import os
import re
import sys

global fileINname,fileINnameshort,fichier

fileINname= str(sys.argv[1])
INext=fileINname.find(".csv")
fileINnameshort=fileINname[0:INext]
fichier=fileINnameshort

fileDISname=fileINnameshort+".dis.html"
if os.path.exists(fileDISname) : 
  
  fileDIS = open(fileDISname,"r")
  html=fileDIS.read()
  fileDIS.close()
  header,tout=html.split("<body><p>")
  # (from disambextract.py3)
  sent1=tout.find('<span class="sent"')
  tout1=tout[sent1:]
  endoffile=tout1.find('</p></body></html>')-1
  tout2=tout1[:endoffile]

  # protect against possible nl suppression in manual edits (sentence splits/joins)
  tout2,n2=re.subn(r'</span></span>\n</span>\n<span class="sent">','</span>\n</span>\n</span>\n<span class="sent">',tout2,0,re.U|re.MULTILINE)
  if n2!=0:
    print(fileDISname,":",n2,"changements fin de phrase (w) Ancien format .dis -> nouveau format")

  sentences=tout2.split("</span>\n</span>\n</span>\n")  # closing tag for last w|c|t + tag for annot + tag for sent

  print(fileDISname,":",len(sentences), "sentences")
else:
  sys.exit("\n\033[1mno file named "+fileDISname+" -> cannot create -corpaudio.dis.htlm...\033[0m\n")


fileIN = open(fileINname, "r")
tout=fileIN.read()
fileIN.close()
tout=re.sub(r"\n$(?![\r\n])", "",tout)  # fixes end of file extra empty line

lines=tout.split("\n")
print(fileINname,":",len(lines)-1," sentences")

if len(sentences)!=len(lines)-1:
  sys.exit("\n      \033[1m.csv and .dis.html do not have the same number of sentences ?\033[0m\n")
else:
  print("\nWarning: .csv and .dis.html sentences are supposed to be aligned but this is not checked here!\n      Please check manually if problems arise")


lineindex=0

toutout=""

nsent=-1  # index in tab of sentences
for line in lines:
  lineindex+=1
  if lineindex==1 : continue
  if line.strip()=="": continue

  nsent+=1
  ntabs=line.count("\t")
  if ntabs >= 5:
    speaker,ref,start,end,tx,ft=line.split("\t",5)
  else: sys.exit("\033[1mtab missing ("+str(ntabs)+"/5) on line "+str(lineindex)+" :\033[0m"+line)

  # timecodes: un peu de validations (mais pas de séquence/speaker...)
  ncol=start.count(":")
  if ncol==2:
    starth,startm,starts_ms=start.split(":")
  else:
    sys.exit("\033[1mnot the right number of ':' ("+str(ncol)+"/2) on line "+str(lineindex)+" :\033[0m"+line)
  
  if "." in starts_ms:
    starts,startms=starts_ms.split(".")
  else:
    sys.exit("\033[1mstart: no dot before milliseconds on line "+str(lineindex)+" :\033[0m"+line)
  
  if int(startm)>59: sys.exit("\033[1mstart: minutes > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(starts)>59: sys.exit("\033[1mstart: seconds > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(startms)>999: sys.exit("\033[1mstart: milliseconds > 999 ??? "+str(lineindex)+" :\033[0m"+line)
  timestartms=int(startms)+int(starts)*1000+int(startm)*60000+int(starth)*3600000
  
  ncol=end.count(":")
  if ncol==2:
    endh,endm,ends_ms=end.split(":")
  else:
    sys.exit("\033[1mnot the right number of ':' ("+str(ncol)+"/2) on line "+str(lineindex)+" :\033[0m"+line)

  if "." in ends_ms:
    ends,endms=ends_ms.split(".")
  else:
    sys.exit("\033[1mend: no dot before milliseconds on line "+str(lineindex)+" :\033[0m"+line)
  if int(endm)>59: sys.exit("\033[1mend: minutes > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(ends)>59: sys.exit("\033[1mend: seconds > 59 ??? "+str(lineindex)+" :\033[0m"+line)
  if int(endms)>999: sys.exit("\033[1mend: milliseconds > 999 ??? "+str(lineindex)+" :\033[0m"+line)
  timeendms=int(endms)+int(ends)*1000+int(endm)*60000+int(endh)*3600000
  
# après les validations des timecode, injection des informations dans -corpusaudio.dis.html
  
  sent=sentences[lineindex-2]+"</span>\n</span>\n</span>\n"  # -2 because csv starts at line 2 and index in sentences starts at 0
  
  timecouple="{:.3f}".format(timestartms/1000)+","+"{:.3f}".format(timeendms/1000)

  jumpprefix='<b class="go"><a href="javascript:jump('+timecouple+');" class="ec"></a></b><span class="sent">'
  frprefix='<span class="fr">'+ft+'</span><span class="annot">'
  sent=sent.replace('<span class="sent">',jumpprefix)
  sent=sent.replace('<span class="annot">',frprefix)
  toutout+=sent



#-------------------
# injecter les styles pour "fr" et "audio"
header=re.sub(r"\n\s*</style>","""
      .fr {font-style:italic; color:grey; display:block;}
      audio {height:30px; border-radius: 8px; width:100%}
      video {border: 1px solid #aaa;  background-color: beige; height:30%; max-height:30%; object-fit: initial;} 
      ::cue {font-size: 18px; position: relative; top: 10px;}
      a:after{padding: 2px; display:none; position: relative; top: 34px; left: 2px; width: 58px; max-width: 300px;
          text-align: right; font-size:8pt; font-weight: normal; color: #fef4c5; background-color: #000000;
          -moz-border-radius: 4px; -webkit-border-radius: 4px; -ms-border-radius: 4px; border-radius: 4px;
          overflow:auto; text-decoration:none; z-index:2; }
      a:hover:after{display: inline;z-index:2;}
      .ec {width:34px;height:34px;background-image:url("/IMG/webp/play34x34.webp");background-repeat: no-repeat;
         float:left; width:60px;border-right: 2px solid white;z-index:1}
      .go {border-bottom:1px dotted pink;z-index:1}  
      /* not well fixed: layers with z-index : "play" still pushes the text after... */
      b.go a:hover{background-color: beige ;border-right: 2px solid red;z-index:2}
      b.go a:visited{background-color: lightgrey ;opacity:50%;z-index:2}
      b.go a:after{content: "play / a' y'a lamɛn";z-index:2}
      #haut {position:fixed;top:0px;left:0px;z-index:100;width:100%;border-bottom:3px solid lightslategray;background-color: lightgrey;opacity:100%;}
   </style>
"""  ,header)
header=header.replace('span.lemma, span.lemma.var { clear:','span.lemma, span.lemma.var { color: red; clear:')

audioprefix='<audio controls preload="metadata"><source src="'+fileINnameshort+'.wav" type="audio/wav"></audio></p><p>'

tout=header+'<body><p id="haut">'+audioprefix+toutout+"""</body>
   <script type="text/javascript">  
      let audiovid = "audio"; 
      if (document.getElementsByTagName(audiovid).length == 0) {
         if (document.getElementsByTagName('video').length > 0){ audiovid = "video";}
         }
      // else { alert("no <audio> or <video> tag???");}  // else always kicks in on load
      var media = document.getElementsByTagName(audiovid)[0];   // only takes in 1st audio or 1st video
      function jump(start, end) {  // jumps to time offset in seconds.milliseconds
         media.currentTime = start;
         media.play();
         setTimeout("media.pause();", (end-start)*1000+250);
      }
   </script>
</html>"""


fileOUTname=fileINnameshort+"-corpusaudio.dis.html"
fileOUT=open(fileOUTname,"w")
fileOUT.write(tout)
fileOUT.close()

print("\033[42;30;1mJob done, check output as "+fileINnameshort+"-corpusaudio.dis.html\033[0m\n")