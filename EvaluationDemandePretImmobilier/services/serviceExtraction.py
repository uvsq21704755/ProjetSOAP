import logging
import sys
from spyne import Application, rpc, srpc, ServiceBase, Integer, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
import re
import os
import xml.etree.ElementTree as ET
from wsgiref.simple_server import make_server



def extractionDonnees(cheminFichierTxt):
    with open(cheminFichierTxt, 'r') as fichier:
        fichierTxt = fichier.read()
    infosExtraites = re.findall(r'(?<=:\s)[a-zA-ZàéÉ0-9\'\,\-\sA-Z@.]+\n', fichierTxt)
    for i in range(0,len(infosExtraites)):
        infosExtraites[i] = infosExtraites[i].replace("\n",'')
        
    print(infosExtraites)
    return infosExtraites



def ecritureXML(cheminFichierTxt, donnees):
    
    client = ET.Element("client")
    
    numDossier = ET.SubElement(client, "numDossier")
    idDossier=os.path.basename(cheminFichierTxt)
    idDossier=idDossier.replace(".txt","")
    numDossier.text = str(idDossier)
    
    nom = ET.SubElement(client, "nom")
    nom.text = donnees[0]
    
    adresse = ET.SubElement(client, "adresse")
    adresse.text = donnees[1]
        
    email = ET.SubElement(client, "email")
    email.text = donnees[2]
    
    numTelephone = ET.SubElement(client, "numTelephone")
    numTelephone.text = donnees[3]
    
    montantPret = ET.SubElement(client, "montantPret")
    montantPret.text = donnees[4]

    dureePret = ET.SubElement(client, "dureePret")
    dureePret.text = donnees[5]

    descriptionPropriete = ET.SubElement(client, "descriptionPropriete")
    descriptionPropriete.text = donnees[6]
    
    revenuMensuel = ET.SubElement(client, "revenuMensuel")
    revenuMensuel.text = donnees[7]

    depenseMensuelle = ET.SubElement(client, "depenseMensuelle")
    depenseMensuelle.text = donnees[8]
    
    idBanque = ET.SubElement(client, "idBanque")
    idBanque.text = donnees[9]
    
    idPropriete = ET.SubElement(client, "idPropriete")
    idPropriete.text = donnees[10]
        
    arbre = ET.tostring(client, encoding="unicode")
    
    lienXML = "./EvaluationDemandePretImmobilier/services/demandeXml/"+idDossier+".xml"
    nomFichierXML = open(lienXML, "w", encoding="utf-8")
    nomFichierXML.write(str(arbre))
    nomFichierXML.close()
                
    print("Ecriture du fichier XML terminée")
                
    return lienXML
    
    

class serviceExtraction(ServiceBase): 
    @srpc(Unicode, _returns=Unicode)
    def extractionTxt(cheminFichierTxt):
        print("Chemin txt :"+cheminFichierTxt)
        cheminFichierXML=ecritureXML(cheminFichierTxt, extractionDonnees(cheminFichierTxt))
        print("Chemin xml :"+cheminFichierXML)
        return cheminFichierXML
   

wsdl_appExtraction = Application([serviceExtraction],
    tns='serviceExtraction',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)