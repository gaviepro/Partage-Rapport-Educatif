import os
from re import template 
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import oudjirasign as osy
from datetime import datetime

app = Flask(__name__)
 
today = datetime.today()
#Réglage heure Date limite pour chaque filiere (annee, mois,jour) 
limite_info = datetime(2022, 12, 12, 23, 59, 59)
limite_bio = datetime(2023, 2, 12, 23, 59, 59)
limite_phy = datetime(2023, 3, 12, 23, 59, 59)

#Variable des chemins des differents dossier
grp_info ="rendu/info/groupe_"
grp_bio ="rendu/bio/groupe_"
grp_phy ="rendu/phy/groupe_"

#Generation des clés de signature
privatekey, publickey = osy.generatersakeys()
privatekey= osy.importPrivateKey(privatekey)
public= osy.importPublicKey(publickey)

#Fonction pour verifier la date limite de chaque filliere
def check_date(parcour) :
    match parcour : 
        case "info":
            if limite_info > today :
                return render_template("informatique.html")
            else :
                return render_template("limite.html")
        case "bio":
            if limite_bio > today :
                return render_template("biologie.html")
            else :
                return render_template("limite.html")
        case "phy":
            if limite_phy>today:
                return render_template("physique.html")
            else :
                return render_template("limite.html")
        case _:
            return 'null'

#Fonction de gestion des sauvegardes de fichier par rapport aux groupes et parcours 
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

#Fonction reponse du formulaire et signature du doc
def formulaire(parcour):
    resultat = request.form
    groupe = resultat['Groupe']
    fichier = request.files['fichier']
    if fichier.filename != '' and groupe != '' : 
        filename = secure_filename(fichier.filename)
        #appel fonction pour ranger les fichiers dans les dossiers
        rangement(parcour,groupe,fichier,filename)
        #Signature du fichier en prenant le chemin du fichier defini dans val()
        hash = osy.hacherdocs(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        signature = osy.signerdocs(hash, privatekey)
        return render_template("valide.html",sign = signature)
    else :
        return render_template("invalide.html")

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