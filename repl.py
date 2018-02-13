#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT : éviter la méthode "replace" qui retourne une chaine en ANSI - utiliser re.sub
# xxx.py on line x, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details

# entrée : le fichier.XXX.pars.html
# entrée : le fichier REPL.txt qui doit être dans le même répertoire
#          (voir ci-dessous : il peut être customisé pour un texte particulier : noms des personnages, etc)
#          Format de ce fichier : chaque ligne contient une sequence "non ambigüe en bambara non tonal dans tous contextes"
#          donc de préférence une sequence de plus de 3 mots, pour chaque mot: le mot et sa desambiguisation: le lexeme:la partie du discours:la glose
#           exemples d'ambiguités à éviter dans ce fichier:
#             1 mot : ɲɛna : peut être à la fois le perfectif de ɲɛ́ mais aussi la postposition ɲɛ́na "devant"
#             2 mots : "a ko" peut vouloir dire "il a dit" mais aussi "l'affaire de ça"
#             ... FAIRE TRES ATTENTION AVANT D'ABIMER COMPLETEMENT VOTRE FICHIER - FAIRE TOUJOURS DES SAUVEGARDES AVANT!
#          chaque ligne est en deux parties séparées par ===
#             la première partie contient les mots
#             la deuxième partie contient les désambiguisations
#          Dans chaque partie, le mots sont séparés par 1 seul underline _, les desambiguisations aussi
#          tout doit être tonalisé de façon a être utilisable sur un texte tonalisé
#          exemple : ò_tɛ́_báasi_yé===ò:prn:ce_tɛ́:cop:COP.NEG_báasi:n:problème_yé:pp:PP
#          NB: on peut introduire des gloses complexes, comme par exemple sɔ̀rɔla:v: [sòrɔ:v:obtenir la:mrph:PFV.INTR]
#             ex: ò_tɛ̀mɛnen_kɔ́===ò:prn:ce_tɛ̀mɛnen:ptcp: [tɛ̀mɛ:v:passer nen:mrph:PTCP.RES]_kɔ́:pp:après
#          NB2 : le nombre de mots n'est pas forcément égal de part et d'autre du === ce qui permet des abbréviations comme "i ko min" -> "iko"
#          NB3 : les commentaires dans le fichier REPL sont recommandés : # en début de ligne
# sortie : le fichier XXX.repl.html
# sortie : le fichier XXX.remplacements.log.txt   listant les nombres de remplacements effectués

# cas particulier : si on veut faire des remplacements dans le fichier .dis :
# renommer votre fichier REPLperso.txt en REPL.txt, dans le même répertoire que le fichier .dis.html
# derrière la commande repl-globaux.py, entrer le nom complet du fichier (avec .dis.html à la fin)
# Le fichier en sortie sera toujours le fichier .repl.html
# si vous êtes OK avec ce fichier, renommer l'ancien fichier .dis.html en .disXXX.html (ou XXX est un n° séquentiel, n° de version)
#                    puis renommer le fichier .repl.html en .dis.html afin de l'utiliser dans gdisamb

# appel : repl-globaux.py NAMEFICH OPTION
# ou les paramètres sont : 
#    NAMEFICH : par exemple dumestre_geste_de_segu_4avenement_da (SANS l'extension ".pars.html")
#              ou alors le nom complet si c'est un fichier .dis : dumestre_geste_de_segu_4avenement_da.dis.html
#    OPTION : seulement si c'est un texte tonal, indiquer : tonal
#             si c'est un texte Bailleul (tonal sans ton haut) : bailleul
# par exemple : rempl-globaux.py dumestre_geste_de_segu_4avenement_da tonal
#
# A DEVELOPPER

# . marquer les alertes pour signaler certains remplacements dangereux ; ! en début de ligne (man gɛlɛn)
# . marqueurs génériques : ^ début de ligne (class annot),  $ fin de ligne  (utile en particulier pour les PP : ex: yé_$ mais aussi dɛ́_$)
# . primitives génériques : PERS pour tous les pronoms personnels (+ PERSSG, PERSPL ...)
# . GLOSS génériques : N ADJ V PRMRK... (par exemple pour automatiser "bɛ N dun", "PRMRK boli") - nécessite de s'assurer le caractère unique des gloss intermédiaires!
# PROJET
# détecter des AMBIGUOUShasname à changer en AMBIGUOUSselectname
# 1ère tentative AMBIGUOUShasname : <span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)</span><sub class="ps">([^<]+)</sub>([^<]*)</sub>(<span class="lemma var">[^<]+<sub class="ps">[.]+</sub><sub class="gloss">[.]+</sub>)</span)\n</span>

import os
import re
#import regex # TESTS NON CONCLUANTS PAR RAPPORT A re // (((?!lemma\svar).)*)
# il faudrait pouvoir utiliser à la place Oniguruma , comme Sublime Text 2
# problème résolu maintenant mais je laisse quand même ce commentaire pour référence 2/5/16
import sys
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import daba.formats
import unicodedata as u
from time import gmtime, strftime, time
# print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
import time
timestart=time.time()
# directory where this script resides
scriptdir = os.path.dirname(os.path.realpath(__file__))

def update_progress(progress):
    barLength = 40 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\r[{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), int(progress*1000)/10.0, status)
    sys.stdout.write(text)
    sys.stdout.flush()

#à compléter : 
# 1) débuts et fins de phrase (+ de ligne, ponctuations...)
# 2) variantes : ok pour le pipe ?
# 3) assimilations : évitons pour l'instant
# 4) variables, par ex PERS=(ń|í|à|án|áw|ù|né|àle|ále|òlu)
# ------------------------------------------------------------------------------

wordsearch=re.compile(ur'\<span class\=\"w\"\ stage=\"([a-z0-9\.\-]*)\">([^\<]*)\<')
lemmasearch=re.compile(ur'\<span class\=\"lemma\"\>([^\<]*)\<')
psambsearch=re.compile(ur'<span class="lemma">[^\<]+<sub class="ps">([^\<]+/[^\<]+)<')
lemmavarsearch=re.compile(ur'\<span class\=\"lemma var\"\>([^\<]*)\<')
punctsearch=re.compile(ur'\<span class\=\"c\">([^\<]*)\<')
assimsearch=re.compile(ur'\'$')
assimilation=0
glosssearch=re.compile(ur'\<sub class\=\"gloss\"\>([^\<]*)\<')
ambiguous=re.compile(ur'\<span class\=\"w\".*lemma var.*\n\<\/span\>')
textscript=re.compile(ur'\<meta content\=\"([^\"]*)\" name\=\"text\:script\" \/\>',re.U)

nmmcquestion=0

nargv=len(sys.argv)
if nargv==1 : 
  print "repl.py needs -at least- one argument : file name"
  sys.exit
if nargv>1 : filename= str(sys.argv[1])


if ".pars.html" in filename :
  i_pars=filename.find(".pars.html")
  filenametemp=filename[0:i_pars]
# sauf si on donne en entrée un fichier dis
elif ".dis.html" in filename :   
  filenamein=filename
  i_dis=filename.find(".dis.html")
  filenametemp=filename[0:i_dis]
else : # nom donné sans extension (défaut recommandé)
  filenamein=filename+".pars.html"
  filenametemp=filename

filenameout=filenametemp+".repl.html"

fileIN = open(filenamein, "rb")
#fileIN = open(filenamein, "r")
fileOUT = open (filenameout,"wb")
tonal=""
arg=""
notfast=True

if nargv>2 : 
  arg= str(sys.argv[2])
  # print "arg="+arg

  if arg=="check" or arg=="-check" :
    try:
      fileMMC=open("bamadaba-mmc.txt")
    except : sys.exit ("arg 'check' needs file bamadaba-mmc.txt in current directory")
    mmc=[]
    mmcshort=[]
    linemmc=fileMMC.readline()
    while linemmc:
      entrymmc=linemmc[0:len(linemmc)-1] # strip trailing linefeed
      mmc.append(entrymmc)
      # handle variants & double ps
      mmclist=entrymmc.split(u":",2)
      mmclx=mmclist[0]
      mmcps=mmclist[1]
      mmcgloss=mmclist[2]   # au sens large avec les sous gloses
      mmcgloss1=mmcgloss
      if u"[" in mmcgloss: 
        mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
      mmcshort.append(mmclx+u":"+mmcps+u":"+mmcgloss)
      #log.write( "\n"+entrymmc+"\n")
      #log.write( "lx="+mmclx+"\n")
      #log.write( "ps="+mmcps+"\n")
      #log.write( "gl="+mmcgloss+"\n")
      if u"|" in mmclx :
        #log.write( "\n"+entrymmc+"\n")
        mmclxlist=mmclx.split(u"|")
        for mmclxel in mmclxlist:
          mmc.append(mmclxel+u":"+mmcps+u":"+mmcgloss1)
          #log.write(mmclxel+u":"+mmcps+u":"+mmcgloss+"\n")
          if u"[" in mmcgloss: 
            mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
          mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)
          if u"/" in mmcps:
            mmcpslist=mmcps.split(u"/")
            for mmcpsel in mmcpslist:
              mmc.append(mmclxel+u":"+mmcpsel+u":"+mmcgloss1)
              #log.write(mmclxel+u":"+mmcpsel+u":"+mmcgloss+"\n")
              if u"[" in mmcgloss: 
                mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
              mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)

      if u"/" in mmcps:
        #log.write( "\n"+entrymmc+"\n")
        mmcpslist=mmcps.split(u"/")
        for mmcpsel in mmcpslist:
          mmc.append(mmclx+u":"+mmcpsel+u":"+mmcgloss1)
          #log.write(mmclx+u":"+mmcpsel+u":"+mmcgloss+"\n")
          if u"[" in mmcgloss: 
            mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
          mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)

      #if len(mmc)>2000 : break

      linemmc=fileMMC.readline()
    fileMMC.close()
    print "check : mmc loaded "+str(len(mmc))+" words"
    #print 'sample 50 : "'+mmc[50]+'" '
    #print 'sample 12000 : "'+mmc[12000]+'" '
  elif arg=="fast" or arg=="-fast" :
   notfast=False
   try:
      fileREPC= open ("REPL-C.txt","r")
      print "using REPL-C.txt"
   except : 
    try:
      fileREPCname="REPL-STANDARD-C.txt"
      if filenametemp.endswith(".old") and "baabu_ni_baabu" not in filenametemp :
          fileREPCname = "REPL-STANDARD-C.old.txt"
          tonal = "old"
      else:
          tonal = "new"
      fileREPC = open (fileREPCname,"r")
      # print "Compiled rules from : "+fileREPCname
    except:
      try:
        fileREPCname = os.path.join(scriptdir, "REPL-STANDARD-C.txt")
        if filenametemp.endswith(".old")  and "baabu_ni_baabu" not in filenametemp:
            fileREPCname = os.path.join(scriptdir, "REPL-STANDARD-C.old.txt")
        fileREPC = open (fileREPCname,"r")
        # print "Compiled rules from : "+fileREPCname
      except :
        sys.exit("repl.py needs a REPL-C.txt file or a REPL-STANDARD-C.txt file in the current directory (or in REPL)")

if notfast:
  try:
    fileREP = open ("REPL.txt","rb")
    print "using REPL.txt"
  except : 
    try:
      fileREP = open ("REPL-STANDARD.txt","rb")
      print "using REPL-STANDARD.txt"
    except:
      try:
        fileREP = open(os.path.join(scriptdir, "REPL-STANDARD.txt"), "r")
        print "using {}".format(os.path.join(scriptdir, "REPL-STANDARD.txt"))
      except :
        sys.exit("repl.py needs a REPL.txt file or a REPL-STANDARD.txt file in the current directory (or in REPL)")

  logfilename=filenametemp+"-replacements.log"
  log =  open (logfilename,"w")

  toutrepl=fileREP.read()
  nlignereplall=toutrepl.count(u"\n")
  nlignereplact=re.findall(ur"\n[^\#\s\n]",toutrepl,re.U+re.MULTILINE)
  nlignerepl=len(nlignereplact)
  print nlignereplall," lignes   ", nlignerepl," règles"
  #fileREP.seek(0, 0)

nligne=1
nbreplok=0
nbmodif=0
nbmots=0
nbrulesapplied=0

newline="@"
tout=u""
sub0=u""
lineOUT=u""
tout=fileIN.read()
tout=tout.decode("utf-8")
"""
line = fileIN.readline()
while line:
  tout=tout+line.decode("utf-8")
  nligne=nligne+1
  line = fileIN.readline()
"""
nligne=tout.count(u"\n")

# script=textscript.search(tout).group(1)
txtsc=textscript.search(tout)
if txtsc!=None :   # supposedly = if txtsc :
  script=txtsc.group(1)
else :
    script="Nouvel orthographe malien"
    if filenametemp.endswith(".old"): script="Ancien orthographe malien"
    print " ! textscript not set for "+filenametemp+" !!!  ASSUMED : "+script

if notfast: print "text:script="+script
if script=="Ancien orthographe malien" : tonal="old"
elif script=="Nouvel orthographe malien" : tonal="new"
# elif script=="bailleul" : tonal="bailleul" # <---------- n'existe pas en réalité, vérifier arg !!!

if "baabu_ni_baabu" in filename: tonal="new"

if arg=="tonal" : tonal="tonal"
elif arg=="bailleul" : tonal="bailleul"

if tonal=="" : sys.exit("text:script non defini : pas de meta ou pas d'argument (tonal, bailleul)")

totalmots = tout.count("class=\"w\"")   # is needed in the final message to compute average ambiguous left and elapse time/word
    
if notfast:
    print tout.count("class=\"annot\""), " phrases"
    print totalmots, " mots"

if notfast:
    ambs = ambiguous.findall(tout)
    nbambs = len(ambs)
    print nbambs, " mots ambigus restants apres gparser, soit : ", 100*nbambs/totalmots, "%"
    psambs = psambsearch.findall(tout)
    nbpsambs = len(psambs)
    psambslist = ""
    if nbpsambs > 0:
      for psamb in psambs:
        if psamb not in psambslist: psambslist=psambslist+psamb+" "
    print nbpsambs, " ps ambigues ( "+psambslist+")", 100*nbpsambs/totalmots, "%"

psvalides="|adj|adv|adv.p|conj|conv.n|cop|dtm|intj|mrph|n|n.prop|num|onomat|pers|pm|pp|prep|prn|prt|ptcp|v|vq|"
valides=u"_COMMA_DOT_QUESTION_COLON_SEMICOLON_EXCLAM_PUNCT_NAME_NPROPRE_NPROPRENOMM_NPROPRENOMF_NPROPRENOMMF_NPROPRENOMCL_NPROPRETOP_PERS_PRONOM_VERBE_VPERF_VQ_DTM_PARTICIPE_PRMRK_COPULE_ADJECTIF_POSTP_NUM_NUMANNEE_ADV_ADVP_CONJ_PREP_AMBIGUOUS_DEGRE_DEBUT_BREAK_ADVN_PRT_LAQUO_RAQUO_PARO_PARF_GUILLEMET_PRMRKQUAL_VQADJ_CONJPREP_COMMENT_TAG_FIN_CONJPOSS_PRNDTM_TIRET_ADJN_DOONIN_PERCENT_NORV_AORN_DORP_ADJORD_PMORCOP_"
# toujours commencer et finir par _
# autres mots utilisés, traitements spéciaux : NUMnan, degremove, ADVNforcen, ADVNforceadv, CONJPREPforceconj, CONJPREPforceprep
gvalides=u"NOM.M_NOM.F_NOM.MF_NOM.CL_NOM.ETRG_NOM.FRA_CFA_FUT_QUOT_PP_IN_CNTRL_PROG_PFV.INTR_PL_PL2_AUGM_AG.OCC_PTCP.PRIV_GENT_AG.PRM_LOC_PRICE_MNT1_MNT2_STAT_INSTR_PTCP.RES_NMLZ_COM_RECP.PRN_ADJ_DIR_ORD_DIM_PRIV_AG.EX_RECP_PTCP.POT_CONV.PROG_ST_DEQU_ABSTR_CAUS_SUPER_IN_EN_1SG_1SG.EMPH_2SG_2SG.EMPH_3SG_3SG.EMPH_1PL_1PL.EMPH_2PL_2PL.EMPH_3PL_BE_IPFV_IPFV.AFF_PROG.AFF_INFR_COND.NEG_FOC_PRES_TOP.CNTR_2SG.EMPH_3SG_REFL_DEF_INF_SBJV_POSS_QUAL.AFF_PROH_TOP_PFV.NEG_QUAL.NEG_COND.AFF_REL_REL.PL2_CERT_ORD_DEM_RECP_DISTR_COP.NEG_IPFV.NEG_PROG.NEG_INFR.NEG_FUT.NEG_PST_Q_PFV.TR_EQU_IMP_RCNT_ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_DES_ADR_"
#  ANAPH, ANAPH.PL, ART, OPT, OPT2, PTCP.PROG removed
#  CFA à cause de la glose de dɔrɔmɛ qui finit par franc.CFA !!!
fixevalides="_ETRG_ETRG.FRA_CHNT_Q_PREV_"
# cf kàmana:n:PREV de kamanagan
pmlist=u"bɛ́nà:pm:FUT_bɛ́n':pm:FUT_bɛ:pm:IPFV.AFF_b':pm:IPFV.AFF_be:pm:IPFV.AFF_bɛ́kà:pm:PROG.AFF_bɛ́k':pm:PROG.AFF_bɛ́ka:pm:INFR_bága:pm:INFR_bìlen:pm:COND.NEG_kà:pm:INF_k':pm:INF_ka:pm:SBJV_k':pm:SBJV_ka:pm:QUAL.AFF_mán:pm:QUAL.NEG_kànâ:pm:PROH_kàn':pm:PROH_ma:pm:PFV.NEG_m':pm:PFV.NEG_mánà:pm:COND.AFF_mán':pm:COND.AFF_máa:pm:COND.AFF_nà:pm:CERT_n':pm:CERT_tɛ:pm:IPFV.NEG_t':pm:IPFV.NEG_tɛ́kà:pm:PROG.NEG_tɛ́k':pm:PROG.NEG_tɛ́ka:pm:INFR.NEG_tɛ́k':pm:INFR.NEG_tɛ́nà:pm:FUT.NEG_tɛ́n':pm:FUT.NEG_ye:pm:PFV.TR_y':pm:PFV.TR_yé:pm:IPFV_yé:pm:IMP_y':pm:IMP_yékà:pm:RCNT_màa:pm:DES_mà:pm:DES_m':pm:DES_"
coplist=u"bɛ́:cop:être_b':cop:être_b':cop:être_yé:cop:être_kó:cop:QUOT_k':cop:QUOT_dòn:cop:ID_dò:cop:ID_tɛ́:cop:COP.NEG_t':cop:COP.NEG_yé:cop:EQU_y':cop:EQU_bé:cop:être_"
prnlist=u"ɲɔ́gɔn:prn:RECP_mîn:prn:REL_mínnu:prn:REL.PL2_nìnnú:prn:DEM.PL_mín:prn:REL_nìn:prn:DEM_"
dtmlist=u"ìn:dtm:DEF_mîn:dtm:REL_nìn:dtm:DEM_nìn:dtm/prn:DEM_mín:dtm:REL_mínnu:dtm:REL.PL2_nìnnú:dtm:DEM.PL_nìnnú:dtm/prn:DEM.PL_"
perslist=u"ń:pers:1SG_nê:pers:1SG.EMPH_í:pers:2SG_í:pers:REFL_ê:pers:2SG.EMPH_à:pers:3SG_àlê:pers:3SG.EMPH_án:pers:1PL_ánw:pers:1PL.EMPH_a':pers:2PL_á:pers:2PL_á':pers:2PL_áw:pers:2PL.EMPH_ù:pers:3PL_òlû:pers:ce.PL2_"
pplist=u"ka:pp:POSS_lá:pp:POSS_bólo:pp:CNTRL_yé:pp:PP_y':pp:PP_lɔ́:pp:IN_nɔ́:pp:IN_rɔ́:pp:IN_mà:pp:ADR_"   # c'est tout ??? oui car les autres ont des gloses en minuscules, cf besoin de "check"
conjlist=u"ô:conj:DISTR_ôo:conj:DISTR_"
prtlist=u"dè:prt:FOC_dùn:prt:TOP.CNTR_dún:prt:TOP.CNTR_kɔ̀ni:prt:TOP.CNTR2_tùn:prt:PST_wà:prt:Q_"
mrphlist=u"lá:mrph:CAUS_la:mrph:CAUS_ná:mrph:CAUS_mà:mrph:SUPER_rɔ́:mrph:IN_lu:mrph:PL2_nu:mrph:PL2_ba:mrph:AUGM_baa:mrph:AG.OCC_baga:mrph:AG.OCC_bali:mrph:PTCP.PRIV_ka:mrph:GENT_la:mrph:AG.PRM_na:mrph:AG.PRM_la:mrph:LOC_na:mrph:LOC_la:mrph:PRICE_na:mrph:PRICE_la:mrph:MNT1_na:mrph:MNT1_lata:mrph:MNT2_nata:mrph:MNT2_la:mrph:PROG_na:mrph:PROG_la:mrph:PFV.INTR_na:mrph:PFV.INTR_n':mrph:PFV.INTR_ra:mrph:PFV.INTR_rá:mrph:IN_rɔ́:mrph:IN_w:mrph:PL_"
mrphlist=mrphlist+u"lama:mrph:STAT_nama:mrph:STAT_lan:mrph:INSTR_nan:mrph:INSTR_len:mrph:PTCP.RES_nen:mrph:PTCP.RES_li:mrph:NMLZ_ni:mrph:NMLZ_ma:mrph:COM_ma:mrph:RECP.PRN_man:mrph:ADJ_ntan:mrph:PRIV_"
mrphlist=mrphlist+u"ma:mrph:DIR_nan:mrph:ORD_nin:mrph:DIM_bali:mrph:PRIV_nci:mrph:AG.EX_ɲɔgɔn:mrph:RECP_ɲwan:mrph:RECP_ta:mrph:PTCP.POT_tɔ:mrph:CONV.PROG_tɔla:mrph:CONV.PROG_tɔ:mrph:ST_baatɔ:mrph:ST_bagatɔ:mrph:ST_ya:mrph:DEQU_yɛ:mrph:DEQU_ya:mrph:ABSTR_lá:mrph:CAUS_ná:mrph:CAUS_mà:mrph:SUPER_màn:mrph:SUPER_sɔ̀:mrph:EN_"
# restent u"ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_"
lxpsgvalides=pmlist+coplist+prnlist+dtmlist+perslist+pplist+conjlist+prtlist+mrphlist
lxpsg=re.compile(ur"[\_\[\s]([^:\[\_0-9]+:[a-z\/\.]+:[A-Z0-9][A-Z0-9\.\'\|]*)[\_\s\]]",re.U)   # ne vérifie que les gloses spéciales en majuscules, par ex. pas les pp comme lá:pp:à


# PRE : systematic global replaces  #################################################################

# normalize single quotes to avoid pop-up messages in gdisamb complaining that k' is not the same as k’
# tilted quote (word) to straight quotes (as in Bamadaba)
tout=re.sub(u"’",u"'",tout,0,re.U+re.MULTILINE)

# eliminer EMPR ex: ONI::EMPR
# see last section of bamana.gram
wsearch=ur'<span class="w" stage="[^\"]+">([A-Z\-]+)<span class="lemma">[a-z\-]+<sub class="gloss">EMPR</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # eliminer EMPR ex: ONI::EMPR
if nombre>0 :
  if notfast: 
    msg="%i modifs EMPR->ABR " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# autres ABR possibles
# exemple : <span class="w" stage="-1">TPI<span class="lemma">tpi</span>\n</span>
wsearch=ur'<span class="w" stage="-1">([A-Z\-0-9]+)<span class="lemma">[a-zA-Z\-0-9]+</span>\n</span>'
wrepl=ur'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # autres ABR possibles
if nombre>0 :
  if notfast: 
    msg="%i modifs Majuscules sans gloss->ABR " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

#eliminer gloss vides ex: baarakelen::
# ex :<span class="lemma var">odewudi</span>
# maybe this is a bug in bamana.gram
wsearch=ur'<span class="lemma var">([^<]+)</span>'
wrepl=ur''
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # gloss vides ex: baarakelen::
if nombre>0 :
  if notfast: 
    msg="%i modifs Gloss vide en lemma var" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# ex plus difficile pour les pluriels de mots inconnus (et d'autres dérivations communes possibles ?... à surveiller!)
# exemple traité : on ne garde pas le lemma var n/adj/dtm/prn/ptcp/n.prop/num, on garde les autres (si il y a des dérivations possibles)
# <span class="lemma">siyansikalanw<span class="lemma var">siyansikalanw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">siyansikalan<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">siyansikalanw<sub class="ps">n</sub><span class="m">siyansika<sub class="ps">v</sub></span><span class="m">lan<sub class="ps">mrph</sub><sub class="gloss">INSTR</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span>\n</span>

wsearch=ur'<span class="lemma">([^<]+)<span class="lemma var">([^<]+)<sub class="ps">n/adj/dtm/prn/ptcp/n\.prop/num</sub><span class="m">[^<]+<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">(.+)</span></span>\n</span>'
wrepl=ur'<span class="lemma">\g<1><span class="lemma var">\g<2></span></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # Gloss vide en lemma et n/adj/dtm/prn/ptcp/n.prop/num
if nombre>0 :
  if notfast: 
    msg="%i modifs Gloss vide en lemma et n/adj/dtm/prn/ptcp/n.prop/num" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# éliminer les doublons dans les lemma var (pas nécessairement contigüs) NE MARCHE PAS STRUCTURE CASSEE
## wsearch=ur'<span class="lemma var">(?P<stem>[^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub>(?P<stemgloss>[^\n]+)</span>([^\n]*)<span class="lemma var">(?P=stem)<sub class="ps">(?P=stemps)</sub>(?P=stemgloss)</span>'
## wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub>\g<3></span>\g<4>'
# éliminer les doublons dans les lemma var (nécessairement contigüs)
wsearch=ur'<span class="lemma var">(?P<stem>[^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub>(?P<stemgloss>[^\n]+)</span><span class="lemma var">(?P=stem)<sub class="ps">(?P=stemps)</sub>(?P=stemgloss)</span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub>\g<3></span>'

tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # Gloss doubles lemma var/lemma var
if nombre>0 :
  if notfast: 
    msg="%i modifs Gloss doubles lemma var/lemma var" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# Éliminer les doublons lemma / lemma var qui suit (même mot dans 2 dicos, 2 dérivations similaires appliquées…)
# ex : <span class="w" stage="0">kɔnseyew<span class="lemma">kɔnseyew<sub class="ps">n</sub><span class="m">kɔnseye<sub class="ps">n</sub><sub class="gloss">conseiller</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span><span class="lemma var">kɔnseyew<sub class="ps">n</sub><span class="m">kɔnseye<sub class="ps">n</sub><sub class="gloss">conseiller</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n</span>
# contrex : <span class="w" stage="0">pikiri<span class="lemma">pikiri<sub class="ps">n</sub><sub class="gloss">piqûre</sub><span class="lemma var">pikiri<sub class="ps">n</sub><sub class="gloss">piqûre</sub></span></span>\n</span>
# nb piqûre et piqûre sont deux écritures différentes!!
# wsearch=ur'<span class="lemma">(?P<stem>[^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub>(?P<stemgloss>.+)<span class="lemma var">(?P=stem)<sub class="ps">(?P=stemps)</sub>(?P=stemgloss)</span></span>\n</span>'
# NB le lemma var n'est pas nécessairement identique au lemma, en particulier par ex. lemma=ɲìninkali lamma var=ɲininkali (pas de ton dans la glose calculée automatiquement par gparser)
wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub><sub class="gloss">([^<]+)</sub>(?P<stemm>.+)<span class="lemma var">[^<]+<sub class="ps">(?P=stemps)</sub>(?P=stemm)</span></span>\n</span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<3></sub>\g<4></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  if notfast: 
    msg="%i modifs Gloss doubles lemma/lemma var  - mais lemma var pas = lemma" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# éliminer les gloses bizarres des ordinaux : <span class="lemma">39nan<span class="lemma var">39nan<
wsearch=ur'<span class="lemma">(?P<stem>[0-9]+)nan<span class="lemma var">(?P=stem)nan<sub class="ps">adj</sub><span class="m">(?P=stem)<sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span></span>\n'
wrepl=ur'<span class="lemma">\g<1>nan<sub class="ps">adj</sub><span class="m">\g<1><sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  if notfast: 
    msg="%i modifs ordinaux type 39nan avec lemma var" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# remettre dans l'ordre n/v les doublons dictionnaire v/n pour les détections NORV
# CAS SIMPLE
#wsearch=ur'<span class="w" stage="([^>]+)">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><sub class="gloss">([^<]+)</sub><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span>\n</span>'
#                                                                           1        2                                                  3                                                                      4                                                                       5                                                                6                                                                                              


# CAS COMPLEXE avec sub m
#   <span class="w" stage="0">ɲɛfɔ<span class="lemma">ɲɛ́fɔ<sub class="ps">v</sub><sub class="gloss">expliquer</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span><span class="lemma var">ɲɛ́fɔ<sub class="ps">n</sub><sub class="gloss">explication</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span></span></span>
#   </span>
#4 = <sub class="gloss">expliquer</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span>
#6 = <sub class="gloss">explication</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span>
wsearch=ur'<span class="w" stage="([^>]+)">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span>\n</span>'
#                                                                           1        2                                                  3                                                                      4                                                                       5                                                                6                                                                                              
wrepl=ur'<span class="w" stage="\g<1>">\g<2><span class="lemma">\g<6><sub class="ps">n</sub><\g<7>><span class="lemma var">\g<3><sub class="ps">v</sub><\g<4>></span></span>\n</span>'
# attention décalage $5 $6 -> $6 $7 à cause de la formule (((?!lemma var).)*)
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  if notfast: 
    msg="%i modifs doublons v/n -> n/v pour NORV" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# éliminer les doublons où le second choix, calculé, n'a pas de glose
# test SublimeText (?P<stem> impossible):
# <span class="lemma">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">([^<]+)</sub><(((?!lemma var).)*)></span></span>\n</span>
# trop rare : wsearch=ur'<span class="lemma">(?P<lemma>[^<]+)<sub class="ps">(?P<ps>[^<]+)</sub><sub class="gloss">([^<]+)</sub><(?P<details>((?!lemma var).)*)><span class="lemma var">(?P=lemma)<sub class="ps">(?P=ps)</sub><(?P=details)></span></span>\n</span>'
# dans wulikajɔ / wuli-ka-jɔ   va éliminer le second. non ne marche pas, a aussi une glose
# wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">(?P<ps>[^<]+)</sub><sub class="gloss">([^<]+)</sub><(?P<details>((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">(?P=ps)</sub><(?P=details)></span></span>\n</span>'
wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">(?P<ps>[^<]+)</sub><sub class="gloss">(?P<gloss>[^<]+)</sub><(?P<details>((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">(?P=ps)</sub><sub class="gloss">(?P=gloss)</sub><(?P=details)></span></span>\n</span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<3></sub><\g<4>></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  if notfast: 
    msg="%i modifs doublons entrée lexicale identiques" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

#
# déterminer les noms propres, même vaguement!
#
# mot non initial commençant par une majuscule
# et ambigu :
wsearch=ur"</span><span class=\"w\" stage=\"[0-9\-]+\">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-]+)<.*lemma var.*></span>\n"
wrepl=u"</span><span class=\"w\" stage=\"0\">\g<1><span class=\"lemma\">\g<1><sub class=\"ps\">n.prop</sub><sub class=\"gloss\">NOM</sub></span>\n"
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)
if nombre>0 :
  if notfast: 
    msg="%i modifs NOMPROPRE non-initial ambigu " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# # ou inconnu (pas trouvé):
#</span><span class="w" stage="[0-9\-]+">[A-ZƐƆƝŊ][a-zɛɔɲŋ\-]+<span class="lemma">([^<]+)</span>

# NOW THE BIG TASK     -go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!--
if notfast : print "arg="+arg

if arg=="fast" or arg=="-fast":
  nblinerepl=0
  linerepl=fileREPC.readline()
  #linerepl=linerepl.decode('utf-8')
  while linerepl :
    linerepl=re.sub(ur"\n$",u"",linerepl,0,re.U+re.MULTILINE)    # strip trailing newline char
    nblinerepl=nblinerepl+1
    wsearch, wrepl = linerepl.split("===")
    wsearch = wsearch.replace(u"¤¤",ur"\n")
    wrepl = wrepl.replace(u"¤¤",u"\n")
    
    tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # derniers parametres : count (0=no limits to number of changes), flags re.U+
    if nombre>0 :
      nbrulesapplied=nbrulesapplied+1
      nbmodif=nbmodif+nombre
    linerepl=fileREPC.readline()

else :
  fileREPCname="REPL-STANDARD-C.txt"
  if ".old" in filenametemp : fileREPCname="REPL-STANDARD-C.old.txt"
  fileREPC = open (fileREPCname,"wb")

  ###### replacement rules as per REPL.txt ######################################################################################################

  nblinerepl=0
  
  toutrepl=toutrepl.decode("utf-8")
  toutrepllines=toutrepl.split(u"\n")
  for linerepl in toutrepllines :
    nblinerepl=nblinerepl+1

    log.write("#   "+linerepl+"\n")

    if linerepl[0:1]==u"#":
      continue
    if linerepl[0:1]==u"\n" or len(linerepl)<=2 :  # le premier test ne marche pas sur mac 
      continue
    if u"===" not in linerepl :
      log.write("erreur de === :"+str(nblinerepl)+" : "+linerepl+"\n len="+str(len(linerepl)))
      sys.exit(linerepl+"\nil manque un === sur la ligne")

    if u"__" in linerepl :
      log.write("erreur de _ _: "+str(nblinerepl)+" : "+linerepl+"\n")
      sys.exit(linerepl+"\nil y a un double _ sur la ligne")

    wsearch=u""
    wrepl=u""
    wrepl2=u""
    sequence=u""
    
    if u"#" in linerepl :
      linerepl_sp=linerepl.split(u"#")
      linerepl=linerepl_sp[0].strip()
      
    if "====" in linerepl :
      sys.exit(linerepl+"\n==== au lieu de === ?")

    linerepl=linerepl.strip()   # strips trailing spaces ?
    elements=linerepl.split(u"===")
    liste_mots=elements[0]

    if tonal=="bailleul" : 
      liste_mots=re.sub(u"́","",liste_mots)
      liste_mots=re.sub(u"̂","",liste_mots)
    elif tonal!="tonal" :  
      liste_mots=re.sub(u"́","",liste_mots)
      liste_mots=re.sub(u"̀","",liste_mots)
      liste_mots=re.sub(u"̌","",liste_mots)
      liste_mots=re.sub(u"̂","",liste_mots)
    if tonal=="old" : # dans ce cas, les tons sont éliminés mais on revient à l'ancienne écriture
      liste_mots=re.sub(u"ɛɛ","èe",liste_mots)
      liste_mots=re.sub(u"ɛ","è",liste_mots)
      liste_mots=re.sub(u"Ɛ","È",liste_mots)
      liste_mots=re.sub(u"ɔɔ","òo",liste_mots)
      liste_mots=re.sub(u"ɔ","ò",liste_mots)
      liste_mots=re.sub(u"Ɔ","Ò",liste_mots)
      liste_mots=re.sub(u"ɲ","ny",liste_mots)
      liste_mots=re.sub(u"Ɲ","Ny",liste_mots)
    elif  tonal=="new" :    # or use a non-capturing alternative (?:ɲ|ny)   and (?:Ɲ|Ny)
      liste_mots=re.sub(u"ɲ","(?:ɲ|ny)",liste_mots)
      liste_mots=re.sub(u"Ɲ","(?:Ɲ|Ny)",liste_mots)
    liste_mots=re.sub(u"é","é",liste_mots)   # normaliser les caractères français éventuels (ETRG.FRA intégraux possibles)
    liste_mots=re.sub(u"è","è",liste_mots)
    liste_mots=re.sub(u"ë","ë",liste_mots)
    liste_mots=re.sub(u"à","à",liste_mots)
    liste_mots=re.sub(u"â","â",liste_mots)
    liste_mots=re.sub(u"ù","ù",liste_mots)
    liste_mots=re.sub(u"û","û",liste_mots)
    liste_mots=re.sub(u"ô","ô",liste_mots)
    liste_mots=re.sub(u"î","î",liste_mots)
    liste_mots=re.sub(u"ï","ï",liste_mots)
    liste_mots=re.sub(u"ç","ç",liste_mots)

    liste_gloses=elements[1]

    #
    # PETITES VALIDATIONS
    #

    if u" " in liste_mots:
      log.write("pas d'espace à gauche de === svp !\n")
      sys.exit("\n"+liste_mots+"\nespace à gauche de ===")
      
    semicolumns=re.findall(u"\:",liste_gloses)
    nbsemic=len(semicolumns)
    if (2*int(nbsemic/2))!=nbsemic :
      log.write("il manque un : dans '"+liste_gloses+"'\n")
      sys.exit("\n"+liste_gloses+"\nerreur de syntaxe ':' dans une glose")   # test sur l'ensemble de la liste des glose, pas sur chaque glose prise individuellement

    openbrackets=re.findall(u"\[",liste_gloses)
    nbopen=len(openbrackets)
    closebrackets=re.findall(u"\]",liste_gloses)
    nbclose=len(closebrackets)
    if nbopen!=nbclose :
      log.write("problème de [ et ] mal ouvertes/fermées dans '"+liste_gloses+"'\n")
      sys.exit("\n"+liste_gloses+"\nerreur de syntaxe '[/]' dans une glose")

    spacesemicolumns=re.findall(u"\s\:",liste_gloses)
    nbspsemic=len(spacesemicolumns)
    if nbspsemic>0 :
      log.write("il y a un espace devant un : dans '"+liste_gloses+"'\n")
      sys.exit("\n"+liste_gloses+"\nerreur de syntaxe ' :' dans une glose") 

    doublelowbar=re.findall(u"\_\_",liste_gloses)
    nbdoublelowbar=len(doublelowbar)
    if nbdoublelowbar>0 :
      log.write("il y a une répétition de _ dans '"+liste_gloses+"'\n")
      sys.exit("\n"+liste_gloses+"\nerreur de syntaxe ' :' dans une glose") 

    # gloses spéciales
    # noms valides ?
    #                 verif seulement sur liste_mot car liste_gloses peut contenir de nombreuses glose majuscules comme PFV.TR
    m=re.findall(ur"(\_[A-Z][A-Z]+\_)",u"_"+re.sub(u"\_",u"__",liste_mots)+u"_")   # caution: findall only find non overlapping sequences _TU_YA_SI_ only finds _TU_ and _SI_, but  not _YA_
    #print u"_"+re.sub(u"\_",u"__",liste_mots)+u"_"
    #print m
    if m!=None:
      for gspe in m :
        #print gspe
        if gspe not in valides:
          # vérifier si c'est défini comme un nom propre
          gspe_error=True
          m1=lxpsg.findall(u"_"+liste_gloses+u"_")
          if m1!=None :
            for lxpsgloss in m1 :
              #log.write("- "+lxpsgloss+"\n")
              lxpsgloss_elem=lxpsgloss.split(":")
              lxpsgloss_lx=lxpsgloss_elem[0]
              lxpsgloss_ps=lxpsgloss_elem[1]
              log.write(lxpsgloss_lx+":"+lxpsgloss_ps+"\n")
              if (gspe==u"_"+lxpsgloss_lx+u"_" and lxpsgloss_ps==u"n.prop") :
                gspe_error=False
                log.write(gspe+" : accepte!\n")
                break
          if gspe_error :     
            log.write("(non bloquant) Glose speciale non valide a gauche de === : "+gspe+"\n"+liste_mots+"\n")
            #sys.exit("Glose speciale non valide a gauche de === : "+gspe+"\n"+liste_mots)
    #
    # pour la partie gloses, il faut être plus complet : valider également les gloses Corpus !!!
    #
    m=re.findall(ur"(\_[0-9]*[A-Z][A-Z\.]+[0-9]*\_)",u"_"+re.sub(u"\_",u"__",liste_gloses)+u"_")
    if m!=None:
      for gspe in m :
        #print gspe
        if gspe not in valides+gvalides:
          log.write("Glose speciale non valide a droite de === : "+gspe+"\n"+liste_mots+"\n")
          sys.exit("\nGlose speciale non valide a droite de === : "+gspe+"\n"+liste_gloses)
    
    # maintenant validons les gloses spéciales en détail
    m=lxpsg.findall(u"_"+re.sub(u"\_",u"__",liste_gloses)+u"_")
    if m!=None :
      for lxpsgloss in m :
        #log.write("- "+lxpsgloss+"\n")
        lxpsgloss_elem=lxpsgloss.split(":")
        lxpsgloss_ps=lxpsgloss_elem[1] 
        lxpsgloss_gloss=lxpsgloss_elem[2]
        # ajout de quelques "not in" pour permettre quelques gloses en majuscules a liste non fermée
        # 18 OCT 16 : Pourquoi ne pas sortir les n.prop de ce test ??? ≠===================================
        #if "_"+lxpsgloss_gloss+"_" not in "_ETRG.FRA_TOP_NOM.M_NOM.F_NOM.MF_NOM.CL_NOM.ETRG_" :
        if (lxpsgloss_ps!="n.prop" and lxpsgloss_gloss+u"_" not in fixevalides) :
          if  lxpsgloss+u"_" not in lxpsgvalides:
            log.write(lxpsgloss_gloss+" : problème avec la glose ?standard? "+lxpsgloss+"\n"+"Valides:"+lxpsgvalides+"\n")
            sys.exit("\n"+liste_gloses+"\n"+lxpsgloss_gloss+" : Glose ?standard? non valide a gauche de ===\nVoir le log : "+logfilename)

    # nombre de gloses de part et d'autre de ===
    
    elements=valides[1:len(valides)-1].split(u"_")   # ôter les _ avant et après avant de faire un split
    for element in elements:
      if element in liste_mots+"_"+liste_gloses:
        nbelement=re.findall(element,liste_mots)
        nbelementg=re.findall(element,liste_gloses)
        # if element=='TIRET': print "TIRET nbelement=",len(nbelement), " nbelementg=", len(nbelementg)
        if (len(nbelement)!=len(nbelementg)) and not (len(nbelementg)==0 and element in "_TIRET_"):
          log.write(u"il n'y a pas le même nombre de '"+element+u"' de part et d'autre de ===\n")
          sys.exit("\n"+liste_mots+"\n"+liste_gloses+"\nErreur de syntaxe! pas le meme nombre de '"+element+"' de part et d'autre de ===\nvoir le log : "+logfilename)

    # autres validations à ajouter ici ?
    
    mots=liste_mots.split(u"_")
    gloses=liste_gloses.split(u"_")
    
    for mot in mots :
      if mot==u"COMMA"      : wsearch=wsearch+ur'<span class="c">,</span>\n'
      elif mot==u"DOT"      : wsearch=wsearch+ur'<span class="c">\.</span>\n'
      elif mot==u"QUESTION" : wsearch=wsearch+ur'<span class="c">\?</span>\n'
      elif mot==u"COLON"    : wsearch=wsearch+ur'<span class="c">\:</span>\n'
      elif mot==u"SEMICOLON": wsearch=wsearch+ur'<span class="c">\;</span>\n'
      elif mot==u"EXCLAM"   : wsearch=wsearch+ur'<span class="c">\!</span>\n'
      elif mot==u"TIRET"    : wsearch=wsearch+ur'<span class="c">\-</span>\n'
      elif mot==u"PUNCT"    : wsearch=wsearch+ur'<span class="c">([^<]+)</span>\n' 
      # nb: le point, et autres séparateurs de sentence, n'a normalement pas d'effet ici ! cf DEBUT
      elif mot==u"COMMENT"  : wsearch=wsearch+ur'<span class="comment">([^<]+)</span>\n' 
      elif mot==u"TAG"      : wsearch=wsearch+ur'<span class="t">([^<]+)</span>\n' 
      # attention <st> n'est pas un tag !!! <span class="c">&lt;st&gt;</span>
      elif mot==u"DEGRE"    : wsearch=wsearch+ur'<span class="c">\°</span>\n'
      elif mot==u"degremove": wsearch=wsearch+ur'<span class="c">\°</span>\n'
      # le même mais pas de vérif quil existe de l'autre côté de === : on veut l'éliminer!
      # en minuscules pour échapper aux tests sur les mot-clefs "valides"
      elif mot==u"LAQUO"    : wsearch=wsearch+ur'<span class="c">\«</span>\n'
      elif mot==u"RAQUO"    : wsearch=wsearch+ur'<span class="c">\»</span>\n'
      elif mot==u"PARO"    : wsearch=wsearch+ur'<span class="c">\(</span>\n'
      elif mot==u"PARF"    : wsearch=wsearch+ur'<span class="c">\)</span>\n'
      elif mot==u"GUILLEMET"    : wsearch=wsearch+ur'<span class="c">\"</span>\n'
      elif mot==u"PERCENT"  : wsearch=wsearch+ur'<span class="c">\%</span>\n'
      elif mot==u"DEBUT"    : wsearch=wsearch+ur'<span class="annot">'
      elif mot==u"FIN"      : wsearch=wsearch+ur'</span>\n</span>\n'
      elif mot==u"BREAK"    : wsearch=wsearch+ur'<span class="t">\&lt\;br\/\&gt\;</span>\n'  # t = tag 
      
      # cette formule marche pour les composés, excluants ceux qui sont ambigus, à essayer !
      # <span class="w" stage="0">[^<]*<span class="lemma">[^<]*<sub class="ps">n</sub><(((?!lemma var).)*)>\n</span>
      # et aussi, moins de groupes !
      # <span class="w" stage="0">[^<]*<span class="lemma">[^<]*<sub class="ps">n</sub><((?!lemma var).*)>\n</span>
      # mais pas fiable dans python re ?
      # pour mémoire, formule précédente (uniquement non composés):
      # <span class="w" stage="0">([^<]*)<span class="lemma">([^<]*)<sub class="ps">n</sub><sub class="gloss">([^<]*)</sub></span>\n</span>
      # finalement une formule qui marche :...
      elif mot==u"NAME"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PERS"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pers</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PRONOM"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">prn</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PRT"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">prt</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"VERBE"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"VPERF"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)PFV.INTR(((?!lemma var).)*)>\n</span>'
      # elif mot==u"VPERF"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><span class="m">([^<]+)<sub class="ps">v</sub><sub class="gloss">([^<]+)</sub></span><span class="m">(ra|la|na)<sub class="ps">mrph</sub><sub class="gloss">PFV.INTR</sub></span></span>\n</span>'
      elif mot==u"ADJORD"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)<sub class="gloss">ORD</sub>(((?!lemma var).)*)>\n</span>'
      elif mot==u"VQ"       : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">vq</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"VQADJ"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">vq/adj</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"DTM"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">dtm</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PRNDTM"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prn/dtm|dtm/prn)</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"POSTP"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pp</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PRMRK"       : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pm</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PRMRKQUAL"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pm</sub><sub class="gloss">(QUAL.AFF|QUAL.NEG)</sub></span>\n</span>'
      elif mot==u"COPULE"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">cop</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"ADJECTIF" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"ADJN"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(adj/n|n/adj)</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PARTICIPE": wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">ptcp</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"NUM"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">num</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"NUMANNEE"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([1-2][0-9][0-9][0-9])<span class="lemma">([1-2][0-9][0-9][0-9])<sub class="ps">num</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"ADV"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"ADVP"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv\.p</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"ADVN"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv/n</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"CONJ"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(conj|prep/conj|conj/prep)</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"PREP"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prep|prep/conj|conj/prep)</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"CONJPREP" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prep/conj|conj/prep)</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"CONJPOSS" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">conj</sub><sub class="gloss">POSS</sub></span>\n</span>'
      elif mot==u"NPROPRE"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"NPROPRENOMM"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.M</sub></span>\n</span>'
      elif mot==u"NPROPRENOMF"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.F</sub></span>\n</span>'
      elif mot==u"NPROPRENOMMF"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.MF</sub></span>\n</span>'
      elif mot==u"NPROPRENOMCL"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.CL</sub></span>\n</span>'
      elif mot==u"NPROPRETOP"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub>(((?!lemma var).)*)</span>\n</span>'
      elif mot==u"DOONIN"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">dɔ́ɔnin<sub class="ps">adj/n</sub><(((?!lemma var).)*)>\n</span>'
      elif mot==u"NORV"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)></span></span>\n</span>'
      elif mot==u"PMORCOP"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pm</sub><sub class="gloss">([^<]+)</sub><span class="lemma var">([^<]+)<sub class="ps">cop</sub><sub class="gloss">([^<]+)</sub></span></span>\n</span>'
      elif mot==u"AORN"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span>\n</span>'
      elif mot==u"DORP"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">dtm</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">prn</sub><(((?!lemma var).)*)></span></span>\n</span>'
      # to be implemented : GNMEMBER
      # <span class="lemma">([^<]+)<sub class="ps">(n|n.prop|pers|prn|dtm|adj|ptcp|prt)</sub><sub class="gloss">([^<]+)</sub>|<span class="lemma">([^<]+)<sub class="ps">(conj|prep\/conj|pp)</sub><sub class="gloss">(POSS|et|ainsi\.que)</sub>
      # add around this class="w" and not lemma var
      # check impact on capt_gr_index  (TEST THOROUGHLY!!!)
      elif mot==u"AMBIGUOUS": wsearch=wsearch+ur'<span class="w"(.*)lemma var(.*)\n</span>'
      else :
        if u"'" in mot: mot=re.sub(ur"\'",u"[\'\’]+",mot)   # satanées curly brackets
        wsearch=wsearch+ur'<span class="w" stage="[a-z0-9\.\-]+">'+mot+u'<.*</span>\n</span>'
      if sequence=="": sequence=mot
      else : sequence=sequence+" "+mot
    
    
    lmots=len(mots)
    lgloses=len(gloses)

    if lmots!=lgloses:
      log.write(u"!= NB ELEM DIFFERENTS:  ("+str(lmots)+u") !=  ("+str(lgloses)+")\n")

    imots=-1
    capt_gr_index=0   # capturing group index (si on a plusieurs symboles)

    for glose in gloses :
      imots=imots+1    # commence donc à 0
      if glose==u"COMMA"      : wrepl=wrepl+ur'<span class="c">,</span>\n'
      elif glose==u"DOT"      : wrepl=wrepl+ur'<span class="c">.</span>\n'
      elif glose==u"DOTnone"  : wrepl=wrepl+ur"" # cas spécial où on élimine le DOT (uniquement pour dɔrɔmɛ ?)
      elif glose==u"QUESTION" : wrepl=wrepl+ur'<span class="c">?</span>\n'
      elif glose==u"COLON"    : wrepl=wrepl+ur'<span class="c">:</span>\n'
      elif glose==u"SEMICOLON": wrepl=wrepl+ur'<span class="c">;</span>\n'
      elif glose==u"EXCLAM"   : wrepl=wrepl+ur'<span class="c">!</span>\n'
      elif glose==u"TIRET"    : wrepl=wrepl+ur'<span class="c">-</span>\n'
      elif glose==u"DEBUT"    : wrepl=wrepl+ur'<span class="annot">'
      elif glose==u"FIN"      : wrepl=wrepl+ur'</span>\n</span>\n'
      elif glose==u"BREAK"    : wrepl=wrepl+ur'<span class="t">&lt;br/&gt;</span>\n'
      elif glose==u"DEGRE"    : wrepl=wrepl+ur'<span class="c">°</span>\n'
      elif glose==u"LAQUO"    : wrepl=wrepl+ur'<span class="c">«</span>\n'
      elif glose==u"RAQUO"    : wrepl=wrepl+ur'<span class="c">»</span>\n'
      elif glose==u"PARO"     : wrepl=wrepl+ur'<span class="c">(</span>\n'
      elif glose==u"PARF"     : wrepl=wrepl+ur'<span class="c">)</span>\n'
      elif glose==u"GUILLEMET"    : wrepl=wrepl+ur'<span class="c">"</span>\n'
      elif glose==u"PERCENT"  : wrepl=wrepl+ur'<span class="c">%</span>\n'
      elif glose==u"PUNCT"    :
        wrepl=wrepl+ur'<span class="c">\g<'+str(capt_gr_index+1)+u'></span>\n'
        capt_gr_index=capt_gr_index+1
      elif glose==u"COMMENT"    :
        wrepl=wrepl+ur'<span class="comment">\g<'+str(capt_gr_index+1)+u'></span>\n'
        capt_gr_index=capt_gr_index+1
      elif glose==u"TAG"    :
        wrepl=wrepl+ur'<span class="t">\g<'+str(capt_gr_index+1)+u'></span>\n'
        capt_gr_index=capt_gr_index+1
      elif glose==u"NAME"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
        # ces +1 bizarres sont apparus après l'introduction de la glose correcte pour ?!lemma var    ...  à surveiller !   
      elif glose==u"PERS"     : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pers</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"PRONOM"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prn</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"PRT"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prt</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"VERBE"    : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"VPERF"    : 
        #log.write(ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>PFV.INTR\g<'+str(capt_gr_index+5)+'>>\n</span>')
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>PFV.INTR\g<'+str(capt_gr_index+5)+'>>\n</span>'
        capt_gr_index=capt_gr_index+5+1  # j'aurais pensé +2 : il y a deux groupes  (?!lemma var) autour de PFV.INTR
      #elif glose==u"VPERF"    : 
      #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><span class="m">\g<'+str(capt_gr_index+3)+ur'><sub class="ps">v</sub><sub class="gloss">\g<'+str(capt_gr_index+4)+ur'></sub></span><span class="m">\g<'+str(capt_gr_index+5)+ur'><sub class="ps">mrph</sub><sub class="gloss">PFV.INTR</sub></span></span>\n</span>'
      #  capt_gr_index=capt_gr_index+5 # +1 (pas de (?!lemma var))
      elif glose==u"ADJORD"    : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+ur'><sub class="gloss">ORD</sub>\g<'+str(capt_gr_index+5)+'>>\n</span>'
        capt_gr_index=capt_gr_index+5+1
      elif glose==u"VQ"       : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">vq</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"VQADJ"       : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">vq/adj</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"VQADJforcevq"       : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">vq</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"VQADJforceadj"       : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"DTM"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"PRNDTM"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prn/dtm</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"PRNDTMforceprn"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prn</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"PRNDTMforcedtm"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"POSTP"    : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pp</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"PRMRK"       : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pm</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"PRMRKQUAL"       : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pm</sub><sub class="gloss">\g<'+str(capt_gr_index+3)+ur'></sub></span>\n</span>'
        capt_gr_index=capt_gr_index+3 # pas de +1 : pas de !lemma var
      elif glose==u"COPULE"   : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">cop</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"ADJECTIF" : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"ADJN" : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj/n</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"ADJNforceadj" : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"ADJNforcen" : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"PARTICIPE"     : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">ptcp</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"NUM"      : 
        wrepl=wrepl+ur'<span class="w" stage="tokenizer">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">num</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"NUMANNEE"      : 
        wrepl=wrepl+ur'<span class="w" stage="tokenizer">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">num</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"NUMnan"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'>nan<span class="lemma">\g<'+str(capt_gr_index+1)+ur'>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<'+str(capt_gr_index+1)+ur'><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"ADV"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adv</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"ADVP"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adv.p</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"ADVN"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adv/n</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"ADVNforcen"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"ADVNforceadv"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adv</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"CONJ"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">\g<'+str(capt_gr_index+3)+u'></sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"PREP"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">\g<'+str(capt_gr_index+3)+u'></sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"CONJPREP"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">conj/prep</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"CONJPREPforceconj"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">conj</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"CONJPREPforceprep"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prep</sub><\g<'+str(capt_gr_index+4)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+4+1
      elif glose==u"CONJPOSS"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">conj</sub><sub class="gloss">POSS</sub>\n</span>'
        capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
      elif glose==u"NPROPRE"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"NPROPREforcetop"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span>\n</span>'
        capt_gr_index=capt_gr_index+3+1
      elif glose==u"NPROPRENOMM"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><sub class="gloss">NOM.M</sub></span>\n</span>'
        capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
      elif glose==u"NPROPRENOMF"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><sub class="gloss">NOM.F</sub></span>\n</span>'
        capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
      elif glose==u"NPROPRENOMMF"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><sub class="gloss">NOM.F</sub></span>\n</span>'
        capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
      elif glose==u"NPROPRENOMCL"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><sub class="gloss">NOM.CL</sub></span>\n</span>'
        capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
      elif glose==u"NPROPRETOP"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub>\g<'+str(capt_gr_index+3)+ur'></span>\n</span>'
        capt_gr_index=capt_gr_index+3+1 # nb: certains TOP ont une sous-glose, par. ex. avec jamana
      elif glose==u"DOONINforceadvn"      : 
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">dɔ́ɔnin<sub class="ps">adv/n</sub><\g<'+str(capt_gr_index+2)+ur'>>\n</span>'
        capt_gr_index=capt_gr_index+2+1
      elif glose==u"NORVname" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n</span>'
        capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
      elif glose==u"NORVverbe" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+5)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+6)+ur'>></span>\n</span>'
        capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)
      elif glose==u"PMORCOP" :   # leave as it is
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pm</sub><sub class="gloss">\g<'+str(capt_gr_index+3)+ur'></sub><span class="lemma var">\g<'+str(capt_gr_index+4)+ur'><sub class="ps">cop</sub><sub class="gloss">\g<'+str(capt_gr_index+5)+ur'></sub></span></span>\n</span>'
        capt_gr_index=capt_gr_index+5+1
      elif glose==u"PMORCOPpm" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pm</sub><sub class="gloss">\g<'+str(capt_gr_index+3)+ur'></sub></span>\n</span>'
        capt_gr_index=capt_gr_index+5+1
      elif glose==u"PMORCOPcop" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+4)+ur'><sub class="ps">cop</sub><sub class="gloss">\g<'+str(capt_gr_index+5)+ur'></sub></span>\n</span>'
        capt_gr_index=capt_gr_index+5+1
      elif glose==u"AORNname" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n</span>'
        capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
      elif glose==u"AORNadj" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+5)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+6)+ur'>></span>\n</span>'
        capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)
      elif glose==u"DORPdtm" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n</span>'
        capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
      elif glose==u"DORPprn" :
        wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prn</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n</span>'
        capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)

      elif glose==u"AMBIGUOUS":
        wrepl=wrepl+ur'<span class="w" \g<'+str(capt_gr_index+1)+ur'>lemma var\g<'+str(capt_gr_index+2)+ur'>\n</span>'
        capt_gr_index=capt_gr_index+2
      else :
        # glose est supposé aveoir une forme lx:ps:gloss [sub]

        # petite validation sur glose :
        ncol=glose.count(u":")
        if ncol==0 :
          print "\nglose incorrecte (format lx:ps:gloss [sub]) non respecté, pas de ':' :",glose
          log.write(u"glose incorrecte (format lx:ps:gloss [sub]) non respecté, pas de ':' :"+glose+"\n")
          sys.exit("\n"+liste_gloses+"\n\narrêt de repl.")
        elif ncol!=2*(ncol/2) :
          print "\nglose incorrecte (format lx:ps:gloss [sub]) non respecté, nombre incorrect de ':' :",glose
          log.write(u"glose incorrecte (format lx:ps:gloss [sub]) non respecté, nombre incorrect de ':' :"+glose+"\n")
          sys.exit("\n"+liste_gloses+"\n\narrêt de repl.")

        if re.search(ur"\s[A-ZƐƆƝŊa-zɛɔɲŋ\.̀́̌̂\']*\s",glose) :     #    *  : can also be double space
          print "\nglose incorrecte (format lx:ps:gloss [sub]) non respecté, espaces mal placés :",glose
          log.write(u"glose incorrecte (format lx:ps:gloss [sub]) non respecté, espaces mal placés :"+glose+"\n")
          sys.exit("\n"+liste_gloses+"\n\narrêt de repl.")
        if lmots==lgloses :
          word=mots[imots]
          
        else:  # try the old method
        
          # attention : résout la plupart des cas
          # sauf 
          # 1) split/join : revoir stage=
          # 2) Bailleul : quid si on remplace ton haut par ton bas (on remplace alors l'original, aïe!)
          i_colon=glose.find(u":")
          word=glose[0:i_colon]
          if u"|" in word :
            words=word.split(u"|")
            word=words[0]
          if tonal=="bailleul" : 
            word=re.sub(u"́","",word)
            word=re.sub(u"̂","",word)
          elif tonal!="tonal" :  
            word=re.sub(u"́","",word)
            word=re.sub(u"̀","",word)
            word=re.sub(u"̌","",word)
            word=re.sub(u"̂","",word)
          if tonal=="old" : # dans ce cas, les tons sont éliminés mais on revient à l'ancienne écriture
            word=re.sub(u"ɛɛ","èe",word)
            word=re.sub(u"ɛ","è",word)
            word=re.sub(u"Ɛ","È",word)
            word=re.sub(u"ɔɔ","òo",word)
            word=re.sub(u"ɔ","ò",word)
            word=re.sub(u"Ɔ","Ò",word)
            word=re.sub(u"ɲ","ny",word)
            word=re.sub(u"Ɲ","Ny",word)
        
        #if u"POSTP_kà_tɛ̀mɛ_NAME_kàn" in liste_mots:
        #  log.write(u"check glose :"+glose+u"\n")

        # ICI on peut vérifier glose // Bamadaba mmc 
        if arg=="check" or arg=="-check":
          docheck=True
          #if    u": [" in glose : docheck=False
          #elif u"§§" in glose : docheck=False
          if u"§§" in glose : docheck=False
          elif u"nan:adj:ORDINAL" in glose : docheck=False
          elif u":num:CARDINAL" in glose : docheck=False
          elif u":conv.n:" in glose : docheck=False
          elif u":n.prop:ABR" in glose : docheck=False
          elif re.search(ur"\:n\.prop\:[A-Z\-]+",glose) : docheck=False
          elif u"ETRG.FRA" in glose : docheck=False
          elif u"::CHNT" in glose : docheck=False
          elif u":n.prop:NOM.ETRG" in glose : docheck=False
          elif u":n.prop:NOM.FRA" in glose : docheck=False
          elif u":n.prop:NOM.ESP" in glose : docheck=False
          elif u":n.prop:NOM.US" in glose : docheck=False
          elif u":n.prop:NOM.ENG" in glose : docheck=False
          elif u":n.prop:NOM.POR" in glose : docheck=False
          elif u":n.prop:NOM.ITA" in glose : docheck=False
          elif u":n.prop:NOM.RUS" in glose : docheck=False
          elif u":n.prop:NOM.FUL" in glose : docheck=False
          elif u":n.prop:TOP" in glose : docheck=False
          elif glose==u"bà:num:mille" : docheck=False
          elif glose==u"bàa:num:mille" : docheck=False
          elif glose==u"nìnnú:prn:DEM.PL [nìn:prn:DEM nu:mrph:PL2]" : docheck=False
          elif glose==u"nìnnú:dtm:DEM.PL [nìn:dtm:DEM nu:mrph:PL2]" : docheck=False
          elif glose==u"fàr':v:ajouter" : docheck=False
          elif glose==u"kàbini:conj:depuis [kàbi:conj:depuis ní:conj:si]" : docheck=False
          elif glose==u"kàbini:prep:depuis [kàbi:prep:depuis ní:prep:si]" : docheck=False
          elif glose==u"dɔ́wɛrɛ:prn:autre [dɔ́:prn:certain wɛ́rɛ:adj:autre]" : docheck=False
          elif glose==u"yànni:conj:avant.que [yàn:n:ici ni:conj:et]" : docheck=False
          elif glose==u"yànni:prep:avant.que [yàn:n:ici ni:prep:et]" : docheck=False
          elif glose==u"cɛ̀nímùsoya:n:rapports.sexuels [cɛ̀:n:mâle ni:conj:et mùso:n:femme ya:mrph:ABSTR]" : docheck=False
          elif glose==u"bámanankan:n:langue.bambara [bámànan:n:bambara kán:n:cou]"  : docheck=False
          elif glose==u"bámanankan:n:langue.bambara [bámàna:n:bambara kán:n:cou]"  : docheck=False
          elif glose==u"n':prep:si" : docheck=False
          elif glose==u"ní:prep:si" : docheck=False
          elif glose==u"bímɛtɛrɛ:n:décamètre [bî:num:dizaine mɛ́tɛrɛ:n:mètre]" : docheck=False
          elif glose==u"dɔ́wɛrɛ:prn:autre [dɔ́:prn:certain wɛ́rɛ:dtm:autre]" : docheck=False
          elif glose==u"dùgujɛ:n:aube [dùgu:n:terre jɛ́:adj:blanc]" : docheck=False
          elif glose==u"sábula:prep:parce.que [sábu:n:cause lá:pp:à]" : docheck=False
          elif glose==u"bámànandunun:n:tambour" : docheck=False
          elif glose==u"jákabɔ:n:se.moquer [jáka:n:dîme bɔ́:v:sortir]" : docheck=False
          elif glose==u"wíli:v:bouillir" : docheck=False
          elif glose==u"Má:n:Dieu" : docheck=False
          elif glose==u"díyagoya:v:contraindre [díya:v:rendre.agréable [dí:vq:agréable ya:mrph:DEQU] gó:vq:désagréable ya:mrph:DEQU]" : docheck=False
          elif glose==u"díya:v:rendre.agréable [dí:vq:agréable ya:mrph:DEQU]" : docheck=False
          elif glose==u"díya:n:bon.goût [dí:vq:agréable ya:mrph:DEQU]" : docheck=False
          elif glose==u"yɛ̀rɛmahɔrɔnya:n:liberté [yɛ̀rɛmahɔrɔn:n:homme.libre [yɛ̀rɛ̂:dtm:même mà:pp:ADR hɔ́rɔn:n:libre] ya:mrph:ABSTR]"  : docheck=False
          elif glose==u"mínisiriso:n:ministère [mínisiri:n:ministre só:n:maison]" : docheck=False
          elif glose==u"ládiyalifɛn:n:prix [ládiya:v:récompenser [lá:mrph:CAUS díya:v:rendre.agréable [dí:vq:agréable ya:mrph:DEQU] li:mrph:NMLZ] fɛ́n:n:chose]"  : docheck=False
          elif glose==u"hɔ́rɔnya:n:liberté [hɔ́rɔn:n:libre ya:mrph:ABSTR]" : docheck=False
          elif glose==u"júguman:n:méchant [júgu:vq:mauvais man:mrph:ADJ]" : docheck=False
          elif glose==u"bùlonba:n:case.à.palabres [bùlon:n:antichambre ba:mrph:AUGM]" : docheck=False
          elif glose==u"tánnifilafili:n:plénitude [tán:num:dix ni:conj:et fìla:num:deux fìli:v:jeter]" : docheck=False
          elif glose==u"kɛ́cogo:n:manière.de.faire [kɛ́:v:faire cógo:n:manière]" : docheck=False
          elif glose==u"báden:n:frère.soeur.utérin(e) [bá:n:mère dén:n:enfant]" : docheck=False
          elif glose==u"sényɛrɛkɔrɔ:n:autosuffisance [sé:v:arriver ń:pers:1SG yɛ̀rɛ̂:dtm:même kɔ́rɔ:pp:sous]" : docheck=False
          elif glose==u"dúnta:ptcp:comestible [dún:v:manger ta:mrph:PTCP.POT]" : docheck=False
          elif glose==u"bìlama:adj:actuel [bì:n:aujourd'hui lama:mrph:STAT]" : docheck=False
          elif glose==u"jɛ́man:adj:blanc [jɛ́:vq:blanc man:mrph:ADJ]" : docheck=False
          elif glose==u"màliden:n:malien [Màli:n.prop:TOP dén:n:enfant]" : docheck=False
          elif glose==u"mánanin:n:sac.plastique [mána:n:substance.collante nin:mrph:DIM]" : docheck=False
          elif glose==u"nísɔndiya:n:joie [nísɔn:n:humeur [ní:n:âme sɔ̀n:n:cœur] dí:adj:agréable ya:mrph:ABSTR]" : docheck=False
          elif glose==u"tíminandiya:n:bonne.application [tíminandi:n:appliqué tími:v:s'appliquer nan:mrph:dans dí:adj:agréable ya:mrph:ABSTR]" : docheck=False
          elif glose==u"kɔ̀ɔkɛ:n:frère.aîné [kɔ̀rɔ:n:aîné kɛ:adj:mâle]" : docheck=False
          elif glose==u"kɔ̀ɔmuso:n:grande.soeur [kɔ̀rɔ:n:aîné mùso:adj:femme]" : docheck=False
          elif glose==u"màakɔrɔbaya:n:vieillesse [màakɔrɔba:n:vieux [màa:n:homme kɔ̀rɔ:adj:vieux ba:mrph:AUGM] ya:mrph:ABSTR]" : docheck=False
          elif glose==u"bànajuguba:n:maladie.très.grave [bàna:n:maladie júgu:adj:mauvais ba:mrph:AUGM]" : docheck=False
          elif glose==u"bàlabilen:adj:sorgho.rouge" : docheck=False
          elif glose==u"tɔ́ri:intj:absolument.pas" : docheck=False
          elif glose==u"sófɛri:n:chauffeur" : docheck=False
          elif glose==u"kásadiyalan:n:parfum [kása:n:odeur díya:v:rendre.agréable [dí:vq:agréable ya:mrph:DEQU]" : docheck=False
          elif glose==u"dɔ̀lɔso:n:bar [dɔ̀lɔ:n:bière.de.mil só:n:maison]" : docheck=False
          elif glose==u"díɲɛdenya:n:libertinage [díɲɛden:n:initié.à.tout [díɲɛ:n:monde dén:n:enfant] ya:mrph:ABSTR]" : docheck=False
          elif glose==u"sɛ̀gɛnbagatɔ:n:pauvre [sɛ̀gɛn:v:fatiguer baa:mrph:AG.OCC tɔ:mrph:ST]" : docheck=False
          elif glose==u"kòrosakorosa:n:urticaire" : docheck=False
          elif glose==u"dɔ́wɛrɛ:prn:autre [dɔ́:prn:certain wɛ́rɛ:adj:autre]" : docheck=False
          elif glose==u"ǹka:prep:mais" : docheck=False
          elif glose==u"dádiya:v:aiguiser [dá:n:bouche dí:vq:agréable ya:mrph:DEQU]" : docheck=False
          elif glose==u"sábu:prep:parce.que" : docheck=False
          elif glose==u"desigaramu:n:décigramme" : docheck=False
          elif glose==u"kɛ̀mɛmɛtɛrɛ:n:hectomètre [kɛ̀mɛ:num:cent mɛ́tɛrɛ:n:mètre]" : docheck=False
          elif glose==u"santigaramu:n:centigramme" : docheck=False
          elif glose==u"penalitiduurutan:n:tirs.au.but [penaliti:n:penalty dúuru:num:cinq tán:v:donner.coup.de.pied]" : docheck=False
          elif glose==u"cámanko:n:pluralité [cáman:adj:nombreux [cá:vq:nombreux man:mrph:ADJ] kó:n:affaire]" : docheck=False
          elif glose==u"sùkarocayabana:n:diabète.maladie [súkaro:n:sucre cáya:v:multiplier [cá:vq:nombreux ya:mrph:DEQU] bàna:n:maladie]" : docheck=False
          elif glose==u"báyɛlɛmani===báyɛlɛmani:n:transformation [báyɛ̀lɛma:v:transformer [bá:n:base yɛ̀lɛma:v:changer] li:mrph:NMLZ]" : docheck=False
          elif glose==u"kásadiyalan:n:parfum [kása:n:odeur díya:v:rendre.agréable [dí:vq:agréable ya:mrph:DEQU] lan:mrph:INSTR]" : docheck=False
          elif glose==u"jòlimangoya:n:antipathie [jòlimango:adj:antipathique [jòliman:n:sang.actif [jòli:n:sang màn:mrph:SUPER] gó:adj:désagréable] ya:mrph:ABSTR]" : docheck=False

          if docheck==True and glose not in mmc :
            derivation=False

            gloselist=glose.split(u":",2)
            gloselx=gloselist[0]
            gloseps=gloselist[1]
            glosegloss=gloselist[2]
            if u"[" in glosegloss:
              maingloss=glosegloss[0:glosegloss.find(u"[")]
              maingloss=maingloss.strip()
            else: maingloss=glosegloss.strip()
            
            if maingloss=="":
              if gloseps=="v":
                if re.search(ur"(ra|la|na|r'|l'|n')$",gloselx) and re.search(ur"\:PFV\.INTR\]$",glosegloss) : derivation=True
                elif re.search(ur"(la|na|l'|n')$",gloselx) and re.search(ur"\:PROG\]$",glosegloss) : derivation=True
              
              elif gloseps=="n":
                if re.search(ur"w$",gloselx) and re.search(ur"\:PL\]$",glosegloss) : derivation=True
                elif re.search(ur"ba$",gloselx) and re.search(ur"\:AUGM\]$",glosegloss) : derivation=True
                elif re.search(ur"(la|na)$",gloselx) and re.search(ur"\:AG\.PRM\]$",glosegloss) : derivation=True
                elif re.search(ur"(baa|baga)$",gloselx) and re.search(ur"\:AG\.OCC\]$",glosegloss) : derivation=True
                elif re.search(ur"(li|ni)$",gloselx) and re.search(ur"\:NMLZ\]$",glosegloss) : derivation=True
              
              elif gloseps=="adj":
                if re.search(ur"w$",gloselx) and re.search(ur"\:PL\]$",glosegloss) : derivation=True
              elif gloseps=="dtm":
                if re.search(ur"w$",gloselx) and re.search(ur"\:PL\]$",glosegloss) : derivation=True
              elif gloseps=="prn":
                if re.search(ur"w$",gloselx) and re.search(ur"\:PL\]$",glosegloss) : derivation=True
              elif gloseps=="ptcp":
                if re.search(ur"w$",gloselx) and re.search(ur"\:PL\]",glosegloss) : derivation=True
                elif re.search(ur"(len|nen)$",gloselx) and re.search(ur"\:PTCP\.RES\]$",glosegloss) : derivation=True
                elif re.search(ur"ta$",gloselx) and re.search(ur"\:PTCP\.POT\]$",glosegloss) : derivation=True
                elif re.search(ur"bali$",gloselx) and re.search(ur"\:PTCP\.PRIV\]$",glosegloss) : derivation=True
            
            if derivation==False :
              if  nmmcquestion<20 : print 'sample glose not in mmc : "'+glose+'"'
              if gloseps!="n.prop" and re.search(ur"^[A-ZƐƆƝŊ]+",gloselx) :
                glose2=gloselx.lower()+gloseps+glosegloss
                if glose2 not in mmc:
                  log.write("?_ "+glose+"\n")
                  nmmcquestion=nmmcquestion+1
              else:
                if not re.search(ur"^[0-9]+",gloselx) : # ne pas traiter CARDINAL et ORDINAL
                  log.write("? "+glose+"\n")
                  nmmcquestion=nmmcquestion+1
            else :
              subglose=re.sub(ur"\[|\]","",glosegloss)
              subglose=re.sub(ur"  ","",subglose)
              subgloses=subglose.split(" ")
              for subg in subgloses:
                if subg!="":
                  subglist=subg.split(u":",2)
                  subglx=subglist[0]
                  subgps=subglist[1]
                  subggloss=subglist[2].strip()
                  if subggloss!="":
                    if u"." in subglx : subglx=re.sub(ur"\.","",subglx)
                    subg=subglx+u":"+subgps+u":"+subggloss
                    if subg not in mmcshort:
                      log.write("??_ "+subg+"\n")

        # end of complete checks -----------------------------------------------------------------------------
        
        if u"§§" in glose:   # un lemma var est proposé, (un seul!)
          pglose=glose.split(u"§§")
          glose1=pglose[0]
          glose2=pglose[1]
          html1=daba.formats.glosstext_to_html(glose1,variant=False, encoding='utf-8')
          html1=re.sub(ur"\<\/span\>$",u"",html1)
          html2=daba.formats.glosstext_to_html(glose2,variant=True, encoding='utf-8')
          wrepl=wrepl+u"<span class=\"w\" stage=\"0\">"+word+html1+html2+u"</span>\n</span>"
        else :
          htmlgloss=daba.formats.glosstext_to_html(glose,variant=False, encoding='utf-8')
          #log.write("[] glosstext_to_html: "+glose+" -> "+htmlgloss+"\n")
          wrepl=wrepl+u"<span class=\"w\" stage=\"0\">"+word+htmlgloss+u"\n</span>"
    
    nbreplok=nbreplok+1
    iprogress=nbreplok/float(nlignerepl)
    update_progress(iprogress)

    tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # derniers parametres : count (0=no limits to number of changes), flags re.U+

    # écrire les formules compilées

    wsearch=re.sub(ur"\n",u"¤¤",wsearch,0,re.U+re.MULTILINE)
    wsearch=re.sub(ur"\\n",u"¤¤",wsearch,0,re.U+re.MULTILINE)  
    
    wrepl=re.sub(ur"\n",u"¤¤",wrepl,0,re.U+re.MULTILINE)
    wrepl=re.sub(ur"\\n",u"¤¤",wrepl,0,re.U+re.MULTILINE)
    
    fileREPC.write(wsearch+u"==="+wrepl+u"\n")

    if nombre>0 :
      msg="%i modifs avec " % nombre +sequence+"\n"
      log.write(msg.encode("utf-8"))
      nbrulesapplied=nbrulesapplied+1
      nbmodif=nbmodif+nombre
      # recalculer lmots, enlever les ponctuations
      lmots=0
      for glose in gloses :
        if glose+"_" not in valides :
          lmots=lmots+1
      nbmots=nbmots+(nombre*lmots)
    
# POST : systematic global replaces ###############################################

# handle double pm   like dtm/prn 
# simple cases (simple gloss)

wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub>(<span class="lemma var">|</span>)'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub></span>\g<5>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # FIN: ps double -> lemma/lemma var duplication
if nombre>0 :
  if notfast: 
    msg="%i modifs ps double -> lemma/lemma var duplication " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=ur'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub></span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # FIN: double -> lemma var/lemma var duplication
if nombre>0 :
  if notfast: 
    msg="%i modifs double -> lemma var/lemma var duplication " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# how to handle complex gloss like dɔw ?
# ONLY Complex gloss with two sub components (and no main gloss)
wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # FIN: ps double complexgloss -> lemma/lemma var duplication
if nombre>0 :
  if notfast: 
    msg="%i modifs ps double complexgloss -> lemma/lemma var duplication " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


wsearch=ur'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span></span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # FIN: double  complexgloss-> lemma var/lemma var duplication
if nombre>0 :
  if notfast: 
    msg="%i modifs double  complexgloss-> lemma var/lemma var duplication " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# ONLY Complex gloss with two sub components (and explicit main gloss)

wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # FIN: ps double complexgloss -> lemma/lemma var duplication
if nombre>0 :
  if notfast: 
    msg="%i modifs ps double complexgloss -> lemma/lemma var duplication " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


wsearch=ur'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span></span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  # FIN: double  complexgloss-> lemma var/lemma var duplication
if nombre>0 :
  if notfast: 
    msg="%i modifs double  complexgloss-> lemma var/lemma var duplication " % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# fin : decoration pour consultation dans le navigateur
#  ambigüs
'''
wsearch=ur'<span class="w"(.*)lemma var(.*)\n</span>'
wrepl=ur'<span class="w" style="background-color:beige;"\g<1>lemma var\g<2>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  
if nombre>0 :
  msg="%i  highlight ambiguous words left for better navigator visualisation" % nombre +"\n"
  if notfast: log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
'''
wsearch=ur'</style>'
wrepl=ur'span.lemma.var {background-color:lightblue;}\n</style><title>'+filenametemp+ur'</title>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  
if nombre>0 :
  if notfast: 
    msg="%i  highlight ambiguous words left for better navigator visualisation" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
# inconnus
wsearch=ur'<span class="lemma">([^<]+)</span>'
wrepl=ur'<span class="lemma" style="background-color:red;">\g<1>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U+re.MULTILINE)  
if nombre>0 :
  if notfast: 
    msg="%i  highlight unkown words left for better navigator visualisation" % nombre +"\n"
    log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# FINISH
if notfast: 
  msg="\n %i modifs au total" % nbmodif
  log.write(msg.encode('utf-8'))
  msg="\n %i mots modifies au total" % nbmots
  log.write(msg.encode('utf-8'))

fileOUT.write(tout)
#fileOUT.write(tout.encode("utf-8"))

fileIN.close()
fileOUT.close()
if notfast :
  fileREP.close()
  if arg=="check" or arg=="-check" :
    log.write("------------mmc----------------\n")
    for mmcitem in mmc :
      log.write(mmcitem+"\n")
    log.write("------------fin mmc------------\n")

  log.close()
else :
  fileREPC.close()

if nbmodif==0 : 
  os.remove(logfilename)
  os.remove(filenameout)
  print "    yelemali si ma soro / pas de remplacements / no replacements\n    Baasi te! / Desole ! / Sorry!"
else: 
  if notfast : print ""
  filegiven=filenameout
  # renommer les fichiers, si dis :
  if ".dis.html" in filenamein :
    indexfile=1
    filenameinrename=filenamein+str(indexfile)
    while os.path.isfile(filenameinrename) :
      indexfile=indexfile+1
      filenameinrename=filenamein+str(indexfile)
    os.rename(filenamein, filenameinrename)
    print "\n   !",filenamein, "a ete renomme / has been renamed \n->",filenameinrename,"\n"
    os.rename(filenameout, filenamein)
    filegiven=filenamein
  else :
    if notfast : print "   "+filegiven+" ... mara dilannen don / fichier disponible / file is available\n"
   
  if notfast : print "    "+str(nbmots)+" mots desambiguises / disambiguated words"
  
  ambs=ambiguous.findall(tout)
  nbambs=len(ambs)
  if notfast : print "   ",nbambs, " mots ambigus restants  / ambiguous words left ", 100*nbambs/totalmots, "%"
   
  if notfast: 
    psambs=psambsearch.findall(tout)
    nbpsambs=len(psambs)
    psambslist=""
    if nbpsambs>0:
      for psamb in psambs:
        if psamb not in psambslist: psambslist=psambslist+psamb+" "
    print "   ",nbpsambs, " ps ambigues restantes / remaining ambiguous ps ( "+psambslist+")", 100*nbpsambs/totalmots, "%"
    print "    "+str(nbrulesapplied)+" regles appliquees / rules applied"
    print "    "+str(nbmodif)+" remplacements effectues / replacements done"
    print "    "+str(nbreplok)+" regles appliquées, voir le détail dans / see detail of applied rules in :"+logfilename
 
    if arg=="check" or arg=="-check" :
      print "    check : mots absents de Bamadaba : ", nmmcquestion

# print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timeend=time.time()
timeelapsed=timeend-timestart
# en minutes, approximativement
if notfast : print "    duree du traitement : "+str(int(timeelapsed))+" secondes, soit ",timeelapsed/totalmots," secondes/mot"
else : print filegiven+" ; ",totalmots," ; ",nbambs," ; ",int(timeelapsed)