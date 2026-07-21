# Documentation

Le dossier **SAFE-M-ORP** contient plusieurs éléments : un dossier `Data`, un dossier `documentation`, un dossier source `SRC`, ainsi que des fichiers à la racine (`.gitattributes`, `AUTHORS.md`, `LICENCE.rst`, `README.md`).

## Dossier Data

Le dossier `Data` contient les fichiers `data_figures`, `data_(T,V)` et `data_calibration`, qui regroupent les sauvegardes des données des mesures effectuées.

## Dossier source (SRC)

Le dossier source contient les fichiers code permettant de faire fonctionner le programme.
On y trouve 5 éléments : un fichier `consigne.py`, un fichier `calibration.py`, un fichier `Mesure.py`, un dossier `__pycache__` (cache), et un dossier `arduino_redox` contenant le code arduino.

### 2.1) Fichier consigne.py

Le fichier consigne contient le code du menu. Grâce à l'importation des informations du fichier calibration et Mesures, on peut choisir les consignes que doit suivre le boîtier de commande.

6 propositions sont faites à l'utilisateur, en fonction du choix fait par ce dernier, des mesures peuvent être effectuées, ou, pour les choix plus précis, un 2ème menu peut s'afficher afin de préciser la demande.
L'utilisateur peut choisir entre plusieurs options :

1. Calibration la sonde - permettant choisir dans un nouveau menu une calibration d'usine; à 1 ou 2 étalon.
2. Mesure simple - permettant de choisir le nombre de mesures souhaitée
3. Mesure en continu - permettant de suivre en temps réel l'évolution des mesures
4. Réinitialiser la calibration - permettant d'enregistrer une nouvelle valeur de calibration
5. Tracer un graphique à partur d'un fichier csv - permet de reprendre des données sauvegardé ou importé. 
6. Quitter le programme

Lors de la calibration à 1 étalon, l'enregistrement se fait automatiquement après la calibration complète.

Lors de la réalisation des mesures (options 2 et 3), l'utilisateur choisit, avant l'enregistrement, le format de sortie : représentation graphique ou données brutes. La procédure d'enregistrement diffère ensuite selon l'option sélectionnée :

- **Option 2. Mesure simple** : Les résultats s'enregistrent automatiquement dans un dossier data.
- **Option 3. Mesure en continue** : après avoir pressé `q`, choisir l'option enregistrer les données (ou quitter).

### 2.2) Fichier calibration.py

Ce fichier regroupe les fonctions permettant de :

- Définir le coefficient correctif (nul dans le cas de la calibration d'usine)
- Réajuster la valeur de potentiel mesuré en fonction du coefficient correctif défini au-dessus
- Sauvegarder les données de la calibration

### 2.3) Fichier Mesure.py

Ce fichier regroupe les fonctions permettant de :

- Lister la température et le voltage
- Tracer les graphiques de températures et de voltage
- Sauvegarde des données sous forme *csv* ou *pdf*
- Connection automatique au port Arduino
### 2.4) Dossier __pycache__

Ce dossier contient le cache du code.

### 2.5) Dossier arduino_redox

Ce dossier contient le code téléversé dans le boîtier arduino permettant de faire l'acquisition des données.

## Remarques à l'utilisateur

- L'arrêt du programme en cours se fait lorsque la touche `q` est pressée. Cependant il est nécessaire parfois que la touche soit pressée plusieurs fois afin que le programme cesse complètement ou bien de cliquer sur le grapgique avant de presser q.

- Le calibrage utilisé, si celui-ci n'est pas réalisé en amont des mesures effectuées, est basé sur le dernier enregistrement de la sonde. Veillez donc à calibrer correctement la machine avant la réalisation des mesures. Réinitialiser le calibrage renvoie un terme correctif nul.

- Pour changer la fréquence de mesure : changer la fonction `time.sleep` de la mesure souhaitée (`graphe_live`, `data_live`, etc.)

- À la fin de l'utilisation du programme, choisir impérativement l'option 6. Quitter le programme afin d'éviter les bugs.