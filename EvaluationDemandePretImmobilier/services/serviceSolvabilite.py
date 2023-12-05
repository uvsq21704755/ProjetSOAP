# Utilitaires
import xml.etree.ElementTree as ET
import json

# Spyne
from spyne import Application, srpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11

def creationDBBanque():
    
    lienJSON = "./EvaluationDemandePretImmobilier/services/bdd/banque.json"

    banque = [
        {"idBanque": 11, "age": 25, "enfants": 0, "emploi": 0, "nbCreditsEnCours": 0, "antecedents": 0, "tauxEndettement": 0},
        {"idBanque": 22, "age": 50, "enfants": 4, "emploi": 1, "nbCreditsEnCours": 4, "antecedents": 1, "tauxEndettement": 45}
    ]

    json_string = json.dumps(banque, indent=4) 

    with open(lienJSON, "w") as json_file:
        json_file.write(json_string)

    return lienJSON

def recupDonnees(lienXML, lienJSON):
    
    tree = ET.parse(lienXML)
    root = tree.getroot()
    
    donnees = []
    donnees.append(root.find('.//idBanque').text)
    donnees.append(root.find('.//montantPret').text)
    donnees.append(root.find('.//dureePret').text)
    donnees.append(root.find('.//revenuMensuel').text)
    donnees.append(root.find('.//depenseMensuelle').text)
    
    with open(lienJSON, "r") as json_file:
        banque = json.load(json_file)
    
    for i in range(0,len(donnees)):
        donnees[i] = donnees[i].replace('\n','')

    for client in banque:
        if str(client["idBanque"]) == str(donnees[0]):
            donnees.append(client["age"])
            donnees.append(client["enfants"])
            donnees.append(client["emploi"])
            donnees.append(client["nbCreditsEnCours"])
            donnees.append(client["antecedents"])
            donnees.append(client["tauxEndettement"])

    return donnees

def calculScoring(donnees,lienXML):
    
    idBanque = donnees[0]
    montantPret = donnees[1]
    dureePret = donnees[2]
    revenuMensuel = donnees[3]
    depenseMensuelle = donnees[4]
    age = donnees[5]
    enfants = donnees[6]
    emploi = donnees[7]
    nbCreditsEnCours = donnees[8]
    antecedents = donnees[9]
    tauxEndettement = donnees[10]
    
    score = -1
    ageI = int(age)
    antecedentsI = int(antecedents)
    dureePretI = int(dureePret)
    enfantsI = int(enfants)
    emploiI= int(emploi)
    montantPretI = int(montantPret)
    tauxEndettementI = int(tauxEndettement)
    depenseMensuelleI = int(depenseMensuelle)
    capaciteEmpruntI = (int(revenuMensuel) * 33) / 100
    revenuMensuelI = int(revenuMensuel)

    decision = "Pas de décision"
    
    if ageI < 18 or tauxEndettementI >= 33 or (depenseMensuelleI + capaciteEmpruntI) > revenuMensuelI:
        if ageI < 18: decision = 'Non Admissible'
        if tauxEndettementI >= 33: decision = 'Non Admissible'
        if (depenseMensuelleI + capaciteEmpruntI) > revenuMensuelI: decision = 'Non Admissible'
    
    else:
        score = 0
        
        if 18 <= ageI < 35:
            if enfantsI == 0:
                if emploiI == 0: score += 10
                else: score += 5
            if enfantsI == 1:
                if emploiI == 0: score += 8
                else: score += 3
            if enfantsI == 2:
                if emploiI == 0: score += 6
                else: score = 2
            if enfantsI > 3:
                if emploiI == 0: score += 5
                else: decision = 'Non Admissible'
            
            if dureePretI < 10: score += 10
            elif 10 <= dureePretI < 15: score += 8
            elif 15 <= dureePretI < 20: score += 6
            elif 20 <= dureePretI < 25: score += 4
            elif dureePretI >= 25: score += 2
    
            if montantPretI < 100000: score += 10
            elif 100000 <= montantPretI < 150000: score += 8
            elif 150000 <= montantPretI < 200000: score += 6
            elif 200000 <= montantPretI < 250000: score += 4
            elif montantPretI >= 250000: score += 2

            if antecedentsI == 0: score += 10
            elif antecedentsI == 1: score += 7
            elif antecedentsI == 2: score += 4
            elif antecedentsI == 3: score += 1
            elif antecedentsI >= 4: decision = 'Non Admissible'
            
        elif 35 <= ageI < 60:
            if enfantsI == 0:
                if emploiI == 0: score += 8
                else: score += 5
            if enfantsI == 1:
                if emploiI == 0: score += 6
                else: score += 3
            if enfantsI == 2:
                if emploiI == 0: score += 5
                else: score += 2
            if enfantsI > 3:
                if emploiI == 0: score += 4
                else: decision = 'Non Admissible'
            
            if dureePretI < 10: score += 9
            elif 10 <= dureePretI < 15: score += 7
            elif 15 <= dureePretI < 20: score += 5
            elif 20 <= dureePretI < 25: score += 3
            elif dureePretI >= 25: score += 1
            
            if montantPretI < 100000: score += 9
            elif 100000 <= montantPretI < 150000: score += 7
            elif 150000 <= montantPretI < 200000: score += 5
            elif 200000 <= montantPretI < 250000: score += 3
            elif montantPretI >= 250000: score += 1
                
            if antecedentsI == 0: score += 8
            elif antecedentsI == 1: score += 5
            elif antecedentsI == 2: score += 2
            elif antecedentsI == 3: score += 0
            elif antecedentsI >= 4: decision = 'Non Admissible'
        
        elif 60 <= ageI:
            if enfantsI == 0:
                if emploiI == 0: score += 6
                else: score += 5
            if enfantsI == 1:
                if emploiI == 0: score += 4
                else: score += 3
            if enfantsI == 2:
                if emploiI == 0: score += 2
                else: decision = 'Non Admissible'
            if enfantsI > 3:
                if emploiI == 0: score += 0
                else: decision = 'Non Admissible'
            
            if dureePretI < 10: score += 6
            elif 10 <= dureePretI < 15: score += 4
            elif 15 <= dureePretI < 20: score += 2
            elif 20 <= dureePretI < 25: score += 1
            elif dureePretI >= 25: decision = 'Non Admissible'
            
            if montantPretI < 100000: score += 6
            elif 100000 <= montantPretI < 150000: score += 4
            elif 150000 <= montantPretI < 200000: score += 2
            elif 200000 <= montantPretI < 250000: score += 1
            elif montantPretI >= 250000: decision = 'Non Admissible'
                
            if antecedentsI == 0: score += 6
            elif antecedentsI == 1: score += 4
            elif antecedentsI == 2: score += 1
            elif antecedentsI == 3: score += 0
            elif antecedentsI >= 4: decision = 'Non Admissible'
            
        if score != -1:       
            if 30 < score <= 40:
                if decision != 'Non Admissible': decision = 'Tres favorable'
            elif 20 < score <= 30:
                if decision != 'Non Admissible': decision = 'Sous conditions'
            elif 10 < score <= 20:
                if decision != 'Non Admissible': decision = 'A defendre'
            elif 0 <= score <= 10:
                if decision != 'Non Admissible': decision = 'Peu probable'
    
    tree = ET.parse(lienXML)
    root = tree.getroot()
        
    score_element = ET.Element("score")
    score_element.text = str(score)
    decision_element = ET.Element("decisionScore")
    decision_element.text = decision
    root.append(score_element)
    root.append(decision_element)
    tree.write(lienXML)
        
    return lienXML

class serviceSolvabilite(ServiceBase): 

    @srpc(Unicode, _returns = Unicode)
    def verificationSolvabilite(lienXML):

        lienJSON = creationDBBanque()
        donnees=recupDonnees(lienXML,lienJSON)
        return calculScoring(donnees,lienXML)
    
    
wsdl_appSolvabilite = Application([serviceSolvabilite],
    tns = 'serviceSolvabilite',
    in_protocol = Soap11(validator='lxml'),
    out_protocol = Soap11()
)
