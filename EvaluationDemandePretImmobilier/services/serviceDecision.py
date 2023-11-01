import logging
import sys
from spyne import Application, rpc, srpc, ServiceBase, Integer, Unicode, String, UnsignedInteger
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from wsgiref.simple_server import make_server
import os
import xml.etree.ElementTree as ET

CHEMIN_RACINE = "./EvaluationDemandePretImmobilier/services/"


def recupXML(lienXML):
    
    tree = ET.parse(lienXML)
    root = tree.getroot()
    
    donnees = []
    donnees.append(root.find('.//numDossier').text)
    donnees.append(root.find('.//nom').text)
    donnees.append(root.find('.//montantPret').text)
    donnees.append(root.find('.//dureePret').text)
    donnees.append(root.find('.//score').text)
    donnees.append(root.find('.//decisionScore').text)
    donnees.append(root.find('.//decisionConformite').text)
    donnees.append(root.find('.//estimationValeur').text)
    if (donnees.append(root.find('.//decisionConformite').text)) == 'Non admissible a un pret immobilier':
        donnees.append(root.find('.//raisons').text)
    
    return donnees



def decision(donnees,lienXML):
    
    raisons = ""
    
    #stockage des donnees
    numDossier = donnees[0]
    nom = donnees[1]
    montantPret = int(donnees[2])
    dureePret = donnees[3]
    score = donnees[4]
    decisionScore = donnees[5]
    decisionConformite = donnees[6]
    estimationValeur = int(donnees[7])
    if str(decisionScore) == 'Non admissible a un pret immobilier':
        raisons = donnees[8]
        
        
    
    # Refus sans plus d'analyses :
    motif = "inconnu"
    test = -1
    
    if score == -1:
        motif = "à cause de votre situation financière actuelle"
        test = 0
        
    if decisionConformite == 'Non admissible a un pret immobilier':
        motif = "pour cette adresse immobilière pour la/les raison.s suivante.s :" + raisons
        test = 0
        
    if montantPret > (int(estimationValeur) + 10000):
        motif = "votre demande est supérieure à la moyenne du marché pour un batiment du même type et dans le même secteur"
        test = 0
            
    
    if decisionScore == 'Tres favorable' and decisionConformite == 'Admissible a un pret immobilier':
        test = 1
        
    elif decisionScore == 'Sous conditions' and decisionConformite == 'Admissible a un pret immobilier' :
        test = 1

    elif decisionScore == 'A defendre' and decisionConformite == 'Admissible a un pret immobilier':
        test = 1
        
    else:
        motif = "votre score n'est pas suffisant"
        test = 0
        

    #affichage du bon fichier sur l'interface

    lienTxt = str(CHEMIN_RACINE)+"reponseTxt/"+numDossier+".txt"
    reponseTxt = open(lienTxt,"w")
    
    if test == 0:

        refusTxt = open(str(CHEMIN_RACINE)+"modeles/refus.txt","r")
        lecture = refusTxt.read()
        lecture = lecture.replace("[nom]", str(nom))
        lecture = lecture.replace("[numeroDossier]", str(numDossier))
        lecture = lecture.replace("[motifs]", str(motif))
        refusTxt.close()
    
    else:

        acceptTxt = open(str(CHEMIN_RACINE)+"modeles/acceptation.txt","r")
        lecture = acceptTxt.read()
        lecture = lecture.replace("[nom]", str(nom))
        lecture = lecture.replace("[numeroDossier]", str(numDossier))
        lecture = lecture.replace("[montantPret]", str(montantPret)+" euros")
        lecture = lecture.replace("[dureePret]", str(dureePret)+" ans")
        acceptTxt.close()
        
    reponseTxt.write(lecture) 
    reponseTxt.close()
    
    return lienTxt

class serviceDecision(ServiceBase): 
    @srpc(Unicode,_returns=Unicode)
    def decisionApprobation(lienXML):
        donnees = recupXML(lienXML)
        lienTXT = decision(donnees, lienXML)
        return lienTXT


wsdl_appDecision = Application([serviceDecision],
    tns='serviceDecision',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)