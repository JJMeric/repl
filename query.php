<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>

<head>
<title>Bamadaba - Dictionnaire Bambara</title>
 <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
 <meta charset="utf-8">
 <meta name="generator" content="Bamadaba/Corbama daba tools, SIL Toolbox &amp; MySQL" />
 <meta name="date-generated" content="vendredi 26 décembre 2025 - 15:00" />
 <meta name="robots" content="INDEX,FOLLOW">
<meta name="title" content="Bamadaba - Dictionnaire bambara">
<meta name="description" content="dictionnaire bambara français" />
<meta name="keywords" content="bambara, bamanankan, mandingue, mandé, bamako, ségou, mali, INALCO, LLACAN, Valentin Vydrine, Bailleul, Dumestre" />
<meta name="Author" content="Valentin Vydrine"><meta name="Author" content="Jean-Jacques Méric"><meta name="reply-to" content="contact@mali-pense.net">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
 <link rel="stylesheet" href="/bm/stylesheets/lexiquepro-corpus.css?v=2023Feb222000" type="text/css" />
 <script src="/bm/javascript/lexiquepro-corpus.js?v=2023Feb222000" type="text/javascript"></script>
</head>

<body>
<div id="haut" style="height: 8%;">
        <div style="height: 30%;font-family: 'Noto Sans','Arial';position: absolute;top: 0px;left: 10px;color: white;font-size: 75%;width:15%;background-color:lightblue;text-align:center;">
                <a href="http://cormand.huma-num.fr/" title="Le dictionnaire orthographique bambara, l'un des outils du Corpus bambara de référence" target=_blank>BAMADABA</a>
        </div>
        <div class="altindex" style="width:15%;background-color:lightblue;text-align:center;font-size:75%;">
                <a href="queryf.php" title="rechercher dans l'index français?">en français?</a>
        </div>
        <div class="search1" id="recherche">
            <a class=touche onClick="vinput('ɛ')" title="e ouvert">ɛ</a>
            <a class=touche onClick="vinput('ɔ')" title="o ouvert">ɔ</a>
            <a class=touche onClick="vinput('ɲ')" title="ny">ɲ</a>
            <a class=touche onClick="vinput('ŋ')" title="ng">ŋ</a>
            <form action="" method="GET" style="padding-right:10px;">
            <small>Mot bambara à rechercher:</small><input type="text" id='ɲini1' name="w" style="width:35%;">
            <input type="submit" style="width:15%; float:right; background-image: url('/bm/images/search-icon.png');background-repeat: no-repeat; " >
            </form>
        </div>
</div>
<div id="bas" style="top: 9%;">

<?php
$querylink=""; # = self - cf sylink

#echo "hello world";

#if (function_exists('mysqli_connect')) { echo '<br/>mysqli_connect exists';} else { echo '<br/>mysqli_connect does not exist';}
$connection = mysqli_connect('sql.lautre.net', 'jjmeric_bamadaba', '0IpHibwq') or die('Impossible de se connecter : ' . mysql_error());

#echo "<br/>Connected successfully";

#if (function_exists('mysqli_select_db')) { echo '<br/>mysqli_select_db exists';} else { echo '<br/>mysqli_select_db does not exist';}

mysqli_select_db($connection,'jjmeric_bamadaba') or die('<br/>Impossible de sélectionner la base de données');
#echo "<br/>DB jjmeric_bamadaba selected!";

$mydb = mysqli_connect('sql.lautre.net', 'jjmeric_bamadaba', '0IpHibwq', 'jjmeric_bamadaba') or die('Impossible de se sélectionner $mydb bamadaba : ' . mysql_error());

mysqli_set_charset($mydb,"utf8");

# interrogation du l'index français
# exemple: SELECT * FROM lx INNER JOIN gvf ON gvf.id=lx.id WHERE lx.gf="parole" or (gvf.gvf="parole" and gvf.id=lx.id)

# interrogation en bambara
# problème à régler : les tons ne sont pas pris en compte dans la requête, c'est identique à "sans ton"

#$word="à";
$word=$_GET['w'];
#$word=$_POST['w'];
$id=$_GET['id'];

if ($word=="" and id=="") 
        {echo "<h>Bienvenue dans Bamadaba. Merci de remplir le formulaire de recherche</h>";}
else {

#protections de base:
$word=trim($word);
$word=stripslashes($word);
$word=str_replace("'", "\'", $word);
$word=str_replace('"', '\"', $word);
$word=htmlspecialchars($word);

# autres protections:

$nerr=0;
$rejeter=False;

$pattern="/([^abcdefghijklmnoprstuwyzɛɔɲŋ\-\'\"\ś̀̌̂])/ui";
$rejeter=preg_match($pattern,$word,$matches, PREG_OFFSET_CAPTURE);
list($found,$pos)=$matches[1];

if ($rejeter) { 
        $word2=str_replace($found,"<u>$found</u>",$word);
        echo "<br>\n$word2 : Il y a une ou des lettres qui ne sont pas dans l'alphabet du bambara<br>";$nerr+=1;}

$pattern="/([bcdfghjklmɲŋprstyz])$/i";
$rejeter=preg_match($pattern,$word,$matches, PREG_OFFSET_CAPTURE);
list($found,$pos)=$matches[1];

if ($rejeter) { 
        $word2=substr($word,0,-1)."<u>$found</u>";
        echo "<br>\n$word2 : Il y a une consonne finale qui n'existe pas dans l'orthographe du bambara<br>";$nerr+=1;}

$pattern="/(a[eiouɛɔ]|e[aiouɛɔ]|i[aeouɛɔ]|o[aeiuɛɔ]|u[aeioɛɔ]|ɛ[aeiouɔ]|ɔ[aeiuoɛ]))/ui";
$rejeter=preg_match($pattern,$word,$matches, PREG_OFFSET_CAPTURE);
list($found,$pos)=$matches[1];

if ($rejeter) { 
        $word2=str_replace($found,"<u>$found</u>",$word);
        echo "<br>\n$word2 : Il y a une succession de voyelles qui n'existe pas dans l'orthographe du bambara<br>";$nerr+=1;}

$pattern="/([bcdfghjklmɲŋprstyzwn][bcdfghjklmɲŋprstyzwn])/ui";
$rejeter=preg_match($pattern,$word,$matches, PREG_OFFSET_CAPTURE);
list($found,$pos)=$matches[1];

if ($rejeter) { 
        if (in_array($found,array("bl", "br", "bw", "by", "dl", "dr", "dy", "fl", "fr", "fw", "fy", "gl", "gr", "gw", "kl", "kr", "kw", "mn", "my", "nb", "nc", "nd", "nf", "ng", "nk", "nl", "nm", "nn", "np", "nr", "ns", "nt", "nw", "nz", "pl", "pr", "py", "rb", "rd", "rf", "rk", "rl", "rm", "rn", "rr", "rs", "rt", "sh", "sk", "sm", "st", "sw", "sy", "tl", "tn", "tr", "tw", "ty", "ɲw", "ny")) ) {
                $rejeter=False;
        }
        else {
                if (in_array($found,array("cw", "dw", "ml", "mm", "pw")) and $found==substr($word,0,2) ) {
                        $rejeter=False;
                }
                else {
                        if(($found=="rw" and $word=="arw") or ($found=="dw" and $word=="adw") or ($found=="hw" and substr($word,0,3)=="shw") or ($found=="kn" and $word=="Shɛkna") or ($found=="sp" and $word=="paspas") or ($found=="hy" and substr($word,0,3)=="shy") or ($found=="hy" and substr($word,-5)=="shyɛn") or ($found=="hy" and in_array($word,array("kurashyɛ", "jishyɔlɔlan")))) {
                                $rejeter=False;}
                        else {
                                $word2=str_replace($found,"<u>$found</u>",$word);
                                echo "<br>\n$word2 : Il y a une succession de consonnes qui n'existe pas dans l'orthographe du bambara<br>";$nerr+=1;}
                        
                }
        }
}

if ($nerr>0) {
        if ($nerr==1) {echo "Une erreur";} else {echo "$nerr erreurs";}
}
else {


# using JOIN seems a heavy cpu load
#    SELECT * FROM lx
#    INNER JOIN va ON lx.lx='hábada' OR (va.va='hábada' AND va.id=lx.id)

if ($id!="") {$sql = "SELECT * FROM lx WHERE lx.id = ".$id;}
else {$sql = "SELECT * FROM lx WHERE lx.lx = '".$word."'";}
#
# DIACRITIQUES IGNOREES (tons)
# essayer mysqli_query($mydb,$sql, "SET NAMES 'utf8'");
# pour permettre la détection correcte des caractères unicode comme les diacritiques
# mais ceci n'est pas recommandé, plutôt:
/* change character set to utf8mb4 */
# mysqli_set_charset($mydb, "utf8mb4"); # ça ne suffit pas
# printf("Current character set: %s\n", mysqli_character_set_name($mydb));
/* SHOW VARIABLES LIKE '%char%'
Variable_name 	Value 	
character_set_client 	utf8mb4
character_set_connection 	utf8mb4
character_set_database 	utf8
character_set_filesystem 	binary
character_set_results 	utf8mb4
character_set_server 	latin1                <-  c'est peut-être le problème
character_set_system 	utf8
character_sets_dir 	/usr/share/mysql/charsets/   */
# ce qui marche dans php_myadmin : COLLATE utf8mb4_general_ci;
# erreur "disparité du jeton" (token mismatch) ???

# $sql=$sql." COLLATE utf8mb4_general_ci";   # ne marche pas: la requête est en erreur!
# tester : à la creation de la table on indique : COLLATE utf8_unicode_ci
#                 est-ce qu'il faudrait changer à COLLATE utf8mb4_general_ci   ???

$dictps=['n'=>'nom','n.prop'=>'nom propre','v'=>'verbe','pm'=>'marque prédicative','cop'=>'copule','ptcp'=>'participe','vq'=>'verbe qualitatif','adj'=>'adjectif','adv'=>'adverbe','adv.p'=>'adverbe préverbal','prep'=>'préposition','conj'=>'conjonction','pp'=>'postposition','pers'=>'pronom personnel','prn'=>'pronom','dtm'=>'déterminant','onomat'=>'onomatopée','intj'=>'interjection','prt'=>'particule','num'=>'numératif','mrph'=>'morphème','IPFV.NEG'=>'Imperfectif négatif','PFV.TR'=>'Perfectif transitif','PFV.NEG'=>'Perfectif négatif'];

$dictgl =['1PL'=>'Première personne du pluriel', '1PL.EMPH'=>'Première personne du pluriel (Emphatique)', '1SG'=>'Première personne du singulier', '1SG.EMPH'=>'Pronom personnel emphatique de la 1ère personne du singulier', '2PL'=>'Deuième eprsonne du pluriel', '2PL'=>'Deuxième personne du pluriel (Emphatique)', '2SG'=>'Deuxième personne du singulier', '2SG.EMPH'=>'Deuxième personne du singulier (Emphatique)', '3PL'=>'Troisième personne du pluriel', '3SG'=>'Troisième personne du singulier', 'ADR'=>'Postposition à valeur adressative et directive', 'CERT'=>'Marque du futur certain', 'COND.AFF'=>'Marque du conditionnel affirmatif', 'COND.NEG'=>'Conditionnel négatif', 'COP.NEG'=>'Copule d’un énoncé non-verbal locatif ou présentatif négatif', 'DEF'=>'Article défini', 'DEM'=>'Pronom démonstratif', 'DISTR'=>'Marque du distributif', 'EQU'=>'Copule d’un énoncé équatif non-verbal affirmatif', 'ETRG.FRA'=>'Emprunt au français', 'ETRG.ARB'=>'Emprunt à l\'arabe', 'ETRG.FUL'=>'Emprunt au peul', 'FOC'=>'Focus constrastif', 'FUT.AFF'=>'Futur affirmatif', 'FUT.NEG'=>'Marque du futur négatif', 'ID'=>'Présentatif affirmatif', 'IMP'=>'marque de l’impératif de la 2ème personne du pluriel', 'INF'=>'Infinitif', 'INFR.AFF'=>'Parfait inférentiel affirmatif', 'INFR.NEG'=>'Marque négative du parfait inférentif', 'IPFV.AFF'=>'Imperfectif affirmatif', 'NOM.CL'=>'Nom clanique', 'NOM.ETRG'=>'Nom étranger', 'NOM.F'=>'Prénom féminin', 'NOM.M'=>'Prénom masculin', 'NOM.MF'=>'Prénom masculin ou féminin', 'OPT'=>'Marque prédicative dans l’énoncé exprimant une bénédiction', 'POSS'=>'Marque possessive', 'PP'=>'Postposition polysémique (valeurs adréssative, bénéfactive, transformative, d\'identification, etc.)', 'PROH'=>'Marque du prohibitif', 'PST'=>'marque du passé discontinu', 'Q'=>'Particule d’interrogation totale', 'QUAL.AFF'=>'Marque de l\'énoncé qualitatif affirmatif', 'QUAL.NEG'=>'Marque de l\'énoncé négatif ', 'RECP'=>'Pronom réciproque', 'REFL'=>'Pronom réfléchi', 'REL'=>'Marque de relativisation', 'SBJV'=>'Subjonctif', 'SEQ'=>'Marque séquentative', 'TOP'=>'Toponyme', 'TOP.CNTR'=>'Marque de topicalisation contrastive du sujet', 'TOP.CNTR2'=>'Marque de topicalisation contrastive'];

$dictvl =['vt'=>'verbe transitif', 
	'vi'=>'verbe intransitif',
	'vr'=>'verbe réfléchi'];

$dictdi =['(b)'=>'(bambara)',
        'b'=>'(bambara)',
        '(bk)'=>'(Bɛlɛkɔ)',
        '(-bk)'=>'(inconnu à Bɛlɛkɔ)',
        'bk'=>'(Bɛlɛkɔ)',
        '(bk,bn)'=>'(Bɛlɛkɔ, Banan)',
        '(-bk,-bn)'=>'(inconnu à Bɛlɛkɔ et à Banan)',
        '(-bk, -bn)'=>'(inconnu à Bɛlɛkɔ et à Banan)',
        '(-bk, -bn; f)'=>'(Falajɛ - inconnu à Bɛlɛkɔ et à Banan)',
        '(bk, bn)'=>'(Bɛlɛkɔ, Banan)',
        '(bk,bn,f)'=>'(Bɛlɛkɔ, Banan, Falajɛ)',
        '(-bk,bn)'=>'(Banan, inconnu à Bɛlɛkɔ)',
        '(-bk,-bn,-f)'=>'(inconnu à Bɛlɛkɔ, Banan et à Falajɛ)',
        '(-bk,-f)'=>'(inconnu à Bɛlɛkɔ et à Falajɛ)',
        'bk, bn'=>'(Bɛlɛkɔ, Banan)',
        '(áu Bɛ́lɛdugu)'=>'(Bɛlɛdugu)',
        '(bl)'=>'(Bɛlɛkɔ)',
        '(Bl)'=>'(Bɛlɛkɔ)',
        'bl'=>'(Bɛlɛkɔ)',
        '(bmk)'=>'(Bamakɔ)',
        '(-bmk)'=>'(inconnu à Bamakɔ)',
        '(bmk,bk)'=>'(Bamakɔ, Bɛlɛkɔ)',
        '(-bmk,-bk)'=>'(inconnu à Bamakɔ et à Bɛlɛkɔ)',
        '(bmk) (-f,-bk,-bn)'=>'Bamakɔ, inconnu à Bɛlɛkɔ et à Banan)',
        '(bn)'=>'(Banan)',
        '(-bn)'=>'(inconnu à Banan)',
        '(bn,bk)'=>'(Banan, Bɛlɛkɔ)',
        '(-bn,bk)'=>'(Bɛlɛkɔ, inconnu à Banan)',
        '(-bn,-bk)'=>'(inconnu à Banan et à Bɛlɛkɔ)',
        '(-bn/-bk)'=>'(inconnu à Banan et à Bɛlɛkɔ)',
        '(bn,f)'=>'(Banan, Falajɛ)',
        '(-bn,-f)'=>'(inconnu à Banan et à Falajɛ)',
        '(bn; bk)'=>'(Banan, Bɛlɛkɔ)',
        '(bn; f)'=>'(Banan, Falajɛ)',
        '(bS)'=>'(Bambara de Ségou)',
        'bS'=>'(Bambara de Ségou)',
        '(bz)'=>'(Mgr Bazin)',
        'bz'=>'(Mgr Bazin 1901-1910)',
        '(d)'=>'(Dumestre)',
        '(du)'=>'(Dumestre, Dùgukuna)',
        '(dú)'=>'(Dumestre, Dùgukuna)',
        'd'=>'(Dumestre)',
        'du'=>'(Dumestre, Dùgukuna)',
        'dú'=>'(Dumestre, Dùgukuna)',
        '(f)'=>'(Falajɛ)',
        '(-f)'=>'(inconnu à Falajɛ)',
        '(- f)'=>'(inconnu à Falajɛ)',
        '(f,bk)'=>'(Falajɛ, Bɛlɛkɔ)',
        '(-f,-bk)'=>'(inconnu à Falajɛ et à Bɛlɛkɔ)',
        '(-f, -bk)'=>'(inconnu à Falajɛ et à Bɛlɛkɔ)',
        '(f,bk,bn)'=>'(Falajɛ, Bɛlɛkɔ, Banan)',
        '(-f,-bk,-bn)'=>'(Inconnu à Falajɛ, Bɛlɛkɔ et à Banan)',
        '(f,bn)'=>'(Falajɛ, Banan)',
        '(-f,-bn)'=>'(inconnu à Falajɛ et à Banan)',
        '(-f, -bn)'=>'(inconnu à Falajɛ et à Banan)',
        '(-f,bn)'=>'(Banan, inconnu à Falajɛ)',
        '(f, bn)'=>'(Falajɛ, Banan)',
        '(f,kl)'=>'(Falajɛ, Kolokani)',
        '(-f,-kl)'=>'(inconnu à Falajɛ et à Kolokani)',
        '(jula, bmk)'=>'(jula, Bamakɔ)',
        '(jk)'=>'(document sur la santé de Jakité)',
        '(jo)'=>'(Joseph Traoré de Basabugu à Falajɛ)',
        '(Jó)'=>'(Joseph Traoré de Basabugu à Falajɛ)',
        '(kb)'=>'(journal Kibaru)',
        '(k)'=>'(Kolokani)',
        '(kl)'=>'(Kolokani)',
        '(-kl)'=>'(inconnu à Kolokani)',
        '(kn)'=>'(Kolokani)',
        '(-kn)'=>'(inconnu à Kolokani)',
        '(xas)'=>'(khassonké)',
        '(m)'=>'(maninka)',
        'm'=>'(maninka)',
        'mF'=>'(maninka de Faranah)',
        '(mo)'=>'(Mgr Paul-Marie Molin 1885-1967)',
        '(mó)'=>'(Mgr Paul-Marie Molin 1885-1967)',
        'tou'=>'(Mgr Toulotte 1892-1897)'];

$retour = mysqli_query($mydb,$sql);
if ($retour === FALSE) {
	echo "<br/>La requête échoué:$sql\n";
} else {
	echo "<br/>";
	$matches=0;
	$retour1 = mysqli_query($mydb,$sql);  # pourquoi refaire une query ici ???
	if (!$enreg = mysqli_fetch_array($retour1, MYSQLI_BOTH)) {  # not found in lx
		echo "$word absent des lexèmes, recherche dans les variantes<br />\n";
		$sql_va="SELECT id FROM va WHERE va.va = '$word'";
		$retva = mysqli_query($mydb,$sql_va);
		if ($retva != FALSE) {
			$va_idlist="";
			while ($enreg_va = mysqli_fetch_array($retva, MYSQLI_BOTH)) {
    				$nva+=1;
    				$va_idlist=$va_idlist.$enreg_va["id"].", ";
    			}
    			if ($va_idlist!="") {
    				$va_idlist=chop($va_idlist,", ");
    				$sql = "SELECT * FROM lx WHERE lx.id IN ($va_idlist)";
    				$retour = mysqli_query($mydb,$sql);
				if ($retour === FALSE) {
					echo "<br/>La requête a échoué:$sql\n";
				}
    			}
    			else {
    				echo "$word absent des variantes, recherche dans les \"variantes à éviter\"<br>\n";
    				$sql_ve="SELECT id FROM ve WHERE ve.ve = '$word'";
				$retve = mysqli_query($mydb,$sql_ve);
				if ($retve != FALSE) {
					$ve_idlist="";
					while ($enreg_ve = mysqli_fetch_array($retve, MYSQLI_BOTH)) {
		    				$nve+=1;
		    				$ve_idlist=$ve_idlist.$enreg_ve["id"].", ";
		    			}
		    			if ($ve_idlist!="") {
		    				$ve_idlist=chop($ve_idlist,", ");
		    				$sql = "SELECT * FROM lx WHERE lx.id IN ($ve_idlist)";
		    				$retour = mysqli_query($mydb,$sql);
						if ($retour === FALSE) {
							echo "<br/>La requête a échoué:$sql\n";
						}
		    			}
		    			else {
		    				echo "$word absent des \"variantes à éviter\"<br>\n";
		    			}
		    		}
    			}
		}

	}

	while ($enreg = mysqli_fetch_array($retour, MYSQLI_BOTH)) {
		$matches+=1;
		$gloss=$enreg["gf"];
		if (array_key_exists($gloss,$dictgl)) {$gloss=$dictgl[$gloss];}
		else {$gloss=str_replace("."," ",$gloss);}
    		echo "<small>".$enreg["id"]."</small> <b>".$enreg["lx"]."</b> ".$dictps[$enreg["ps"]]." : <b>$gloss</b><br />\n";
    		echo "<ul id='lx'>\n";
    		echo "<li><i>glose désamb.: ".$enreg["mmc"]."</i></li>\n";
    		# .. autres données
    		$lt=$enreg["lt"];
    		if ($lt != "") {echo "<li>litt.: $lt</li>\n";}
    		$ph=$enreg["ph"];
    		if ($ph != "") {echo "<li>phon.: $ph</li>\n";}
    		$bw=$enreg["bw"];
    		if ($bw != "") {echo "<li>empr.: $bw</li>\n";}
    		$di=$enreg["di"];
    		if ($di != "") {
    			if (array_key_exists($di,$dictdi)) {$di=$dictdi[$di];}
    			echo "<li>dialecte: $di</li>\n";}
    		$lat=$enreg["lat"];
    		if ($lat != "") {echo "<li>nom latin: $lat</li>\n";}
    		$vl=$enreg["vl"];
    		if ($vl != "") {
    			if (array_key_exists($vl,$dictvl)) {$vl=$dictvl[$vl];}
    			echo "<li>Valeur: $vl</li>\n";
    		}
    		$smf=$enreg["smf"];
    		if ($smf != "") {echo "<li>$smf</li>\n";}
    		$usf=$enreg["usf"];
    		if ($usf != "") {echo "<li>usage: $usf</li>\n";}
    		# togow
    		$dm=$enreg["dm"]; 
    		if ($dm != "") {echo "<li>empr.: $dm</li>\n";}
    		# jamuw
    		$resp=$enreg["resp"];
    		if ($resp != "") {echo "<li>adresse respectueuse: $resp</li>\n";}
    		$equ=$enreg["equ"];
    		if ($equ != "") {echo "<li>équivalent à: $equ</li>\n";}
    		$equf=$enreg["equf"];
    		if ($equf != "") {echo "<li>équivalent féminin: $equf</li>\n";}
    		$equm=$enreg["equm"];
    		if ($equm != "") {echo "<li>équivalent masculin: $equm</li>\n";}
    		$sen=$enreg["sen"];
    		if ($sen != "") {echo "<li>cousin de plaisanterie: $sen</li>\n";}
    		$eth=$enreg["eth"];
    		if ($eth != "") {echo "<li>ethnie: $eth</li>\n";}
    		$cast=$enreg["cast"];
    		if ($cast != "") {echo "<li>caste: $cast</li>\n";}
    		$reg=$enreg["reg"];
    		if ($reg != "") {echo "<li>région: $reg</li>\n";}
    		$ttm=$enreg["ttm"];
    		if ($ttm != "") {echo "<li>totem: $ttm</li>\n";}

    		$sql_va="SELECT * FROM va WHERE va.id = ".$enreg["id"];
    		#echo "<br>\nsql_va=$sql_va";
    		$retva=mysqli_query($mydb,$sql_va);
    		if ($retva != FALSE) {
    			$vatxt="";
    			$nva=0;
    			while ($enreg_va = mysqli_fetch_array($retva, MYSQLI_BOTH)) {
    				$nva+=1;
    				$di=$enreg_va["di"];
    				if ($di !="") {
    					if (array_key_exists($di,$dictdi)) {$di=$dictdi[$di];}
    					$di="<i>$di</i>";}
    				$vatxt=$vatxt.$enreg_va["va"]."$di, ";
    			}
    			$vatxt=chop($vatxt,", ");  # remove last comma
    			if ($vatxt !="") {
    				echo "<li>variante";
    				if ($nva>1) echo "s";
    				echo " : $vatxt</li>\n";
    			}
    		}
    		else {echo "\nerreur sur $sql_va \n";}

    		$sql_ve="SELECT * FROM ve WHERE ve.id = ".$enreg["id"];
    		#echo "<br>\nsql_ve=$sql_ve";
    		$retve=mysqli_query($mydb,$sql_ve);
    		if ($retve != FALSE) {
    			$vetxt="";
    			$nve=0;
    			while ($enreg_ve = mysqli_fetch_array($retve, MYSQLI_BOTH)) {
    				$nve+=1;
    				#echo "<br>\n$nve ".$enreg_ve["ve"];
    				$di=$enreg_ve["di"];
    				#echo "<br>\ndi='$di' ";
    				if ($di !="") {
    					if (array_key_exists($di,$dictdi)) {$di=$dictdi[$di];}
    					$di="<i>$di</i>";}
    				$vetxt=$vetxt.$enreg_ve["ve"]."$di, ";
    				#echo "<br>\nvetxt: $vetxt";
    			}
    			$vetxt=chop($vetxt,", ");  # remove last comma
    			if ($vetxt !="") {
    				if ($nve>1) { 
    					echo "<li>variantes \"à éviter\"";
    				}
    				else {
    					echo "<li>variante \"à éviter\"";
    				}
    				echo " : $vetxt</li>\n";
    			}
    		}
    		else {echo "\nerreur sur $sql_ve \n";}

    		$an=$enreg["an"];
    		if ($an != "") {echo "<li>antonyme: $an</li>\n";}

    		$sql_sy="SELECT * FROM sy WHERE sy.id = ".$enreg["id"];
    		#echo "<br>\nsql_sy=$sql_sy";
    		$retsy=mysqli_query($mydb,$sql_sy);
    		if ($retsy != FALSE) {
    			$sytxt="";
    			$nsy=0;
    			while ($enreg_sy = mysqli_fetch_array($retsy, MYSQLI_BOTH)) {
    				$nsy+=1;
                                $sylink=$enreg_sy["sy"];
                                $idlxsy=$enreg_sy["idlxsy"];
                                if ($idlxsy!=0) {
                                        $sylink="<a href='$querylink?id=$idlxsy'>$sylink</a>";
                                }
                                $sydi=$enreg_sy["di"];
                                if $sydi=="":   $sytxt=$sytxt.$sylink.", ";
    				else:           $sytxt=$sytxt.$sylink."<i>$sydi</i>, ";
    			}
    			$sytxt=chop($sytxt,", ");  # remove last comma
    			if ($sytxt !="") {
    				echo "<li>synonyme";
    				if ($nsy>1) echo "s";
    				echo " : $sytxt</li>\n";
    			}
    		}
    		else {echo "\nerreur sur $sql_sy \n";}

                $cql=$enreg["cql"];
                $occ=$enreg["occ"];
                if ($cql!="") { 
                        list($cqllx,$cqlps,$cqlgf)=explode(":",$cql);
                        if ($cqlps=="mrph") {
                                $nosketch="http://cormande.huma-num.fr/corbama/#concordance?corpname=corbama-net-tonal&tab=advanced&queryselector=cql&attrs=word&viewmode=kwic&attr_allpos=all&shorten_refs=1&glue=1&gdexcnt=300&itemsPerPage=20&structs=s%2Cg&refs=%3Ddoc.id&default_attr=lemma&showresults=1&f_tab=basic&f_showrelfrq=1&operations=%5B%7B%22name%22%3A%22cql%22%2C%22arg%22%3A%22%5Btag%3D%5C%22".$cqlgf."%5C%22%5D%22%2C%22query%22%3A%7B%22queryselector%22%3A%22cqlrow%22%2C%22cql%22%3A%22%5Btag%3D%5C%22".$cqlgf."%5C%22%5D%22%2C%22default_attr%22%3A%22lemma%22%7D%7D%5D";}
                        else {
                                $nosketch="http://cormande.huma-num.fr/corbama/#concordance?corpname=corbama-net-non-tonal&tab=advanced&queryselector=cql&attrs=word%2Ctag%2Cgloss&viewmode=kwic&attr_allpos=kw&shorten_refs=1&glue=1&gdexcnt=300&itemsPerPage=20&structs=s%2Cg&refs=%3Ddoc.id%2C%23&default_attr=lemma&showresults=1&f_tab=basic&f_showrelfrq=1&operations=%5B%7B%22name%22%3A%22cql%22%2C%22arg%22%3A%22%5Bword%3D%5C%22(%3Fi)".$cqllx.".*%5C%22%20%26%20lemma%3D%5C%22".$cqllx."%5C%22%20%26%20tag%3D%5C%22".$cqlps."%5C%22%20%26%20gloss%3D%5C%22".$cqlgf."%5C%22%5D%22%2C%22query%22%3A%7B%22queryselector%22%3A%22cqlrow%22%2C%22cql%22%3A%22%5Bword%3D%5C%22(%3Fi)".$cqllx.".*%5C%22%20%26%20lemma%3D%5C%22".$cqllx."%5C%22%20%26%20tag%3D%5C%22".$cqlps."%5C%22%20%26%20gloss%3D%5C%22".$cqlgf."%5C%22%5D%22%2C%22default_attr%22%3A%22lemma%22%7D%7D%5D";}

                        if ($occ>1) {echo "<li>Corbama-net: $occ occurrences <a href=\"$nosketch\" target=_blank>(ici)</a></li>\n";}
                        else {echo "<li>Corbama-net: une occurrence <a href=\"$nosketch\" target=_blank>(ici)</a></li>\n";}
                }

                echo "</ul>\n";
    		# fin des données lx

    		$sql_retex="SELECT * from lxx where lxx.id = ".$enreg["id"];
    		#echo "<br>\nsql_retex: $sql_retex \n";
    		$retex=mysqli_query($mydb,$sql_retex);
    		if ($retex != FALSE) {
    			while ($enreg_ex = mysqli_fetch_array($retex, MYSQLI_BOTH)) {
    				echo "<ul id='exempleslx'>\n";
    				if ($enreg_ex["exf"] != "") {
    					echo "<li>".$enreg_ex["ex"]."\n<ul id='exf'>\n<li>".$enreg_ex["exf"]."</li></ul>\n</li>\n";
    				}
    				else {
    					echo "<li>".$enreg_ex["ex"]."</li>\n";
    					}
    				echo "</ul>\n";
    			}
    			
    		}
    		else { echo "\nerreur sur $sql_retex \n";}

                # IMAGES
                $sql_retimg="SELECT * from lximg where lximg.id = ".$enreg["id"];
                #echo "<br>\nsql_retimg: $sql_retimg \n";
                $retimg=mysqli_query($mydb,$sql_retimg);
                if ($retimg != FALSE) {
                        while ($enreg_img = mysqli_fetch_array($retimg, MYSQLI_BOTH)) {
                                echo "<ul id='lximg'>\n";
                                $urlimg=$enreg_img["urlimg"];
                                $urlimg=str_replace("{jpg}","http://www.mali-pense.net/IMG/jpg",$urlimg);
                                $urlimg=str_replace("{png}","http://www.mali-pense.net/IMG/png",$urlimg);
                                $urlimg=str_replace("{webp}","http://www.mali-pense.net/IMG/webp",$urlimg);
                                $urlimg=str_replace("{cache}","http://www.mali-pense.net/local/cache-vignettes",$urlimg);
                                $refimg=$enreg_img["refimg"];
                                if ($refimg!="") {$refimg="<a href='$refimg' target=_blank>";$closea="</a>";}
                                else {$closea="";}
                                $txtimg=$enreg_img["txtimg"];
                                if ($txtimg!="") {$txtimg="<br>$txtimg<br>";}
                                echo "$refimg<img src='$urlimg'>$closea $txtimg";
                                echo "</ul>\n";
                        }                      
                }
                else { echo "\nerreur sur $sql_retimg \n";}

                # AUDIOS
                $sql_retaudio="SELECT * from lxaudio where lxaudio.id = ".$enreg["id"];
                #echo "<br>\nsql_retaudio: $sql_retaudio \n";
                $retaudio=mysqli_query($mydb,$sql_retaudio);
                if ($retaudio != FALSE) {
                        while ($enreg_audio = mysqli_fetch_array($retaudio, MYSQLI_BOTH)) {
                                echo "<ul id='lxaudio'>\n";
                                $urlaudio=$enreg_audio["urlaudio"];
                                $urlaudio=str_replace("{mp3}","http://www.mali-pense.net/IMG/mp3",$urlaudio);
                                $urlaudio=str_replace("{wav}","http://www.mali-pense.net/IMG/wav",$urlaudio);
                                $urlaudio=str_replace("{mp4}","http://www.mali-pense.net/IMG/mp4",$urlaudio);
                                $refaudio=$enreg_audio["refaudio"];
                                if ($refaudio!="") {$refaudio="<a href='$refaudio' target=_blank>";$closea="</a>";}
                                else {$closea="";}
                                $txtaudio=$enreg_audio["txtaudio"];
                                if ($txtaudio!="") {
                                        $txtaudio=str_replace("{refVVZD}"," <i class=gzd><a>ↈ</a></i>",$txtaudio);
                                        $txtaudio=str_replace("{refVVAM}"," <i class=gam><a>ↈ</a></i>",$txtaudio);
                                        $txtaudio=str_replace("{refVVKC}","  <i class=gsv><a>ↈ</a></i>",$txtaudio);
                                        $txtaudio=str_replace("{refVVSK}","  <i class=gkc><a>ↈ</a></i>",$txtaudio);
                                        $txtaudio="<br><small>$refaudio$txtaudio$closea</small><br>";
                                }
                                if (substr($urlaudio,0,1)!="<") {
                                        echo "<audio src='$urlaudio' preload=\"none\" controls></audio> $txtaudio";
                                }
                                else {  # it's a video! but no need to lazyload here
                                        echo "$urlaudio $txtaudio";
                                }
                                echo "</ul>\n";
                        }                      
                }
                else { echo "\nerreur sur $sql_retaudio \n";}

    		$sql_gvf="SELECT * from gvf where gvf.id = ".$enreg["id"];
    		#echo "<br>\nsql_gvf: $sql_gvf. \n";
    		$ret2=mysqli_query($mydb,$sql_gvf);
    		if ($ret2 != FALSE) {
    			while ($enreg_gvf = mysqli_fetch_array($ret2, MYSQLI_BOTH)) {
    				$ms=$enreg_gvf["ms"];
    				if ($ms == 0) {$mss="";}
    				else {$mss="$ms ";}
    				$gvf=$enreg_gvf["gvf"];
				echo "<ul id='gvf'>\n<li>$mss<b>$gvf</b>\n";
				echo "<ul id='infosgvf'>\n"; # autres infos sur les gvf
				$vl=$enreg_gvf["vl"];
		    		if ($vl != "") {
		    			if (array_key_exists($vl,$dictvl)) {$vl=$dictvl[$vl];}
		    			echo "<li>valeur: $vl</li>\n";
		    		}
		    		$smf=$enreg_gvf["smf"];
		    		if ($smf != "") {echo "<li>$smf</li>\n";}
		    		$usf=$enreg_gvf["usf"];
		    		if ($usf != "") {echo "<li>usage: $usf</li>\n";}
		    		$lat=$enreg_gvf["lat"];
		    		if ($lat != "") {echo "<li>nom latin: $lat</li>\n";}
				$sql_sy="SELECT * FROM gvfsy WHERE gvfsy.idgvf = ".$enreg_gvf["idgvf"];
		    		$retsy=mysqli_query($mydb,$sql_sy);
		    		if ($retsy != FALSE) {
		    			$sytxt="";
		    			$nsy=0;
		    			while ($enreg_sy = mysqli_fetch_array($retsy, MYSQLI_BOTH)) {
		    				$nsy+=1;
                                                $sylink=$enreg_sy["sy"];
                                                $idlxsy=$enreg_sy["idlxsy"];
                                                if ($idlxsy!=0) {
                                                        $sylink="<a href='$querylink?id=$idlxsy'>$sylink</a>";
                                                }
		    				$sytxt=$sytxt.$sylink.", ";
		    			}
		    			$sytxt=chop($sytxt,", ");  # remove last comma
		    			if ($sytxt !="") {
		    				echo "<li>synonyme";
		    				if ($nsy>1) echo "s";
		    				echo " : $sytxt</li>\n";
		    			}
		    		echo "</ul>\n";
		    		}
		    		else {echo "\nerreur sur $sql_sy \n";}

		    		# exemples sur les gvf - si existent
				$sql_retex="SELECT * from gvfx where gvfx.idgvf = ".$enreg_gvf["idgvf"];
				#echo "\nGVF sql_retex: $sql_retex \n";
				$retex=mysqli_query($mydb,$sql_retex);
				if ($retex != FALSE) {
		    			while ($enreg_ex = mysqli_fetch_array($retex, MYSQLI_BOTH)) {
		    				echo "<ul id='exemplesgvf'>\n";
		    				if ($enreg_ex["exf"] != "") {
		    					echo "<li>".$enreg_ex["ex"]."\n<ul id='exf'>\n<li>".$enreg_ex["exf"]."</li></ul>\n</li>\n";
		    				}
		    				else {
		    					echo "<li>".$enreg_ex["ex"]."</li>\n";
		    					}
		    				echo "</ul>\n";
		    			}
				}
				else { echo "\nerreur sur $sql_retex \n";}
                                
                                # IMAGES
                                $sql_retimg="SELECT * from gvfimg where gvfimg.idgvf = ".$enreg_gvf["idgvf"];
                                $retimg=mysqli_query($mydb,$sql_retimg);
                                if ($retimg != FALSE) {
                                        while ($enreg_img = mysqli_fetch_array($retimg, MYSQLI_BOTH)) {
                                                echo "<ul id='lximg'>\n";
                                                $urlimg=$enreg_img["urlimg"];
                                                $urlimg=str_replace("{jpg}","http://www.mali-pense.net/IMG/jpg",$urlimg);
                                                $urlimg=str_replace("{png}","http://www.mali-pense.net/IMG/png",$urlimg);
                                                $urlimg=str_replace("{webp}","http://www.mali-pense.net/IMG/webp",$urlimg);
                                                $urlimg=str_replace("{cache}","http://www.mali-pense.net/local/cache-vignettes",$urlimg);
                                                $refimg=$enreg_img["refimg"];
                                                if ($refimg!="") {$refimg="<a href='$refimg' target=_blank>";$closea="</a>";}
                                                else {$closea="";}
                                                $txtimg=$enreg_img["txtimg"];
                                                if ($txtimg!="") {$txtimg="<br>$txtimg<br>";}
                                                echo "$refimg<img src='$urlimg'>$closea $txtimg";
                                                echo "</ul>\n";
                                        }                      
                                }
                                else { echo "\nerreur sur $sql_retimg \n";}

                                # AUDIOS
                                $sql_retaudio="SELECT * from gvfaudio where gvfaudio.idgvf = ".$enreg_gvf["idgvf"];
                                $retaudio=mysqli_query($mydb,$sql_retaudio);
                                if ($retaudio != FALSE) {
                                        while ($enreg_audio = mysqli_fetch_array($retaudio, MYSQLI_BOTH)) {
                                                echo "<ul id='lxaudio'>\n";
                                                $urlaudio=$enreg_audio["urlaudio"];
                                                $urlaudio=str_replace("{mp3}","http://www.mali-pense.net/IMG/mp3",$urlaudio);
                                                $urlaudio=str_replace("{wav}","http://www.mali-pense.net/IMG/wav",$urlaudio);
                                                $urlaudio=str_replace("{mp4}","http://www.mali-pense.net/IMG/mp4",$urlaudio);
                                                $refaudio=$enreg_audio["refaudio"];
                                                if ($refaudio!="") {$refaudio="<a href='$refaudio' target=_blank>";$closea="</a>";}
                                                else {$closea="";}
                                                $txtaudio=$enreg_audio["txtaudio"];
                                                if ($txtaudio!="") {
                                                        $txtaudio=str_replace("{refVVZD}"," <i class=gzd><a>ↈ</a></i>",$txtaudio);
                                                        $txtaudio=str_replace("{refVVAM}"," <i class=gam><a>ↈ</a></i>",$txtaudio);
                                                        $txtaudio=str_replace("{refVVKC}","  <i class=gsv><a>ↈ</a></i>",$txtaudio);
                                                        $txtaudio=str_replace("{refVVSK}","  <i class=gkc><a>ↈ</a></i>",$txtaudio);
                                                        $txtaudio="<br><small>$refaudio$txtaudio$closea</small><br>";
                                                }
                                                if (substr($urlaudio,0,1)!="<") {
                                                        echo "<audio src='$urlaudio' preload=\"none\" controls></audio> $txtaudio";
                                                }
                                                else {  # it's a video! but no need to lazyload here
                                                        echo "$urlaudio $txtaudio";
                                                }
                                                echo "</ul>\n";
                                        }                      
                                }
                                else { echo "\nerreur sur $sql_retaudio \n";}


				echo "</li>\n</ul>\n";  # ferme les gvf
			}
    		}
		else { echo "\nerreur sur $sql_gvf\n";}
    	
	}
	if ($id==""){
                if ($matches == 0) {
		echo "rien n'a été trouvé à propos de: $word";
        	}
        	else {
        		echo "$matches occurrence";
        		if ($matches>1) {echo "s";}
                }
	}
}
} # fermeture du test sur word=""
} # a passé les validations

$sql_dates="SELECT * from dates";
$rdates=mysqli_query($mydb,$sql_dates);
if ($rdates != FALSE) {
        while ($enreg_dates = mysqli_fetch_array($rdates, MYSQLI_BOTH)) {
                $export=$enreg_dates["export"];
                $corbama=$enreg_dates["corbama"];
                $medias_img=$enreg_dates["medias_img"];
                $medias_audio=$enreg_dates["medias_audio"];
                if ($export!="") {echo "<small><ul>\nsources:<li>\nBamadaba: $export</li>\n";}
                if ($corbama!="") {echo "<li>\nCorbama: $corbama</li>\n";}
                if ($medias_img!="") {echo "<li>\nimages: $medias_img</li>\n";}
                if ($medias_audio!="") {echo "<li>\naudios, vidéos: $medias_audio</li>\n";}
                echo "</ul></small>";
        }
}
// Et pour mettre fin à la connexion
mysqli_close();
?>
<br/><br/><br/><br/><br/>
</div>
</body>
</html>