# Utilitaires
import json
import xml.etree.ElementTree as ET
import random
import re

# Spyne
from spyne import Application, ServiceBase, Unicode, srpc
from spyne.protocol.soap import Soap11

nombres_en_texte = {
    "un": "1",
    "deux": "2",
    "trois": "3",
}

def creationDBImmobilier():
    
    lienJSON = "./EvaluationDemandePretImmobilier/services/bdd/immobilier.json"
    
    immobilier = [
        {"idImmobilier": 1, "adresse": "123 Rue de la Liberte, 75001 Paris, France", "age": 9, "normeLegal": 0, "normeReglementaire": 0, "litigesEnCours": 0, "normeElectricite": "NF C 15-100", "normeGaz": "NF P 45-500"},
        {"idImmobilier": 2, "adresse": "45 avenue des Etats-Unis, 78000 Versailles, France", "age": 23, "normeLegal": 1, "normeReglementaire": 1, "litigesEnCours": 1, "normeElectricite":"NF C 14-100" , "normeGaz": ""},
    ]
    
    json_string = json.dumps(immobilier, indent=4) 

    with open(lienJSON, "w") as json_file:
        json_file.write(json_string)
        
    return lienJSON

def creationDBMarcheImmobilier():
    
    lienJSON = "./EvaluationDemandePretImmobilier/services/bdd/marcheImmobilier.json"
    
    marcheImmobilier = [
        {"adresse": "1 Rue Gpasdidee", "codePostal": 75001, "batiment": "Maison", "nbEtage": "2", "valeur": 190000},
        {"adresse": "36 Rue LaFayette", "codePostal": 75001, "batiment": "Maison", "nbEtage": "2", "valeur": 230000},
        {"adresse": "25 Avenue Victor Hugo", "codePostal": 75001, "batiment": "Maison", "nbEtage": "1", "valeur": 140000},
        {"adresse": "12 Rue Jp", "codePostal": 75001, "batiment": "Maison", "nbEtage": "2", "valeur": 210000},
        {"adresse": "1 Rue Jesaispas", "codePostal": 78000, "batiment": "Maison", "nbEtage": "6", "valeur": 150000},
        {"adresse": "3 Rue Truc", "codePostal": 78000, "batiment": "Maison", "nbEtage": "7", "valeur": 180000},
        {"adresse": "27 Avenue Bidule", "codePostal": 78000, "batiment": "Maison", "nbEtage": "5", "valeur": 100000},
        {"adresse": "42 Rue Mj", "codePostal": 78000, "batiment": "Maison", "nbEtage": "6", "valeur": 120000}
    ]
    
    json_string = json.dumps(marcheImmobilier, indent=4) 

    with open(lienJSON, "w") as json_file:
        json_file.write(json_string)
        
    return lienJSON

def recupDonneesImmobilier(lienXML, lienJSONImmobilier):
    
    tree = ET.parse(lienXML)
    root = tree.getroot()
    
    donnees = []
    donnees.append(root.find('.//idPropriete').text)
    donnees.append(root.find('.//adresse').text)
    
    with open(lienJSONImmobilier, "r") as json_file:
        immobilier = json.load(json_file)
    
    for i in range(0,len(donnees)):
        donnees[i] = donnees[i].replace('\n','')
    
    for propriete in immobilier:
        if str(propriete["idImmobilier"]) == str(donnees[0]):
            donnees.append(propriete["age"])
            donnees.append(propriete["normeLegal"])
            donnees.append(propriete["normeReglementaire"])
            donnees.append(propriete["litigesEnCours"])
            donnees.append(propriete["normeElectricite"])
            donnees.append(propriete["normeGaz"])
            
    return donnees

def recupDonneesMarcheImmobilier(lienXML):
    
    tree = ET.parse(lienXML)
    root = tree.getroot()
    
    donnees = []
    donnees.append(root.find('.//adresse').text)
    donnees.append(root.find('.//descriptionPropriete').text)
    
    return donnees

def verificationConformite(donnees, lienXML, lienJSONImmobilier): 
    
    idImmobilier = donnees[0]
    adresse = donnees[1]
    age = donnees[2]
    normeLegal = donnees[3]
    normeReglementaire = donnees[4]
    litigesEnCours = donnees[5]
    normeElectricite = donnees[6]
    normeGaz = donnees[7]
    
    decision = 'Admissible a un pret immobilier'
    facteur1 = ''
    facteur2 = ''
    facteur3 = ''
    facteur4 = ''
    facteur5 = ''
    
    random_number = random.randint(0, 1)
    
    if random_number == 0:
        visitevirutelle = "Visite virtuelle non demandée et non effectuée"
        visitesurplace = "Visite sur place non demandée et non effectuée"
    else:
        visitevirutelle = "Visite virtuelle demandée et effectuée"
        visitesurplace = "Visite sur place non demandée et non effectuée"

    if age < 10:
        if normeElectricite not in ['NFC 15-100', 'NF C 15-100', 'C 15-100']:
            facteur1 = 'Non conforme : Electricite'
            decision = 'Non admissible a un pret immobilier'               

            if visitevirutelle == "Visite virtuelle demandée et effectuée": visitesurplace = "Visite sur place non concluante"                 
            elif visitevirutelle == "Visite virtuelle demandée et effectuée": visitesurplace = "Visite sur place concluante"
            
            if normeGaz == '':
                if visitevirutelle == "Visite virtuelle demandée et effectuée" and visitesurplace != "Visite sur place non concluante": visitesurplace = "Visite sur place concluante"
            elif normeGaz != 'NF P 45-500':
                facteur2 = 'Non conforme : Gaz '
                decision = 'Non admissible a un pret immobilier'

                if visitevirutelle == "Visite virtuelle demandée et effectuée": visitesurplace = "Visite sur place non concluante"                 
                elif visitevirutelle == "Visite virtuelle demandée et effectuée" and visitesurplace != "Visite sur place non concluante": visitesurplace = "Visite sur place concluante"

    if normeLegal != 0:
        facteur3 = 'Normes non legales!'
        decision = 'Non admissible a un pret immobilier'
    if normeReglementaire != 0:
        facteur4 = 'Normes non reglementaires !'
        decision = 'Non admissible a un pret immobilier'
    if litigesEnCours != 0:
        facteur5 = 'Il y a au moins 1 litige en cours'
        decision = 'Non admissible a un pret immobilier'
        
    tree = ET.parse(lienXML)
    root = tree.getroot()
    decision_element = ET.Element("decisionConformite")
    decision_element.text = decision
    root.append(decision_element)
        
    if decision == 'Non admissible a un pret immobilier':
        raison_element = ET.Element("raisons")
        raison_element.text = ''

        if facteur1 == 'Non conforme : Electricite':
            raison_element.text += facteur1
        if facteur2 == 'Non conforme : Gaz':
            raison_element.text += facteur2
        if facteur3 == 'Normes non legales !':
            raison_element.text += facteur3
        if facteur4 == 'Normes non reglementaires !':
            raison_element.text += facteur4
        if facteur5 == 'Il y a au moins 1 litige en cours':
            raison_element.text += facteur5
            
        root.append(raison_element)
        
    tree.write(lienXML)
    
    return lienXML
    
def valeurMarche(donnees, lienXML, lienJSONMarcheImmobilier):
    
    adresseXML = donnees[0]
    descriptionProprieteXML = donnees[1]
    
    codePostalXML = int(re.search(r'\b\d{5}\b', adresseXML).group())
    modeleRegex = r"(Maison|Appartement)|(maison|appartement)(?:.*?(\b\w+\b)?\s?[ée]tage[s])?"
    resultat = re.search(modeleRegex, descriptionProprieteXML, re.IGNORECASE)
    
    nbEtageXML = None
    batimentXML = None
    moyenne_valeur = 0
    
    if resultat:
        batimentXML = resultat.group(1)
        nbEtageExtrait = resultat.group(2) if resultat.group(2) else None
        nbEtageXML = nombres_en_texte.get(nbEtageExtrait.lower(), nbEtageExtrait) if nbEtageExtrait else None
    else:
        print("[serviceEvaluation] : Aucun match trouvé")
         
    with open(lienJSONMarcheImmobilier, "r") as json_file:
        marcheImmobilier = json.load(json_file)
    somme = 0
    nbElements = 1

    if nbEtageXML == None:
        for propriete in marcheImmobilier:
            if (str(propriete["codePostal"]) == str(codePostalXML)) and (str(propriete['batiment']) == str(batimentXML)):
                somme += propriete["valeur"]
                nbElements += 1
    else:
        for propriete in marcheImmobilier:
            if (str(propriete["codePostal"]) == str(codePostalXML)) and (str(propriete['batiment']) == str(batimentXML)) and (str(propriete["nbEtage"]) == str(nbEtageXML)):
                somme += propriete["valeur"]
                nbElements += 1

    if resultat is not None and resultat[0] is not None:
        moyenne_valeur = int(somme/nbElements)
    else:
        print("[serviceEvaluation] : Aucun résultat trouvé pour le code_postal", codePostalXML, ", le bâtiment", batimentXML, "et le nombre d'étages", nbEtageXML)

    estimationValeur_element = ET.Element("estimationValeur")
    estimationValeur_element.text = str(moyenne_valeur)
    tree = ET.parse(lienXML)
    root = tree.getroot()
    root.append(estimationValeur_element)
    tree.write(lienXML)
    
    return lienXML

class serviceEvaluation(ServiceBase): 

    @srpc(Unicode, _returns=Unicode)
    def evaluationPropriete(lienXML):
        
        lienJSONImmobilier = creationDBImmobilier()
        lienJSONMarcheImmobilier = creationDBMarcheImmobilier()
        donneesImmobilier = recupDonneesImmobilier(lienXML, lienJSONImmobilier)
        donneesMarcheImmobilier = recupDonneesMarcheImmobilier(lienXML)
        verificationConformite(donneesImmobilier, lienXML, lienJSONImmobilier)
        valeurMarche(donneesMarcheImmobilier, lienXML, lienJSONMarcheImmobilier)

        return lienXML

wsdl_appEvaluation = Application([serviceEvaluation],
    tns = 'serviceEvaluation',
    in_protocol = Soap11(validator='lxml'),
    out_protocol = Soap11()
)
