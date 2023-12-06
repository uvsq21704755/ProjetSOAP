# Utilitaires
import random
import os
import asyncio
import requests
import threading
import xml.etree.ElementTree as ET


# Spyne, WSGI, Flask
from spyne import Application, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import spyne.server.wsgi as wsgi
from spyne.util.wsgi_wrapper import WsgiMounter
from wsgiref.simple_server import make_server
from flask import Flask, render_template, request
from suds.client import Client


# Import des services
import serviceExtraction
import serviceSolvabilite
import serviceEvaluation
import serviceDecision


BDclient = "../static/client.json"
CHEMIN_RACINE = "./EvaluationDemandePretImmobilier/services/"


class serviceComposite(ServiceBase):

    def recupDossier(numDoss: int):
        if os.path.exists(str(CHEMIN_RACINE)+"demandeTxt/"+str(numDoss)+".txt"):
            nouvelleDemandeClient(numDoss)


def nouvelleDemandeClient(numDoss: int):

    wsdl_url = "http://localhost:8000/serviceExtraction?wsdl"
    wsdl_headers = {'Content-Type': 'text/xml'}
    requests.get(wsdl_url, headers=wsdl_headers).text
    
    client = Client(wsdl_url)
    client.service.extractionTxt(str(CHEMIN_RACINE)+"demandeTxt/"+str(numDoss)+".txt")
    soapRecu = client.last_received()

    lienSOAP = str(CHEMIN_RACINE)+"soap/extraction.xml"
    soapFichier = open(lienSOAP,'w',encoding="utf-8")
    soapFichier.write(str(soapRecu))
    soapFichier.close()
    
    tree = ET.parse(lienSOAP)
    root = tree.getroot()
    namespace = {'soap11env': 'http://schemas.xmlsoap.org/soap/envelope/', 'tns': 'serviceExtraction'}
    lienXML = str(root.find('.//tns:extractionTxtResult', namespaces=namespace).text)



    wsdl_url2 = "http://localhost:8000/serviceSolvabilite?wsdl"
    client = Client(wsdl_url2)
    client.service.verificationSolvabilite(lienXML)
    soapRecu2 = client.last_received()
    
    lienSOAP2 = str(CHEMIN_RACINE)+"soap/solvabilite.xml"
    soapFichier2 = open(lienSOAP2,'w',encoding="utf-8")
    soapFichier2.write(str(soapRecu2))
    soapFichier2.close()
    
    
    
    wsdl_url3 = "http://localhost:8000/serviceEvaluation?wsdl"
    client = Client(wsdl_url3)
    client.service.evaluationPropriete(lienXML)
    soapRecu3 = client.last_received()
    
    lienSOAP3 = str(CHEMIN_RACINE)+"soap/evaluation.xml"
    soapFichier3 = open(lienSOAP3,'w',encoding="utf-8")
    soapFichier3.write(str(soapRecu3))
    soapFichier3.close()
    
    
    
    wsdl_url4 = "http://localhost:8000/serviceDecision?wsdl"
    client = Client(wsdl_url4)
    client.service.decisionApprobation(lienXML)
    soapRecu4 = client.last_received()
    
    lienSOAP4 = str(CHEMIN_RACINE)+"soap/decision.xml"
    soapFichier4 = open(lienSOAP4,'w',encoding="utf-8")
    soapFichier4.write(str(soapRecu4))
    soapFichier4.close()

    tree = ET.parse(lienSOAP4)
    root = tree.getroot()
    namespace = {'soap11env': 'http://schemas.xmlsoap.org/soap/envelope/', 'tns': 'serviceDecision'}
    lienTXT = str(root.find('.//tns:decisionApprobationResult', namespaces=namespace).text)
    
    return

wsdl_app = Application([serviceComposite],
    tns = 'http://localhost:8000',
    in_protocol = Soap11(validator='lxml'),
    out_protocol = Soap11()
)

if __name__ == '__main__':
    
    def creerSite():
        app = Flask(__name__)

        @app.route('/')
        def pageAccueil():
            return render_template('accueil.html')

        @app.route('/connexion.html')
        def pageConnexion():
            return render_template('connexion.html')
        
        @app.route('/formulaire.html')
        def pageFormulaire():
            return render_template('formulaire.html')

        @app.route('/confirmation.html')
        def pageConfirmation():
            return render_template('confirmation.html')
        
        @app.route('/disponible.html')
        def pageDisponible():
            return render_template('disponible.html')
        
        @app.route('/traitement.html')
        def pageTraitement():
            return render_template('traitement.html')
        
        @app.route('/introuvable.html')
        def pageIntrouvable():
            return render_template('introuvable.html')
        
        @app.route('/enregistrer', methods=['POST'])
        async def enregistrer():
            
            nom = request.form['nom']
            adresse = request.form['adresse']
            email = request.form['email']
            telephone = request.form['telephone']
            montantpret = request.form['montantpret']
            dureepret = request.form['dureepret']
            descriptionpropriete = request.form['descriptionpropriete']
            revenumensuel = request.form['revenumensuel']
            depensemensuelle = request.form['depensemensuelle']
            idbanque = request.form['idbanque']
            idpropriete = request.form['idpropriete']
            
            
            numDoss = random.randint(0,1000000)
            nomFichier = str(numDoss)+".txt"

            while os.path.exists(nomFichier):

                numDoss = random.randint(0,1000000)
                nomFichier = str(numDoss)+".txt"

            chemin = CHEMIN_RACINE+"demandeTxt/"+nomFichier
            
            
            fichierTxt = open(str(chemin),"w",encoding = "UTF-8") 
            fichierTxt.write(f'Nom du Client: {nom}\n')
            fichierTxt.write(f'Adresse: {adresse}\n')
            fichierTxt.write(f'Email: {email}\n')
            fichierTxt.write(f'Numéro de Téléphone: {telephone}\n')
            fichierTxt.write(f'Montant du Prêt Demandé: {montantpret}\n')
            fichierTxt.write(f'Durée du Prêt: {dureepret}\n')
            fichierTxt.write(f'Description de la Propriété: {descriptionpropriete}\n')
            fichierTxt.write(f'Revenu Mensuel: {revenumensuel}\n')
            fichierTxt.write(f'Dépenses Mensuelles: {depensemensuelle}\n')
            fichierTxt.write(f'Numero de compte bancaire: {idbanque}\n')
            fichierTxt.write(f'Référence de la propriété: {idpropriete}\n')
            fichierTxt.close()

            htmlResponse = open(CHEMIN_RACINE+"templates/confirmation.html","r",encoding = "UTF-8")
            strHtmlResponse = htmlResponse.read()
            strHtmlResponse = strHtmlResponse.replace("123456789", str(numDoss))
            htmlResponse.close()

            thread = threading.Thread(target = serviceComposite.recupDossier, args = (numDoss,))
            thread.start()

            # Retourne la page web réponse à l'interface
            return strHtmlResponse  
        
        @app.route('/resultat', methods = ['POST'])
        def resultat():

            numerodossier = request.form['numerodossier']
            nomFichier = str(numerodossier)+".txt"
            chemin1 = str(CHEMIN_RACINE+"demandeTxt/"+nomFichier)
            chemin2 = str(CHEMIN_RACINE+"reponseTxt/"+nomFichier)
            
            if os.path.exists(str(chemin1)):
                
                if os.path.exists(str(chemin2)):
                    
                    return open(str(CHEMIN_RACINE+"templates/disponible.html"),"r", encoding = "UTF-8").read().replace("REPONSE", open(str(CHEMIN_RACINE+"reponseTxt/"+nomFichier),"r", encoding = "UTF-8").read().replace("\n","<br></br>"))
                else:
                    return open(str(CHEMIN_RACINE+"templates/traitement.html"),"r", encoding = "UTF-8").read()
            else:
                return open(str(CHEMIN_RACINE+"templates/introuvable.html"),"r", encoding = "UTF-8").read()
            return None

        return app

    wsgi_app = WsgiApplication(wsdl_app)
    
    wsgi_app = WsgiMounter({
        '': creerSite(),
        'serviceExtraction': serviceExtraction.wsdl_appExtraction,
        'serviceSolvabilite': serviceSolvabilite.wsdl_appSolvabilite,
        'serviceEvaluation': serviceEvaluation.wsdl_appEvaluation,
        'serviceDecision': serviceDecision.wsdl_appDecision
    })
    
    server = make_server('localhost', 8000, wsgi_app)
    server.serve_forever()




