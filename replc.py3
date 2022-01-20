#!/usr/bin/env python
# -*- coding: utf-8 -*-

# quick memo re processor number - jjm
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
# 1ère tentative AMBIGUOUShasname : <span class="w" stage="[^>]+">([^<]+)<span class="lemma">([^<]+)</span><sub class="ps">([^<]+)</sub>([^<]*)</sub>(<span class="lemma var">[^<]+<sub class="ps">[.]+</sub><sub class="gloss">[.]+</sub>)</span)</span>\n

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
import daba.formats
import unicodedata as u
from time import gmtime, strftime, time
# print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
import time
import collections

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

wordsearch=re.compile(r'\<span class\=\"w\"\ +stage=\"([a-z0-9\.\-]*)\">([^\<]*)\<')
allwords=re.compile(r'\<span class\=\"w\"\ +stage=\"[a-z0-9\.\-]*\">([^\<]*)<')
allpuncts=re.compile(r'\<span class\=\"c\">([^\<]*)\</span\>')
alltags=re.compile(r'\<span class\=\"t\">([^\<]*)\</span\>')

lemmasearch=re.compile(r'\<span class\=\"lemma\"\>([^\<]*)\<')
psambsearch=re.compile(r'<span class="lemma">[^\<]+<sub class="ps">([^\<]+/[^\<]+)<')
# unknownsearch=re.compile(ur'<span class="lemma"(?: style="background-color:red;")*>([^<\n]+)\n*</span>')
unknownsearch=re.compile(r'<span class="lemma">([^<\n]+)\n*</span>')
# unparsedsearch=re.compile(ur'>((?P<mot>[^<]+))<span class="lemma" style="background-color:yellow;">(?P=mot)<span class="lemma var">(?P=mot)<')
# unparsedsearch=re.compile(ur'>([^<]+)<span class="lemma"(?: style="background-color:yellow;)*">[^<]+<span class="lemma var">[^<]+<')
unparsedsearch=re.compile(r'>([^<]+)<span class="lemma">[^<]+<span class="lemma var">[^<]+<')
lemmavarsearch=re.compile(r'\<span class\=\"lemma var\"\>([^\<]*)\<')
punctsearch=re.compile(r'\<span class\=\"c\">([^\<]*)\<')
assimsearch=re.compile(r'\'$')
assimilation=0
glosssearch=re.compile(r'\<sub class\=\"gloss\"\>([^\<]*)\<')
ambiguous=re.compile(r'\<span class\=\"w\".*lemma var.*\<\/span\>\n')
#textscript=re.compile(ur'\<meta content\=\"([^\"]*)\" name\=\"text\:script\" \/\>|\<meta name\=\"text\:script\" content\=\"([^\"]*)\" \/\>',re.U)
textscript=re.compile(r'(?:\<meta content\=\"|\<meta name\=\"text\:script\" content\=\")([^\"]*)(?:\" name\=\"text\:script\" \/\>|\" \/\>)',re.U) # as of daba 0.9.0 dec 2020 meta format order changed!

nmmcquestion=0

nargv=len(sys.argv)
if nargv==1 : 
  print("repl.py needs -at least- one argument : file name")
  sys.exit
if nargv>1 : filename= str(sys.argv[1])

if ".dis.fra" in filename:
  #sys.exit("repl.py does not handle .dis.fra files")
  print("WARNING repl.py does not know how to handle .dis.fra files - results unclear")
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

#fileIN = open(filenamein, "rb")
fileIN = open(filenamein, "r")
#fileOUT = open (filenameout,"wb")
fileOUT = open (filenameout,"w")
tonal=""

arg=""
arg3=""

if nargv>2 : 
  arg= str(sys.argv[2])      # expected tonal ou bailleul
  # print "arg="+arg

if nargv>3:
  arg3= str(sys.argv[3])

try:
  fileREP = open ("REPL.txt","r")  # was rb
  print("using REPL.txt")
except : 
  try:
    fileREP = open ("REPL-STANDARD.txt","r")  # was rb
    print("using REPL-STANDARD.txt")
  except:
    try:
      fileREP = open(os.path.join(scriptdir, "REPL-STANDARD.txt"), "r")
      print("using {}".format(os.path.join(scriptdir, "REPL-STANDARD.txt")))
    except :
      sys.exit("repl.py needs a REPL.txt file or a REPL-STANDARD.txt file in the current directory (or in REPL)")

logfilename=filenametemp+"-replacements.log"
log =  open (logfilename,"w")

toutrepl=fileREP.read()
nlignereplall=toutrepl.count('\n')
nlignereplact=re.findall(r"\n[^\#\s\n]",toutrepl,re.U|re.MULTILINE)
nlignerepl=len(nlignereplact)
print(nlignereplall," lignes   ", nlignerepl," règles")

nligne=1
nbreplok=0
nbmodif=0
nbmots=0
nbrulesapplied=0
nb_unknown=0
nb_unparsed=0
unparsedwords=[]

newline="@"
tout=""
sub0=""
lineOUT=""
tout=fileIN.read()
#py3  tout=tout.decode("utf-8")
"""
line = fileIN.readline()
while line:
  tout=tout+line.decode("utf-8")
  nligne=nligne+1
  line = fileIN.readline()
"""
nligne=tout.count("\n")

# script=textscript.search(tout).group(1)
txtsc=textscript.search(tout)
if txtsc!=None :   # supposedly = if txtsc :
  script=txtsc.group(1)
else :
    script="Nouvel orthographe malien"
    if filenametemp.endswith(".old"): script="Ancien orthographe malien"
    print(" ! textscript not set for "+filenametemp+" !!!  ASSUMED : "+script)

if script=="Ancien orthographe malien" : tonal="old"
elif script=="Nouvel orthographe malien" : tonal="new"
# elif script=="bailleul" : tonal="bailleul" # <---------- n'existe pas en réalité, vérifier arg !!!

if  filenametemp.startswith("baabu_ni_baabu") or filenametemp.startswith("gorog_meyer-contes_bambara1974") :
  tonal="newny"


print("text:script="+script+    ",    tonal="+tonal)

if arg=="tonal" : tonal="tonal"
elif arg=="bailleul" : tonal="bailleul"

if tonal=="" : sys.exit("text:script non defini : pas de meta ou pas d'argument (tonal, bailleul)")

totalmots = tout.count("class=\"w\"")   # is needed in the final message to compute average ambiguous left and elapse time/word
    
print(tout.count("class=\"annot\""), " phrases")
print(totalmots, " mots")

ambs = ambiguous.findall(tout)
nbambs = len(ambs)
print("situation initiale / initial state :")
print(nbambs, " mots ambigüs restants / ambigous words remaining : ", 100*nbambs/totalmots, "%")
psambs = psambsearch.findall(tout)
nbpsambs = len(psambs)
psambslist = ""
if nbpsambs > 0:
  for psamb in psambs:
    if psamb not in psambslist: psambslist=psambslist+psamb+" "
  print(nbpsambs, " ps ambigües / ambiguous ps ( "+psambslist+")", 100*nbpsambs/totalmots, "%")

unknownwords=unknownsearch.findall(tout)
nb_unknown=len(unknownwords)
if nb_unknown >0 :
  unknownwordslist=""
  for unknownw in unknownwords:
    if unknownw+" " not in unknownwordslist: unknownwordslist=unknownwordslist+unknownw+" "
  print(" ",nb_unknown, " mots inconnus / unknown words   ( "+unknownwordslist+")")
  
unparsedwords=unparsedsearch.findall(tout)
nb_unparsed=len(unparsedwords)
if nb_unparsed >0 :
  unparsedwordslist=""
  for unparsedw in unparsedwords:
    if unparsedw+" " not in unparsedwordslist: unparsedwordslist=unparsedwordslist+unparsedw+" "
  print(" ",nb_unparsed, " mots mal parsés / words with failed parse attempt   ( "+unparsedwordslist+")")

# à créer : VQORADJ- concerne 20 vq (var comprises)


psvalides="|adj|adv|adv.p|conj|conv.n|cop|dtm|intj|mrph|n|n.prop|num|onomat|pers|pm|pp|prep|prn|prt|ptcp|v|vq|"
valides="_COMMA_DOT_QUESTION_COLON_SEMICOLON_EXCLAM_PUNCT_NAME_NPROPRE_NPROPRENOM_NPROPRENOMM_NPROPRENOMF_NPROPRENOMMF_NPROPRENOMCL_NPROPRETOP_PERS_PRONOM_VERBE_VPERF_VNONPERF_VERBENMOD_VQ_DTM_PARTICIPE_PRMRK_COPULE_ADJECTIF_POSTP_NUM_NUMANNEE_ADV_ADVP_CONJ_PREP_AMBIGUOUS_DEGRE_DEBUT_BREAK_ADVN_VN_PRT_LAQUO_RAQUO_PARO_PARF_APOSTROPHE_GUILLEMET_PRMRKQUAL_VQADJ_VQORADJ_CONJPREP_COMMENT_TAG_FIN_CONJPOSS_PPPOSS_PRNDTM_TIRET_ADJN_DOONIN_PERCENT_NORV_NORADJ_AORN_DORP_ADJORD_PMORCOP_DTMORADV_INTJ_IPFVAFF_IPFVNEG_PFVTR_PFVNEG_PMINF_PMSBJV_NICONJ_YEUNDEF_YEPP_NIUNDEF_NAUNDEF_NONVERBALGROUP_NUMORD_MONTH_COPEQU_COPQUOT_COPNEG_ACTION_CONSONNE_LANA_LETTRE_"
# toujours commencer et finir par _
# autres mots utilisés, traitements spéciaux : NUMnan, degremove, ADVNforcen, ADVNforceadv, CONJPREPforceconj, CONJPREPforceprep
gvalides="NOM.M_NOM.F_NOM.MF_NOM.CL_NOM.ETRG_NOM.FRA_CFA_FUT_QUOT_PP_IN_CNTRL_PROG_PFV.INTR_PL_PL2_AUGM_AG.OCC_PTCP.PRIV_GENT_AG.PRM_LOC_PRIX_MNT1_MNT2_STAT_INSTR_PTCP.RES_NMLZ_NMLZ2_COM_RECP.PRN_ADJ_DIR_ORD_DIM_PRIV_AG.EX_RECP_PTCP.POT_CONV_ST_DEQU_ABSTR_CAUS_SUPER_IN_EN_1SG_1SG.EMPH_2SG_2SG.EMPH_3SG_3SG.EMPH_1PL_1PL.EMPH_2PL_2PL.EMPH_3PL_IPFV_IPFV.AFF_PROG.AFF_INFR_COND.NEG_FOC_PRES_TOP.CNTR_2SG.EMPH_3SG_REFL_DEF_INF_SBJV_OPT2_POSS_QUAL.AFF_PROH_TOP_PFV.NEG_QUAL.NEG_COND.AFF_REL_REL.PL2_CERT_ORD_DEM_RECP_DISTR_COP.NEG_IPFV.NEG_PROG.NEG_INFR.NEG_FUT.NEG_PST_Q_PFV.TR_EQU_IMP_RCNT_ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.USA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_DES_ADR_"
#  ANAPH, ANAPH.PL, ART, OPT, OPT2, PTCP.PROG removed
#  CFA à cause de la glose de dɔrɔmɛ qui finit par franc.CFA !!!
fixevalides="_ETRG_ETRG.FRA_ETRG.USA_ETRG.ENG_ETRG.GER_ETRG.ARB_CHNT_Q_PREV_"
# cf kàmana:n:PREV de kamanagan
# --- liste des auxiliaires dont les gloses sont des mot-clefs en majuscules
pmlist="bɛ́nà:pm:FUT_bɛ́n':pm:FUT_bɛ:pm:IPFV.AFF_b':pm:IPFV.AFF_be:pm:IPFV.AFF_bi:pm:IPFV.AFF_bɛ́kà:pm:PROG.AFF_bɛ́k':pm:PROG.AFF_bɛ́ka:pm:INFR_bága:pm:INFR_bìlen:pm:COND.NEG_kà:pm:INF_k':pm:INF_ka:pm:SBJV_k':pm:SBJV_ka:pm:QUAL.AFF_man:pm:QUAL.NEG_kànâ:pm:PROH_kàn':pm:PROH_ma:pm:PFV.NEG_m':pm:PFV.NEG_mánà:pm:COND.AFF_mán':pm:COND.AFF_máa:pm:COND.AFF_nà:pm:CERT_n':pm:CERT_tɛ:pm:IPFV.NEG_te:pm:IPFV.NEG_ti:pm:IPFV.NEG_t':pm:IPFV.NEG_tɛ́kà:pm:PROG.NEG_tɛ́k':pm:PROG.NEG_tɛ́ka:pm:INFR.NEG_tɛ́k':pm:INFR.NEG_tɛ́nà:pm:FUT.NEG_tɛ́n':pm:FUT.NEG_ye:pm:PFV.TR_y':pm:PFV.TR_yé:pm:IPFV_yé:pm:IMP_y':pm:IMP_yékà:pm:RCNT_màa:pm:DES_mà:pm:DES_m':pm:DES_"
coplist="bɛ́:cop:être_b':cop:être_b':cop:être_yé:cop:être_kó:cop:QUOT_k':cop:QUOT_dòn:cop:ID_dò:cop:ID_tɛ́:cop:COP.NEG_té:cop:COP.NEG_t':cop:COP.NEG_yé:cop:EQU_y':cop:EQU_bé:cop:être_"
prnlist="ɲɔ́gɔn:prn:RECP_ɲwán:prn:RECP_ɲɔ́ɔn:prn:RECP_mîn:prn:REL_mínnu:prn:REL.PL2_nìnnú:prn:DEM.PL_mín:prn:REL_nìn:prn:DEM_"
dtmlist="ìn:dtm:DEF_mîn:dtm:REL_nìn:dtm:DEM_nìn:dtm/prn:DEM_mín:dtm:REL_mínnu:dtm:REL.PL2_nìnnú:dtm:DEM.PL_nìnnú:dtm/prn:DEM.PL_"
perslist="ń:pers:1SG_nê:pers:1SG.EMPH_í:pers:2SG_í:pers:REFL_ê:pers:2SG.EMPH_à:pers:3SG_àlê:pers:3SG.EMPH_án:pers:1PL_ánw:pers:1PL.EMPH_a':pers:2PL_á:pers:2PL_á':pers:2PL_áw:pers:2PL.EMPH_ù:pers:3PL_òlû:pers:ce.PL2_ra:mrph:OPT2_la:mrph:OP2_na:mrph:OPT2_"
pplist="ka:pp:POSS_lá:pp:POSS_bólo:pp:CNTRL_yé:pp:PP_y':pp:PP_lɔ́:pp:IN_nɔ́:pp:IN_rɔ́:pp:IN_mà:pp:ADR_mɔ̀:pp:ADR_"   # c'est tout ??? oui car les autres ont des gloses en minuscules, cf besoin de "check"
conjlist="ô:conj:DISTR_ôo:conj:DISTR_wô:conj:DISTR_"
prtlist="dè:prt:FOC_dùn:prt:TOP.CNTR_dún:prt:TOP.CNTR_kɔ̀ni:prt:TOP.CNTR2_tùn:prt:PST_kùn:prt:PST_wà:prt:Q_"
mrphlist="lá:mrph:CAUS_la:mrph:CAUS_ná:mrph:CAUS_mà:mrph:SUPER_màn:mrph:SUPER_rɔ́:mrph:IN_lu:mrph:PL2_nu:mrph:PL2_ba:mrph:AUGM_baa:mrph:AG.OCC_baga:mrph:AG.OCC_bali:mrph:PTCP.PRIV_ka:mrph:GENT_la:mrph:AG.PRM_na:mrph:AG.PRM_la:mrph:LOC_na:mrph:LOC_la:mrph:PRIX_na:mrph:PRIX_la:mrph:MNT1_na:mrph:MNT1_lata:mrph:MNT2_nata:mrph:MNT2_la:mrph:PROG_na:mrph:PROG_la:mrph:PFV.INTR_na:mrph:PFV.INTR_n':mrph:PFV.INTR_ra:mrph:PFV.INTR_rá:mrph:IN_rɔ́:mrph:IN_w:mrph:PL_"
mrphlist=mrphlist+"lama:mrph:STAT_nama:mrph:STAT_lan:mrph:INSTR_nan:mrph:INSTR_len:mrph:PTCP.RES_nen:mrph:PTCP.RES_li:mrph:NMLZ_ni:mrph:NMLZ_\:mrph:NMLZ2_ma:mrph:COM_ma:mrph:RECP.PRN_man:mrph:ADJ_ntan:mrph:PRIV_"
mrphlist=mrphlist+"ma:mrph:DIR_nan:mrph:ORD_nin:mrph:DIM_bali:mrph:PRIV_nci:mrph:AG.EX_ɲɔgɔn:mrph:RECP_ɲwan:mrph:RECP_ta:mrph:PTCP.POT_tɔ:mrph:CONV_tɔ:mrph:ST_ya:mrph:DEQU_yɛ:mrph:DEQU_ya:mrph:ABSTR_lá:mrph:CAUS_lán:mrph:CAUS_ná:mrph:CAUS_rɔ́:mrph:CAUS_ma:mrph:SUPER_man:mrph:SUPER_sɔ̀:mrph:EN_"
# restent u"ABR_ETRG_ETRG.ARB_ETRG.FRA_ETRG.FUL_NOM.CL_NOM.ETRG_NOM.F_NOM.M_NOM.MF_PREV_TOP_CARDINAL_CHNT_"
lxpsgvalides=pmlist+coplist+prnlist+dtmlist+perslist+pplist+conjlist+prtlist+mrphlist
lxpsg=re.compile(r"[\_\[\s]([^:\[\_0-9]+:[a-z\/\.]+:[A-Z0-9][A-Z0-9\.\'\|]*)[\_\s\]]",re.U)
# !!! lxpsg  ne vérifie que les gloses spéciales en majuscules, par ex. PAS les pp comme lá:pp:à ou les conj comm ní:conj:si
# ajouter une validation spéciale pour ces auxiliaires !!!!! 9/01/2022
# --- liste des auxiliaires dont les gloses sont des mots en français
# -listaux2=u"à_et_si_ce_ce.PL2_"   # <= construire d'après lxpsgvalides2
# -pplist2=u"lá:pp:à_ná:pp:à_bála:pp:sur_bálan:pp:sur_bára:pp:chez_bólokɔrɔ:pp:sous.la.main_"
# -pplist2=pplist2+u"cɛ́:pp:entre_cɛ́fɛ̀:pp:parmi_cɛ́la:pp:parmi_cɛ́mà:pp:parmi_dáfɛ̀:pp:auprès_dála:pp:auprès_"
# -pplist2=pplist2+u"fɛ̀:pp:par_jùfɛ̀:pp:sous_jùkɔ́rɔ:pp:dessous_jùlá:pp:à.l'endroit.de_kàlamà:pp:au.courant.de_"
# -pplist2=pplist2+u"kámà:pp:pour_kàn:pp:sur_kánmà:pp:pour_kánna:pp:sur_kɛ̀rɛfɛ̀:pp:par.côté_kósɔ̀n:pp:à.cause.de_"
# -pplist2=pplist2+u"kɔ́:pp:après_kɔ́fɛ̀:pp:derrière_kɔ́kàn:pp:à.l'extérieur_kɔ́kɔrɔ:pp:en.soutien.de_kɔ́nɔ:pp:dans_"
# -pplist2=pplist2+u""
# -conjlist2=u"ni:conj:et_n':conj:et_ní:conj:si_n':conj:si_"
# -preplist2=u"ni:prep:et_n':prep:et_ní:prep:si_n':prep:si_"
# -prnlist2=u"ò:prn:ce_òlû:prn:ce.PL2_"
# <--- IDEE ABANDONNEE : CES TESTS SONT FAITS LORS DES -CHECKS PERIODIQUES AVEC TOUT BAMADABA

# alternativement : compiler les listes d'après bamadaba ???

replcompile=False
if arg=="-c" or arg3=="-c" : replcompile=True

# PRE : systematic global replaces  #################################################################

# check if file is new format nov 2021
if '</span><span class="w"' in tout or '</span><span class="c"' in tout:
  print("adapting file to new html format")
  tout,nadapt=re.subn(r'\n</span><span class="(w|c|t)"','</span>\n<span class="\g<1>"',tout,0,re.U|re.MULTILINE)
  print(nadapt,"lines adapted")


# normalize single quotes to avoid pop-up messages in gdisamb complaining that k' is not the same as k’
# tilted quote (word) to straight quotes (as in Bamadaba)
tout=re.sub("’","'",tout,0,re.U|re.MULTILINE)

# inconnus : normaliser sinon REPL ne peut rien faire avec ce \n au milieu
wsearch=r'<span class="lemma">([^<\n]+)\n+</span>'
wrepl=r'<span class="lemma">\g<1></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  normalise unknown words " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

"""# Dukure ---------------------------------------------------
# normaliser les Ɲ
wsearch=ur'<span class="w" stage="([^\"]+)">Л([^\<\n]+)<span class="lemma">л([^<\n]+)<'
wrepl=ur'<span class="w" stage="\g<1>">Ɲ\g<2><span class="lemma">ɲ\g<3><'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  DUK normalise Л->Ɲ " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

#  normaliser les ʃ - !!! suppose qu'il n'y en a qu'un par mot !!!
wsearch=ur'<span class="w" stage="([^\"]+)">([^\<\ʃ]*)ʃ([^\<]+)<span class="lemma">([^\<\ʃ]*)ʃ([^\<]+)<'
wrepl=ur'<span class="w" stage="\g<1>">\g<2>sh\g<3><span class="lemma">\g<4>sh\g<5><'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  DUK normalise ʃ->sh " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# on est sensé être en non tonal (attention dans kà c'est le dernier!)
wsearch=ur'<span class="w" stage="([^\"]+)">([^\<\̀]*)\̀([^\<]*)<span class="lemma">([^\<\̀]*)\̀([^\<]*)<'
wrepl=ur'<span class="w" stage="\g<1>">\g<2>\g<3><span class="lemma">\g<4>\g<5><'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  DUK normalise supprimer le premier ton bas " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# ------------------------------ fin Dukure
"""

# propre names with initial CAPITAL letter please !
# >([A-Za-z])([^<]+)<sub class="ps">n.prop
# >\u$1$2<sub class="ps">n.prop
wsearch=r'>([A-Za-z])([^<]+)<sub class="ps">n\.prop'
#FAILS wrepl=ur'>\u\g<1>\g<2><sub class="ps">n.prop'
#FAILS wrepl=ur'>\U1\g<2><sub class="ps">n.prop'
def npropucase(m):
  first=m.groups()[0].upper()
  second=m.groups()[1]
  return '>'+first+second+'<sub class="ps">n.prop'

tout,nombre=re.subn(wsearch,npropucase,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs n.prop with initial Capital character" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# idem pour Ala !!!
wsearch=r'>ála<sub class="ps">n<'
wrepl=r'>Ála<sub class="ps">n<'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # eliminer EMPR ex: ONI::EMPR
if nombre>0 :
  msg="%i modifs ala->Ala " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# non Majuscules non parsés et mis en majuscules!
wsearch=r'>([A-ZƐƆƝŊ])([^<]+)<span class="lemma">[a-zɛɔɲŋ][^<]+</span></span>\n'
wrepl=r'>\g<1>\g<2><span class="lemma">\g<1>\g<2><sub class="ps">n.prop</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs NPropre-npropre -> NPropre-NPropre-n.prop " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# idem pour les emprunts
# <span class="w" stage="6">Marakèsh<span class="lemma">marakɛsh<sub class="gloss">EMPR</sub></span>
wsearch=r'>([A-ZƐƆƝŊ])([^<]+)<span class="lemma">[a-zɛɔɲŋ][^<]+<sub class="gloss">EMPR</sub></span></span>\n'
wrepl=r'>\g<1>\g<2><span class="lemma">\g<1>\g<2><sub class="ps">n.prop</sub><sub class="gloss">EMPR</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs NPropre-npropre-EMPR -> NPropre-NPropre-n.prop-EMPR " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# eliminer EMPR ex: ONI::EMPR
# see last section of bamana.gram
wsearch=r'<span class="w" +stage="[^\"]+">([A-Z\-]+)<span class="lemma">[a-z\-]+<sub class="gloss">EMPR</sub></span></span>\n'
wrepl=r'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # eliminer EMPR ex: ONI::EMPR
if nombre>0 :
  msg="%i modifs EMPR->ABR " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# dots in calculated lemma or lemma var cause artificial ambiguity sometimes 22/12/18 kalayali
# first dot
wsearch=r'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=r'<span class="\g<1>">\g<2>\g<3><'
tout,nombre1=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# second dot
wsearch=r'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=r'<span class="\g<1>">\g<2>\g<3><'
tout,nombre2=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# third dot
wsearch=r'<span class="(lemma|lemma var)">([^\.\<\n]+)\.([^\<\n]+)<'
wrepl=r'<span class="\g<1>">\g<2>\g<3><'
tout,nombre3=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
# more dots ignored
nombre=nombre1+nombre2+nombre3
if nombre>0 :
  msg="%i modifs enlever les points dans les lx " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# autres ABR possibles
# exemple : <span class="w" stage="-1">TPI<span class="lemma">tpi</span></span>\n
wsearch=r'<span class="w" +stage="-1">([A-Z\-0-9]+)<span class="lemma">[a-zA-Z\-0-9]+</span></span>\n'
wrepl=r'<span class="w" stage="repl">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">ABR</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # autres ABR possibles
if nombre>0 :
  msg="%i modifs Majuscules sans gloss->ABR " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

#eliminer gloss vides ex: baarakelen::
# ex :<span class="lemma var">odewudi</span>
# maybe this is a bug in bamana.gram
wsearch=r'<span class="lemma var">([^<]+)</span>'
wrepl=r''
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # gloss vides ex: baarakelen::
if nombre>0 :
  msg="%i modifs Gloss vide en lemma var" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# ex plus difficile pour les pluriels de mots inconnus (et d'autres dérivations communes possibles ?... à surveiller!)
# exemple traité : on ne garde pas le lemma var n/adj/dtm/prn/ptcp/n.prop/num, on garde les autres (si il y a des dérivations possibles)
# <span class="lemma">siyansikalanw<span class="lemma var">siyansikalanw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">siyansikalan<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">siyansikalanw<sub class="ps">n</sub><span class="m">siyansika<sub class="ps">v</sub></span><span class="m">lan<sub class="ps">mrph</sub><sub class="gloss">INSTR</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n

# ne marche pas pour: (est-ce que ça marche avec la correction du 2d n\.prop   ?)
# <span class="w" stage="0">konyèw<span class="lemma">konyɛw<span class="lemma var">konyɛw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">konyɛ<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">koɲɛw<sub class="ps">n</sub><span class="m">kóɲɛ<sub class="ps">n</sub><sub class="gloss">affaire</sub><span class="m">kó<sub class="ps">n</sub><sub class="gloss">affaire</sub></span><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">fois</sub></span></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>
# </span>
# revue de la formule complète le 16/2/18
# retains only if the FIRST lemma var, other multiple lemma vars eliminated (TO BE RESOLVED!)
wsearch=r'<span class="lemma">[^<]+<span class="lemma var">[^<]+<sub class="ps">n/adj/dtm/prn/ptcp/n\.prop/num</sub><span class="m">[^<]+<sub class="ps">n/adj/dtm/prn/ptcp/n\.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">(((?!lemma var).)+)</span>((<span class="lemma var">[^\n]+</span>)*)</span></span>\n'
wrepl=r'<span class="lemma">\g<1></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss vide en lemma et n/adj/dtm/prn/ptcp/n.prop/num
if nombre>0 :
  msg="%i modifs Gloss vide en lemma et n/adj/dtm/prn/ptcp/n.prop/num" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# éliminer les doublons dans les lemma var (pas nécessairement contigüs) NE MARCHE PAS STRUCTURE CASSEE
## wsearch=ur'<span class="lemma var">(?P<stem>[^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub>(?P<stemgloss>[^\n]+)</span>([^\n]*)<span class="lemma var">(?P=stem)<sub class="ps">(?P=stemps)</sub>(?P=stemgloss)</span>'
## wrepl=ur'<span class="lemma var">\g<1><sub class="ps">\g<2></sub>\g<3></span>\g<4>'
# éliminer les doublons dans les lemma var (nécessairement contigüs)
wsearch=r'<span class="lemma var">(?P<stem>[^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub>(?P<stemgloss>[^\n]+)</span><span class="lemma var">(?P=stem)<sub class="ps">(?P=stemps)</sub>(?P=stemgloss)</span>'
wrepl=r'<span class="lemma var">\g<1><sub class="ps">\g<2></sub>\g<3></span>'

tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma var/lemma var
if nombre>0 :
  msg="%i modifs Gloss doubles lemma var/lemma var" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# Éliminer les doublons lemma / lemma var qui suit (même mot dans 2 dicos, 2 dérivations similaires appliquées…)
# ex : <span class="w" stage="0">kɔnseyew<span class="lemma">kɔnseyew<sub class="ps">n</sub><span class="m">kɔnseye<sub class="ps">n</sub><sub class="gloss">conseiller</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span><span class="lemma var">kɔnseyew<sub class="ps">n</sub><span class="m">kɔnseye<sub class="ps">n</sub><sub class="gloss">conseiller</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span></span>\n
# contrex : <span class="w" stage="0">pikiri<span class="lemma">pikiri<sub class="ps">n</sub><sub class="gloss">piqûre</sub><span class="lemma var">pikiri<sub class="ps">n</sub><sub class="gloss">piqûre</sub></span></span></span>\n
# nb piqûre et piqûre sont deux écritures différentes!!
# wsearch=ur'<span class="lemma">(?P<stem>[^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub>(?P<stemgloss>.+)<span class="lemma var">(?P=stem)<sub class="ps">(?P=stemps)</sub>(?P=stemgloss)</span></span></span>\n'
# NB le lemma var n'est pas nécessairement identique au lemma, en particulier par ex. lemma=ɲìninkali lamma var=ɲininkali (pas de ton dans la glose calculée automatiquement par gparser)
wsearch=r'<span class="lemma">([^<]+)<sub class="ps">(?P<stemps>[^<]+)</sub><sub class="gloss">([^<]+)</sub>(?P<stemm>.+)<span class="lemma var">[^<]+<sub class="ps">(?P=stemps)</sub>(?P=stemm)</span></span></span>\n'
wrepl=r'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<3></sub>\g<4></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  msg="%i modifs Gloss doubles lemma/lemma var  - mais lemma var pas = lemma" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


""" VOIR PLUS BAS # éliminer les gloses bizarres des ordinaux : <span class="lemma">39nan<span class="lemma var">39nan<
wsearch=ur'<span class="lemma">(?P<stem>[0-9]+)nan<span class="lemma var">(?P=stem)nan<sub class="ps">adj</sub><span class="m">(?P=stem)<sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span></span>\n'
wrepl=ur'<span class="lemma">\g<1>nan<sub class="ps">adj</sub><span class="m">\g<1><sub class="ps">num</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  msg="%i modifs ordinaux type 39nan avec lemma var" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
"""

# remettre dans l'ordre n/v les doublons dictionnaire v/n pour les détections NORV
# CAS SIMPLE
#wsearch=ur'<span class="w" stage="([^>]+)">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><sub class="gloss">([^<]+)</sub><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span></span>\n'
#                                                                           1        2                                                  3                                                                      4                                                                       5                                                                6                                                                                              


# CAS COMPLEXE avec sub m
#   <span class="w" stage="0">ɲɛfɔ<span class="lemma">ɲɛ́fɔ<sub class="ps">v</sub><sub class="gloss">expliquer</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span><span class="lemma var">ɲɛ́fɔ<sub class="ps">n</sub><sub class="gloss">explication</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span></span></span>
#   </span>
#4 = <sub class="gloss">expliquer</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span>
#6 = <sub class="gloss">explication</sub><span class="m">ɲɛ́<sub class="ps">n</sub><sub class="gloss">oeil</sub></span><span class="m">fɔ́<sub class="ps">v</sub><sub class="gloss">dire</sub></span>
wsearch=r'<span class="w" +stage="([^>]+)">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span></span>\n'
#                                                                           1        2                                                  3                                                                      4                                                                       5                                                                6                                                                                              
wrepl=r'<span class="w" stage="\g<1>">\g<2><span class="lemma">\g<6><sub class="ps">n</sub><\g<7>><span class="lemma var">\g<3><sub class="ps">v</sub><\g<4>></span></span></span>\n'
# attention décalage $5 $6 -> $6 $7 à cause de la formule (((?!lemma var).)*)
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  msg="%i modifs doublons v/n -> n/v pour NORV" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# éliminer les doublons où le second choix, calculé, n'a pas de glose
# test SublimeText (?P<stem> impossible):
# <span class="lemma">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">([^<]+)</sub><(((?!lemma var).)*)></span></span></span>\n
# trop rare : wsearch=ur'<span class="lemma">(?P<lemma>[^<]+)<sub class="ps">(?P<ps>[^<]+)</sub><sub class="gloss">([^<]+)</sub><(?P<details>((?!lemma var).)*)><span class="lemma var">(?P=lemma)<sub class="ps">(?P=ps)</sub><(?P=details)></span></span></span>\n'
# dans wulikajɔ / wuli-ka-jɔ   va éliminer le second. non ne marche pas, a aussi une glose
# wsearch=ur'<span class="lemma">([^<]+)<sub class="ps">(?P<ps>[^<]+)</sub><sub class="gloss">([^<]+)</sub><(?P<details>((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">(?P=ps)</sub><(?P=details)></span></span></span>\n'
wsearch=r'<span class="lemma">([^<]+)<sub class="ps">(?P<ps>[^<]+)</sub><sub class="gloss">(?P<gloss>[^<]+)</sub><(?P<details>((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">(?P=ps)</sub><sub class="gloss">(?P=gloss)</sub><(?P=details)></span></span></span>\n'
wrepl=r'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<3></sub><\g<4>></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # Gloss doubles lemma/lemma var
if nombre>0 :
  msg="%i modifs doublons entrée lexicale identiques" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

#
# déterminer les noms propres, même vaguement!
#
# mot non initial commençant par une majuscule
# et ambigu :
# remarque : ça pose problème pour Waraba, Suruku, Sonsannin... pour l'instant fixés dans REPL-STANDARD

# <span class="w" stage="0">Kati<span class="lemma">Kati<sub class="ps">n.prop</sub><sub class="gloss">TOP</sub><span class="lemma var">káti<sub class="ps">n</sub><sub class="gloss">caractère</sub></span><span class="lemma var">káti<sub class="ps">adv</sub><sub class="gloss">très.fort</sub></span></span></span>\n
#wsearch=ur'</span><span class="w" stage="[0-9\-]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">(?P=w)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub>((<span class="lemma var">[^<]+<sub class="ps">[^<\.]+</sub><sub class="gloss">[^<]+</sub></span>)+)</span></span>\n'
#wsearch=ur'</span><span class="w" stage="[0-9\-]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">(?P=w)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub><.*lemma var.*></span></span>\n'
#wrepl=ur'</span><span class="w" stage="0">\g<1><span class="lemma">\g<1><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span></span>\n'
#wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub><.*lemma var.*></span></span>\n'
wsearch=r'(</span>|</span>\n)<span class="w" +stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub><.*"ps">(?!n\.prop).*></span></span>\n'
# the above fails in sublime text editor ? works ok with \< after non capturing group
#wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub><.*"ps">(?:n|v|adj|vq|pers|prn|dtm|conj|prep|prt|adv|adv.p|pp|pm|cop|intj|onomat)<.*></span></span>\n'
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma TOP et lemmavar non n.prop " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=r'(</span>|</span>\n)<span class="w" +stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.CL</sub><.*"ps">(?!n\.prop).*></span></span>\n'
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.CL</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma NOM.CL et lemmavar non n.prop " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=r'(</span>|</span>\n)<span class="w" +stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.M</sub><.*"ps">(?!n\.prop).*></span></span>\n'
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.M</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma NOM.M et lemmavar non n.prop " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=r'(</span>|</span>\n)<span class="w" +stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.F</sub><..*"ps">(?!n\.prop).*></span></span>\n'
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">n.prop</sub><sub class="gloss">NOM.F</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non initial avec lemma NOM.F et lemmavar non n.prop " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# this should not screw valid ones like Eziputikaw
#wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">(.+GENT.+)<span class="lemma var">(?P<lv>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<sub class="ps">n.prop</sub><sub class="gloss">(?P=lv)</sub></span></span>\n'
# but one extra span after ???
# <span class="w" stage="1">Keyilakaw<span class="lemma">keyilakaw<span class="lemma var">keyilakaw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">keyilaka<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">keyilakaw<sub class="ps">n/n.prop</sub><span class="m">keyi<sub class="ps">n/n.prop</sub></span><span class="m">la<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">keyilakaw<sub class="ps">n/n.prop</sub><span class="m">keyila<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span></span>\n
# pars <span class="w" stage="0">Keyilakaw<span class="lemma">keyilakaw<sub class="ps">n/n.prop</sub><span class="m">keyi<sub class="ps">n/n.prop</sub></span><span class="m">la<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span>\n
# exemple span en trop
# <span class="w" stage="0">Horimakaw<span class="lemma">horimakaw<sub class="ps">n/n.prop</sub><span class="m">horima<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span></span>\n
# pars <span class="w" stage="1">Horimakaw<span class="lemma">horimakaw<span class="lemma var">horimakaw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">horimaka<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">horimakaw<sub class="ps">n/n.prop</sub><span class="m">horima<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">horimakaw<sub class="ps">n</sub><span class="m">hori<sub class="ps">n</sub></span><span class="m">ma<sub class="ps">mrph</sub><sub class="gloss">COM</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">horimakaw<sub class="ps">n</sub><span class="m">hori<sub class="ps">n</sub></span><span class="m">ma<sub class="ps">mrph</sub><sub class="gloss">RECP.PRN</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span></span>\n
# another case: repl
# <span class="w" stage="0">Timunakaw<span class="lemma">timunakaw<sub class="ps">n/n.prop</sub><span class="m">timu<sub class="ps">n/n.prop</sub></span><span class="m">na<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span></span>\n
# pars <span class="w" stage="1">Timunakaw<span class="lemma">timunakaw<span class="lemma var">timunakaw<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub><span class="m">timunaka<sub class="ps">n/adj/dtm/prn/ptcp/n.prop/num</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">timunakaw<sub class="ps">n/n.prop</sub><span class="m">timu<sub class="ps">n/n.prop</sub></span><span class="m">na<sub class="ps">mrph</sub><sub class="gloss">LOC</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span><span class="lemma var">timunakaw<sub class="ps">n/n.prop</sub><span class="m">timuna<sub class="ps">n/n.prop</sub></span><span class="m">ka<sub class="ps">mrph</sub><sub class="gloss">GENT</sub></span><span class="m">w<sub class="ps">mrph</sub><sub class="gloss">PL</sub></span></span></span></span>\n
#
wsearch=r'(</span>|</span>\n)<span class="w" +stage="[0-9\-]+">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class="lemma">((((?!lemma var).)+)GENT(((?!lemma var).)+))<span class="lemma var">[^\n]+</span></span>\n'
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs NOMPROPRE non-initial ambigu type -kaw GENT (lemma sans ps/gloss) " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# <span class="w" stage="-1">Pekosi<span class="lemma">pekosi<span class="lemma var">Pekosi<sub class="ps">n.prop</sub><sub class="gloss">Pekosi</sub></span></span></span>\n
wsearch=r'(</span>|</span>\n)<span class="w" +stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">[^<]+<span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span></span>\n'
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<2><sub class="ps">n.prop</sub><sub class="gloss">NOM</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres NOMPROPRE non-initial ambigus " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# <span class="w" stage="0">Ɛntɛrinɛti<span class="lemma">ɛntɛrinɛti<sub class="ps">n</sub><sub class="gloss">Internet</sub><span class="lemma var">Ɛntɛrinɛti<sub class="ps">n.prop</sub><sub class="gloss">Ɛntɛrinɛti</sub></span></span>
#  wsearch=ur'(</span>|</span>\n)<span class="w" stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub><span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span></span>\n'
#  wrepl=ur'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3><sub class="ps">\g<4></sub><sub class="gloss">\g<5></sub></span></span>\n'

# essai avec sous-structure : (((?!<span class="lemma var">).)+)
wsearch=r'(</span>|</span>\n)<span class="w" +stage="[0-9\-b]+">(?P<w>[A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.]+)<span class="lemma">(((?!<span class="lemma var">).)+)<span class="lemma var">(?P=w)<sub class="ps">n.prop</sub><sub class="gloss">(?P=w)</sub></span></span></span>\n'
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<3></span></span>\n'

tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs autres , éliminer NOMPROPRE en lemma var ambigus " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# wsearch=ur"(</span>|</span>\n)<span class=\"w\" stage=\"[0-9\-]+\">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<.+lemma var.+></span>\n"
wsearch=r"(</span>|</span>\n)<span class=\"w\" +stage=\"[0-9\-]+\">([A-ZƐƆƝŊ][a-zɛɔɲŋ\-\.́̀̌̂]+)<span class=\"lemma\">[^<]+<span class=\"lemma var\">.+></span>\n"
wrepl=r'\g<1><span class="w" stage="0">\g<2><span class="lemma">\g<2><sub class="ps">n.prop</sub><sub class="gloss">NOM</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
if nombre>0 :
  msg="%i modifs NOMPROPRE non-initial ambigu total (lemma sans ps/gloss) -> NOM " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# handling NUMnan type not handled well in gparser  - CASE   "23nan"
# (bamana.gram rules no longer works)
prefsearch=r'<span class="sent">([^<]*)(?P<stem>[0-9]+)(?P<stemnan>nan|NAN|n)([\s\.\,\;\:\?\!\)\"\&][^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
nextsearch=r'<span class="w" +stage="tokenizer">(?P=stem)<span class="lemma">(?P=stem)<sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span></span>\n<span class="w" +stage="[^\"]">(?P=stemnan)<span class="lemma">(?:nan|ń)<sub class="ps">(?:num|pers)</sub><sub class="gloss">(?:ORD|1SG)</sub></span></span>\n'
prefrepl='<span class="sent">\g<1>\g<2>\g<3>\g<4><span class="annot">\g<5>'
nextrepl='<span class="w" stage="0">\g<2>\g<3><span class="lemma">\g<2>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<2><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span></span>\n'
wsearch=prefsearch+nextsearch
wrepl=prefrepl+nextrepl
#print ("\nNUMnan wsearch:",wsearch)
nombre=1
while nombre>0:
  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
  if nombre>0 :
    msg="%i modifs to handle NUMnan type words like 78nan " % nombre +"\n"
    log.write(msg)
    nbrulesapplied=nbrulesapplied+1
    nbmodif=nbmodif+nombre
    nbmots=nbmots+nombre

# handling NUM nan types not handled well in gparser - CASE   "23 nan" - case where the original text splits 23 & nan
prefsearch=r'<span class="sent">([^<]*)(?P<stem>[0-9]+) (?P<stemnan>nan|NAN)([\s\.\,\;\:\?\!\)\"\&][^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
nextsearch=r'<span class="w" +stage="tokenizer">(?P=stem)<span class="lemma">(?P=stem)<sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span></span>\n<span class="w" stage="2">(?P=stemnan)<span class="lemma">nan<sub class="ps">num</sub><sub class="gloss">ORD</sub></span></span>\n'
prefrepl='<span class="sent">\g<1>\g<2>\g<3>\g<4><span class="annot">\g<5>'
nextrepl='<span class="w" stage="0">\g<2>\g<3><span class="lemma">\g<2>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<2><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span></span>\n'
wsearch=prefsearch+nextsearch
wrepl=prefrepl+nextrepl
# print ("\nNUMnan wsearch:",wsearch)
nombre=1
while nombre>0:
  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
  if nombre>0 :
    msg="%i modifs to handle NUM nan type words like 78 nan " % nombre +"\n"
    log.write(msg)
    nbrulesapplied=nbrulesapplied+1
    nbmodif=nbmodif+nombre
    nbmots=nbmots+nombre


# NOW THE BIG TASK     -go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!---go!--
allwordslist=allwords.findall(tout,re.U|re.MULTILINE)

allwordsshortlist=[]
ndigits=0
for thisword in allwordslist:
  if thisword not in allwordsshortlist: 
    allwordsshortlist.append(thisword)
    if re.match(r"^[0-9]+$",thisword): ndigits=ndigits+1
allwordsshortlist=sorted(allwordsshortlist)
allwordsset=set(allwordsshortlist)

print("nombre de mots uniques:", len(allwordsshortlist))
print("nombre de nombres: ",ndigits)
# print allwordsshortlist
log.write("allwordsshortlist :\n")
for x in allwordsshortlist: log.write(x+"\n")
log.write("--------------- fin de allwordsshortlist :\n")

allpunctslist=allpuncts.findall(tout,re.U|re.MULTILINE)
allpunctsshortlist=[]
for thispunct in allpunctslist:
  if thispunct not in allpunctsshortlist: allpunctsshortlist.append(thispunct)
allpunctdisplay=""
for thispunct in allpunctsshortlist : allpunctdisplay=allpunctdisplay+thispunct+" "
print(len(allpunctsshortlist),"ponctuations uniques:", allpunctdisplay)


alltagslist=alltags.findall(tout,re.U|re.MULTILINE)
ntags=len(alltagslist)
print("nombre de tags: ",ntags)

if arg!="" :print("arg="+arg)
if arg3!="" :print("arg3="+arg)

if replcompile:
  fileREPCname="REPL-STANDARD-C.txt"
  if filenametemp.endswith(".old") : fileREPCname="REPL-STANDARD-C.old.txt"
  if tonal=="newny" : fileREPCname="REPL-STANDARD-C-ny.txt"
  fileREPC = open (fileREPCname,"w")

###### replacement rules as per REPL.txt ######################################################################################################
nblinerepl=0
napplicable=0
  
#py3 toutrepl=toutrepl.decode("utf-8")
toutrepllines=toutrepl.split("\n")
for linerepl in toutrepllines :
  nblinerepl=nblinerepl+1

  log.write("#   "+linerepl+"\n")

  if linerepl[0:1]=="#":
    continue
  if linerepl[0:1]=="\n" or len(linerepl)<=2 :  # le premier test ne marche pas sur mac 
    continue
  if ("===" not in linerepl) and ("=>=" not in linerepl) and (">>=" not in linerepl) and (">==" not in linerepl) and ("=*=" not in linerepl):
      log.write("erreur de === :"+str(nblinerepl)+" : "+linerepl+"\n len="+str(len(linerepl)))
      sys.exit(linerepl+"\nseparator === (or >== ) (or =>= )  (or >>= ) (or =*= ) is missing on line")

  if ((">==" in linerepl) or (">>=" in linerepl)) and ("_" in linerepl) :
      log.write("erreur sep >== ou >>= et plusieurs mots:"+str(nblinerepl)+" : "+linerepl+"\n len="+str(len(linerepl)))
      sys.exit(linerepl+"\nseparator >==  or >>= forbidden if more than one word")

  if "__" in linerepl :
    log.write("erreur de _ _: "+str(nblinerepl)+" : "+linerepl+"\n")
    sys.exit(linerepl+"\nil y a un double _ sur la ligne")

  wsearch=""
  wrepl=""
  wrepl2=""
  sequence=""
    
  if "#" in linerepl :
    linerepl_sp=linerepl.split("#")
    linerepl=linerepl_sp[0].strip()
      
  if "====" in linerepl :
    sys.exit(linerepl+"\n==== au lieu de === ?")

  linerepl=linerepl.strip()   # strips trailing spaces ?
   
  # setting ucase1 - also try capitalising initial word
  # setting topl - also try the plural form in -w
  if "===" in linerepl :
    liste_mots,liste_gloses=linerepl.split("===")
    ucase1=False
    topl=False
    differ=False
  elif ">==" in linerepl :
    liste_mots,liste_gloses=linerepl.split(">==")
    ucase1=False
    topl=True
    differ=False
  elif "=>=" in linerepl :
    liste_mots,liste_gloses=linerepl.split("=>=")
    ucase1=True
    topl=False
    differ=False
  elif ">>=" in linerepl :
    liste_mots,liste_gloses=linerepl.split(">>=")
    ucase1=True
    topl=True
    differ=False
  elif "=*=" in linerepl :
    liste_mots,liste_gloses=linerepl.split("=*=")
    ucase1=False
    topl=False
    differ=True
    
  if tonal=="bailleul" : 
    liste_mots=re.sub("́","",liste_mots)
    liste_mots=re.sub("̂","",liste_mots)
  elif tonal!="tonal" :  
    # ne pas faire pour les mots ETRG.FRA dans les définitions uniques (les tons haut bas et descendants sont utilisés pour simuler les accents français)
    if not (("_" not in liste_mots) and ("ETRG.FRA" in liste_gloses)):
      liste_mots=re.sub("́","",liste_mots)
      #liste_mots=re.sub("̀","̀*",liste_mots)   # DUKure : les tons bas ----- à enlever pour word
      # cette ligne ci-dessus est très dangereuse car fò* peut être à la fois fo "saluer" et fɔ "dire" A REVOIR
      liste_mots=re.sub("̀","",liste_mots)  # cas normal
      liste_mots=re.sub("̌","",liste_mots)
      liste_mots=re.sub("̂","",liste_mots)
  if tonal=="old" : # dans ce cas, les tons sont éliminés mais on revient à l'ancienne écriture
    liste_mots=re.sub("ɛɛ","èe",liste_mots)
    liste_mots=re.sub("ɛ","è",liste_mots)
    liste_mots=re.sub("Ɛ","È",liste_mots)
    liste_mots=re.sub("ɔɔ","òo",liste_mots)
    liste_mots=re.sub("ɔ","ò",liste_mots)
    liste_mots=re.sub("Ɔ","Ò",liste_mots)
    liste_mots=re.sub("ɲ","ny",liste_mots)
    liste_mots=re.sub("Ɲ","Ny",liste_mots)
  elif  tonal=="newny" :  
    liste_mots=re.sub("ɲ",r"ny",liste_mots)
    liste_mots=re.sub("Ɲ",r"Ny",liste_mots)

  liste_mots=re.sub("é","é",liste_mots)   # normaliser les caractères français éventuels (ETRG.FRA intégraux possibles)
  liste_mots=re.sub("è","è",liste_mots)
  liste_mots=re.sub("ë","ë",liste_mots)
  liste_mots=re.sub("à","à",liste_mots)
  liste_mots=re.sub("â","â",liste_mots)
  liste_mots=re.sub("ù","ù",liste_mots)
  liste_mots=re.sub("û","û",liste_mots)
  liste_mots=re.sub("ô","ô",liste_mots)
  liste_mots=re.sub("î","î",liste_mots)
  liste_mots=re.sub("ï","ï",liste_mots)
  liste_mots=re.sub("ç","ç",liste_mots)

    
  #
  # PETITES VALIDATIONS
  #

  if " " in liste_mots:
    log.write("pas d'espace à gauche de === svp !\n")
    sys.exit("\n"+liste_mots+"\nespace à gauche de ===")
    
  semicolumns=re.findall("\:",liste_gloses)
  nbsemic=len(semicolumns)
  if (2*int(nbsemic/2))!=nbsemic :
    log.write("il manque un : dans '"+liste_gloses+"'\n")
    sys.exit("\n"+liste_gloses+"\nerreur de syntaxe ':' dans une glose")   # test sur l'ensemble de la liste des glose, pas sur chaque glose prise individuellement

  openbrackets=re.findall("\[",liste_gloses)
  nbopen=len(openbrackets)
  closebrackets=re.findall("\]",liste_gloses)
  nbclose=len(closebrackets)
  if nbopen!=nbclose :
    log.write("problème de [ et ] mal ouvertes/fermées dans '"+liste_gloses+"'\n")
    sys.exit("\n"+liste_gloses+"\nerreur de syntaxe '[/]' dans une glose")

  spacesemicolumns=re.findall("\s\:",liste_gloses)
  nbspsemic=len(spacesemicolumns)
  if nbspsemic>0 :
    log.write("il y a un espace devant un : dans '"+liste_gloses+"'\n")
    sys.exit("\n"+liste_gloses+"\nerreur de syntaxe ' :' dans une glose") 

  doublelowbar=re.findall("\_\_",liste_gloses)
  nbdoublelowbar=len(doublelowbar)
  if nbdoublelowbar>0 :
    log.write("il y a une répétition de _ dans '"+liste_gloses+"'\n")
    sys.exit("\n"+liste_gloses+"\nerreur de syntaxe ' :' dans une glose") 

  # gloses spéciales
  # noms valides ?
  #                 verif seulement sur liste_mot car liste_gloses peut contenir de nombreuses glose majuscules comme PFV.TR
  m=re.findall(r"(\_[A-Z][A-Z]+\_)","_"+re.sub("\_","__",liste_mots)+"_")   # caution: findall only find non overlapping sequences _TU_YA_SI_ only finds _TU_ and _SI_, but  not _YA_
  #print u"_"+re.sub(u"\_",u"__",liste_mots)+u"_"
  #print m
  if m!=None:
    for gspe in m :
      #print gspe
      if gspe not in valides:
        # vérifier si c'est défini comme un nom propre
        gspe_error=True
        m1=lxpsg.findall("_"+liste_gloses+"_")
        if m1!=None :
          for lxpsgloss in m1 :
            #log.write("- "+lxpsgloss+"\n")
            lxpsgloss_elem=lxpsgloss.split(":")
            lxpsgloss_lx=lxpsgloss_elem[0]
            lxpsgloss_ps=lxpsgloss_elem[1]
            log.write(lxpsgloss_lx+":"+lxpsgloss_ps+"\n")
            if (gspe=="_"+lxpsgloss_lx+"_" and lxpsgloss_ps=="n.prop") :
              gspe_error=False
              log.write(gspe+" : accepte!\n")
              break
        if gspe_error :     
          log.write("(non bloquant) Glose speciale non valide a gauche de === : "+gspe+"\n"+liste_mots+"\n")
          #sys.exit("Glose speciale non valide a gauche de === : "+gspe+"\n"+liste_mots)
  #
  # pour la partie gloses, il faut être plus complet : valider également les gloses Corpus !!!
  #
  m=re.findall(r"(\_[0-9]*[A-Z][A-Z\.]+[0-9]*\_)","_"+re.sub("\_","__",liste_gloses)+"_")
  if m!=None:
    for gspe in m :
      #print gspe
      if gspe not in valides+gvalides:
        log.write("Glose speciale non valide a droite de === : "+gspe+"\n"+liste_mots+"\n")
        sys.exit("\nGlose speciale non valide a droite de === : "+gspe+"\n"+liste_gloses)
  
  # maintenant validons les gloses spéciales en détail
  m=lxpsg.findall("_"+re.sub("\_","__",liste_gloses)+"_")
  if m!=None :
    for lxpsgloss in m :
      #log.write("- "+lxpsgloss+"\n")
      lxpsgloss_elem=lxpsgloss.split(":")
      lxpsgloss_ps=lxpsgloss_elem[1] 
      lxpsgloss_gloss=lxpsgloss_elem[2]
      # ajout de quelques "not in" pour permettre quelques gloses en majuscules a liste non fermée
      # 18 OCT 16 : Pourquoi ne pas sortir les n.prop de ce test ??? ≠===================================
      #if "_"+lxpsgloss_gloss+"_" not in "_ETRG.FRA_TOP_NOM.M_NOM.F_NOM.MF_NOM.CL_NOM.ETRG_" :
      if (lxpsgloss_ps!="n.prop" and lxpsgloss_gloss+"_" not in fixevalides) :
        if  lxpsgloss+"_" not in lxpsgvalides:
          log.write(lxpsgloss_gloss+" : problème avec la glose ?standard? "+lxpsgloss+"\n"+"Valides:"+lxpsgvalides+"\n")
          sys.exit("\n"+liste_gloses+"\n"+lxpsgloss_gloss+" : Glose ?standard? non valide a gauche de === "+lxpsgloss+"\nVoir le log : "+logfilename)

  # nombre de gloses de part et d'autre de ===
  
  elements=valides[1:len(valides)-1].split("_")   # ôter les _ avant et après avant de faire un split
  for element in elements:
    if element in liste_mots+"_"+liste_gloses:
      nbelement=re.findall("_"+element,"_"+liste_mots)
      nbelementg=re.findall("_"+element,"_"+liste_gloses)
      # if element=='TIRET': print "TIRET nbelement=",len(nbelement), " nbelementg=", len(nbelementg)
      if not differ and (len(nbelement)!=len(nbelementg)) and not (len(nbelementg)==0 and element in "_TIRET_"):
        log.write("il n'y a pas le même nombre de '_"+element+"' de part et d'autre de ===\n")
        sys.exit("\n"+liste_mots+"\n"+liste_gloses+"\nErreur de syntaxe! pas le meme nombre de '"+element+"' de part et d'autre de ===\nvoir le log : "+logfilename)

  mots=liste_mots.split("_")
  gloses=liste_gloses.split("_")
  nbmots=len(mots)
  nbgloses=len(gloses)

  if not differ:
    if nbmots!=nbgloses:
      log.write("il n'y a pas le même nombre d'éléments de part et d'autre (ou alors spécifier =*= comme séparateur)\n")
      sys.exit("\n"+liste_mots+"\n"+liste_gloses+"\nErreur de syntaxe! pas le meme nombre d'éléments de part et d'autre (ou alors spécifier =*= comme séparateur)\nvoir le log : "+logfilename)
  
  if differ:
    if nbmots==nbgloses:
      log.write("il y a le même nombre d'éléments de part et d'autre, alors que =*= est spécifié)\n")
      sys.exit("\n"+liste_mots+"\n"+liste_gloses+"\nErreur de syntaxe! il y a le même nombre d'éléments de part et d'autre, alors que =*= est spécifié\nvoir le log : "+logfilename)
  # autres validations à ajouter ici ?
  
  # tests d'applicabilité - si pas applicable, sortir de la boucle de test: break et passer à la règle suivante: continue
  applicable=True
  def testapplic(klist):
    test=False
    for x in klist:
      if x in allwordsshortlist:
        test=True
    return test
  if not replcompile : # dans ce cas, on applique les tests d'applicabilité pour accélérer le traitement
    indexmot=-1
    for mot in mots:
      indexmot=indexmot+1
      if "_"+mot+"_" not in valides :
        if ucase1 and topl:
          if "*" in mot or "(" in mot or "[" in mot:
            lmots=r"("+mot+r"|"+mot+"w"+r"|"+mot[0].upper()+mot[1:]+r"|"+mot[0].upper()+mot[1:]+"w"+r")"
            r=re.compile(r""+lmots)  # mot brut ou mots de la forme bà*na ou (?:b|B)ana
            newlist=list(filter(r.match,allwordsshortlist))
            #if mot not in allwordsshortlist:
            if len(newlist)==0:
              applicable=False
              break
          else:
            if (mot not in allwordsset) and (mot+"w" not in allwordsset) and (mot[0].upper()+mot[1:] not in allwordsset) and (mot[0].upper()+mot[1:]+"w" not in allwordsset):
              applicable=False
              break
        elif ucase1:
          if "*" in mot or "(" in mot or "[" in mot:
            lmots=r"("+mot+r"|"+mot[0].upper()+mot[1:]+r")"
            #print "lmots:",lmots
            r=re.compile(r""+lmots)  # mot brut ou mots de la forme bà*na ou (?:b|B)ana
            newlist=list(filter(r.match,allwordsshortlist))
            #if mot not in allwordsshortlist:
            if len(newlist)==0:
              applicable=False
              break
          else:
            if (mot not in allwordsset) and (mot[0].upper()+mot[1:] not in allwordsset):
              applicable=False
              break    
        elif topl:
          if "*" in mot or "(" in mot or "[" in mot:
            lmots=r"("+mot+r"|"+mot+"w"+r")"
            r=re.compile(r""+lmots)  # mot brut ou mots de la forme bà*na ou (?:b|B)ana
            newlist=list(filter(r.match,allwordsshortlist))
            #if mot not in allwordsshortlist:
            if len(newlist)==0:
              applicable=False
              break
          else:
            if (mot not in allwordsset) and (mot+"w" not in allwordsset):
              applicable=False
              break
            
        else:
          # ajouter ici le code pour les transf Ɲ et verbes Majusc
          # modifs DUKure ---------------
          """"
          if mot[0]=="ɲ" : 
            mot=ur"(?:ɲ|л|Л)"+mot[1:]  # majuscule en cas (no testé) de verbe
            #print "mot: ",mot
          elif mot[0]=="Ɲ" :
            mot=ur"(?:Ɲ|Л)"+mot[1:]
            #print "mot: ",mot
          else:
            if not differ:

              motglose=gloses[indexmot]
              if "§§" in motglose:
                motglose1,motglose2=motglose.split(u"§§")  # sont supposés être des vraies gloses::
                motglose1_elements=motglose1.split(u":")
                motglose2_elements=motglose2.split(u":")
                if motglose1_elements[1]=="v" :
                  #print "§§ mot/glose :",mot,motglose1
                  firstl=mot[0].upper()
                  mot=ur"(?:"+mot[0]+ur"|"+firstl+ur")"+mot[1:]
                  #print "§§ mot verbe:",mot
                elif motglose2_elements[1]=="v" :
                  #print "§§ mot/glose :",mot,motglose2
                  firstl=mot[0].upper()
                  mot=ur"(?:"+mot[0]+ur"|"+firstl+ur")"+mot[1:]
                  #print "§§ mot verbe:",mot
              else:
                if u":" in motglose:
                  motglose_elements=motglose.split(u":")
                else: 
                  print "\n",linerepl
                  sys.exit(mot+" -> erreur: pas de glose pour cet élément?")
                if motglose_elements[1]=="v" :
                  #print "mot/glose :",mot,motglose
                  firstl=mot[0].upper()
                  mot=ur"(?:"+mot[0]+ur"|"+firstl+ur")"+mot[1:]
                  #print "mot verbe:",mot
          #fin modifs DUKure -------------
          """
          # modifs Duk pour les verbes capitalisés
          if not differ:

            motglose=gloses[indexmot]
            if "§§" in motglose:
              motglose1,motglose2=motglose.split("§§")  # sont supposés être des vraies gloses::
              motglose1_elements=motglose1.split(":")
              motglose2_elements=motglose2.split(":")
              if motglose1_elements[1]=="v" :
                #print "§§ mot/glose :",mot,motglose1
                firstl=mot[0].upper()
                if firstl!=mot[0] :
                  mot=r"["+mot[0]+firstl+r"]"+mot[1:]
                #print "§§ mot verbe:",mot
              elif motglose2_elements[1]=="v" :
                #print "§§ mot/glose :",mot,motglose2
                firstl=mot[0].upper()
                if firstl!=mot[0] :
                  mot=r"["+mot[0]+firstl+r"]"+mot[1:]
                #print "§§ mot verbe:",mot
            else:
              if ":" in motglose:
                motglose_elements=motglose.split(":")
              else: 
                print("\n",linerepl)
                sys.exit(mot+" -> erreur: pas de glose pour cet élément?")
              if motglose_elements[1]=="v" :
                #print "mot/glose :",mot,motglose
                firstl=mot[0].upper()
                if firstl!=mot[0] :
                  mot=r"["+mot[0]+firstl+r"]"+mot[1:]
                #print "mot verbe:",mot
        #fin modifs DUKure -------------

          if "*" in mot or "(" in mot or "[" in mot:
            r=re.compile(r""+mot)  # mot brut ou mots de la forme bà*na ou (?:b|B)ana
            newlist=list(filter(r.match,allwordsshortlist))
            if len(newlist)==0:
              applicable=False
              break
          else:
            if mot not in allwordsset:
              applicable=False
              break

      else:
        if mot=="EXCLAM":
          if "!" not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="QUESTION":
          if "?" not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="COMMA":
          if "," not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="COLON":
          if ":" not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="SEMICOLON":
          if ":" not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="DOT":
          if "." not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="LAQUO":
          if "«" not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="RAQUO":
          if "»" not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="PARO":
          if "(" not in allpunctsshortlist:
            applicable=False
            break
        elif mot=="PARF":
          if ")" not in allpunctsshortlist:
            applicable=False
            break

        elif mot=="LANA":
          applicable=testapplic(["la","na","lá","ná"])
          if not applicable: break
        elif mot=="NUM":
          if ndigits==0 and not testapplic(["kelen","fila","fla","saba","naani","duuru","wɔɔrɔ","wolonwula","wolonfila","segin","seegin","kɔnɔntɔn","kélen","fìla","flà","sàba","náani","dúuru","wɔ́ɔrɔ","wólonwula","wólonfila","ségin","séegin","kɔ́nɔntɔn","wòorò","kònòntòn","tan","bi","mugan","dɛbɛ","kɛmɛ","silameyakɛmɛ","tán","bî","mùgan","dɛ̀bɛ","kɛ̀mɛ","sìlameyakɛmɛ"or "dèbè","kèmè","silameyakèmè"]): 
            applicable=False
            break
        elif mot=="PFVTR":
          applicable=testapplic(["ye","y'","yé"])
          if not applicable: break
        elif mot=="PFVNEG":
          applicable=testapplic(["ma","m'","má"])
          if not applicable: break
        elif mot=="IPFVNEG":
          applicable=testapplic(["tɛ","t'","tè","tɛ́","ti"])
          if not applicable: break
        elif mot=="IPFVAFF":
          applicable=testapplic(["bɛ","b'","bè","bɛ́","bi"])
          if not applicable: break
        elif mot=="COPNEG":
          applicable=testapplic(["tɛ","t'","tè","tɛ́","Tɛ","Tɛ́"])
          if not applicable: break
        elif mot=="NICONJ" or mot=="NIUNDEF":
          applicable=testapplic(["ni","n'","ní"])
          if not applicable: break
        elif mot=="TAG":
          if ntags==0 :
            applicable=False
            break

  if not applicable: 
    log.write("NON APPLICABLE : "+liste_mots+" -> mot absent : "+mot+"\n")

    continue  # skips the rest of the bigger loop of REPL rules
  # si on arrive là c'est que c'est applicable
  napplicable=napplicable+1

  indexmot=-1
  
  for mot in mots :
    indexmot=indexmot+1
    if mot=="COMMA"      : wsearch=wsearch+r'<span class="c">,</span>\n'
    elif mot=="DOT"      : wsearch=wsearch+r'<span class="c">\.</span>\n'
    elif mot=="QUESTION" : wsearch=wsearch+r'<span class="c">\?</span>\n'
    elif mot=="COLON"    : wsearch=wsearch+r'<span class="c">\:</span>\n'
    elif mot=="SEMICOLON": wsearch=wsearch+r'<span class="c">\;</span>\n'
    elif mot=="EXCLAM"   : wsearch=wsearch+r'<span class="c">\!</span>\n'
    elif mot=="TIRET"    : wsearch=wsearch+r'<span class="c">\-</span>\n'
    #elif mot==u"PUNCT"    : wsearch=wsearch+ur'<span class="c">([^<]+)</span>\n' 
    # nb: le point, et autres séparateurs de sentence, n'a normalement pas d'effet ici ! cf DEBUT
    elif mot=="COMMENT"  : wsearch=wsearch+r'<span class="comment">([^<]+)</span>\n' 
    elif mot=="TAG"      : wsearch=wsearch+r'<span class="t">([^<]+)</span>\n' 
    # attention <st> n'est pas un tag !!! <span class="c">&lt;st&gt;</span>
    elif mot=="PUNCT"    : wsearch=wsearch+r'<span class="([ct])">([^<]+)</span>\n' 
    elif mot=="DEGRE"    : wsearch=wsearch+r'<span class="c">\°</span>\n'
    elif mot=="degremove": wsearch=wsearch+r'<span class="c">\°</span>\n'
    # le même mais pas de vérif quil existe de l'autre côté de === : on veut l'éliminer!
    # en minuscules pour échapper aux tests sur les mot-clefs "valides"
    elif mot=="LAQUO"    : wsearch=wsearch+r'<span class="c">\«</span>\n'
    elif mot=="RAQUO"    : wsearch=wsearch+r'<span class="c">\»</span>\n'
    elif mot=="PARO"    : wsearch=wsearch+r'<span class="c">\(</span>\n'
    elif mot=="PARF"    : wsearch=wsearch+r'<span class="c">\)</span>\n'
    elif mot=="GUILLEMET"    : wsearch=wsearch+r'<span class="c">\"</span>\n'
    elif mot=="APOSTROPHE"    : wsearch=wsearch+r'''<span class="c">(?:\'|\‘)</span>\n'''
    elif mot=="PERCENT"  : wsearch=wsearch+r'<span class="c">\%</span>\n'
    elif mot=="DEBUT"    : wsearch=wsearch+r'<span class="annot">'
    elif mot=="FIN"      : wsearch=wsearch+r'</span>\n</span>\n'
    elif mot=="BREAK"    : wsearch=wsearch+r'<span class="t">\&lt\;br\/\&gt\;</span>\n'  # t = tag 
    elif mot=="LETTRE"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([a-zA-ZɛɔɲŋƐƆƝŊ])<[^\n]+</span>\n'  # pour mettrre cette lettre en tag
    
    # cette formule marche pour les composés, excluants ceux qui sont ambigus, à essayer !
    # <span class="w" stage="0">[^<]*<span class="lemma">[^<]*<sub class="ps">n</sub><(((?!lemma var).)*)></span>\n
    # et aussi, moins de groupes !
    # <span class="w" stage="0">[^<]*<span class="lemma">[^<]*<sub class="ps">n</sub><((?!lemma var).*)></span>\n
    # mais pas fiable dans python re ?
    # pour mémoire, formule précédente (uniquement non composés):
    # <span class="w" stage="0">([^<]*)<span class="lemma">([^<]*)<sub class="ps">n</sub><sub class="gloss">([^<]*)</sub></span></span>\n
    # finalement une formule qui marche :...
    elif mot=="NAME"     : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="ACTION"     : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)><sub class="gloss">NMLZ</sub></span></span></span>\n'
    elif mot=="PERS"     : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pers</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="PRONOM"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">prn</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="PRT"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">prt</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="INTJ"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">intj</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="VERBE"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="VPERF"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)PFV\.INTR(((?!lemma var).)*)></span>\n'
    elif mot=="VNONPERF"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var|PFV\.INTR).)*)></span>\n'
    elif mot=="VERBENMOD"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">(((?!na|nana|nà|nàna|taa|taga|taara|tagara|táa|tága|táara|tágara).)*)<span class="lemma">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)></span>\n'   # verbe non modal: pas taa ni na
    # CAVEAT : this expression will not match if verb starts with na e.g. naminɛ !!!!!!!!!!!!!!!!!!!!!! Negating exact match impossible in REGEXP???
    elif mot=="ADJORD"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)<sub class="gloss">ORD</sub>(((?!lemma var).)*)></span>\n'
    elif mot=="VQ"       : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">vq</sub><(((?!lemma var).)*)></span>\n'
    #elif mot==u"VQADJ"    : wsearch=wsearch+ur'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">vq/adj</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="DTM"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">dtm</sub><(((?!lemma var).)*)></span>\n'
    #elif mot==u"PRNDTM"   : wsearch=wsearch+ur'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prn/dtm|dtm/prn)</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="POSTP"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pp</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="PRMRK"       : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pm</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="PRMRKQUAL"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pm</sub><sub class="gloss">(QUAL.AFF|QUAL.NEG)</sub></span></span>\n'
    elif mot=="COPULE"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">cop</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="ADJECTIF" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)></span>\n'
    #elif mot==u"ADJN"     : wsearch=wsearch+ur'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(adj/n|n/adj)</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="PARTICIPE": wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">ptcp</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="NUM"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">num</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="NUMORD"    : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)ORDINAL(((?!lemma var).)*)></span>\n'
    elif mot=="NUMANNEE"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([1-2][0-9][0-9][0-9])<span class="lemma">([1-2][0-9][0-9][0-9])<sub class="ps">num</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="ADV"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="ADVP"      : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv\.p</sub><(((?!lemma var).)*)></span>\n'
    #elif mot==u"ADVN"     : wsearch=wsearch+ur'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adv/n</sub><(((?!lemma var).)*)></span>\n'
    #elif mot==u"VN"     : wsearch=wsearch+ur'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(?:v/n|n/v)</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="CONJ"     : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(conj|prep/conj|conj/prep)</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="PREP"     : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prep|prep/conj|conj/prep)</sub><(((?!lemma var).)*)></span>\n'
    #elif mot==u"CONJPREP" : wsearch=wsearch+ur'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">(prep/conj|conj/prep)</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="CONJPOSS" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">conj</sub><sub class="gloss">POSS</sub></span></span>\n'
    elif mot=="PPPOSS" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'
    elif mot=="COPEQU" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">cop</sub><sub class="gloss">EQU</sub></span></span>\n'
    elif mot=="COPQUOT" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">cop</sub><sub class="gloss">QUOT</sub></span></span>\n'
    elif mot=="NPROPRE"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="NPROPRENOM"  : 
      lastnproprenom=r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM</sub></span></span>\n'
      wsearch=wsearch+lastnproprenom
    elif mot=="NPROPRENOMM"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.M</sub></span></span>\n'
    elif mot=="NPROPRENOMF"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.F</sub></span></span>\n'
    elif mot=="NPROPRENOMMF"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.MF</sub></span></span>\n'
    elif mot=="NPROPRENOMCL"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">NOM\.CL</sub></span></span>\n'
    elif mot=="NPROPRETOP"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n\.prop</sub><sub class="gloss">TOP</sub>(((?!lemma var).)*)</span></span>\n'
    elif mot=="DOONIN"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">dɔ́ɔnin<sub class="ps">adj/n</sub><(((?!lemma var).)*)></span>\n'
    elif mot=="NORV"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">v</sub><(((?!lemma var).)*)></span></span></span>\n'
    elif mot=="NORADJ"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)></span></span></span>\n'
    elif mot=="VQORADJ"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">vq</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)></span></span></span>\n'
    elif mot=="PMORCOP"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">pm</sub><sub class="gloss">([^<]+)</sub><span class="lemma var">([^<]+)<sub class="ps">cop</sub><sub class="gloss">([^<]+)</sub></span></span></span>\n'
    elif mot=="AORN"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">adj</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">n</sub><(((?!lemma var).)*)></span></span></span>\n'
    elif mot=="DORP"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">dtm</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">prn</sub><(((?!lemma var).)*)></span></span></span>\n'
    elif mot=="DTMORADV"   : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">([^<]+)<sub class="ps">dtm</sub><(((?!lemma var).)*)><span class="lemma var">([^<]+)<sub class="ps">adv</sub><(((?!lemma var).)*)></span></span></span>\n'
    # to be implemented : GNMEMBER
    # <span class="lemma">([^<]+)<sub class="ps">(n|n.prop|pers|prn|dtm|adj|ptcp|prt)</sub><sub class="gloss">([^<]+)</sub>|<span class="lemma">([^<]+)<sub class="ps">(conj|prep\/conj|pp)</sub><sub class="gloss">(POSS|et|ainsi\.que)</sub>
    # add around this class="w" and not lemma var
    # arg impact on capt_gr_index  (TEST THOROUGHLY!!!)

    # PM and COPs - ajouter bi à IPFVAFF ??? ATTENTION bi : peut être bî dizaine! - enlevé le 14/12/19
    elif mot=="IPFVAFF"     : 
      if tonal=="new" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(bɛ|be|b')<span class="lemma">[^\n]+</span></span>\n'''
      elif tonal=="newny" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(bɛ|be|b')<span class="lemma">[^\n]+</span></span>\n'''
      elif tonal=="old" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(bè|be|b')<span class="lemma">[^\n]+</span></span>\n'''
      elif tonal=="tonal" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(bɛ|bɛ́|be|b')<span class="lemma">[^\n]+</span></span>\n'''  
    elif mot=="IPFVNEG"     : 
      if tonal=="new" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(tɛ|te|ti|t')<span class="lemma">[^\n]+</span></span>\n'''
      elif tonal=="newny" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(tɛ|te|ti|t')<span class="lemma">[^\n]+</span></span>\n'''
      elif tonal=="old" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(tè|te|ti|t')<span class="lemma">[^\n]+</span></span>\n'''
      elif tonal=="tonal" : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(tɛ|tɛ́|te|ti|t')<span class="lemma">[^\n]+</span></span>\n'''
    elif mot=="COPNEG"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(tɛ|tɛ́|t'|Tɛ|T')<span class="lemma">[^\n]+</span></span>\n'''
    elif mot=="PFVTR"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(ye|y')<span class="lemma">[^\n]+</span></span>\n'''
    elif mot=="PFVNEG"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(ma|m')<span class="lemma">[^\n]+</span></span>\n'''
    elif mot=="PMINF"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(ka|k'|Ka|K'|kà|Kà)<span class="lemma">[^\n]+</span></span>\n'''
    elif mot=="PMSBJV"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(ka|k'|ká)<span class="lemma">[^\n]+</span></span>\n'''
    elif mot=="NICONJ"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(ni|n'|ní)<span class="lemma">[^\n]+</span></span>\n'''
    elif mot=="LANA"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(l|n)(a|á)<[^\n]+</span>\n'''

    elif mot=="CONSONNE"     : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">([^AEIOUƐƆaeiouɛɔ][^\n\<]*)<span class="lemma">([^\n]+)</span></span>\n'''
    
    elif mot=="MONTH" : 
      if tonal=="new" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">(zanwuyekalo|zanwiyekalo|feburuyekalo|feburiyekalo|feburuye-kalo|fewuruyekalo|marisikalo|awirilikalo|mɛkalo|zuwɛnkalo|zuluyekalo|zuliyekalo|utikalo|sɛtanburukalo|sɛtamburukalo|ɔkutɔburukalo|nowanburukalo|nowamburukalo|desanburukalo|desamburukalo)<span class="lemma">([^\n]+)</span></span>\n'
      elif tonal=="newny" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">(zanwuyekalo|zanwiyekalo|feburuyekalo|feburiyekalo|feburuye-kalo|fewuruyekalo|marisikalo|awirilikalo|mɛkalo|zuwɛnkalo|zuluyekalo|zuliyekalo|utikalo|sɛtanburukalo|sɛtamburukalo|ɔkutɔburukalo|nowanburukalo|nowamburukalo|desanburukalo|desamburukalo)<span class="lemma">([^\n]+)</span></span>\n'
      elif tonal=="old" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">(zanwuyekalo|zanwiyekalo|feburuyekalo|feburiyekalo|feburuye-kalo|fewuruyekalo|marisikalo|awirilikalo|mèkalo|zuwènkalo|zuluyekalo|zuliyekalo|utikalo|sètanburukalo|sètamburukalo|òkutɔburukalo|nowanburukalo|nowamburukalo|desanburukalo|desamburukalo)<span class="lemma">([^\n]+)</span></span>\n'
      elif tonal=="tonal" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">(zánwuyekalo|zánwiyekalo|féburuyekalo|féburiyekalo|féburuye-kalo|féwuruyekalo|márisikalo|áwirilikalo|mɛ̀kalo|zùwɛnkalo|zùluyekalo|zùliyekalo|ùtikalo|sɛ́tanburukalo|sɛ́tamburukalo|ɔ́kutɔburukalo|nòwanburukalo|nòwamburukalo|désanburukalo|désamburukalo)<span class="lemma">([^\n]+)</span></span>\n'  
    elif mot=="YEUNDEF"  : wsearch=wsearch+r'''<span class="w" +stage="[^>]+">(yé|ye|y')<[^\n]+lemma var[^\n]+</span></span>\n'''
    elif mot=="YEPP" : wsearch=wsearch+r'<span class="w" +stage="[^>]+">([^<]+)<span class="lemma">yé<sub class="ps">pp</sub><sub class="gloss">PP</sub></span></span>\n'
    elif mot=="NIUNDEF"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">(ní|ni)<[^\n]+lemma var[^\n]+</span></span>\n'
    elif mot=="NAUNDEF"  : wsearch=wsearch+r'<span class="w" +stage="[^>]+">(ná|na)<[^\n]+lemma var[^\n]+</span></span>\n'

    # elif mot==u"NONVERBALGROUP": wsearch=wsearch+ur'((<span class="w" +stage="0">[^<]+<span class="lemma">[^<]+<sub class="ps">(?!v|vq|cop|pm)</sub>(((?!lemma var).)*)</span></span>\n)+)'
    # elif mot==u"NONVERBALGROUP": wsearch=wsearch+ur'((<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">[^<]+<sub class="ps">(?:n|adj|pp|ptcp|n\.prop|num|dtm|prn|pers|conj)</sub>(((?!lemma var).)*)</span></span>\n)+)'
    elif mot=="NONVERBALGROUP": 
      """
      wsearch=wsearch+ur'((<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">[^<]+<sub class="ps">(?:n|adj|ptcp|n\.prop|num|dtm|prn|pers)</sub>(((?!lemma var).)*)</span></span>\n'
      wsearch=wsearch+ur'''|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:ka|k')<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'''
      wsearch=wsearch+ur'''|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:ni|n')<sub class="ps">conj</sub><sub class="gloss">et</sub></span></span>\n'''
      wsearch=wsearch+ur'''|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:àní|àn')<sub class="ps">conj</sub><sub class="gloss">ainsi.que</sub></span></span>\n'''
      wsearch=wsearch+ur'|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:wàlímà)<sub class="ps">conj</sub><sub class="gloss">ou.bien</sub></span></span>\n'
      wsearch=wsearch+ur'|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:ô)<sub class="ps">conj</sub><sub class="gloss">DISTR</sub></span></span>\n'
      wsearch=wsearch+ur'|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:dè)<sub class="ps">prt</sub><sub class="gloss">FOC</sub></span></span>\n'
      wsearch=wsearch+ur'|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:kɔ̀ni)<sub class="ps">prt</sub><sub class="gloss">TOP.CNTR2</sub></span></span>\n'
      wsearch=wsearch+ur'|<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:fána)<sub class="ps">prt</sub><sub class="gloss">aussi</sub></span></span>\n)+)'
      """
      # inconvénient : le NVG peut être réduit à une seule conj isolée ou une seule prt isolée ???!!!
      # chercher à corriger avec une formule du style : N|PRT+ CONJ*
      # essayer GN | GN CONJ | GN PRT | GN PRT CONJ 
      # modif 15/6/2020
      
      NOMINAL=r'<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">[^<]+<sub class="ps">(?:n|adj|ptcp|n\.prop|num|dtm|prn|pers)</sub>(((?!lemma var).)*)</span></span>\n'
      #wsearch=wsearch+ur'(('+NOMINAL  #  <- il faut FINIR par ça
      wsearch=wsearch+r'(('+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:ka|k')<sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:ni|n')<sub class="ps">conj</sub><sub class="gloss">et</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:àní|àn')<sub class="ps">conj</sub><sub class="gloss">ainsi.que</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:wàlímà)<sub class="ps">conj</sub><sub class="gloss">ou.bien</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:ô)<sub class="ps">conj</sub><sub class="gloss">DISTR</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:dè)<sub class="ps">prt</sub><sub class="gloss">FOC</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:kɔ̀ni)<sub class="ps">prt</sub><sub class="gloss">TOP.CNTR2</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="w" +stage="[^\"]+">[^<]+<span class="lemma">(?:fána)<sub class="ps">prt</sub><sub class="gloss">aussi</sub></span></span>\n'''
      wsearch=wsearch+r'|'+NOMINAL+r'''<span class="c">(?:«|»|\"|\'|\‘|\(|\)|\/)</span>\n'''
      wsearch=wsearch+r'|'+NOMINAL
      wsearch=wsearch+r')+)'
      # added 17/11/2020: <span class="c">«</span>
      
      #print "new NOMINAL wsearch:\n",wsearch
      
    elif mot=="AMBIGUOUS": wsearch=wsearch+r'<span class="w"(.*)lemma var(.*)</span>\n'
    else :
      if "'" in mot: mot=re.sub(r"\'","[\'\’]+",mot)   # satanées curly brackets
      """
      motsearch=mot
      if tonal=="new":  # useful for Dumestre script tagged as "new" but not using ɲ (Baabu ni baabu etc.)
        motsearch=re.sub(u"ɲ",ur"(?:ɲ|ny)",mot)
        motsearch=re.sub(u"Ɲ",ur"(?:Ɲ|Ny)",motsearch)
      wsearch=wsearch+ur'<span class="w" +stage="[a-z0-9\.\-]+">'+motsearch+ur'<.*</span></span>\n'
      """
      if wsearch=="" and ucase1 :
        winitial=mot[0:1]
        wrest=mot[1:len(mot)]
        # mot2=ur"(?:"+winitial.upper()+ur"|"+winitial+ur")"+wrest   # non-capturing group
        #mot2=ur"(["+winitial.upper()+winitial+ur"]"+wrest+ur")"    # character class supposedly faster, at least less verbose!
        #print mot, mot2
        #wsearch=wsearch+ur'<span class="w" +stage="[a-z0-9\.\-]+">'+mot2+ur'<.*</span></span>\n'
        mot=r"(["+winitial.upper()+winitial+r"]"+wrest+r")"    # character class supposedly faster, at least less verbose!
        #print mot, mot2
        mot2=mot # pour compatibilité avec le code pour topl+ucase1
        wsearch=wsearch+r'<span class="w" +stage="[a-z0-9\.\-]+">'+mot+r'<.*</span></span>\n'

      else:
        # modifs DUKure ---------------
        """
        if mot[0]=="ɲ" : 
          mot=ur"(?:ɲ|л|Л)"+mot[1:]  # majuscule en cas (no testé) de verbe
          print "mot: ",mot
        elif mot[0]=="Ɲ" :
          mot=ur"(?:Ɲ|Л)"+mot[1:]
          print "mot: ",mot
        else:
          """
        if not differ:

          motglose=gloses[indexmot]
          if "§§" in motglose:
            motglose1,motglose2=motglose.split("§§")  # sont supposés être des vraies gloses::
            motglose1_elements=motglose1.split(":")
            motglose2_elements=motglose2.split(":")
            if motglose1_elements[1]=="v" :
              #print "§§ mot/glose :",mot,motglose1
              firstl=mot[0].upper()
              if firstl!=mot[0]: 
                mot=r"["+mot[0]+firstl+r"]"+mot[1:]
              #print "§§ mot verbe:",mot
            elif motglose2_elements[1]=="v" :
              #print "§§ mot/glose :",mot,motglose2
              firstl=mot[0].upper()
              if firstl!=mot[0]:
                mot=r"["+mot[0]+firstl+r"]"+mot[1:]
              #print "§§ mot verbe:",mot
          else:
            if ":" in motglose:
              motglose_elements=motglose.split(":")
            else: 
              print("\n",linerepl)
              sys.exit("erreur: pas de glose pour cet élément?")
            if motglose_elements[1]=="v" :
              #print "mot/glose :",mot,motglose
              firstl=mot[0].upper()
              if firstl!=mot[0]:
                mot=r"["+mot[0]+firstl+r"]"+mot[1:]
              #print "mot verbe:",mot
        #fin modifs DUKure -------------

        if "*" in mot or "(" in mot or "[" in mot :
          wsearch=wsearch+r'<span class="w" +stage="[a-z0-9\.\-]+">('+mot+r')<.*</span></span>\n' # WORD CAPTURE
        else: 
          wsearch=wsearch+r'<span class="w" +stage="[a-z0-9\.\-]+">'+mot+r'<.*</span></span>\n'

    if sequence=="": sequence=mot
    else : sequence=sequence+" "+mot
  
  
  lmots=len(mots)
  lgloses=len(gloses)
  motscapt=sequence.split(" ")   # assumes mot cannot contain space!

  imots=-1
  capt_gr_index=0   # capturing group index (si on a plusieurs symboles)
  prefsearch=r""

  if lmots==lgloses:
    if "§§" in liste_gloses:
      if topl or ucase1 : sys.exit("\n§§ alternate gloss cannot use > for uppercase-test or force-plural:\n"+linerepl)
  else :
    log.write("!= NB ELEM DIFFERENTS:  ("+str(lmots)+") !=  ("+str(lgloses)+")\n")

    if topl or ucase1 : sys.exit("\n> forbidden for force-plural or uppercase-test : the numbers of elements differ\n"+linerepl)
    # dans ce cas il devrait être possible de modifier aussi la "sentence":
    # <span class="sent">([^<]+ )halibi([ \.][^£]+)<span class="w" stage="3">halibi<span class="lemma">

    # check that gloses does not contain capitalized keyword // CANCELLED - NO THIS IS POSSIBLE
    #                 verif seulement sur liste_mot car liste_gloses peut contenir de nombreuses glose majuscules comme PFV.TR
    #   m=re.findall(ur"(\_[A-Z][A-Z]+\_)",u"_"+re.sub(u"\_",u"__",liste_mots)+u"_")   # caution: findall only find non overlapping sequences _TU_YA_SI_ only finds _TU_ and _SI_, but  not _YA_
    #   if len(m)!=0:
    #     sys.exit("number of elements differ, of which capitalized keywords : "+liste_mots)

    # find target words (new syntax in different number of words)
  
    gloseslx=re.findall(r"([^\:\_]+)\:[^\_]+",liste_gloses)
    liste_gloseslx=" ".join(gloseslx)
    # ensure target words are in the same orthography
    if tonal=="bailleul" : 
          liste_gloseslx=re.sub("́","",liste_gloseslx)
          liste_gloseslx=re.sub("̂","",liste_gloseslx)
    elif tonal!="tonal" :  
          liste_gloseslx=re.sub("́","",liste_gloseslx)
          liste_gloseslx=re.sub("̀","",liste_gloseslx)
          liste_gloseslx=re.sub("̌","",liste_gloseslx)
          liste_gloseslx=re.sub("̂","",liste_gloseslx)
    if tonal=="old" : # dans ce cas, les tons sont éliminés mais on revient à l'ancienne écriture
          liste_gloseslx=re.sub("ɛɛ","èe",liste_gloseslx)
          liste_gloseslx=re.sub("ɛ","è",liste_gloseslx)
          liste_gloseslx=re.sub("Ɛ","È",liste_gloseslx)
          liste_gloseslx=re.sub("ɔɔ","òo",liste_gloseslx)
          liste_gloseslx=re.sub("ɔ","ò",liste_gloseslx)
          liste_gloseslx=re.sub("Ɔ","Ò",liste_gloseslx)
          liste_gloseslx=re.sub("ɲ","ny",liste_gloseslx)
          liste_gloseslx=re.sub("Ɲ","Ny",liste_gloseslx)
    elif tonal=="newny":
          #if oldny :       # cas type Baabu ni baabu
          liste_gloseslx=re.sub("ɲ","ny",liste_gloseslx)
          liste_gloseslx=re.sub("Ɲ","Ny",liste_gloseslx)
      
      # build prefixes for the search and replace expressions 
    liste_mots_spaced=liste_mots.replace("_"," ")
    liste_mots_spaced=re.sub(r"([A-Z]+[\s])*","",liste_mots_spaced)  # eliminated capitalized keywords after/before
    liste_mots_spaced=re.sub(r"([\s][A-Z]+)*","",liste_mots_spaced)  # eliminated capitalized keywords after/before
    # relookahead=ur">"+liste_mots_spaced.replace(" ","<|>")+ur"<"   #  "1 lɔ" → ">1<|>lɔ<"   as found in <span class="lemma">lɔ< ...
    if liste_mots_spaced=="1 lɔ": liste_mots_spaced="1lɔ"  # workaround gparser trick
    prefsearch=r'<span class="sent">([^<]*)'+liste_mots_spaced+'([^<]*)<span class="annot">(((?!"sent")[^¤])*)'    #  ?!"sent": do no span over several sentences / [^¤]: because . does not take \n
    if liste_mots_spaced[0:1].isupper(): liste_gloseslx=liste_gloseslx[0:1].upper()+liste_gloseslx[1:len(liste_gloseslx)]
    prefrepl='<span class="sent">\g<1>'+liste_gloseslx+'\g<2><span class="annot">\g<3>'
    # don't forget to advance the index !
    capt_gr_index=capt_gr_index+3+1
    
  for glose in gloses :
    imots=imots+1    # commence donc à 0
    if glose=="COMMA"      : wrepl=wrepl+r'<span class="c">,</span>\n'
    elif glose=="DOT"      : wrepl=wrepl+r'<span class="c">.</span>\n'
    elif glose=="DOTnone"  : wrepl=wrepl+r"" # cas spécial où on élimine le DOT (uniquement pour dɔrɔmɛ ?)
    elif glose=="QUESTION" : wrepl=wrepl+r'<span class="c">?</span>\n'
    elif glose=="COLON"    : wrepl=wrepl+r'<span class="c">:</span>\n'
    elif glose=="SEMICOLON": wrepl=wrepl+r'<span class="c">;</span>\n'
    elif glose=="EXCLAM"   : wrepl=wrepl+r'<span class="c">!</span>\n'
    elif glose=="TIRET"    : wrepl=wrepl+r'<span class="c">-</span>\n'
    elif glose=="DEBUT"    : wrepl=wrepl+r'<span class="annot">'
    elif glose=="FIN"      : wrepl=wrepl+r'</span>\n</span>\n'
    elif glose=="BREAK"    : wrepl=wrepl+r'<span class="t">&lt;br/&gt;</span>\n'
    elif glose=="LETTREtag"    : 
      wrepl=wrepl+r'<span class="t">\g<'+str(capt_gr_index+1)+r'></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="DEGRE"    : wrepl=wrepl+r'<span class="c">°</span>\n'
    elif glose=="LAQUO"    : wrepl=wrepl+r'<span class="c">«</span>\n'
    elif glose=="RAQUO"    : wrepl=wrepl+r'<span class="c">»</span>\n'
    elif glose=="PARO"     : wrepl=wrepl+r'<span class="c">(</span>\n'
    elif glose=="PARF"     : wrepl=wrepl+r'<span class="c">)</span>\n'
    elif glose=="GUILLEMET"    : wrepl=wrepl+r'<span class="c">"</span>\n'
    elif glose=="APOSTROPHE"    : wrepl=wrepl+r'<span class="c">\'</span>\n'
    elif glose=="PERCENT"  : wrepl=wrepl+r'<span class="c">%</span>\n'
    elif glose=="PUNCT"    :
      #wrepl=wrepl+ur'<span class="c">\g<'+str(capt_gr_index+1)+ur'></span>\n'
      #capt_gr_index=capt_gr_index+1
      # changed 2018-04-09 : can also be a tag!
      wrepl=wrepl+r'<span class="\g<'+str(capt_gr_index+1)+r'>">\g<'+str(capt_gr_index+2)+r'></span>\n'
      capt_gr_index=capt_gr_index+2
    elif glose=="COMMENT"    :
      wrepl=wrepl+r'<span class="comment">\g<'+str(capt_gr_index+1)+r'></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="TAG"    :
      wrepl=wrepl+r'<span class="t">\g<'+str(capt_gr_index+1)+r'></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="NAME"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
      # ces +1 bizarres sont apparus après l'introduction de la glose correcte pour ?!lemma var    ...  à surveiller !   
    elif glose=="ACTION"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+r'>><sub class="gloss">NMLZ</sub></span></span></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="PERS"     : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">pers</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="PRONOM"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">prn</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="PRT"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">prt</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="INTJ"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">intj</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="VERBE"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="VNONPERF"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="VPERF"    : 
      #log.write(ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>PFV.INTR\g<'+str(capt_gr_index+5)+'>></span>\n')
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+r'>PFV.INTR\g<'+str(capt_gr_index+5)+r'>></span>\n'
      capt_gr_index=capt_gr_index+5+1  # j'aurais pensé +2 : il y a deux groupes  (?!lemma var) autour de PFV.INTR
    elif glose=="VPERFopt"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+r'>OPT2\g<'+str(capt_gr_index+5)+r'>></span>\n'
      capt_gr_index=capt_gr_index+5+1  # j'aurais pensé +2 : il y a deux groupes  (?!lemma var) autour de PFV.INTR
    elif glose=="VPERFprog"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+r'>PROG\g<'+str(capt_gr_index+5)+r'>></span>\n'
      capt_gr_index=capt_gr_index+5+1  # j'aurais pensé +2 : il y a deux groupes  (?!lemma var) autour de PFV.INTR
    elif glose=="VERBENMOD"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+3)+r'><sub class="ps">v</sub><\g<'+str(capt_gr_index+4)+r'>></span>\n'
      capt_gr_index=capt_gr_index+4+1
    elif glose=="ADJORD"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+r'><sub class="gloss">ORD</sub>\g<'+str(capt_gr_index+5)+r'>></span>\n'
      capt_gr_index=capt_gr_index+5+1
    elif glose=="VQ"       : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">vq</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    #elif glose==u"VQADJ"       : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">vq/adj</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    #elif glose==u"VQADJforcevq"       : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">vq</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    #elif glose==u"VQADJforceadj"       : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    elif glose=="DTM"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    #elif glose==u"PRNDTM"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prn/dtm</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    #elif glose==u"PRNDTMforceprn"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prn</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    #elif glose==u"PRNDTMforcedtm"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    elif glose=="POSTP"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">pp</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="PRMRK"       : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">pm</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="PRMRKQUAL"       : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">pm</sub><sub class="gloss">\g<'+str(capt_gr_index+3)+r'></sub></span></span>\n'
      capt_gr_index=capt_gr_index+3 # pas de +1 : pas de !lemma var
    elif glose=="COPULE"   : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">cop</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="ADJECTIF" : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="ADJECTIFforcen" :    # ex sabanan est adj dand Bamadaba mais parfois devient n
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    #elif glose==u"ADJN" : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj/n</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    #elif glose==u"ADJNforceadj" : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    #elif glose==u"ADJNforcen" : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    elif glose=="PARTICIPE"     : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">ptcp</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="NUM"      : 
      wrepl=wrepl+r'<span class="w" stage="tokenizer">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">num</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="NUMORD"    : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+3)+r'>ORDINAL\g<'+str(capt_gr_index+5)+r'>></span>\n'
      capt_gr_index=capt_gr_index+5+1  # j'aurais pensé +2 : il y a deux groupes  (?!lemma var) autour de ORDINAL - cf VPERF
    elif glose=="NUMANNEE"      : 
      wrepl=wrepl+r'<span class="w" stage="tokenizer">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">num</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="NUMnan"      :   # this is deprecated with the new PRE handlings - oct 2019
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'>nan<span class="lemma">\g<'+str(capt_gr_index+1)+r'>nan<sub class="ps">adj</sub><sub class="gloss">ORDINAL</sub><span class="m">\g<'+str(capt_gr_index+1)+r'><sub class="ps">num</sub><sub class="gloss">CARDINAL</sub></span><span class="m">nan<sub class="ps">mrph</sub><sub class="gloss">ORD</sub></span></span></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="ADV"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">adv</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="ADVP"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">adv.p</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    #elif glose==u"ADVN"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adv/n</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    #elif glose==u"ADVNforcen"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    #elif glose==u"ADVNforceadv"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">adv</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    #elif glose==u"VNforcen"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    #elif glose==u"VNforcev"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">v</sub><\g<'+str(capt_gr_index+3)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+3+1
    elif glose=="CONJ"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">\g<'+str(capt_gr_index+3)+'></sub><\g<'+str(capt_gr_index+4)+r'>></span>\n'
      capt_gr_index=capt_gr_index+4+1
    elif glose=="PREP"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">\g<'+str(capt_gr_index+3)+'></sub><\g<'+str(capt_gr_index+4)+r'>></span>\n'
      capt_gr_index=capt_gr_index+4+1
    #elif glose==u"CONJPREP"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">conj/prep</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    #elif glose==u"CONJPREPforceconj"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">conj</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    #elif glose==u"CONJPREPforceprep"      : 
    #  wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+2)+ur'><sub class="ps">prep</sub><\g<'+str(capt_gr_index+4)+ur'>></span>\n'
    #  capt_gr_index=capt_gr_index+4+1
    elif glose=="CONJPOSS"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">conj</sub><sub class="gloss">POSS</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="PPPOSS"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">pp</sub><sub class="gloss">POSS</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="COPEQU"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">cop</sub><sub class="gloss">EQU</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="COPQUOT"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">cop</sub><sub class="gloss">QUOT</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="NPROPRE"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><\g<'+str(capt_gr_index+3)+r'>></span>\n'
      capt_gr_index=capt_gr_index+3+1
    elif glose=="NPROPRENOMforcetop"      : 
      lastnproprenomforcetop=r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span></span>\n'
      wrepl=wrepl+lastnproprenomforcetop
      lastnproprenomforcetopindex=capt_gr_index+1    # in order to collect all instances of that candidate TOP name
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="NPROPRENOMforcenom"      : 
      lastnproprenomforcenom=r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><sub class="gloss">NOM</sub></span></span>\n'
      wrepl=wrepl+lastnproprenomforcenom
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="NPROPRENOMM"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><sub class="gloss">NOM.M</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="NPROPRENOMF"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><sub class="gloss">NOM.F</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="NPROPRENOMMF"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><sub class="gloss">NOM.F</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="NPROPRENOMCL"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><sub class="gloss">NOM.CL</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2 # 2 seulement (on ne récupère ni ps ni gloss) pas de +1 : pas de !lemma var
    elif glose=="NPROPRETOP"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n.prop</sub><sub class="gloss">TOP</sub>\g<'+str(capt_gr_index+3)+r'></span></span>\n'
      capt_gr_index=capt_gr_index+3+1 # nb: certains TOP ont une sous-glose, par. ex. avec jamana
    elif glose=="DOONINforceadvn"      : 
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">dɔ́ɔnin<sub class="ps">adv/n</sub><\g<'+str(capt_gr_index+2)+r'>></span>\n'
      capt_gr_index=capt_gr_index+2+1
    elif glose=="NORVname" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose=="NORVverbe" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+5)+r'><sub class="ps">v</sub><\g<'+str(capt_gr_index+6)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)
    elif glose=="NORADJname" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose=="NORADJadj" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+5)+r'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+6)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)
    elif glose=="VQORADJvq" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">vq</sub><\g<'+str(capt_gr_index+3)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose=="VQORADJadj" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+5)+r'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+6)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)
    elif glose=="PMORCOP" :   # leave as it is
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">pm</sub><sub class="gloss">\g<'+str(capt_gr_index+3)+r'></sub><span class="lemma var">\g<'+str(capt_gr_index+4)+r'><sub class="ps">cop</sub><sub class="gloss">\g<'+str(capt_gr_index+5)+r'></sub></span></span></span>\n'
      capt_gr_index=capt_gr_index+5+1
    elif glose=="PMORCOPpm" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">pm</sub><sub class="gloss">\g<'+str(capt_gr_index+3)+r'></sub></span></span>\n'
      capt_gr_index=capt_gr_index+5+1
    elif glose=="PMORCOPcop" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+4)+r'><sub class="ps">cop</sub><sub class="gloss">\g<'+str(capt_gr_index+5)+r'></sub></span></span>\n'
      capt_gr_index=capt_gr_index+5+1
    elif glose=="AORNname" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">n</sub><\g<'+str(capt_gr_index+3)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose=="AORNadj" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+5)+r'><sub class="ps">adj</sub><\g<'+str(capt_gr_index+6)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)
    elif glose=="DORPdtm" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+3)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose=="DORPprn" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">prn</sub><\g<'+str(capt_gr_index+3)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose=="DTMORADVdtm" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'><sub class="ps">dtm</sub><\g<'+str(capt_gr_index+3)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # 2  à cause des 2 (((?!lemma var).)*)
    elif glose=="DTMORADVadv" :
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+5)+r'><sub class="ps">adv</sub><\g<'+str(capt_gr_index+6)+r'>></span></span>\n'
      capt_gr_index=capt_gr_index+5+2 # attention décalage du au 1er (((?!lemma var).)*)

    elif glose=="IPFVAFF":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
      # will need correction in POST for b'
    elif glose=="IPFVNEG":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
      # will need correction in POST for t'
    elif glose=="COPNEG":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+1)+r'><sub class="ps">cop</sub><sub class="gloss">COP.NEG</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="PFVTR":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+1)+r'><sub class="ps">pm</sub><sub class="gloss">PFV.TR</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="PFVNEG":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+1)+r'><sub class="ps">pm</sub><sub class="gloss">PFV.NEG</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="PMINF":
      #wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur'><span class="lemma">\g<'+str(capt_gr_index+1)+ur'><sub class="ps">pm</sub><sub class="gloss">INF</sub></span></span>\n'
      # temp fix : lemma for ka has tone: kà !!! and no capital letters ... - how to replace (ka|k'|Ka|K') by (kà|k'|kà|k') ???
      # will need correction in POST for k' and K'
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">kà<sub class="ps">pm</sub><sub class="gloss">INF</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="PMSBJV":
      # will need correction in POST for k' and K'
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">ka<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="NICONJet":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+1)+r'><sub class="ps">conj</sub><sub class="gloss">et</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="NICONJsi":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">ní<sub class="ps">conj</sub><sub class="gloss">si</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="LANA":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'>\g<'+str(capt_gr_index+2)+r'><span class="lemma">\g<'+str(capt_gr_index+1)+r'>á<sub class="ps">pp</sub><sub class="gloss">à</sub></span></span>\n'
      capt_gr_index=capt_gr_index+2
    elif glose=="CONSONNE":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'></span></span>\n'
      capt_gr_index=capt_gr_index+2
#CAUTION: ur in all strings IMPORTANT otherwise it breaks output to the compile REPL-STANDARD-C files!!!
    elif glose=="MONTH":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">\g<'+str(capt_gr_index+2)+r'></span></span>\n'
      capt_gr_index=capt_gr_index+2
    elif glose=="YEUNDEFequpm":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">yé<sub class="ps">cop</sub><sub class="gloss">EQU</sub><span class="lemma var">yé<sub class="ps">pm</sub><sub class="gloss">PFV.TR</sub></span></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="YEUNDEFppvoir":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">yé<sub class="ps">pp</sub><sub class="gloss">PP</sub><span class="lemma var">yé<sub class="ps">v</sub><sub class="gloss">voir</sub></span></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="YEUNDEFpp":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">yé<sub class="ps">pp</sub><sub class="gloss">PP</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="YEUNDEFequ":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">yé<sub class="ps">cop</sub><sub class="gloss">EQU</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="YEPP":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">yé<sub class="ps">pp</sub><sub class="gloss">PP</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="NIUNDEFet":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">ni<sub class="ps">conj</sub><sub class="gloss">et</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="NAUNDEFa":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">ná<sub class="ps">pp</sub><sub class="gloss">à</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="NAUNDEFvenir":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">nà<sub class="ps">v</sub><sub class="gloss">venir</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1
    elif glose=="NAUNDEFcert":
      wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r'><span class="lemma">nà<sub class="ps">pm</sub><sub class="gloss">CERT</sub></span></span>\n'
      capt_gr_index=capt_gr_index+1

    elif glose=="NONVERBALGROUP":
      wrepl=wrepl+r'\g<'+str(capt_gr_index+1)+r'>'
      # capt_gr_index=capt_gr_index+4  # ou bien autant de fois que de matches et difficile à prévoir : 2 par word x nb de words
      # capt_gr_index=capt_gr_index+20  # nouvelle formule 15-06-2020 !!
      capt_gr_index=capt_gr_index+22  # nouvelle formule 17-11-2020

    elif glose=="AMBIGUOUS":
      wrepl=wrepl+r'<span class="w" \g<'+str(capt_gr_index+1)+r'>lemma var\g<'+str(capt_gr_index+2)+r'></span>\n'
      capt_gr_index=capt_gr_index+2
    else :
      # glose est supposé aveoir une forme lx:ps:gloss [sub]

      # petite validation sur glose :
      ncol=glose.count(":")
      if ncol==0 :
        print("\nglose incorrecte (format lx:ps:gloss [sub]) non respecté, pas de ':' :",glose)
        log.write("glose incorrecte (format lx:ps:gloss [sub]) non respecté, pas de ':' :"+glose+"\n")
        sys.exit("\n"+liste_gloses+"\n\narrêt de repl.")
      elif ncol!=2*(ncol/2) :
        print("\nglose incorrecte (format lx:ps:gloss [sub]) non respecté, nombre incorrect de ':' :",glose)
        log.write("glose incorrecte (format lx:ps:gloss [sub]) non respecté, nombre incorrect de ':' :"+glose+"\n")
        sys.exit("\n"+liste_gloses+"\n\narrêt de repl.")

      if re.search(r"\s[A-ZƐƆƝŊa-zɛɔɲŋ\.̀́̌̂\']*\s",glose) :     #    *  : can also be double space
        print("\nglose incorrecte (format lx:ps:gloss [sub]) non respecté, espaces mal placés :",glose)
        log.write("glose incorrecte (format lx:ps:gloss [sub]) non respecté, espaces mal placés :"+glose+"\n")
        sys.exit("\n"+liste_gloses+"\n\narrêt de repl.")

      if lmots==lgloses :
        word=motscapt[imots]
        # word=re.sub(u"̀\*","",word)   # remove trick for optionnal low tone: remove diacritic and star  <- NOT IF CAPTURED
        

      else:  # try the old method
      
        # attention : résout la plupart des cas
        # sauf 
        # 1) split/join : revoir stage=
        # 2) Bailleul : quid si on remplace ton haut par ton bas (on remplace alors l'original, aïe!)
        i_colon=glose.find(":")
        word=glose[0:i_colon]
        if "|" in word :
          words=word.split("|")
          word=words[0]
        if tonal=="bailleul" : 
          word=re.sub("́","",word)
          word=re.sub("̂","",word)
        elif tonal!="tonal" :  
          word=re.sub("́","",word)
          word=re.sub("̀","",word)
          word=re.sub("̌","",word)
          word=re.sub("̂","",word)
        if tonal=="old" : # dans ce cas, les tons sont éliminés mais on revient à l'ancienne écriture
          word=re.sub("ɛɛ","èe",word)
          word=re.sub("ɛ","è",word)
          word=re.sub("Ɛ","È",word)
          word=re.sub("ɔɔ","òo",word)
          word=re.sub("ɔ","ò",word)
          word=re.sub("Ɔ","Ò",word)
          word=re.sub("ɲ","ny",word)
          word=re.sub("Ɲ","Ny",word)
        elif tonal=="newny":
          #if oldny :       # cas type Baabu ni baabu
          word=re.sub("ɲ","ny",word)
          word=re.sub("Ɲ","Ny",word)
      
      
      if "§§" in glose:   # un lemma var est proposé, (un seul!)
        pglose=glose.split("§§")
        glose1=pglose[0]
        glose2=pglose[1]
        #html1=daba.formats.glosstext_to_html(glose1,variant=False, encoding='utf-8').decode('utf-8')
        html1=daba.formats.glosstext_to_html(glose1,variant=False, encoding='unicode')
        html1=re.sub(r"\<\/span\>$","",html1)
        #html2=daba.formats.glosstext_to_html(glose2,variant=True, encoding='utf-8').decode('utf-8')
        html2=daba.formats.glosstext_to_html(glose2,variant=False, encoding='unicode')
        html2=html2.replace("lemma","lemma var")
        if "*" in word or "(" in word or "[" in word:   # main concern is quote/apostrophe here but may also be loaw tone/ capital on verbs (not handled for §§?)
          wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r">"+html1+html2+r'</span></span>\n'
          capt_gr_index=capt_gr_index+1
          #print "- capturé"
        else:
          wrepl=wrepl+r'<span class="w" stage="0">'+word+html1+html2+r'</span></span>\n'
      else :
        # if "'" in glose: glose=re.sub(ur"\'","\'",glose)  # scared about fó:conj:jusqu'à
        # htmlgloss=daba.formats.glosstext_to_html(glose,variant=False, encoding='utf-8').decode('utf-8')
        # in usr/lib/python3.9/xml/etree/ElementTree.py : tostring()
        # "If encoding is "unicode", a string is returned. Otherwise a bytestring is returned"
        # try : 
        htmlgloss=daba.formats.glosstext_to_html(glose,variant=False, encoding='unicode')

        #log.write("[] glosstext_to_html: "+glose+" -> "+htmlgloss+"\n")
        """ ancien code
        if wrepl=="" and ucase1:
          wordrepl=ur"\g<1>"
          wrepl=wrepl+ur'<span class="w" stage="0">'+wordrepl+htmlgloss+ur'</span>\n'
          capt_gr_index=capt_gr_index+1      # or just =1 ?
        else:
          print "word=",word
          if "*" in word or "(" in word or "[" in word:
            wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur">"+htmlgloss+ur'</span>\n'
            capt_gr_index=capt_gr_index+1
          else:
            wrepl=wrepl+ur'<span class="w" stage="0">'+word+htmlgloss+ur'</span>\n'
        """
        #print "word=",word
        if "*" in word or "(" in word or "[" in word:   # includes ucase1 = true (word has [)
          wrepl=wrepl+r'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+r">"+htmlgloss+r'</span>\n'
          capt_gr_index=capt_gr_index+1
          #print "- capturé"
        else:
          wrepl=wrepl+r'<span class="w" stage="0">'+word+htmlgloss+r'</span>\n'
          #print "- basique"
       
        # a note of warning : wrepl works as a string for re.subn, so ur"" is not strictly needed 
        #       BUT when writing compiled rules ur"" is needed as regards \n, to conserve them as is in the file
        #       number of lines in file should = number of rules printed by program
    
  nbreplok=nbreplok+1
  if nlignerepl!=0: 
    iprogress=nbreplok/float(nlignerepl)
    update_progress(iprogress)

  if "NPROPRENOMforcetop" in liste_gloses:  forcetopiterator=re.finditer(wsearch,tout,re.U|re.MULTILINE)
  
  if prefsearch!=r"":    # if number of elements differ in liste_mots and liste_gloses, update "sent"
      wsearch=prefsearch+wsearch
      wrepl=prefrepl+wrepl
  
  #print "\nwsearch :",wsearch
  #print "\nwrepl :",wrepl
  # test 15062020
  #   wgroups=re.findall(wsearch, tout,re.U|re.MULTILINE)
  #   if len(wgroups)>0: print wgroups
  # test 15062020
  if replcompile:
    #liste_mots_compile=re.sub(ur"\s","_",sequence)
    liste_mots_compile=liste_mots   # 13/5/2021 ignore modifs Dukure, tant pis pour ces textes
    fileREPC.write(liste_mots_compile+"==="+str(ucase1)+"==="+str(topl)+"==="+wsearch+"==="+wrepl+"\n")

  # to log track special cases
  # (last done 20/1/22 - fò confusion fo / fɔ due to "low tone"* in liste_glose after Dukure-fixes)
  """
  if "saluer" in wrepl:
    logsearch=re.finditer(wsearch,tout,re.U|re.MULTILINE)
    logtext=""
    for match in logsearch:
      # logtext==logtext+match.group(0)+"\n"
      s = match.start()
      e = match.end()
      logtext=logtext+tout[s:e]+"\n"
  """

  tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # derniers parametres : count (0=no limits to number of changes), flags re.U|
  # TESTED : |re.IGNORECASE ADDED 14/03/2021 - dropped : too slow!!! + rules with caps
  # if nombre >0 : print "updated",wsearch

  # to log track special cases
  """
  if nombre>0:
    if "saluer" in wrepl:
      log.write("track info for 'saluer' looking for "+liste_mots+"\n"+logtext+"\n")
  """
  
  if prefsearch!=r"":   # modif 15/6/2020 - updating words in sent and glosses creates an OVERLAP 
    nombre_replay=nombre
    while nombre_replay!=0:
      tout,nombre_replay=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)      # pour éviter les problèmes de NON OVERLAP capability of re
      nombre=nombre+nombre_replay

  if topl :  # NOOOO! and nombre==0 : # only action IF main updater did not work !!!
    """
    if ucase1:
      mot2=re.sub("\)","w)",mot2)   # mot2 = ([kK]à*lanw)
      wsearch=ur'<span class="w" +stage="[a-z0-9\.\-]+">'+mot2+ur'<.*</span></span>\n'
    else : 
      #print "topl not ucase AVANT:",wsearch
      #print "topl not ucase AVANT word:",word
      # word may contain re sensitive characters like * wsearch=re.sub(ur""+word+ur"\)\<",word+"w)<",wsearch)   # wsearch contains only one word, just add w
      # it is anyway the first )< 
      wsearch=re.sub(ur"\)\<","w)<",wsearch)
      #print "topl not ucase APRES:",wsearch
    """
    if not ucase1:   # if ucase1 mot2 is already set
      if mot[0]!="(": mot2="("+mot+")" # for compatibility with wrepl \g<1>
      else : mot2=mot
    mot2=re.sub("\)","w)",mot2)   # mot2 = ([kK]à*lanw)
    wsearch=r'<span class="w" +stage="[a-z0-9\.\-]+">'+mot2+r'<.*</span></span>\n'
    
    gloseelems=glose.split(":",2)
    gloselx=gloseelems[0]
    gloseps=gloseelems[1]
    glose=gloselx+"w:"+gloseps+": ["+glose+" w:mrph:PL]"
    # htmlgloss=daba.formats.glosstext_to_html(glose,variant=False, encoding='utf-8').decode('utf-8')
    htmlgloss=daba.formats.glosstext_to_html(glose,variant=False, encoding='unicode')
    """
    if "*" in word or "(" in word or "[" in word:
      wrepl=wrepl+ur'<span class="w" stage="0">\g<'+str(capt_gr_index+1)+ur">"+htmlgloss+ur'</span>\n'
      capt_gr_index=capt_gr_index+1
    """
    """
    if ucase1:
      wordrepl=ur"\g<1>"
      wrepl=ur'<span class="w" stage="0">'+wordrepl+htmlgloss+ur'</span>\n'
      capt_gr_index=capt_gr_index+1      # or just =1 ?
    else:
      wrepl=ur'<span class="w" stage="0">'+word+"w"+htmlgloss+ur'</span>\n'
    """
    
    wrepl=r'<span class="w" stage="0">\g<1>'+htmlgloss+r'</span>\n'
    capt_gr_index=capt_gr_index+1      # or just =1 ?
      
    tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)
    # if nombre >0 : print "topl updated",wsearch
    
    if replcompile:
      fileREPC.write(liste_mots+"==="+str(ucase1)+"==="+str(topl)+"==="+wsearch+"==="+wrepl+"\n")

  if nombre>0 :
    # print "\nwsearch:",wsearch
    # print "wrepl:",wrepl
    # detecting that a name is TOP should propagate to all instances of that name in the text 
    if "NPROPRENOMforcetop" in liste_gloses: 
      for forcetop in forcetopiterator :
        topname=forcetop.group(lastnproprenomforcetopindex)
        # print topname
        lastnproprenom=r'<span class="w" +stage="[^>]+">'+topname+'<span class="lemma">'+topname+'<sub class="ps">n\.prop</sub><sub class="gloss">NOM</sub></span></span>\n'
        lastnproprenomforcetop=r'<span class="w" stage="[^>]+">'+topname+'<span class="lemma">'+topname+'<sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span></span>\n'
        tout,nombre2=re.subn(lastnproprenom,lastnproprenomforcetop,tout,0,re.U|re.MULTILINE)
        nombre=nombre+nombre2
        lastnproprenom=r'<span class="annot"><span class="w" +stage="[^>]+">'+topname+'<span class="lemma">'+topname.lower()+'<sub class="gloss">EMPR</sub></span></span>\n'
        lastnproprenomforcetop=r'<span class="annot"><span class="w" stage="[^>]+">'+topname+'<span class="lemma">'+topname+'<sub class="ps">n.prop</sub><sub class="gloss">TOP</sub></span></span>\n'
        tout,nombre3=re.subn(lastnproprenom,lastnproprenomforcetop,tout,0,re.U|re.MULTILINE)
        nombre=nombre+nombre3
      
    msg="%i modifs avec " % nombre +sequence+"\n"
    log.write(msg)
    nbrulesapplied=nbrulesapplied+1
    nbmodif=nbmodif+nombre
    # recalculer lmots, enlever les ponctuations
    lmots=0
    for glose in gloses :
      if glose+"_" not in valides :
        lmots=lmots+1
    nbmots=nbmots+(nombre*lmots)
  
# POST : systematic global replaces ###############################################

# handle distributed groups type mɔgɔ ô mɔgɔ
#    elif mot==u"WORDA"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">(?P<WORDA>[^\<]+)<[^\n]+</span>\n'
#    elif mot==u"WORDB"    : wsearch=wsearch+ur'<span class="w" stage="[^>]+">(?P=WORDA)<[^\n]+</span>\n'
# 22/5/20 ajouté restriction sur \' car il ne faut pas le faite pour des cas comme : k' o k'      ou b' o b'
# ATTENTION IL NE FAUT PAS LE FAIRE POUR : ye o ye     ????????????????    HOW HOW HOW !!!
wsearch=r'<span class="w" +stage="[^>]+">(?P<WORDA>[^\<\']+)<([^\n]+)</span>\n'   # peut être nom, verbe ou n'importe quoi, même inconnu et ambigu
wsearch=wsearch+r'<span class="w" +stage="[^>]+">o<([^\n]+)</span>\n'   # peut être n'importe quel "o", même déjà défini comme DISTR
#py3 wsearch=wsearch+r'<span class="w" +stage="[^>]+">((?i)(?P=WORDA))<([^\n]+)</span>\n'  # on le capture au cas où il y ait une différence majuscule/minuscule avec le premier
wsearch=wsearch+r'<span class="w" +stage="[^>]+">((?i:(?P=WORDA)))<([^\n]+)</span>\n'  # on le capture au cas où il y ait une différence majuscule/minuscule avec le premier
# ATTENTION: il faut capturer et restitruer correctement le 2ème WORD car il peut y avoir une différence de majuscule: Maa o maa
#wrepl=ur'<span class="w" stage="0">\g<1><\g<2></span>\n'
#wrepl=wrepl+ur'<span class="w" stage="0">o<span class="lemma">ô<sub class="ps">conj</sub><sub class="gloss">DISTR</sub></span></span>\n'
#wrepl=wrepl+ur'<span class="w" stage="0">\g<3><\g<2></span>\n'

def filterrepl(m):
  worda=m.groups()[0]
  defa=m.groups()[1]
  defo=m.groups()[2]
  wordb=m.groups()[3]
  defb=m.groups()[4]
  if worda=="ye":
    wrepl='<span class="w" stage="0">'+worda+'<'+defa+'</span>\n'
    wrepl=wrepl+'<span class="w" stage="0">o<'+defo+'</span>\n'
    wrepl=wrepl+'<span class="w" stage="0">'+wordb+'<'+defb+'</span>\n'
  else:
    wrepl='<span class="w" stage="0">'+worda+'<'+defa+'</span>\n'
    wrepl=wrepl+'<span class="w" stage="0">o<span class="lemma">ô<sub class="ps">conj</sub><sub class="gloss">DISTR</sub></span></span>\n'
    wrepl=wrepl+'<span class="w" stage="0">'+wordb+'<'+defa+'</span>\n'
  return wrepl

tout,nombre=re.subn(wsearch,filterrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i modifs groupe DISTRIBUTIF  " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# handle double pm   like dtm/prn and force disambiguator to choose

# simple cases (simple gloss)

wsearch=r'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub>(<span class="lemma var">|</span>)'
wrepl=r'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub></span>\g<5>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: ps double -> lemma/lemma var duplication
if nombre>0 :
  msg="%i modifs ps double -> lemma/lemma var duplication " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=r'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub></span>'
wrepl=r'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: double -> lemma var/lemma var duplication
if nombre>0 :
  msg="%i modifs double -> lemma var/lemma var duplication " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# how to handle complex gloss like dɔw ?
# ONLY Complex gloss with two sub components (and no main gloss)
wsearch=r'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span>'
wrepl=r'<span class="lemma">\g<1><sub class="ps">\g<2></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: ps double complexgloss -> lemma/lemma var duplication
if nombre>0 :
  msg="%i modifs ps double complexgloss -> lemma/lemma var duplication " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


wsearch=r'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span></span>'
wrepl=r'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><span class="m">\g<4><sub class="ps">\g<5></sub><sub class="gloss">\g<6></sub></span><span class="m">\g<7><sub class="ps">\g<8></sub><sub class="gloss">\g<9></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: double  complexgloss-> lemma var/lemma var duplication
if nombre>0 :
  msg="%i modifs double  complexgloss-> lemma var/lemma var duplication " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# ONLY Complex gloss with two sub components (and explicit main gloss)

wsearch=r'<span class="lemma">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span>'
wrepl=r'<span class="lemma">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: ps double complexgloss -> lemma/lemma var duplication
if nombre>0 :
  msg="%i modifs ps double complexgloss -> lemma/lemma var duplication " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

wsearch=r'<span class="lemma var">([^<]+)<sub class="ps">([^<\/]+)\/([^<]+)</sub><sub class="gloss">([^<]*)</sub><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span><span class="m">([^<]+)<sub class="ps">([^<]+)</sub><sub class="gloss">([^<]+)</sub></span></span>'
wrepl=r'<span class="lemma var">\g<1><sub class="ps">\g<2></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span><span class="lemma var">\g<1><sub class="ps">\g<3></sub><sub class="gloss">\g<4></sub><span class="m">\g<5><sub class="ps">\g<6></sub><sub class="gloss">\g<7></sub></span><span class="m">\g<8><sub class="ps">\g<9></sub><sub class="gloss">\g<10></sub></span></span>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  # FIN: double  complexgloss-> lemma var/lemma var duplication
if nombre>0 :
  msg="%i modifs double  complexgloss-> lemma var/lemma var duplication " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# fin : decoration pour consultation dans le navigateur
#  ambigüs
'''
wsearch=ur'<span class="w"(.*)lemma var(.*)</span>\n'
wrepl=ur'<span class="w" style="background-color:beige;"\g<1>lemma var\g<2></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  highlight ambiguous words left for better navigator visualisation" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
'''
wsearch=r'</style>'
wrepl=r'span.lemma.var {background-color:lightblue;}\n</style><title>'+filenametemp+r'</title>'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  highlight ambiguous words left for better navigator visualisation" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# PMINF POST correction for k' and K'
wsearch=r'<span class="w" stage="0">(k\'|K\')<span class="lemma">kà<sub class="ps">pm</sub><sub class="gloss">INF</sub></span></span>\n'
wrepl=r"""<span class="w" stage="0">\g<1><span class="lemma">k'<sub class="ps">pm</sub><sub class="gloss">INF</sub></span></span>\n"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  PMINF  POST correction(s) for k' and K'" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# PMSBJV POST correction for k' and K'
wsearch=r'<span class="w" stage="0">(k\'|K\')<span class="lemma">ka<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span></span>\n'
wrepl=r"""<span class="w" stage="0">\g<1><span class="lemma">k'<sub class="ps">pm</sub><sub class="gloss">SBJV</sub></span></span>\n"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  PMSBJV POST correction(s) for k' and K'" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# NICONJet POST correction for n'
wsearch=r'<span class="w" stage="0">n\'<span class="lemma">ni<sub class="ps">conj</sub><sub class="gloss">et</sub></span></span>\n'
wrepl=r"""<span class="w" stage="0">n'<span class="lemma">n'<sub class="ps">conj</sub><sub class="gloss">et</sub></span></span>\n"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  NICONJet POST correction(s) for n' " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre
# NICONJsi POST correction for n'
wsearch=r'<span class="w" stage="0">n\'<span class="lemma">ní<sub class="ps">conj</sub><sub class="gloss">si</sub></span></span>\n'
wrepl=r"""<span class="w" stage="0">n'<span class="lemma">n'<sub class="ps">conj</sub><sub class="gloss">si</sub></span></span>\n"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  NICONJsi POST correction(s) for n' " % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVAFF POST correction for b'
wsearch=r'<span class="w" stage="0">b\'<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span></span>\n'
wrepl=r"""<span class="w" stage="0">b'<span class="lemma">b'<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span></span>\n"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVAFF  POST correction(s) for b'" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVAFF POST correction for be
wsearch=r'<span class="w" stage="0">be<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span></span>\n'
wrepl=r'<span class="w" stage="0">be<span class="lemma">be<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVAFF  POST correction(s) for be" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVAFF POST correction for bi
wsearch=r'<span class="w" stage="0">bi<span class="lemma">bɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span></span>\n'
wrepl=r'<span class="w" stage="0">bi<span class="lemma">bi<sub class="ps">pm</sub><sub class="gloss">IPFV.AFF</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVAFF  POST correction(s) for bi" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVNEG POST correction for t'
wsearch=r'<span class="w" stage="0">t\'<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span></span>\n'
wrepl=r"""<span class="w" stage="0">t'<span class="lemma">t'<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span></span>\n"""
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVNEG  POST correction(s) for t'" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVNEG POST correction for te
wsearch=r'<span class="w" stage="0">te<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span></span>\n'
wrepl=r'<span class="w" stage="0">te<span class="lemma">te<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVNEG POST correction(s) for te" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre

# IPFVNEG POST correction for ti
wsearch=r'<span class="w" stage="0">ti<span class="lemma">tɛ<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span></span>\n'
wrepl=r'<span class="w" stage="0">ti<span class="lemma">ti<sub class="ps">pm</sub><sub class="gloss">IPFV.NEG</sub></span></span>\n'
tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
if nombre>0 :
  msg="%i  IPFVNEG POST correction(s) for ti" % nombre +"\n"
  log.write(msg)
  nbrulesapplied=nbrulesapplied+1
  nbmodif=nbmodif+nombre
  nbmots=nbmots+nombre


# tones on gparser generated derivations and flexions lacking tones
# example : sinsinnen:ptcp: [sínsin:v:appuyer nen:mrph:PTCP.RES]
fixsearch=re.compile(r'<span class="(lemma|lemma var)">([^<́̀̌̂]+)<sub class="ps">([^<]+)</sub><span class="m">([^<]+)<')
# captures lemma sinsinnen ptcp and sínsi
# extract all similar constructs 
# 
fixtones=fixsearch.finditer(tout,re.U|re.MULTILINE)
fixedlist=[]
for match in fixtones:
  lemmaclass=match.group(1)
  lemma=match.group(2)
  ps=match.group(3)
  slemma=match.group(4)
  fixeditem=lemmaclass+':'+lemma+':'+ps+':'+slemma
  if fixeditem in fixedlist: continue
  # print(lemma, ps, slemma)
  slemma_notone,ntones=re.subn(r'[́̀̌̂]','',slemma)
  if ntones==0:
    print(lemma+":"+ps+": -> no tone in ",slemma," ???")
  else:
    fixedlist.append(fixeditem)
    lemma_tones=lemma.replace(slemma_notone,slemma)
    # print("->",lemma_tones)
    wsearch=r'<span class="'+lemmaclass+r'">'+lemma      +r'<sub class="ps">'+ps+r'</sub><span class="m">'+slemma+r'<'
    wrepl  =r'<span class="'+lemmaclass+r'">'+lemma_tones+r'<sub class="ps">'+ps+r'</sub><span class="m">'+slemma+r'<'
    tout,nombre=re.subn(wsearch,wrepl,tout,0,re.U|re.MULTILINE)  
    if nombre>0 :
      msg="%i  tones correction(s) " % nombre +" for "+lemma +"\n"
      # print(msg)
      log.write(msg)
      nbrulesapplied=nbrulesapplied+1
      nbmodif=nbmodif+nombre
      nbmots=nbmots+nombre
print("gparser tones fixed items: ",len(fixedlist))
# FINISH
msg="\n %i modifs au total" % nbmodif
log.write(msg)
msg="\n %i mots modifies au total" % nbmots
log.write(msg)

fileOUT.write(tout)

fileIN.close()
fileOUT.close()

fileREP.close()
if replcompile:
  fileREPC.close()

log.close()


if nbmodif==0 : 
  os.remove(logfilename)
  os.remove(filenameout)
  print("    yelemali si ma soro / pas de remplacements / no replacements\n    Baasi te! / Desole ! / Sorry!")
else: 
  filegiven=filenameout
  print("")
  # renommer les fichiers, si dis :
  if ".dis.html" in filenamein :
    indexfile=1
    filenameinrename=filenamein+str(indexfile)
    while os.path.isfile(filenameinrename) :
      indexfile=indexfile+1
      filenameinrename=filenamein+str(indexfile)
    os.rename(filenamein, filenameinrename)
    print("\n   !",filenamein, "a été renommé / has been renamed \n->",filenameinrename,"\n")
    os.rename(filenameout, filenamein)
    filegiven=filenamein
  else :
    print("   "+filegiven+" ... mara dilannen don / fichier disponible / file is available\n")
   
  print("    "+str(nbmots)+" mots desambiguïsés / disambiguated words")
  
  ambs=ambiguous.findall(tout)
  nbambs=len(ambs)
  print("   ",nbambs, " mots ambigüs restants  / ambiguous words left ", 100*nbambs/totalmots, "%")
  # mettres ces mots dans un dictionnaire avec décompte, trier par décompte, afficher les plus fréquents (10?)
  ambsdict={}
  ambword=re.compile(r'<span class="w"\s+stage="[^\"]+">([^<]+)<')
  for ambg in ambs:
    amb1=ambword.search(ambg)
    if amb1:
      amb=amb1.group(1)
      if amb in ambsdict : ambsdict[amb]=ambsdict[amb]+1
      else : ambsdict[amb]=1
    else : print("ambg problem:",ambg)
  print("mots ambigüs uniques", len(ambsdict), ":")
  #ambsord=collections.OrderedDict(sorted(ambsdict.items()))
  ambsord=sorted(list(ambsdict.items()), key=lambda item: item[1], reverse=True)
  nitems=0
  nmax=int(len(ambsdict)/10)  # display 1/10th of the ambiguouis words
  ambsdisplay=""
  for k, v in ambsord : 
    #print k, v
    ambsdisplay=ambsdisplay+k+" : "+str(v)+", "
    nitems=nitems+1
    if nitems >nmax : break
  print(ambsdisplay[:-2])

  psambs=psambsearch.findall(tout)
  nbpsambs=len(psambs)
  psambslist=""
  if nbpsambs>0:
    for psamb in psambs:
      if psamb+" " not in psambslist: psambslist=psambslist+psamb+" "
  print("   ",nbpsambs, " ps ambigües restantes / remaining ambiguous ps ( "+psambslist+")", 100*nbpsambs/totalmots, "%")


  unknownwords=unknownsearch.findall(tout)
  nb_unknown=len(unknownwords)
  if nb_unknown >0 :
    unknownwordslist=""
    for unknownw in unknownwords:
      if unknownw+" " not in unknownwordslist: unknownwordslist=unknownwordslist+unknownw+" "
    print("   ",nb_unknown, " mots inconnus / unknown words   ( "+unknownwordslist+")")
  unknownwordslist=""

  unparsedwords=unparsedsearch.findall(tout)
  nb_unparsed=len(unparsedwords)
  if nb_unparsed >0 :
    unparsedwordslist=""
    for unparsedw in unparsedwords:
      if unparsedw+" " not in unparsedwordslist: unparsedwordslist=unparsedwordslist+unparsedw+" "
    print("   ",nb_unparsed, " mots mal parsés / words with failed parse attempt   ( "+unparsedwordslist+")")
  unparsedwordslist=""

  print("    ",napplicable," règles applicables ")
  print("    ",nbrulesapplied," règles appliquées / rules applied")
  print("    ",nbmodif," remplacements effectués / replacements done")
  print("    ",nbreplok," règles appliquées, voir le détail dans / see detail of applied rules in :"+logfilename)
 
# print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timeend=time.time()
timeelapsed=timeend-timestart
# en minutes, approximativement
print("    durée du traitement : "+str(int(timeelapsed))+" secondes, soit ",timeelapsed/totalmots," secondes/mot")