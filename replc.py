#!/usr/bin/env python
# -*- coding: utf-8 -*-

# quick memo re processor number
"""
import os
import psutil
p=psutil.Process(os.getpid())
p.cpu_num()
"""


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
# PROJET
# détecter des AMBIGUOUShasname à changer en AMBIGUOUSselectname
# 1ère tentative AMBIGUOUShasname : <span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)</span><sub class="ps">([^<]+)</sub>([^<]*)</sub>(<span class="lemma var">[^<]+<sub class="ps">[.]+</sub><sub class="gloss">[.]+</sub>)</span)\n</span>

"""
RESERVE A REGEXP UTILES Dans l'editeur ou dans ce prog

Tous les verbes intransitifs (intransitiva tantum) - 309 au 23/3/19:
\\lx ([^\n]+)\n(((?!\\ps|\\lx)[^¤])*)\\ps v\n(((?!\\vl vr|\\vl vt|\\lx)[^¤])*)\\vl vi\n(((?!\\vl vr|\\vl vt|\\lx)[^¤])*)\n\n

Tous les verbes transitifs (transitiva tantum) - 438 au 23/3/19:
\\lx ([^\n]+)\n(((?!\\ps|\\lx)[^¤])*)\\ps v\n(((?!\\vl vr|\\vl vi|\\lx)[^¤])*)\\vl vt\n(((?!\\vl vr|\\vl vi|\\lx)[^¤])*)\n\n

Tous les verbes réfléchis seulement - 1 au 23/3/19 sonsoli:
\\lx ([^\n]+)\n(((?!\\ps|\\lx)[^¤])*)\\ps v\n(((?!\\vl vt|\\vl vi|\\lx)[^¤])*)\\vl vr\n(((?!\\vl vt|\\vl vi|\\lx)[^¤])*)\n\n


"""

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

if ".dis.fra" in filename:
  #sys.exit("repl.py does not handle .dis.fra files")
  print "WARNING repl.py does not know how to handle .dis.fra files - results unclear"
#elif ".pars.html" in filename :
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
filegiven=filenamein
filenameout=filenametemp+".repl.html"

fileIN = open(filenamein, "rb")
#fileIN = open(filenamein, "r")
fileOUT = open (filenameout,"wb")
tonal=""

arg=""

if nargv>2 : 
  arg= str(sys.argv[2])      # expected tonal ou bailleul
  # print "arg="+arg

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
nlignereplact=re.findall(ur"\n[^\#\s\n]",toutrepl,re.U|re.MULTILINE)
nlignerepl=len(nlignereplact)
print nlignereplall," lignes   ", nlignerepl," règles"

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

if script=="Ancien orthographe malien" : tonal="old"
elif script=="Nouvel orthographe malien" : tonal="new"
# elif script=="bailleul" : tonal="bailleul" # <---------- n'existe pas en réalité, vérifier arg !!!

if  filenametemp.startswith("baabu_ni_baabu") or filenametemp.startswith("gorog_meyer-contes_bambara1974") :
  tonal="newny"


print "text:script="+script+    ",    tonal="+tonal

if arg=="tonal" : tonal="tonal"
elif arg=="bailleul" : tonal="bailleul"

if tonal=="" : sys.exit("text:script non defini : pas de meta ou pas d'argument (tonal, bailleul)")

totalmots = tout.count("class=\"w\"")   # is needed in the final message to compute average ambiguous left and elapse time/word
    
print tout.count("class=\"annot\""), " phrases"
print totalmots, " mots"

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
valides=u"_COMMA_DOT_QUESTION_COLON_SEMICOLON_EXCLAM_PUNCT_NAME_NPROPRE_NPROPRENOM_NPROPRENOMM_NPROPRENOMF_NPROPRENOMMF_NPROPRENOMCL_NPROPRETOP_PERS_PRONOM_VERBE_VPERF_VNONPERF_VQ_DTM_PARTICIPE_PRMRK_COPULE_ADJECTIF_POSTP_NUM_NUMANNEE_ADV_ADVP_CONJ_PREP_AMBIGUOUS_DEGRE_DEBUT_BREAK_ADVN_VN_PRT_LAQUO_RAQUO_PARO_PARF_GUILLEMET_PRMRKQUAL_VQADJ_CONJPREP_COMMENT_TAG_FIN_CONJPOSS_PPPOSS_PRNDTM_TIRET_ADJN_DOONIN_PERCENT_NORV_NORADJ_AORN_DORP_ADJORD_PMORCOP_DTMORADV_INTJ_IPFVAFF_IPFVNEG_PFVTR_PFVNEG_PMINF_PMSBJV_NICONJ_YEUNDEF_NIUNDEF_NAUNDEF_NONVERBALGROUP_NUMORD_MONTH_COPEQU_ACTION_"
# toujours commencer et finir par _
# autres mots utilisés, traitements spéciaux : NUMnan, degremove, ADVNforcen, ADVNforceadv, CONJPREPforceconj, CONJPREPforceprep
gvalides=u"NOM.M_NOM.F_NOM.MF_NOM.CL_NOM.ETRG_NOM.FRA_CFA_FUT_QUOT_PP_IN_CNTRL_PROG_PFV.INTR_PL_PL2_AUGM_AG.OCC_PTCP.PRIV_GENT_AG.PRM_LOC_PRIX_MNT1_MNT2_STAT_INSTR_PTCP.RES_NMLZ_NMLZ2_COM_RECP.PRN_ADJ_DIR_ORD_DIM_PRIV_AG.EX_RECP_PTCP.POT_CONV_ST_DEQU_ABSTR_CAUS_SUPER_IN_EN_1SG_1SG.EMPH_2SG_2SG.EMPH_3SG_3SG.EMPH_1PL_1PL.EMPH_2PL_2PL.EMPH_3PL_BE_IPFV_IPFV.AFF_PROG.AFF_INFR_COND.NEG_FOC_PRES_TOP.CNTR_2SG.EMPH_3SG_REFL_DEF_INF_SBJV_OPT2_POSS_QUAL.AFF_PROH_TOP_PFV.NEG_QUAL.NEG_COND.AFF_REL_REL.PL2_CERT_ORD_DEM_RECP_DISTR_COP.NEG_IPFV.NEG_PROG.NEG_INFR.NEG_FUT.NEG_PST_Q_PFV.TR_EQU_IMP_RCNT_ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.USA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_DES_ADR_"
#  ANAPH, ANAPH.PL, ART, OPT, OPT2, PTCP.PROG removed
#  CFA à cause de la glose de dɔrɔmɛ qui finit par franc.CFA !!!
fixevalides="_ETRG_ETRG.FRA_ETRG.USA_ETRG.ENG_ETRG.GER_CHNT_Q_PREV_"
# cf kàmana:n:PREV de kamanagan
pmlist=u"bɛ́nà:pm:FUT_bɛ́n':pm:FUT_bɛ:pm:IPFV.AFF_b':pm:IPFV.AFF_be:pm:IPFV.AFF_bi:pm:IPFV.AFF_bɛ́kà:pm:PROG.AFF_bɛ́k':pm:PROG.AFF_bɛ́ka:pm:INFR_bága:pm:INFR_bìlen:pm:COND.NEG_kà:pm:INF_k':pm:INF_ka:pm:SBJV_k':pm:SBJV_ka:pm:QUAL.AFF_man:pm:QUAL.NEG_kànâ:pm:PROH_kàn':pm:PROH_ma:pm:PFV.NEG_m':pm:PFV.NEG_mánà:pm:COND.AFF_mán':pm:COND.AFF_máa:pm:COND.AFF_nà:pm:CERT_n':pm:CERT_tɛ:pm:IPFV.NEG_te:pm:IPFV.NEG_ti:pm:IPFV.NEG_t':pm:IPFV.NEG_tɛ́kà:pm:PROG.NEG_tɛ́k':pm:PROG.NEG_tɛ́ka:pm:INFR.NEG_tɛ́k':pm:INFR.NEG_tɛ́nà:pm:FUT.NEG_tɛ́n':pm:FUT.NEG_ye:pm:PFV.TR_y':pm:PFV.TR_yé:pm:IPFV_yé:pm:IMP_y':pm:IMP_yékà:pm:RCNT_màa:pm:DES_mà:pm:DES_m':pm:DES_"
coplist=u"bɛ́:cop:être_b':cop:être_b':cop:être_yé:cop:être_yé:cop:BE_kó:cop:QUOT_k':cop:QUOT_dòn:cop:ID_dò:cop:ID_tɛ́:cop:COP.NEG_té:cop:COP.NEG_t':cop:COP.NEG_yé:cop:EQU_y':cop:EQU_bé:cop:être_"
prnlist=u"ɲɔ́gɔn:prn:RECP_ɲɔ́ɔn:prn:RECP_mîn:prn:REL_mínnu:prn:REL.PL2_nìnnú:prn:DEM.PL_mín:prn:REL_nìn:prn:DEM_"
dtmlist=u"ìn:dtm:DEF_mîn:dtm:REL_nìn:dtm:DEM_nìn:dtm/prn:DEM_mín:dtm:REL_mínnu:dtm:REL.PL2_nìnnú:dtm:DEM.PL_nìnnú:dtm/prn:DEM.PL_"
perslist=u"ń:pers:1SG_nê:pers:1SG.EMPH_í:pers:2SG_í:pers:REFL_ê:pers:2SG.EMPH_à:pers:3SG_àlê:pers:3SG.EMPH_án:pers:1PL_ánw:pers:1PL.EMPH_a':pers:2PL_á:pers:2PL_á':pers:2PL_áw:pers:2PL.EMPH_ù:pers:3PL_òlû:pers:ce.PL2_ra:mrph:OPT2_la:mrph:OP2_na:mrph:OPT2_"
pplist=u"ka:pp:POSS_lá:pp:POSS_bólo:pp:CNTRL_yé:pp:PP_y':pp:PP_lɔ́:pp:IN_nɔ́:pp:IN_rɔ́:pp:IN_mà:pp:ADR_"   # c'est tout ??? oui car les autres ont des gloses en minuscules, cf besoin de "check"
conjlist=u"ô:conj:DISTR_ôo:conj:DISTR_"
prtlist=u"dè:prt:FOC_dùn:prt:TOP.CNTR_dún:prt:TOP.CNTR_kɔ̀ni:prt:TOP.CNTR2_tùn:prt:PST_wà:prt:Q_"
mrphlist=u"lá:mrph:CAUS_la:mrph:CAUS_ná:mrph:CAUS_mà:mrph:SUPER_màn:mrph:SUPER_rɔ́:mrph:IN_lu:mrph:PL2_nu:mrph:PL2_ba:mrph:AUGM_baa:mrph:AG.OCC_baga:mrph:AG.OCC_bali:mrph:PTCP.PRIV_ka:mrph:GENT_la:mrph:AG.PRM_na:mrph:AG.PRM_la:mrph:LOC_na:mrph:LOC_la:mrph:PRIX_na:mrph:PRIX_la:mrph:MNT1_na:mrph:MNT1_lata:mrph:MNT2_nata:mrph:MNT2_la:mrph:PROG_na:mrph:PROG_la:mrph:PFV.INTR_na:mrph:PFV.INTR_n':mrph:PFV.INTR_ra:mrph:PFV.INTR_rá:mrph:IN_rɔ́:mrph:IN_w:mrph:PL_"
mrphlist=mrphlist+u"lama:mrph:STAT_nama:mrph:STAT_lan:mrph:INSTR_nan:mrph:INSTR_len:mrph:PTCP.RES_nen:mrph:PTCP.RES_li:mrph:NMLZ_ni:mrph:NMLZ_\:mrph:NMLZ2_ma:mrph:COM_ma:mrph:RECP.PRN_man:mrph:ADJ_ntan:mrph:PRIV_"
mrphlist=mrphlist+u"ma:mrph:DIR_nan:mrph:ORD_nin:mrph:DIM_bali:mrph:PRIV_nci:mrph:AG.EX_ɲɔgɔn:mrph:RECP_ɲwan:mrph:RECP_ta:mrph:PTCP.POT_tɔ:mrph:CONV_tɔla:mrph:CONV_tɔ:mrph:ST_baatɔ:mrph:ST_bagatɔ:mrph:ST_ya:mrph:DEQU_yɛ:mrph:DEQU_ya:mrph:ABSTR_lá:mrph:CAUS_lán:mrph:CAUS_ná:mrph:CAUS_rɔ́:mrph:CAUS_ma:mrph:SUPER_man:mrph:SUPER_sɔ̀:mrph:EN_"
# restent u"ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_"
lxpsgvalides=pmlist+coplist+prnlist+dtmlist+perslist+pplist+conjlist+prtlist+mrphlist
lxpsg=re.compile(ur"[\_\[\s]([^:\[\_0-9]+:[a-z\/\.]+:[A-Z0-9][A-Z0-9\.\'\|]*)[\_\s\]]",re.U)   # ne vérifie que les gloses spéciales en majuscules, par ex. pas les pp comme lá:pp:à


# PRE : systematic global replaces  #################################################################

# normalize single quotes to avoid pop-up messages in gdisamb complaining that k' is not the same as k’
# tilted quote (word) to straight quotes (as in Bamadaba)
tout=re.sub(u"’",u"'",tout,0,re.U|re.MULTILINE)

# eliminer EMPR ex: ONI::EMPR
# see last section of bamana.gram
wsearch=ur'<span class="w" stage="[^\"]+">([A-Z\-]+)<span class="lemma">[a-z\-]+<sub class="gloss">EMPR</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # eliminer EMPR ex: ONI::EMPR
if nombre>0 :
  msg="%i modifs EMPR->ABR " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# dots in calculated lemma or lemma var cause artificial ambiguity sometimes 22/12/18 kalayali
# first dot
wsearch=ur'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=ur'<span class="\g<1>">\g<2>\g<3><'
tout,nombre1=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# second dot
wsearch=ur'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=ur'<span class="\g<1>">\g<2>\g<3><'
tout,nombre2=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# third dot
wsearch=ur'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=ur'<span class="\g<1>">\g<2>\g<3><'
tout,nombre3=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# more dots ignored
nombre=nombre1+nombre2+nombre3
if nombre>0 :
  msg="%i modifs enlever les points dans les lx " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# autres ABR possibles
# exemple : <span class="w" stage="-1">TPI<span class="lemma">tpi</span>\n</span>
wsearch=ur'<span class="w" stage="-1">([A-Z\-0-9]+)<span class="lemma">[a-zA-Z\-0-9]+</span>\n</span>'
wrepl=ur'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # autres ABR possibles
if nombre>0 :
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
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # gloss vides ex: baarakelen::
if nombre>0 :
  msg="%i modifs Gloss vide en lemma var" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# ex plus difficile pour les pluriels de mots inconnus (et d'autres dérivations communes possibles ?... à surveiller!)
# exemple traité : on ne garde pas le lemma var n/adj/dtm/prn/ptcp/n.prop/num, on garde les autres (si il y a des dérivations possibles)
# <span class="lemma">siyansikalanw<span class="lemma var">siyansikalanw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">siyansikalan<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">siyansikalanw<sub class="ps">n</sub><span class="m">siyansika<sub class="ps">v</sub></span><span class="m">lan<sub class="ps">mrph</sub><sub class="gloss">INSTR</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span>\n</span>

# ne marche pas pour: (est-ce que ça marche avec la correction du 2d n\.prop   ?)
# <span class="w" stage="0">konyèw<span class="lemma">konyɛw<span class="lemma var">konyɛw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">konyɛ<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">koɲɛw<sub class="ps">n</sub><span class="m">kóɲɛ<sub class="ps">n</sub><sub class="gloss">affaire</sub><span class="m">kó<sub class="ps">n</sub><sub class="gloss">affaire</sub></span><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">fois</sub></span></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>
# </span>
# revue de la formule complète le 16/2/18
# retains only if the FIRST lemma var, other multiple lemma vars eliminated (TO BE RESOLVED!)
wsearch=ur'<span class="lemma">[^<]+<span class="lemma var">[^<]+<sub class="ps">n/adj/dtm/prn/ptcp/n\.prop/num</sub><span class="m">[^<]+<sub class="ps">n/adj/dtm/prn/ptcp/n\.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">(((?!lemma var).)+)</span>((<span class="lemma var">[^\n]+</span>)*)</span>\n</span>'
wrepl=ur'<span class="lemma">\g<1></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss vide en lemma et n/adj/dtm/prn/ptcp/n.prop/num
if nombre>0 :
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

tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma var/lemma var
if nombre>0 :
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
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  msg="%i modifs Gloss doubles lemma/lemma var  - mais lemma var pas = lemma" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# éliminer les gloses bizarres des ordinaux : <span class="lemma">39nan<span class="lemma var">39nan<
wsearch=ur'<span class="lemma">(?P<stem>[0-9]+)nan<span class="lemma var">(?P=stem)nan<sub class="ps">adj</sub><span class="m">(?P=stem)<sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span></span>\n'
wrepl=ur'<span class="lemma">\g<1>nan<sub class="ps">adj</sub><span class="m">\g<1><sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
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
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
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
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
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
# remarque : ça pose problème pour Waraba, Suruku, Sonsannin... pour l'instant fixés dans REPL-STANDARD

# <span class="w" stage="0">Kati<span class="lemma">Kati<sub class="ps">n.prop</sub><sub class="gloss">TOP</sub><span class="lemma var">káti<sub class="ps">n</sub><sub class="gloss">caractère</sub></span><span class="lemma var">káti<sub class="ps">adv</sub><sub class="gloss">très.fort</sub></span></span>\n</span>
#wsearch=ur'</span><span class="w" stage="[0-9\-]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">(?P=w)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub>((<span class="lemma var">[^<]+<sub class="ps">[^<\.]+</sub><sub class="gloss">[^<]+</sub></span>)+)</span>\n</span>'
#wsearch=ur'</span><span class="w" stage="[0-9\-]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">(?P=w)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub><.*lemma var.*></span>\n</span>'
#wrepl=ur'</span><span class="w" stage="0">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span>\n</span>'
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma TOP et lemmavar non n.prop " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.CL</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.CL</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma NOM.CL et lemmavar non n.prop " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.M</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.M</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma NOM.M et lemmavar non n.prop " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.F</sub><.*lemma var.*></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.F</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma NOM.F et lemmavar non n.prop " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# this should not screw valid ones like Eziputikaw
#wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">(.+GENT.+)<span class="lemma var">(?P<lv>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n.prop</sub><sub class="gloss">(?P=lv)</sub></span></span>\n'
# but one extra span after ???
# <span class="w" stage="1">Keyilakaw<span class="lemma">keyilakaw<span class="lemma var">keyilakaw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">keyilaka<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">keyilakaw<sub class="ps">n/n.prop</sub><span class="m">keyi<sub class="ps">n/n.prop</sub></span><span class="m">la<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">keyilakaw<sub class="ps">n/n.prop</sub><span class="m">keyila<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n</span>
# pars <span class="w" stage="0">Keyilakaw<span class="lemma">keyilakaw<sub class="ps">n/n.prop</sub><span class="m">keyi<sub class="ps">n/n.prop</sub></span><span class="m">la<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span>\n</span>
# exemple span en trop
# <span class="w" stage="0">Horimakaw<span class="lemma">horimakaw<sub class="ps">n/n.prop</sub><span class="m">horima<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n</span>
# pars <span class="w" stage="1">Horimakaw<span class="lemma">horimakaw<span class="lemma var">horimakaw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">horimaka<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">horimakaw<sub class="ps">n/n.prop</sub><span class="m">horima<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">horimakaw<sub class="ps">n</sub><span class="m">hori<sub class="ps">n</sub></span><span class="m">ma<sub class="ps">mrph</sub><sub class="gloss">COM</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">horimakaw<sub class="ps">n</sub><span class="m">hori<sub class="ps">n</sub></span><span class="m">ma<sub class="ps">mrph</sub><sub class="gloss">RECP.PRN</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n</span>
# another case: repl
# <span class="w" stage="0">Timunakaw<span class="lemma">timunakaw<sub class="ps">n/n.prop</sub><span class="m">timu<sub class="ps">n/n.prop</sub></span><span class="m">na<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n</span>
# pars <span class="w" stage="1">Timunakaw<span class="lemma">timunakaw<span class="lemma var">timunakaw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">timunaka<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">timunakaw<sub class="ps">n/n.prop</sub><span class="m">timu<sub class="ps">n/n.prop</sub></span><span class="m">na<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">timunakaw<sub class="ps">n/n.prop</sub><span class="m">timuna<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n</span>
#
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">((((?!lemma var).)+)GENT(((?!lemma var).)+))<span class="lemma var">[^\n]+</span></span>\n'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs NOMPROPRE non-initial ambigu type -kaw GENT (lemma sans ps/gloss) " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# <span class="w" stage="-1">Pekosi<span class="lemma">pekosi<span class="lemma var">Pekosi<sub class="ps">n.prop</sub><sub class="gloss">Pekosi</sub></span></span>\n</span>
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">[^<]+<span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<2><sub class="ps">n.prop</sub><sub class="gloss">NOM</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non-initial ambigus " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# <span class="w" stage="0">Ɛntɛrinɛti<span class="lemma">ɛntɛrinɛti<sub class="ps">n</sub><sub class="gloss">Internet</sub><span class="lemma var">Ɛntɛrinɛti<sub class="ps">n.prop</sub><sub class="gloss">Ɛntɛrinɛti</sub></span></span>
#  wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub><span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span>\n</span>'
#  wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">\g<4></sub><sub class="gloss">\g<5></sub></span>\n</span>'

# essai avec sous-structure : (((?!<span class="lemma var">).)+)
wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">(((?!<span class="lemma var">).)+)<span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span>\n</span>'
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3></span>\n</span>'

tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres , éliminer NOMPROPRE en lemma var ambigus " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# wsearch=ur"(</span>|</span>\n)<span class=\"w\" stage=\"[0-9\-]+\">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<.+lemma var.+></span>\n"
wsearch=ur"(</span>|</span>\n)<span class=\"w\" stage=\"[0-9\-]+\">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class=\"lemma\">[^<]+<span class=\"lemma var\">.+></span>\n"
wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<2><sub class="ps">n.prop</sub><sub class="gloss">NOM</sub></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs NOMPROPRE non-initial ambigu total (lemma sans ps/gloss) -> NOM " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# handling NUMnan type not handled well in gparser (bamana.gram rules no longer works)
prefsearch=ur'<span class="sent">([^<]*)(?P<stem>[0-9]+)(?P<stemnan>nan|NAN|n)([\s\.\;\:\?\!\)\""][^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
nextsearch=ur'<span class="w" stage="tokenizer">(?P=stem)<span class="lemma">(?P=stem)<sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span>\n</span><span class="w" stage="2">(?P=stemnan)<span class="lemma">(?:nan|ń)<sub class="ps">(?:num|pers)</sub><sub class="gloss">(?:ORD|1SG)</sub></span>\n</span>'
prefrepl=u'<span class="sent">\g<1>\g<2>\g<3>\g<4><span class="annot">\g<5>'
nextrepl=u'<span class="w" stage="0">\g<2>\g<3><span class="lemma">\g<2>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<2><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n</span>'
wsearch=prefsearch+nextsearch
wrepl=prefrepl+nextrepl
#print "\nNUMnan wsearch:",wsearch
nombre=1
while nombre>0:
  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
  if nombre>0 :
    msg="%i modifs to handle NUMnan type words like 78nan " % nombre +"\n"
    log.write(msg.encode("utf-8"))
    nbrulesapplied=nbrulesapplied+1
    nbmodif=nbmodif+nombre
    nbmots=nbmots+nombre

# handling NUM nan types not handled well in gparser
prefsearch=ur'<span class="sent">([^<]*)(?P<stem>[0-9]+) (?P<stemnan>nan|NAN)([\s\.\;\:\?\!\)\"][^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
nextsearch=ur'<span class="w" stage="tokenizer">(?P=stem)<span class="lemma">(?P=stem)<sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span>\n</span><span class="w" stage="2">(?P=stemnan)<span class="lemma">nan<sub class="ps">num</sub><sub class="gloss">ORD</sub></span>\n</span>'
prefrepl=u'<span class="sent">\g<1>\g<2>\g<3>\g<4><span class="annot">\g<5>'
nextrepl=u'<span class="w" stage="0">\g<2>\g<3><span class="lemma">\g<2>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<2><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n</span>'
wsearch=prefsearch+nextsearch
wrepl=prefrepl+nextrepl
#print "\nNUMnan wsearch:",wsearch
nombre=1
while nombre>0:
  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
  if nombre>0 :
    msg="%i modifs to handle NUM nan type words like 78 nan " % nombre +"\n"
    log.write(msg.encode("utf-8"))
    nbrulesapplied=nbrulesapplied+1
    nbmodif=nbmodif+nombre
    nbmots=nbmots+nombre


# NOW THE BIG TASK     -go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!--
print "arg="+arg

fileREPCname="REPL-STANDARD-C.txt"
if filenametemp.endswith(".old") : fileREPCname="REPL-STANDARD-C.old.txt"
if tonal=="newny" : fileREPCname="REPL-STANDARD-C-ny.txt"

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
  if (u"===" not in linerepl) and (u"=>=" not in linerepl) and (u">>=" not in linerepl) and (u">==" not in linerepl):
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
  elif ">==" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u">==")
    ucase1=False
    topl=True
  elif "=>=" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u"=>=")
    ucase1=True
    topl=False
  elif ">>=" in linerepl :
    liste_mots,liste_gloses=linerepl.split(u">>=")
    ucase1=True
    topl=True
    
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
  elif  tonal=="newny" :  
    liste_mots=re.sub(u"ɲ",ur"ny",liste_mots)
    liste_mots=re.sub(u"Ɲ",ur"Ny",liste_mots)

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
          sys.exit("\n"+liste_gloses+"\n"+lxpsgloss_gloss+" : Glose ?standard? non valide a gauche de === "+lxpsgloss+"\nVoir le log : "+logfilename)

  # nombre de gloses de part et d'autre de ===
  
  elements=valides[1:len(valides)-1].split(u"_")   # ôter les _ avant et après avant de faire un split
  for element in elements:
    if element in liste_mots+"_"+liste_gloses:
      nbelement=re.findall("_"+element,"_"+liste_mots)
      nbelementg=re.findall("_"+element,"_"+liste_gloses)
      # if element=='TIRET': print "TIRET nbelement=",len(nbelement), " nbelementg=", len(nbelementg)
      if (len(nbelement)!=len(nbelementg)) and not (len(nbelementg)==0 and element in "_TIRET_"):
        log.write(u"il n'y a pas le même nombre de '_"+element+u"' de part et d'autre de ===\n")
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
    #elif mot==u"PUNCT"    : wsearch=wsearch+ur'<span class="c">([^<]+)</span>\n' 
    # nb: le point, et autres séparateurs de sentence, n'a normalement pas d'effet ici ! cf DEBUT
    elif mot==u"COMMENT"  : wsearch=wsearch+ur'<span class="comment">([^<]+)</span>\n' 
    elif mot==u"TAG"      : wsearch=wsearch+ur'<span class="t">([^<]+)</span>\n' 
    # attention <st> n'est pas un tag !!! <span class="c">&lt;st&gt;</span>
    elif mot==u"PUNCT"    : wsearch=wsearch+ur'<span class="([ct])">([^<]+)</span>\n' 
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
    elif mot==u"ACTION"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)><sub class="gloss">NMLZ</sub></span></span>\n</span>'
    elif mot==u"PERS"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pers</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"PRONOM"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">prn</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"PRT"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">prt</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"INTJ"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">intj</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"VERBE"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"VPERF"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)PFV\.INTR(((?!lemma var).)*)>\n</span>'
    elif mot==u"VNONPERF"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var|PFV\.INTR).)*)>\n</span>'
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
    elif mot==u"NUMORD"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)ORDINAL(((?!lemma var).)*)>\n</span>'
    elif mot==u"NUMANNEE"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([1-2][0-9][0-9][0-9])<span class="lemma">([1-2][0-9][0-9][0-9])<sub class="ps">num</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"ADV"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"ADVP"      : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv\.p</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"ADVN"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv/n</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"VN"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(?:v/n|n/v)</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"CONJ"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(conj|prep/conj|conj/prep)</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"PREP"     : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prep|prep/conj|conj/prep)</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"CONJPREP" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prep/conj|conj/prep)</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"CONJPOSS" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">conj</sub><sub class="gloss">POSS</sub></span>\n</span>'
    elif mot==u"PPPOSS" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span>\n</span>'
    elif mot==u"COPEQU" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">cop</sub><sub class="gloss">EQU</sub></span>\n</span>'
    elif mot==u"NPROPRE"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"NPROPRENOM"  : 
      lastnproprenom=ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM</sub></span>\n</span>'
      wsearch=wsearch+lastnproprenom
    elif mot==u"NPROPRENOMM"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.M</sub></span>\n</span>'
    elif mot==u"NPROPRENOMF"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.F</sub></span>\n</span>'
    elif mot==u"NPROPRENOMMF"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.MF</sub></span>\n</span>'
    elif mot==u"NPROPRENOMCL"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.CL</sub></span>\n</span>'
    elif mot==u"NPROPRETOP"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub>(((?!lemma var).)*)</span>\n</span>'
    elif mot==u"DOONIN"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">dɔ́ɔnin<sub class="ps">adj/n</sub><(((?!lemma var).)*)>\n</span>'
    elif mot==u"NORV"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)></span></span>\n</span>'
    elif mot==u"NORADJ"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)></span></span>\n</span>'
    elif mot==u"PMORCOP"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pm</sub><sub class="gloss">([^<]+)</sub><span class="lemma var">([^<]+)<sub class="ps">cop</sub><sub class="gloss">([^<]+)</sub></span></span>\n</span>'
    elif mot==u"AORN"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span>\n</span>'
    elif mot==u"DORP"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">dtm</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">prn</sub><(((?!lemma var).)*)></span></span>\n</span>'
    elif mot==u"DTMORADV"   : wsearch=wsearch+ur'<span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">dtm</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">adv</sub><(((?!lemma var).)*)></span></span>\n</span>'
    # to be implemented : GNMEMBER
    # <span class="lemma">([^<]+)<sub class="ps">(n|n.prop|pers|prn|dtm|adj|ptcp|prt)</sub><sub class="gloss">([^<]+)</sub>|<span class="lemma">([^<]+)<sub class="ps">(conj|prep\/conj|pp)</sub><sub class="gloss">(POSS|et|ainsi\.que)</sub>
    # add around this class="w" and not lemma var
    # arg impact on capt_gr_index  (TEST THOROUGHLY!!!)

    # PM and COPs - ajouter bi à IPFVAFF ???
    elif mot==u"IPFVAFF"     : 
      if tonal=="new" : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(bɛ|be|bi|b')<span class="lemma">[^\n]+</span>\n</span>'''
      elif tonal=="newny" : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(bɛ|be|bi|b')<span class="lemma">[^\n]+</span>\n</span>'''
      elif tonal=="old" : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(bè|be|bi|b')<span class="lemma">[^\n]+</span>\n</span>'''
    elif mot==u"IPFVNEG"     : 
      if tonal=="new" : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(tɛ|te|ti|t')<span class="lemma">[^\n]+</span>\n</span>'''
      elif tonal=="newny" : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(tɛ|te|ti|t')<span class="lemma">[^\n]+</span>\n</span>'''
      elif tonal=="old" : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(tè|te|ti|t')<span class="lemma">[^\n]+</span>\n</span>'''
    elif mot==u"PFVTR"     : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(ye|y')<span class="lemma">[^\n]+</span>\n</span>'''
    elif mot==u"PFVNEG"     : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(ma|m')<span class="lemma">[^\n]+</span>\n</span>'''
    elif mot==u"PMINF"     : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(ka|k'|Ka|K'|kà|Kà)<span class="lemma">[^\n]+</span>\n</span>'''
    elif mot==u"PMSBJV"     : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(ka|k'|ká)<span class="lemma">[^\n]+</span>\n</span>'''
    elif mot==u"NICONJ"     : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(ni|n'|ní)<span class="lemma">[^\n]+</span>\n</span>'''
    
    elif mot==u"MONTH" : 
      if tonal=="new" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">(zanwuyekalo|zanwiyekalo|feburuyekalo|feburiyekalo|feburuye-kalo|fewuruyekalo|marisikalo|awirilikalo|mɛkalo|zuwɛnkalo|zuluyekalo|zuliyekalo|utikalo|sɛtanburukalo|sɛtamburukalo|ɔkutɔburukalo|nowanburukalo|nowamburukalo|desanburukalo|desamburukalo)<span class="lemma">([^\n]+)</span>\n</span>'
      elif tonal=="newny" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">(zanwuyekalo|zanwiyekalo|feburuyekalo|feburiyekalo|feburuye-kalo|fewuruyekalo|marisikalo|awirilikalo|mɛkalo|zuwɛnkalo|zuluyekalo|zuliyekalo|utikalo|sɛtanburukalo|sɛtamburukalo|ɔkutɔburukalo|nowanburukalo|nowamburukalo|desanburukalo|desamburukalo)<span class="lemma">([^\n]+)</span>\n</span>'
      elif tonal=="old" : wsearch=wsearch+ur'<span class="w" stage="[^>]+">(zanwuyekalo|zanwiyekalo|feburuyekalo|feburiyekalo|feburuye-kalo|fewuruyekalo|marisikalo|awirilikalo|mèkalo|zuwènkalo|zuluyekalo|zuliyekalo|utikalo|sɛtanburukalo|sɛtamburukalo|òkutɔburukalo|nowanburukalo|nowamburukalo|desanburukalo|desamburukalo)<span class="lemma">([^\n]+)</span>\n</span>'
    elif mot==u"YEUNDEF"  : wsearch=wsearch+ur'''<span class="w" stage="[^>]+">(yé|ye|y')<[^\n]+lemma var[^\n]+</span>\n</span>'''
    elif mot==u"NIUNDEF"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">(ní|ni)<[^\n]+lemma var[^\n]+</span>\n</span>'
    elif mot==u"NAUNDEF"  : wsearch=wsearch+ur'<span class="w" stage="[^>]+">(ná|na)<[^\n]+lemma var[^\n]+</span>\n</span>'

    # elif mot==u"NONVERBALGROUP": wsearch=wsearch+ur'((<span class="w" stage="0">[^<]+<span class="lemma">[^<]+<sub class="ps">(?!v|vq|cop|pm)</sub>(((?!lemma var).)*)</span>\n</span>)+)'
    # elif mot==u"NONVERBALGROUP": wsearch=wsearch+ur'((<span class="w" stage="[^\"]+">[^<]+<span class="lemma">[^<]+<sub class="ps">(?:n|adj|pp|ptcp|n\.prop|num|dtm|prn|pers|conj)</sub>(((?!lemma var).)*)</span>\n</span>)+)'
    elif mot==u"NONVERBALGROUP": wsearch=wsearch+ur'''((<span class="w" stage="[^\"]+">[^<]+<span class="lemma">[^<]+<sub class="ps">(?:n|adj|ptcp|n.prop|num|dtm|prn|pers)</sub>(((?!lemma var).)*)</span>\n</span>|<span class="w" stage="[^\"]+">[^<]+<span class="lemma">(?:ka|k')<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span>\n</span>|<span class="w" stage="[^\"]+">[^<]+<span class="lemma">(?:ni|n')<sub class="ps">conj</sub><sub class="gloss">et</sub></span>\n</span>|<span class="w" stage="[^\"]+">[^<]+<span class="lemma">(?:àní|àn')<sub class="ps">conj</sub><sub class="gloss">ainsi.que</sub></span>\n</span>|<span class="w" stage="[^\"]+">[^<]+<span class="lemma">(?:wàlímà)<sub class="ps">conj</sub><sub class="gloss">ou.bien</sub></span>\n</span>|<span class="w" stage="[^\"]+">[^<]+<span class="lemma">(?:dè)<sub class="ps">prt</sub><sub class="gloss">FOC</sub></span>\n</span>|<span class="w" stage="[^\"]+">[^<]+<span class="lemma">(?:fána)<sub class="ps">prt</sub><sub class="gloss">aussi</sub></span>\n</span>)+)'''

    elif mot==u"AMBIGUOUS": wsearch=wsearch+ur'<span class="w"(.*)lemma var(.*)\n</span>'
    else :
      if u"'" in mot: mot=re.sub(ur"\'",u"[\'\’]+",mot)   # satanées curly brackets
      """
      motsearch=mot
      if tonal=="new":  # useful for Dumestre script tagged as "new" but not using ɲ (Baabu ni baabu etc.)
        motsearch=re.sub(u"ɲ",ur"(?:ɲ|ny)",mot)
        motsearch=re.sub(u"Ɲ",ur"(?:Ɲ|Ny)",motsearch)
      wsearch=wsearch+ur'<span class="w" stage="[a-z0-9\.\-]+">'+motsearch+ur'<.*</span>\n</span>'
      """
      if wsearch==u"" and ucase1 :
        winitial=mot[0:1]
        wrest=mot[1:len(mot)]
        # mot2=ur"(?:"+winitial.upper()+ur"|"+winitial+ur")"+wrest   # non-capturing group
        mot2=ur"(["+winitial.upper()+winitial+ur"]"+wrest+ur")"    # character class supposedly faster, at least less verbose!
        #print mot, mot2
        wsearch=wsearch+ur'<span class="w" stage="[a-z0-9\.\-]+">'+mot2+ur'<.*</span>\n</span>'

      else:
        wsearch=wsearch+ur'<span class="w" stage="[a-z0-9\.\-]+">'+mot+ur'<.*</span>\n</span>'

    if sequence=="": sequence=mot
    else : sequence=sequence+" "+mot
  
  
  lmots=len(mots)
  lgloses=len(gloses)

  imots=-1
  capt_gr_index=0   # capturing group index (si on a plusieurs symboles)
  prefsearch=ur""

  if lmots==lgloses:
    if "§§" in liste_gloses:
      if topl or ucase1 : sys.exit("\n§§ alternate gloss cannot use > for uppercase-test or force-plural:\n"+linerepl)
  else :
    log.write(u"!= NB ELEM DIFFERENTS:  ("+str(lmots)+u") !=  ("+str(lgloses)+")\n")

    if topl or ucase1 : sys.exit("\n> forbidden for force-plural or uppercase-test : the numbers of elements differ\n"+linerepl)
    # dans ce cas il devrait être possible de modifier aussi la "sentence":
    # <span class="sent">([^<]+ )halibi([ \.][^£]+)<span class="w" stage="3">halibi<span class="lemma">

    # check that gloses does not contain capitalized keyword // CANCELLED - NO THIS IS POSSIBLE
    #                 verif seulement sur liste_mot car liste_gloses peut contenir de nombreuses glose majuscules comme PFV.TR
    #   m=re.findall(ur"(\_[A-Z][A-Z]+\_)",u"_"+re.sub(u"\_",u"__",liste_mots)+u"_")   # caution: findall only find non overlapping sequences _TU_YA_SI_ only finds _TU_ and _SI_, but  not _YA_
    #   if len(m)!=0:
    #     sys.exit("number of elements differ, of which capitalized keywords : "+liste_mots)

    # find target words (new syntax in different number of words)
  
    gloseslx=re.findall(ur"([^\:\_]+)\:[^\_]+",liste_gloses)
    liste_gloseslx=" ".join(gloseslx)
    # ensure target words are in the same orthography
    if tonal=="bailleul" : 
          liste_gloseslx=re.sub(u"́","",liste_gloseslx)
          liste_gloseslx=re.sub(u"̂","",liste_gloseslx)
    elif tonal!="tonal" :  
          liste_gloseslx=re.sub(u"́","",liste_gloseslx)
          liste_gloseslx=re.sub(u"̀","",liste_gloseslx)
          liste_gloseslx=re.sub(u"̌","",liste_gloseslx)
          liste_gloseslx=re.sub(u"̂","",liste_gloseslx)
    if tonal=="old" : # dans ce cas, les tons sont éliminés mais on revient à l'ancienne écriture
          liste_gloseslx=re.sub(u"ɛɛ","èe",liste_gloseslx)
          liste_gloseslx=re.sub(u"ɛ","è",liste_gloseslx)
          liste_gloseslx=re.sub(u"Ɛ","È",liste_gloseslx)
          liste_gloseslx=re.sub(u"ɔɔ","òo",liste_gloseslx)
          liste_gloseslx=re.sub(u"ɔ","ò",liste_gloseslx)
          liste_gloseslx=re.sub(u"Ɔ","Ò",liste_gloseslx)
          liste_gloseslx=re.sub(u"ɲ","ny",liste_gloseslx)
          liste_gloseslx=re.sub(u"Ɲ","Ny",liste_gloseslx)
    elif tonal=="newny":
          #if oldny :       # cas type Baabu ni baabu
          liste_gloseslx=re.sub(u"ɲ","ny",liste_gloseslx)
          liste_gloseslx=re.sub(u"Ɲ","Ny",liste_gloseslx)
      
      # build prefixes for the search and replace expressions 
    liste_mots_spaced=liste_mots.replace("_"," ")
    liste_mots_spaced=re.sub(ur"([A-Z]+[\s])*","",liste_mots_spaced)  # eliminated capitalized keywords after/before
    liste_mots_spaced=re.sub(ur"([\s][A-Z]+)*","",liste_mots_spaced)  # eliminated capitalized keywords after/before
    # relookahead=ur">"+liste_mots_spaced.replace(" ","<|>")+ur"<"   #  "1 lɔ" → ">1<|>lɔ<"   as found in <span class="lemma">lɔ< ...
    if liste_mots_spaced=="1 lɔ": liste_mots_spaced="1lɔ"  # workaround gparser trick
    prefsearch=ur'<span class="sent">([^<]*)'+liste_mots_spaced+'([^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
    if liste_mots_spaced[0:1].isupper(): liste_gloseslx=liste_gloseslx[0:1].upper()+liste_gloseslx[1:len(liste_gloseslx)]
    prefrepl=u'<span class="sent">\g<1>'+liste_gloseslx+'\g<2><span class="annot">\g<3>'
    # don't forget to advance the index !
    capt_gr_index=capt_gr_index+3+1
    
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
      #wrepl=wrepl+ur'<span class="c">\g<'+str(capt_gr_index+1)+ur'></span>\n'
      #capt_gr_index=capt_gr_index+1
      # changed 2018-04-09 : can also be a tag!
      wrepl=wrepl+ur'<span class="\g<'+str(capt_gr_index+1)+ur'>">\g<'+str(capt_gr_index+2)+ur'></span>\n'
      capt_gr_index=capt_gr_index+2
    elif glose==u"COMMENT"    :
      wrepl=wrepl+ur'<span class="comment">\g<'+str(capt_gr_index+1)+ur'></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose==u"TAG"    :
      wrepl=wrepl+ur'<span class="t">\g<'+str(capt_gr_index+1)+ur'></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose==u"NAME"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
      # ces +1 bizarres sont apparus après l'introduction de la glose correcte pour ?!lemma var    ...  à surveiller !   
    elif glose==u"ACTION"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>><sub class="gloss">NMLZ</sub></span></span>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"PERS"     : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pers</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"PRONOM"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prn</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"PRT"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prt</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"INTJ"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">intj</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"VERBE"    : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"VNONPERF"    : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"VPERF"    : 
      #log.write(ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>PFV.INTR\g<'+str(capt_gr_index+5)+'>>\n</span>')
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>PFV.INTR\g<'+str(capt_gr_index+5)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+5+1  # j'aurais pensé +2 : il y a deux groupes  (?!lemma var) autour de PFV.INTR
    #elif glose==u"VPERF"    : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><span class="m">\g<'+str(capt_gr_index+3)+ur'><sub class="ps">v</sub><sub class="gloss">\g<'+str(capt_gr_index+4)+ur'></sub></span><span class="m">\g<'+str(capt_gr_index+5)+ur'><sub class="ps">mrph</sub><sub class="gloss">PFV.INTR</sub></span></span>\n</span>'
    #  capt_gr_index=capt_gr_index+5 # +1 (pas de (?!lemma var))
    elif glose==u"ADJORD"    : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+ur'><sub class="gloss">ORD</sub>\g<'+str(capt_gr_index+5)+ur'>>\n</span>'
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
    elif glose==u"ADJECTIFforcen" :    # ex sabanan est adj dand Bamadaba mais parfois devient n
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
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
    elif glose==u"NUMORD"    : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+ur'>ORDINAL\g<'+str(capt_gr_index+5)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+5+1  # j'aurais pensé +2 : il y a deux groupes  (?!lemma var) autour de ORDINAL - cf VPERF
    elif glose==u"NUMANNEE"      : 
      wrepl=wrepl+ur'<span class="w" stage="tokenizer">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">num</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"NUMnan"      :   # this is deprecated with the new PRE handlings - oct 2019
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
    elif glose==u"VNforcen"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"VNforcev"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
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
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">conj</sub><sub class="gloss">POSS</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose==u"PPPOSS"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">pp</sub><sub class="gloss">POSS</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose==u"COPEQU"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">cop</sub><sub class="gloss">EQU</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose==u"NPROPRE"      : 
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><\g<'+str(capt_gr_index+3)+ur'>>\n</span>'
      capt_gr_index=capt_gr_index+3+1
    elif glose==u"NPROPRENOMforcetop"      : 
      lastnproprenomforcetop=ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span>\n</span>'
      wrepl=wrepl+lastnproprenomforcetop
      lastnproprenomforcetopindex=capt_gr_index+1    # in order to collect all instances of that candidate TOP name
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
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
    elif glose==u"NORADJname" :
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n</span>'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose==u"NORADJadj" :
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+5)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+6)+ur'>></span>\n</span>'
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
    elif glose==u"DTMORADVdtm" :
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n</span>'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose==u"DTMORADVadv" :
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+5)+ur'><sub class="ps">adv</sub><\g<'+str(capt_gr_index+6)+ur'>></span>\n</span>'
      capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)

    elif glose==u"IPFVAFF":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
      # will need correction in POST for b'
    elif glose==u"IPFVNEG":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
      # will need correction in POST for t'
    elif glose==u"PFVTR":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+1)+ur'><sub class="ps">pm</sub><sub class="gloss">PFV.TR</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"PFVNEG":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+1)+ur'><sub class="ps">pm</sub><sub class="gloss">PFV.NEG</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"PMINF":
      #wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+1)+ur'><sub class="ps">pm</sub><sub class="gloss">INF</sub></span>\n</span>'
      # temp fix : lemma for ka has tone: kà !!! and no capital letters ... - how to replace (ka|k'|Ka|K') by (kà|k'|kà|k') ???
      # will need correction in POST for k' and K'
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">kà<sub class="ps">pm</sub><sub class="gloss">INF</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"PMSBJV":
      # will need correction in POST for k' and K'
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">ka<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"NICONJet":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+1)+ur'><sub class="ps">conj</sub><sub class="gloss">et</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"NICONJsi":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">ní<sub class="ps">conj</sub><sub class="gloss">si</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"MONTH":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'></span>\n</span>'
      capt_gr_index=capt_gr_index+2

    elif glose==u"YEUNDEFequpm":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">yé<sub class="ps">cop</sub><sub class="gloss">EQU</sub><span class="lemma var">yé<sub class="ps">pm</sub><sub class="gloss">PFV.TR</sub></span></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"YEUNDEFppvoir":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">yé<sub class="ps">pp</sub><sub class="gloss">PP</sub><span class="lemma var">yé<sub class="ps">v</sub><sub class="gloss">voir</sub></span></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"YEUNDEFpp":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">yé<sub class="ps">pp</sub><sub class="gloss">PP</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"YEUNDEFequ":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">yé<sub class="ps">cop</sub><sub class="gloss">EQU</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    
    elif glose==u"NIUNDEFet":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">ni<sub class="ps">conj</sub><sub class="gloss">et</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"NAUNDEFa":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">ná<sub class="ps">pp</sub><sub class="gloss">à</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1
    elif glose==u"NAUNDEFvenir":
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">nà<sub class="ps">v</sub><sub class="gloss">venir</sub></span>\n</span>'
      capt_gr_index=capt_gr_index+1

    elif glose==u"NONVERBALGROUP":
      wrepl=wrepl+ur'\g<'+str(capt_gr_index+1)+ur'>'
      capt_gr_index=capt_gr_index+4  # ou bien autant de fois que de matches et difficile à prévoir : 2 par word x nb de words

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
        elif tonal=="newny":
          #if oldny :       # cas type Baabu ni baabu
          word=re.sub(u"ɲ","ny",word)
          word=re.sub(u"Ɲ","Ny",word)
      
      
      if u"§§" in glose:   # un lemma var est proposé, (un seul!)
        pglose=glose.split(u"§§")
        glose1=pglose[0]
        glose2=pglose[1]
        html1=daba.formats.glosstext_to_html(glose1,variant=False, encoding='utf-8')
        html1=re.sub(ur"\<\/span\>$",u"",html1)
        html2=daba.formats.glosstext_to_html(glose2,variant=True, encoding='utf-8')
        wrepl=wrepl+ur'<span class="w" stage="0">'+word+html1+html2+ur'</span>\n</span>'
      else :
        htmlgloss=daba.formats.glosstext_to_html(glose,variant=False, encoding='utf-8')
        #log.write("[] glosstext_to_html: "+glose+" -> "+htmlgloss+"\n")
        if wrepl=="" and ucase1:
          wordrepl=ur"\g<1>"
          wrepl=wrepl+ur'<span class="w" stage="0">'+wordrepl+htmlgloss+ur'\n</span>'
          capt_gr_index=capt_gr_index+1      # or just =1 ?
        else:
          wrepl=wrepl+ur'<span class="w" stage="0">'+word+htmlgloss+ur'\n</span>'
        # a note of warning : wrepl works as a string for re.subn, so ur"" is not strictly needed 
        #       BUT when writing compiled rules ur"" is needed as regards \n, to conserve them as is in the file
        #       number of lines in file should = number of rules printed by program
  
  nbreplok=nbreplok+1
  iprogress=nbreplok/float(nlignerepl)
  update_progress(iprogress)

  if "NPROPRENOMforcetop" in liste_gloses:  forcetopiterator=re.finditer(wsearch,tout,re.U|re.MULTILINE)
  
  if prefsearch!=ur"":    # if number of elements differ in liste_mots and liste_gloses, update "sent"
      wsearch=prefsearch+wsearch
      wrepl=prefrepl+wrepl
      
  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # derniers parametres : count (0=no limits to number of changes), flags re.U|
  fileREPC.write(wsearch+u"==="+wrepl+u"\n")

  if topl : 
    if ucase1:
      mot2=re.sub("\)","w)",mot2)
      wsearch=ur'<span class="w" stage="[a-z0-9\.\-]+">'+mot2+ur'<.*</span>\n</span>'
    else : 
      wsearch=re.sub(word+"\<",word+"w<",wsearch)   # wsearch contains only one word, just add w
    gloseelems=glose.split(":",2)
    gloselx=gloseelems[0]
    gloseps=gloseelems[1]
    glose=gloselx+"w:"+gloseps+": ["+glose+" w:mrph:PL]"
    htmlgloss=daba.formats.glosstext_to_html(glose,variant=False, encoding='utf-8')
    if ucase1:
      wordrepl=ur"\g<1>"
      wrepl=ur'<span class="w" stage="0">'+wordrepl+htmlgloss+ur'\n</span>'
      capt_gr_index=capt_gr_index+1      # or just =1 ?
    else:
      wrepl=ur'<span class="w" stage="0">'+word+"w"+htmlgloss+ur'\n</span>'
      
    tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE) 
    fileREPC.write(wsearch+u"==="+wrepl+u"\n")

  if nombre>0 :
    # print "\nwsearch:",wsearch
    # print "wrepl:",wrepl
    # detecting that a name is TOP should propagate to all instances of that name in the text 
    if "NPROPRENOMforcetop" in liste_gloses: 
      for forcetop in forcetopiterator :
        topname=forcetop.group(lastnproprenomforcetopindex)
        # print topname
        lastnproprenom=ur'<span class="w" stage="[^>]+">'+topname+'<span class="lemma">'+topname+'<sub class="ps">n\.prop</sub><sub class="gloss">NOM</sub></span>\n</span>'
        lastnproprenomforcetop=ur'<span class="w" stage="[^>]+">'+topname+'<span class="lemma">'+topname+'<sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span>\n</span>'
        tout,nombre2=re.subn(lastnproprenom,lastnproprenomforcetop,tout,0,re.U|re.MULTILINE)
        nombre=nombre+nombre2
        lastnproprenom=ur'<span class="annot"><span class="w" stage="[^>]+">'+topname+'<span class="lemma">'+topname.lower()+'<sub class="gloss">EMPR</sub></span>\n</span>'
        lastnproprenomforcetop=ur'<span class="annot"><span class="w" stage="[^>]+">'+topname+'<span class="lemma">'+topname+'<sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span>\n</span>'
        tout,nombre3=re.subn(lastnproprenom,lastnproprenomforcetop,tout,0,re.U|re.MULTILINE)
        nombre=nombre+nombre3
      
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

# handle double pm   like dtm/prn and force disambiguator to choose

# simple cases (simple gloss)

wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub>(<span class="lemma var">|</span>)'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub></span>\g<5>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: ps double -> lemma/lemma var duplication
if nombre>0 :
  msg="%i modifs ps double -> lemma/lemma var duplication " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=ur'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub></span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: double -> lemma var/lemma var duplication
if nombre>0 :
  msg="%i modifs double -> lemma var/lemma var duplication " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# how to handle complex gloss like dɔw ?
# ONLY Complex gloss with two sub components (and no main gloss)
wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: ps double complexgloss -> lemma/lemma var duplication
if nombre>0 :
  msg="%i modifs ps double complexgloss -> lemma/lemma var duplication " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


wsearch=ur'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span></span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: double  complexgloss-> lemma var/lemma var duplication
if nombre>0 :
  msg="%i modifs double  complexgloss-> lemma var/lemma var duplication " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# ONLY Complex gloss with two sub components (and explicit main gloss)

wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span>'
wrepl=ur'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: ps double complexgloss -> lemma/lemma var duplication
if nombre>0 :
  msg="%i modifs ps double complexgloss -> lemma/lemma var duplication " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=ur'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span></span>'
wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: double  complexgloss-> lemma var/lemma var duplication
if nombre>0 :
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
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  highlight ambiguous words left for better navigator visualisation" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
'''
wsearch=ur'</style>'
wrepl=ur'span.lemma.var {background-color:lightblue;}\n</style><title>'+filenametemp+ur'</title>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  highlight ambiguous words left for better navigator visualisation" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
# inconnus
wsearch=ur'<span class="lemma">([^<]+)</span>'
wrepl=ur'<span class="lemma" style="background-color:red;">\g<1>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  highlight unkown words left for better navigator visualisation" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# PMINF POST correction for k' and K'
wsearch=ur'<span class="w" stage="0">(k\'|K\')<span class="lemma">kà<sub class="ps">pm</sub><sub class="gloss">INF</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">\g<1><span class="lemma">k'<sub class="ps">pm</sub><sub class="gloss">INF</sub></span>\n</span>"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  PMINF  POST correction(s) for k' and K'" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# PMSBJV POST correction for k' and K'
wsearch=ur'<span class="w" stage="0">(k\'|K\')<span class="lemma">ka<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">\g<1><span class="lemma">k'<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span>\n</span>"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  PMSBJV POST correction(s) for k' and K'" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# NICONJet POST correction for n'
wsearch=ur'<span class="w" stage="0">n\'<span class="lemma">ni<sub class="ps">conj</sub><sub class="gloss">et</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">n'<span class="lemma">n'<sub class="ps">conj</sub><sub class="gloss">et</sub></span>\n</span>"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  NICONJet POST correction(s) for n' " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
# NICONJsi POST correction for n'
wsearch=ur'<span class="w" stage="0">n\'<span class="lemma">ní<sub class="ps">conj</sub><sub class="gloss">si</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">n'<span class="lemma">n'<sub class="ps">conj</sub><sub class="gloss">si</sub></span>\n</span>"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  NICONJsi POST correction(s) for n' " % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVAFF POST correction for b'
wsearch=ur'<span class="w" stage="0">b\'<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">b'<span class="lemma">b'<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVAFF  POST correction(s) for b'" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVAFF POST correction for be
wsearch=ur'<span class="w" stage="0">be<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">be<span class="lemma">be<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVAFF  POST correction(s) for be" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVAFF POST correction for bi
wsearch=ur'<span class="w" stage="0">bi<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">bi<span class="lemma">bi<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVAFF  POST correction(s) for bi" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVNEG POST correction for t'
wsearch=ur'<span class="w" stage="0">t\'<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
wrepl=ur"""<span class="w" stage="0">t'<span class="lemma">t'<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVNEG  POST correction(s) for t'" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVNEG POST correction for te
wsearch=ur'<span class="w" stage="0">te<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">te<span class="lemma">te<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVNEG POST correction(s) for te" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVNEG POST correction for ti
wsearch=ur'<span class="w" stage="0">ti<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
wrepl=ur'<span class="w" stage="0">ti<span class="lemma">ti<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span>\n</span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVNEG POST correction(s) for ti" % nombre +"\n"
  log.write(msg.encode("utf-8"))
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# FINISH
msg="\n %i modifs au total" % nbmodif
log.write(msg.encode('utf-8'))
msg="\n %i mots modifies au total" % nbmots
log.write(msg.encode('utf-8'))

fileOUT.write(tout)
#fileOUT.write(tout.encode("utf-8"))

fileIN.close()
fileOUT.close()

fileREP.close()

log.close()


if nbmodif==0 : 
  os.remove(logfilename)
  os.remove(filenameout)
  print "    yelemali si ma soro / pas de remplacements / no replacements\n    Baasi te! / Desole ! / Sorry!"
else: 
  filegiven=filenameout
  print ""
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
    print "   "+filegiven+" ... mara dilannen don / fichier disponible / file is available\n"
   
  print "    "+str(nbmots)+" mots desambiguises / disambiguated words"
  
  ambs=ambiguous.findall(tout)
  nbambs=len(ambs)
  print "   ",nbambs, " mots ambigus restants  / ambiguous words left ", 100*nbambs/totalmots, "%"
   
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
 
# print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timeend=time.time()
timeelapsed=timeend-timestart
# en minutes, approximativement
print "    duree du traitement : "+str(int(timeelapsed))+" secondes, soit ",timeelapsed/totalmots," secondes/mot"