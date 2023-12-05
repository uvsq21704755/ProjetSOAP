# Projet SOAP - Evaluation des demandes de prêts immobiliers 

## Configurer l'environnement virtuel et ajouter les dépendances nécessaires

`chmod 774 ./configure`

`./configure`

## Lancer le serveur Flask et l'interface web

`chmod 774 ./run`

`./run`

L'interface est accessible à `http://localhost:8000`

## Interface

### Dépôt d'un dossier de prêt

![](https://github.com/Clem0908/Usefull_bash_scripts/blob/main/depot_dossier.gif)

### Récupération des résultats : acceptation de demande de prêt

![](https://github.com/Clem0908/Usefull_bash_scripts/blob/main/recup_dossier.gif)

### Récupération des résultats : refus de demande de prêt

![](https://github.com/Clem0908/Usefull_bash_scripts/blob/main/refus.gif)

## Scénario 

### Demande acceptée

#### Formulaire
```
Nom : John Doe
Adresse : 123 Rue de la Liberte, 75001 Paris, France
Email : johndoe@email.com
Numéro de téléphone : 0123456789
Montant du pret : 200000
Duree du pret : 20  
Description de la propriete : Maison a deux etages avec jardin, situee dans un quartier residentiel calme  
Revenus mensuel : 5000  
Depenses mensuelles : 3000  
Compte bancaire : 11  
Identifiant propriété : 1
```

#### Résultat

```
Score : 
Decision Score : Très favorable
Decision Conformité : Admissible a un pret immobilier
Raisons : /
EstimationValeur: 
=> DEMANDE DE PRÊT ACCEPTEE
```

### Demande refusée

#### Formulaire
```
Nom : Sarah Smith
Adresse : 45 avenue des Etats-Unis, 78000 Versailles, France
Email : sarahsmith@email.com
Numéro de téléphone : 0123456788
Montant du pret : 150000
Duree du pret : 30  
Description de la propriete : Appartement situee dans un quartier d'affaire 
Revenus mensuel : 2000  
Depenses mensuelles : 1500  
Compte bancaire : 22  
Identifiant propriété : 2
```

#### Résultat

```
Score : 
Decision Score : 
Decision Conformité : 
Raisons : 
EstimationValeur: 
=> DEMANDE DE PRÊT REJETEE
```
