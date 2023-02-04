#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
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

tonal=""
arg=""

try:
  fileMMC=open("bamadaba-mmc.txt")
except : sys.exit ("arg 'check' needs file bamadaba-mmc.txt in current directory")
mmc=[]
mmcshort=[]
linemmc=fileMMC.readline()
while linemmc:
  entrymmc=linemmc[0:len(linemmc)-1] # strip trailing linefeed
  mmc.append(entrymmc)
  mmclist=entrymmc.split(u":",2)
  mmclx=mmclist[0]
  mmcps=mmclist[1]
  mmcgloss=mmclist[2]   # au sens large avec les sous gloses
  mmcgloss1=mmcgloss
  if u"[" in mmcgloss: 
    mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
  mmcshort.append(mmclx+u":"+mmcps+u":"+mmcgloss)
  if u"|" in mmclx :
    mmclxlist=mmclx.split(u"|")
    for mmclxel in mmclxlist:
      mmc.append(mmclxel+u":"+mmcps+u":"+mmcgloss1)
      if u"[" in mmcgloss: 
        mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
      mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)
      if u"/" in mmcps:
        mmcpslist=mmcps.split(u"/")
        for mmcpsel in mmcpslist:
          mmc.append(mmclxel+u":"+mmcpsel+u":"+mmcgloss1)
          if u"[" in mmcgloss: 
            mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
          mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)

  if u"/" in mmcps:
    mmcpslist=mmcps.split(u"/")
    for mmcpsel in mmcpslist:
      mmc.append(mmclx+u":"+mmcpsel+u":"+mmcgloss1)
      if u"[" in mmcgloss: 
        mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
      mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)

  linemmc=fileMMC.readline()
fileMMC.close()
print "check : mmc loaded "+str(len(mmc))+" words"


# replchecks-additions-repl.txt

try:
  fileMMC=open("replchecks-additions-repl.txt")
except : sys.exit ("arg 'check' needs file replchecks-additions-repl.txt in current directory")
linemmc=fileMMC.readline()
while linemmc:
  entrymmc=linemmc[0:len(linemmc)-1] # strip trailing linefeed
  mmc.append(entrymmc)
  mmclist=entrymmc.split(u":",2)
  mmclx=mmclist[0]
  mmcps=mmclist[1]
  mmcgloss=mmclist[2]   # au sens large avec les sous gloses
  mmcgloss1=mmcgloss
  if u"[" in mmcgloss: 
    mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
  mmcshort.append(mmclx+u":"+mmcps+u":"+mmcgloss)
  if u"|" in mmclx :
    mmclxlist=mmclx.split(u"|")
    for mmclxel in mmclxlist:
      mmc.append(mmclxel+u":"+mmcps+u":"+mmcgloss1)
      if u"[" in mmcgloss: 
        mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
      mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)
      if u"/" in mmcps:
        mmcpslist=mmcps.split(u"/")
        for mmcpsel in mmcpslist:
          mmc.append(mmclxel+u":"+mmcpsel+u":"+mmcgloss1)
          if u"[" in mmcgloss: 
            mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
          mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)

  if u"/" in mmcps:
    mmcpslist=mmcps.split(u"/")
    for mmcpsel in mmcpslist:
      mmc.append(mmclx+u":"+mmcpsel+u":"+mmcgloss1)
      if u"[" in mmcgloss: 
        mmcgloss=mmcgloss[0:mmcgloss.find(u"[")].strip()
      mmcshort.append(mmclx+u":"+mmcpsel+u":"+mmcgloss)

  linemmc=fileMMC.readline()
fileMMC.close()
print "check : mmc loaded 2 "+str(len(mmc))+" words"


  
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

logfilename="replchecks.log"
log =  open (logfilename,"w")

toutrepl=fileREP.read()
nlignereplall=toutrepl.count(u"\n")
nlignereplact=re.findall(ur"\n[^\#\s\n]",toutrepl,re.U|re.MULTILINE)
nlignerepl=len(nlignereplact)
print nlignereplall," lignes   ", nlignerepl," règles"

nligne=1
nbreplok=0

psvalides="|adj|adv|adv.p|conj|conv.n|cop|dtm|intj|mrph|n|n.prop|num|onomat|pers|pm|pp|prep|prn|prt|ptcp|v|vq|"
valides="_COMMA_DOT_QUESTION_COLON_SEMICOLON_EXCLAM_PUNCT_NAME_NPROPRE_NPROPRENOM_NPROPRENOMM_NPROPRENOMF_NPROPRENOMMF_NPROPRENOMCL_NPROPRETOP_PERS_PRONOM_VERBE_VPERF_VNONPERF_VERBENMOD_VQ_DTM_PARTICIPE_PRMRK_COPULE_ADJECTIF_POSTP_NUM_NUMANNEE_ADV_ADVP_CONJ_PREP_AMBIGUOUS_DEGRE_DEBUT_BREAK_ADVN_VN_PRT_LAQUO_RAQUO_PARO_PARF_APOSTROPHE_GUILLEMET_PRMRKQUAL_VQADJ_VQORADJ_CONJPREP_COMMENT_TAG_FIN_CONJPOSS_PPPOSS_PRNDTM_TIRET_ADJN_DOONIN_PERCENT_NORV_NORADJ_AORN_DORP_ADJORD_PMORCOP_DTMORADV_INTJ_IPFVAFF_IPFVNEG_PFVTR_PFVNEG_PMINF_PMSBJV_NICONJ_YEUNDEF_KUNDEF_YEPP_NIUNDEF_NAUNDEF_NONVERBALGROUP_NUMORD_MONTH_COPEQU_COPQUOT_COPNEG_ACTION_CONSONNE_LANA_LETTRE_"
# toujours commencer et finir par _
# autres mots utilisés, traitements spéciaux : NUMnan, degremove, ADVNforcen, ADVNforceadv, CONJPREPforceconj, CONJPREPforceprep
gvalides="NOM.M_NOM.F_NOM.MF_NOM.CL_NOM.ETRG_NOM.FRA_CFA_FUT_QUOT_PP_IN_CNTRL_PROG_PFV.INTR_PL_PL2_AUGM_AG.OCC_PTCP.NEG_GENT_AG.PRM_LOC_PRIX_MNT1_MNT2_STAT_INSTR_PTCP.RES_NMLZ_NMLZ2_COM_RECP.PRN_ADJ_DIR_ORD_DIM_PRIV_AG.EX_RECP_PTCP.POT_CONV_ST_DEQU_ABSTR_CAUS_SUPER_IN_EN_1SG_1SG.EMPH_2SG_2SG.EMPH_3SG_3SG.EMPH_1PL_1PL.EMPH_2PL_2PL.EMPH_3PL_IPFV_IPFV.AFF_PROG.AFF_INFR_COND.NEG_FOC_PRES_TOP.CNTR_2SG.EMPH_3SG_REFL_DEF_INF_SBJV_OPT2_POSS_QUAL.AFF_PROH_TOP_PFV.NEG_QUAL.NEG_COND.AFF_REL_REL.PL2_CERT_ORD_DEM_RECP_DISTR_COP.NEG_IPFV.NEG_PROG.NEG_INFR.NEG_FUT.NEG_PST_Q_PFV.TR_EQU_IMP_RCNT_ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.USA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_DES_ADR_"
#  ANAPH, ANAPH.PL, ART, OPT, OPT2, PTCP.PROG removed
#  CFA à cause de la glose de dɔrɔmɛ qui finit par franc.CFA !!!
fixevalides="_ETRG_ETRG.FRA_ETRG.USA_ETRG.ENG_ETRG.GER_ETRG.ARB_ETRG.FUL_ETRG.MNK_CHNT_Q_PREV_INCOGN_"
# cf kàmana:n:PREV de kamanagan
# --- liste des auxiliaires dont les gloses sont des mot-clefs en majuscules
pmlist="bɛ́nà:pm:FUT_bɛ́n':pm:FUT_bɛ:pm:IPFV.AFF_b':pm:IPFV.AFF_be:pm:IPFV.AFF_bi:pm:IPFV.AFF_bɛ́kà:pm:PROG.AFF_bɛ́k':pm:PROG.AFF_bɛ́ka:pm:INFR_bága:pm:INFR_bìlen:pm:COND.NEG_kà:pm:INF_k':pm:INF_ka:pm:SBJV_k':pm:SBJV_ka:pm:QUAL.AFF_man:pm:QUAL.NEG_kànâ:pm:PROH_kàn':pm:PROH_ma:pm:PFV.NEG_m':pm:PFV.NEG_mánà:pm:COND.AFF_mán':pm:COND.AFF_máa:pm:COND.AFF_nà:pm:CERT_n':pm:CERT_tɛ:pm:IPFV.NEG_te:pm:IPFV.NEG_ti:pm:IPFV.NEG_t':pm:IPFV.NEG_tɛ́kà:pm:PROG.NEG_tɛ́k':pm:PROG.NEG_tɛ́ka:pm:INFR.NEG_tɛ́k':pm:INFR.NEG_tɛ́nà:pm:FUT.NEG_tɛ́n':pm:FUT.NEG_ye:pm:PFV.TR_y':pm:PFV.TR_yé:pm:IPFV_yé:pm:IMP_y':pm:IMP_yékà:pm:RCNT_màa:pm:DES_mà:pm:DES_m':pm:DES_"
coplist="bɛ́:cop:être_b':cop:être_b':cop:être_yé:cop:être_kó:cop:QUOT_k':cop:QUOT_dòn:cop:ID_dò:cop:ID_tɛ́:cop:COP.NEG_té:cop:COP.NEG_t':cop:COP.NEG_yé:cop:EQU_y':cop:EQU_bé:cop:être_"
prnlist="ɲɔ́gɔn:prn:RECP_ɲwán:prn:RECP_ɲɔ́ɔn:prn:RECP_mîn:prn:REL_mínnu:prn:REL.PL2_nìnnú:prn:DEM.PL_mín:prn:REL_nìn:prn:DEM_"
dtmlist="ìn:dtm:DEF_mîn:dtm:REL_nìn:dtm:DEM_nìn:dtm/prn:DEM_mín:dtm:REL_mínnu:dtm:REL.PL2_nìnnú:dtm:DEM.PL_nìnnú:dtm/prn:DEM.PL_"
perslist="ń:pers:1SG_nê:pers:1SG.EMPH_í:pers:2SG_í:pers:REFL_ê:pers:2SG.EMPH_à:pers:3SG_àlê:pers:3SG.EMPH_án:pers:1PL_ánw:pers:1PL.EMPH_a':pers:2PL_á:pers:2PL_á':pers:2PL_áw:pers:2PL.EMPH_ù:pers:3PL_òlû:pers:ce.PL2_"
pplist="ka:pp:POSS_lá:pp:POSS_bólo:pp:CNTRL_yé:pp:PP_y':pp:PP_lɔ́:pp:IN_nɔ́:pp:IN_rɔ́:pp:IN_mà:pp:ADR_mɔ̀:pp:ADR_"   # c'est tout ??? oui car les autres ont des gloses en minuscules, cf besoin de "check"
conjlist="ô:conj:DISTR_ôo:conj:DISTR_wô:conj:DISTR_"
prtlist="dè:prt:FOC_dùn:prt:TOP.CNTR_dún:prt:TOP.CNTR_kɔ̀ni:prt:TOP.CNTR2_tùn:prt:PST_kùn:prt:PST_wà:prt:Q_"
mrphlist="lá:mrph:CAUS_la:mrph:CAUS_ná:mrph:CAUS_mà:mrph:SUPER_màn:mrph:SUPER_rɔ́:mrph:IN_lu:mrph:PL2_nu:mrph:PL2_ba:mrph:AUGM_baa:mrph:AG.OCC_baga:mrph:AG.OCC_bali:mrph:PTCP.NEG_ka:mrph:GENT_la:mrph:AG.PRM_na:mrph:AG.PRM_la:mrph:LOC_na:mrph:LOC_la:mrph:PRIX_na:mrph:PRIX_la:mrph:MNT1_na:mrph:MNT1_lata:mrph:MNT2_nata:mrph:MNT2_la:mrph:PROG_na:mrph:PROG_la:mrph:PFV.INTR_na:mrph:PFV.INTR_n':mrph:PFV.INTR_ra:mrph:PFV.INTR_rá:mrph:IN_rɔ́:mrph:IN_w:mrph:PL_"
mrphlist=mrphlist+"lama:mrph:STAT_nama:mrph:STAT_lan:mrph:INSTR_nan:mrph:INSTR_len:mrph:PTCP.RES_nen:mrph:PTCP.RES_li:mrph:NMLZ_ni:mrph:NMLZ_\:mrph:NMLZ2_ma:mrph:COM_ma:mrph:RECP.PRN_man:mrph:ADJ_ntan:mrph:PRIV_ra:mrph:OPT2_la:mrph:OP2_na:mrph:OPT2_"
mrphlist=mrphlist+"ma:mrph:DIR_nan:mrph:ORD_nin:mrph:DIM_bali:mrph:PRIV_nci:mrph:AG.EX_ɲɔgɔn:mrph:RECP_ɲwan:mrph:RECP_ta:mrph:PTCP.POT_tɔ:mrph:CONV_tɔ:mrph:ST_ya:mrph:DEQU_yɛ:mrph:DEQU_ya:mrph:ABSTR_lá:mrph:CAUS_lán:mrph:CAUS_ná:mrph:CAUS_rɔ́:mrph:CAUS_ma:mrph:SUPER_man:mrph:SUPER_sɔ̀:mrph:EN_"
# restent u"ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_"
lxpsgvalides=pmlist+coplist+prnlist+dtmlist+perslist+pplist+conjlist+prtlist+mrphlist
lxpsg=re.compile(r"[\_\[\s]([^:\[\_0-9]+:[a-z\/\.]+:[A-Z0-9][A-Z0-9\.\'\|]*)[\_\s\]]",re.U)

mmcchecked=0
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
  if (u"===" not in linerepl) and (u"=>=" not in linerepl) and (u">>=" not in linerepl) and (u">==" not in linerepl) and (u"=*=" not in linerepl):
      log.write("erreur de === :"+str(nblinerepl)+" : "+linerepl+"\n len="+str(len(linerepl)))
      sys.exit(linerepl+"\nseparator === (or >== ) (or =>= )  (or >>= ) is missing on line")

  if ((u">==" in linerepl) or (u">>=" in linerepl)) and (u"_" in linerepl) :
      log.write("erreur sep >== ou >>= et plusieurs mots:"+str(nblinerepl)+" : "+linerepl+"\n len="+str(len(linerepl)))
      sys.exit(linerepl+"\nseparator >==  or >>= forbidden if more than one word")

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
   
  # setting ucase1 - also try capitalising initial word
  # setting topl - also try the plural form in -w
  if "===" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u"===")
    ucase1=False
    topl=False
    differ=False
  elif ">==" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u">==")
    ucase1=False
    topl=True
    differ=False
  elif "=>=" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u"=>=")
    ucase1=True
    topl=False
    differ=False
  elif ">>=" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u">>=")
    ucase1=True
    topl=True
    differ=False
  elif "=*=" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u"=*=")
    ucase1=False
    topl=False
    differ=True

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
          print "\n"+liste_gloses+"\n"+lxpsgloss_gloss+" : Glose ?standard? non valide a gauche de ===\nVoir le log : "+logfilename
          break

  # nombre de gloses de part et d'autre de ===
  
  elements=valides[1:len(valides)-1].split(u"_")   # ôter les _ avant et après avant de faire un split
  for element in elements:
    if element in liste_mots+"_"+liste_gloses:
      nbelement=re.findall("_"+element,"_"+liste_mots)
      nbelementg=re.findall("_"+element,"_"+liste_gloses)
      # if element=='TIRET': print "TIRET nbelement=",len(nbelement), " nbelementg=", len(nbelementg)
      if not differ and (len(nbelement)!=len(nbelementg)) and not (len(nbelementg)==0 and element in "_TIRET_"):
        log.write(u"il n'y a pas le même nombre de '_"+element+u"' de part et d'autre de ===\n")
        sys.exit("\n"+liste_mots+"\n"+liste_gloses+"\nErreur de syntaxe! pas le meme nombre de '"+element+"' de part et d'autre de ===\nvoir le log : "+logfilename)

  # autres validations à ajouter ici ?
  

  mots=liste_mots.split(u"_")
  gloses=liste_gloses.split(u"_")
  

  lmots=len(mots)
  lgloses=len(gloses)
  nbmots=len(mots)
  nbgloses=len(gloses)

  if not differ:
    if nbmots!=nbgloses:
      log.write(u"il n'y a pas le même nombre d'éléments de part et d'autre (ou alors spécifier =*= comme séparateur)\n")
      sys.exit("\n"+liste_mots+"\n"+liste_gloses+"\nErreur de syntaxe! pas le meme nombre d'éléments de part et d'autre (ou alors spécifier =*= comme séparateur)\nvoir le log : "+logfilename)
  
  if differ:
    if nbmots==nbgloses:
      log.write(u"il y a le même nombre d'éléments de part et d'autre, alors que =*= est spécifié)\n")
      sys.exit("\n"+liste_mots+"\n"+liste_gloses+"\nErreur de syntaxe! il y a le même nombre d'éléments de part et d'autre, alors que =*= est spécifié\nvoir le log : "+logfilename)

  imots=-1
  capt_gr_index=0   # capturing group index (si on a plusieurs symboles)
  prefsearch=ur""

  if lmots==lgloses:
    if "§§" in liste_gloses:
      if topl or ucase1 : sys.exit("\n§§ alternate gloss cannot use > for uppercase-test or force-plural:\n"+linerepl)
  else :
    log.write(u"!= NB ELEM DIFFERENTS:  ("+str(lmots)+u") !=  ("+str(lgloses)+")\n")

    if topl or ucase1 : sys.exit("\n> forbidden for force-plural or uppercase-test : the numbers of elements differ\n"+linerepl)

  # only check lx:ps:gloss forms 
  liste_gloses2=re.sub(ur"(?:_[A-Z]+)_","_",liste_gloses,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"_[A-Z]+$","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"^[A-Z]+_","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"(?:_[A-Z]+[a-z]+)_","_",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"_[A-Z]+[a-z]+$","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"^[A-Z]+[a-z]+_","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"§§","_",liste_gloses2,re.U)  # eliminate double gloss problem in order to check each element separately
  #print "liste_glose2 g: ",liste_gloses2
  # repeat as there is always one remaining (non overlapping problem ?)
  liste_gloses2=re.sub(ur"(?:_[A-Z]+)_","_",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"_[A-Z]+$","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"^[A-Z]+_","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"(?:_[A-Z]+[a-z]+)_","_",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"_[A-Z]+[a-z]+$","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"^[A-Z]+[a-z]+_","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  #liste_gloses2=re.sub(ur"§§","_",liste_gloses2,re.U)  # eliminate double gloss problem in order to check each element separately
  # repeat as there is always one remaining (non overlapping problem ?)
  liste_gloses2=re.sub(ur"(?:_[A-Z]+)_","_",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"_[A-Z]+$","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"^[A-Z]+_","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"(?:_[A-Z]+[a-z]+)_","_",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"_[A-Z]+[a-z]+$","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  liste_gloses2=re.sub(ur"^[A-Z]+[a-z]+_","",liste_gloses2,re.U)  # eliminate capitalized keywords after/before
  #liste_gloses2=re.sub(ur"§§","_",liste_gloses2,re.U)  # eliminate double gloss problem in order to check each element separately

  gloses2=[]
  if "_" not in liste_gloses2:
    liste_gloses3=re.sub(ur"^[A-Z]+[a-z]*$","",liste_gloses2,re.U)
    #print "lg2:",liste_gloses2,"   → lg3: ",liste_gloses3
    if liste_gloses3!="":gloses2.append(liste_gloses3)
    else: 
      continue
  else: gloses2=liste_gloses2.split(u"_")
  for glose in gloses2:
    mmcchecked=mmcchecked+1
    docheck=True
    #if    u": [" in glose : docheck=False
    #elif u"§§" in glose : docheck=False
    if u"§§" in glose : docheck=False  # ne devrait plus arriver (split)
    elif u"nan:adj:ORDINAL" in glose : docheck=False
    elif u":num:CARDINAL" in glose : docheck=False
    elif u":conv.n:" in glose : docheck=False
    elif u":n.prop:ABR" in glose : docheck=False
    elif re.search(ur"\:n\.prop\:[A-Z\-]+",glose) : docheck=False
    elif u"ETRG.FRA" in glose : docheck=False
    elif u"ETRG.ENG" in glose : docheck=False
    elif u"ETRG.USA" in glose : docheck=False
    elif u"ETRG.GER" in glose : docheck=False
    elif u"ETRG.ARB" in glose : docheck=False
    elif u"ETRG.ITA" in glose : docheck=False
    elif u"ETRG.ESP" in glose : docheck=False
    elif u"ETRG.FUL" in glose : docheck=False
    elif u"::CHNT" in glose : docheck=False
    elif u":n.prop:NOM.ETRG" in glose : docheck=False
    elif u":n.prop:NOM.FRA" in glose : docheck=False
    elif u":n.prop:NOM.ESP" in glose : docheck=False
    elif u":n.prop:NOM.US" in glose : docheck=False
    elif u":n.prop:NOM.ENG" in glose : docheck=False
    elif u":n.prop:NOM.POR" in glose : docheck=False
    elif u":n.prop:NOM.ITA" in glose : docheck=False
    elif u":n.prop:NOM.RUS" in glose : docheck=False
    elif u":n.prop:NOM.USA" in glose : docheck=False
    elif u":n.prop:NOM.GER" in glose : docheck=False
    elif u":n.prop:NOM.ARB" in glose : docheck=False
    elif u":n.prop:NOM.FUL" in glose : docheck=False
    elif u":n.prop:TOP" in glose : docheck=False
    elif glose=="NUMnan" : docheck=False
    
    """
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
    """
    gloselx,gloserest=glose.split(":",1)
    if " " in gloselx:
      gloselx=gloselx.replace(" "," ")  # hard spaces in REPL.STANDARD but simple space in Bamadaba: í ko / Burkina Faso ...
      glose=gloselx+":"+gloserest

    if docheck==True and glose not in mmc :
      derivation=False
      # print "glose avant split: "+glose
      if ":" not in glose:
        print "pas de : =",glose, " sur la ligne: ",liste_gloses, " liste_gloses2: ",liste_gloses2
        break
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
      
      if derivation==False and maingloss!="" :
        if  nmmcquestion<40 : print 'sample glose not in mmc : "'+glose+'"'
        glose2=""
        glose3=""
        if gloseps!="n.prop" and re.search(ur"^[A-ZƐƆƝŊ]+",gloselx) :
          glose2=gloselx.lower()+":"+gloseps+":"+glosegloss
          if glose2 not in mmc:
              log.write("?_ "+glose+"\n")
              nmmcquestion=nmmcquestion+1
        elif gloseps=="prep":
            glose3=re.sub("\:prep\:",":conj:",glose)
            print "prep check :",glose3
            if glose3 not in mmc:
              log.write("? "+glose+"\n")
              nmmcquestion=nmmcquestion+1
        elif gloseps=="prn":
            glose3=re.sub("\:prn\:",":dtm:",glose)
            print "prn check :",glose3
            if glose3 not in mmc:
              log.write("? "+glose+"\n")
              nmmcquestion=nmmcquestion+1
        else:
          if not re.search(ur"^[0-9]+",gloselx) : # ne pas traiter CARDINAL et ORDINAL
            log.write("? "+glose+"\n")
            nmmcquestion=nmmcquestion+1
      else :  # si c'est une dérivation ou bien si il n'y a pas de maingloss, vérifier seulement les composants
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
      
  
  nbreplok=nbreplok+1
  iprogress=nbreplok/float(nlignerepl)
  update_progress(iprogress)

  

# FINISH

log.write("------------mmc----------------\n")
for mmcitem in mmc :
  log.write(mmcitem+"\n")
log.write("------------fin mmc------------\n")
log.close()

print "    check : mots absents de Bamadaba : ", nmmcquestion, " sur ", mmcchecked," mots vérifiés"

# print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timeend=time.time()
timeelapsed=timeend-timestart
# en minutes, approximativement
print "    duree du traitement : "+str(int(timeelapsed))+" secondes"