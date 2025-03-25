import os
from re import template 

from flask import request_finished, Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import oudjirasign as osy
from datetime import datetime

app = Flask(__name__)

today = datetime.today()

#Réglage heure de la date limite pour chaque filiere (Laureline/Quentin)
#Déclaration et initalisation des variables permettant la modification par l'utilisateur ayant accés
anne_info = 2022
jour_info = 12
mois_info = 12
limite_info =datetime(anne_info, mois_info, jour_info, 23, 59, 59)

anne_bio = 2022
jour_bio = 12
mois_bio = 12
limite_bio =datetime(anne_bio, mois_bio, jour_bio, 23, 59, 59)

anne_phy = 2022
jour_phy = 12
mois_phy = 12
limite_phy=datetime(anne_phy, mois_phy, jour_phy, 23, 59, 59)

#Choix du type par le prof variable global 
type_info =".pdf,.rar"
type_bio =".pdf,.zip"
type_phy = ".pdf"

#Choix du text par le prof global variable
scribe_info = 'Le nom de votre fichier devra avoir cette nomenclature: VX_NOM_PARTICIPANT_NumGroupe X sera remplacé par la version du rendu, si vous rendez pour la première fois "V1_...", pour la deuxieme fois "V2..." etc'
scribe_bio = 'Le nom de votre fichier devra avoir cette nomenclature: VX_NOM_PARTICIPANT_NumGroupeX sera remplacé par la version du rendu, si vous rendez pour la première fois "V1_...", pour la deuxieme fois "V2..." etc'
scribe_phy = 'Le nom de votre fichier devra avoir cette nomenclature: VX_NOM_PARTICIPANT_NumGroupeX sera remplacé par la version du rendu, si vous rendez pour la première fois "V1_...", pour la deuxieme fois "V2..." etc  '

#Fonction permettant de recuperer le formulaire de changement de date, du type et du text des filieres pour modifier les variables global utilisées (Quentin)
#Toujours en separant chaque filiere avec un switch
def change(parcour):
    resultat=request.form
    a=resultat['anne']
    m=resultat['mois']
    j=resultat['jour']
    type1 = resultat['type_1']
    type2 = resultat['type_2']
    type3 = resultat['type_3']
    scribe = resultat['scribe']
    if type3 =="NULL":
        type3 ="" 
    if type2 =="NULL":
        type2 =""
    if type1 =="NULL":
        type1 ="" 
    match parcour :
        case "info":
            global anne_info 
            global jour_info
            global mois_info
            global limite_info
            global type_info
            global scribe_info
            #Gestion d'erreur en cas de date non remplis et modification des variables
            if j!="NULL" and m !="NULL" and a!="NULL":
                jour = int(j)
                mois = int(m)
                annee = int(a)
                anne_info =annee
                jour_info = jour
                mois_info =mois
                limite_info=datetime(anne_info, mois_info, jour_info, 23, 59, 59)
            if type1 =="" and type2 =="" and type3 == "":
                type_info = type_info
            else:
                type_info = type1+","+type2+","+type3 
            if scribe != "":
                scribe_info = scribe
            return render_template("index.html")
        case "bio":
            global anne_bio 
            global jour_bio
            global mois_bio
            global limite_bio
            global type_bio
            global scribe_bio  
            if j!="NULL" and m !="NULL" and a!="NULL":
                jour = int(j)
                mois = int(m)
                annee = int(a)
                anne_bio =annee
                jour_bio = jour
                mois_bio =mois
                limite_bio=datetime(anne_bio, mois_bio, jour_bio, 23, 59, 59)
            if type1 =="" and type2 =="" and type3 == "":
                type_bio = type_bio
            else:
                type_bio = type1+","+type2+","+type3
            if scribe != "":
                scribe_bio = scribe
            return render_template("index.html")
        case "phy":
            global anne_phy 
            global jour_phy
            global mois_phy
            global limite_phy
            global type_phy    
            if j!="NULL" and m !="NULL" and a!="NULL":
                jour = int(j)
                mois = int(m)
                annee = int(a)
                anne_phy =annee
                jour_phy = jour
                mois_phy =mois
                limite_phy=datetime(anne_phy, mois_phy, jour_phy, 23, 59, 59)    
            if type1 =="" and type2 =="" and type3 == "":
                type_phy = type_phy
            else : 
               type_phy = type1+","+type2+","+type3
            if scribe != "":
                scribe_phy = scribe
            return render_template("index.html")
        case _:
            return "NULL"

#Variable des chemins des differents dossier (Quentin/Luigi)
grp_info ="rendu/info/groupe_"
grp_bio ="rendu/bio/groupe_"
grp_phy ="rendu/phy/groupe_"

#Generation des clés de signature (laureline)
privatekey, publickey = osy.generatersakeys()
privatekey= osy.importPrivateKey(privatekey)
public= osy.importPublicKey(publickey)

#tableau de stockage des noms de rendu (Remy)
tabRendu=[]

#Fonction sécurisant au minimum l'acces au changement des modalités de rendu pour les e tudiants (Quentin)
def check_code(code):
    match code :
        case "1234":
            return render_template("modif_info.html",date = limite_info, type = type_info)
        case "1111":
            return render_template("modif_bio.html",date = limite_bio,type = type_bio)
        case "2222":
            return render_template("modif_phy.html",date = limite_phy,type = type_phy)
        case _:
            return render_template("malin.html")

#Fonction pour verifier la date limite de chaque filliere (Laureline)
def check_date(parcour) :
    match parcour : 
        case "info":
            if limite_info > today :
                return render_template("informatique.html",anne=anne_info,mois=mois_info,jour=jour_info,type = type_info,scribe = scribe_info )
            else :
                return render_template("limite.html")
        case "bio":
            if limite_bio > today :
                return render_template("biologie.html",anne=anne_bio,mois=mois_bio,jour=jour_bio,type = type_bio,scribe = scribe_bio)
            else :
                return render_template("limite.html")
        case "phy":
            if limite_phy>today:
                return render_template("physique.html",anne=anne_phy,mois=mois_phy,jour=jour_phy,type = type_phy,scribe = scribe_phy)
            else :
                return render_template("limite.html")
        case _:
            return 'null'

#Fonction de gestion des sauvegardes de fichier par rapport aux groupes et parcours  (Quentin/luigi)
#range les fichiers dans chaques dossiers
def rangement(parcour,grp,fichier,filename):
    match parcour:
        case "info": #Cas pour le dossier Info
            app.config['UPLOAD_FOLDER'] = grp_info + grp
            fichier.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        case "bio" : #Cas pour le dossier Bio
            app.config['UPLOAD_FOLDER'] =grp_bio+grp
            fichier.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        case "phy": #Cas pour le dossier Phy
            app.config['UPLOAD_FOLDER'] =grp_bio+grp
            fichier.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        case _:
            return 'null'

#Fonction reponse du formulaire et signature du doc (TOUT LE MONDE)
def formulaire(parcour):
    resultat = request.form
    groupe = resultat['Groupe']
    fichier = request.files['fichier']
    if fichier.filename != '' and groupe != '' : 
        filename = secure_filename(fichier.filename)
        #appel fonction pour ranger les fichiers dans les dossiers
        rangement(parcour,groupe,fichier,filename)

        #variable contenant la valeur de la taille du fichier rendu en octets
        tailleFichier=str(os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'],filename)))

        #transformation de la variable today en variable string avec les infos de date voulu
        dateRendu=today.strftime("%A %d %B %Y") 

        rendu= open("rendu_"+parcour+"_"+groupe+".txt", 'a')
        rendu.write("\nDate de rendu: "+dateRendu+"\nParcours:"+ parcour+"\nGroupe: "+groupe+'\n')
        rendu.write("\nFichier rendu: "+ filename+ "\nTaille du fichier rendu: "+tailleFichier+" octets \n")
        nomrendu= "rendu_"+parcour+"_"+groupe+".txt"

        #Signature du fichier en prenant le chemin du fichier defini dans val()
        nomrendu = osy.hacherdocs(nomrendu)
        signature = osy.signerdocs(nomrendu, privatekey)
        tabRendu.append(nomrendu)
      
        return render_template("valide.html")
    else :
        return render_template("invalide.html")

#Download du fihcier de depot (Remy/Laureline)
@app.route('/download')
def download():
    indice=len(tabRendu)
    path=tabRendu[indice-1]
    return send_file(path, as_attachment=True)


#Page accueil
@app.route('/')
def depot():
    return render_template("index.html")
@app.route('/accueil')
def accueil():
    return render_template("index.html")

#Page Depot Info
@app.route('/informatique')
def informatique():
    return check_date("info")
#Page Depot Bio   
@app.route('/biologie')
def biologie():
    return check_date("bio")
#Page depot Phy
@app.route('/physique')
def physique():
    return check_date("phy")

#Page de validation de l'envoie des requetes 
@app.route('/valinfo', methods=["POST", "GET"])
def valinfo():
    return formulaire("info")
@app.route('/valbio', methods=["POST", "GET"])
def valbio():
    return formulaire("bio")
@app.route('/valphy', methods=["POST", "GET"])
def valphy():
    return formulaire("phy")

#Gestion page du code des profs 
@app.route('/prof')
def prof():
    return render_template("prof.html")
@app.route('/valprof', methods=["POST", "GET"])
def valprof():
    resultat =request.form
    code = resultat['code']
    return check_code(code)

#Gestion page des modification apporté par le prof
@app.route('/good_info', methods=["POST", "GET"])
def good_info():
    return change("info")
@app.route('/good_bio', methods=["POST", "GET"])
def good_bio():
    return change("bio")
@app.route('/good_phy', methods=["POST", "GET"])
def good_phy():
    return change("phy")