import Mesure as mes 
import numpy as np
import datetime
import locale
import calibration as cal
from pathlib import Path
import serial
import time
import matplotlib.pyplot as plt
import scipy.stats as stats

#calibration d'usine : 
def calibration_usine():
    """_summary_
    Applique la formule de calibration d'usine à une liste de tensions mesurées.
    Pour chaque valeur de V ('brut'), on convertit : E = (2 - i) * 1000 (qui sera calculé par V_real), mais retourne
    systématiquement C0 = 0 (aucun offset correctif n'est appliqué).
    Cette fonction sert de référence sans correction : elle suppose que le capteur
    est déjà calibré en sortie d'usine. 

Remarque : on ne savait pas si on devait définir une fonction (cacalibration_usine) ou  juste mettre C0 = 0 pour l'option 1 du menu

    Args:
       none 

    Returns:
        int: C0 = 0, terme correctif nul (calibration d'usine sans offset).
    """
    C0 = 0
    return C0

#calibration a un étalon
def calibration_etalon(V):
    """_summary_
    Calcule le terme correctif C0 par calibration à un étalon.
    Demande à l'utilisateur la valeur du potentiel de la solution étalon,
    puis calcule pour chaque tension mesurée l'écart entre la valeur attendue
    et la valeur convertie. C0 est la moyenne de ces écarts, utilisée ensuite
    pour corriger les mesures réelles.

    Args:
        V (list[float]): Liste des tensions brutes mesurées sur la solution étalon (en volts).

    Returns:
        float: C0, terme correctif moyen (offset en mV) à appliquer aux mesures futures.
    """
    E= float(input('quelle est le potentiel de la solution étalon (mV) ? '))
    C=[]
    for i in V :
        X = E-((2-i)*1000)
        C.append(X)
    C0 = np.mean(C)
    return C0
# s, portIN = mes.connexion_port()
# _,V = mes.data(s)
# calibration_etalon(V)

     
#if __name__ == '__main__':
    # T,V = data()
    # print(calibration_etalon(V))



def V_real_f (V,C0):
    """_summary_
    Convertit une liste de tensions brutes en valeurs de potentiel corrigées (en mV),
    en appliquant la formule de conversion du capteur et l'offset de calibration C0.
    La conversion utilisée est : V_corrigé = (2 - i) * 1000 + C0.

    Args:
        V (list[float]): Liste des tensions brutes mesurées par le capteur (en volts).
        C0 (float): Terme correctif issu de la calibration (en mV), peut être = 0 si
         calibration d'usine, ou une valeur calculée via calibration_etalon().

    Returns:
        list[float]: Liste des potentiels corrigés (en mV), de même longueur que V.
    """
    V_real =[]
    for i in V : 
            a = (2-i)*1000 + C0
            V_real.append(float(a))
    return V_real 
#=======================================================
#Enregistrement des données de calibration :

def enregistrement_cal (C0, tendance = None,nb_etalons=None) :
    """_summary_
Enregistre les paramètres de calibration dans un fichier CSV horodaté.
Selon le nombre d'étalons, le fichier contient soit uniquement C0 (calibration
à 1 étalon ou d'usine), soit C0, la pente et l'intercept de la droite de
tendance (calibration à 2 étalons). Le fichier est sauvegardé dans le dossier
Data/data_calibration/.

Args:
    C0 (float): Terme correctif issu de la calibration (en mV).
    tendance (np.poly1d, optional): Objet polynôme contenant la pente et
        l'intercept de la droite d'étalonnage. None si calibration à 1 étalon.
    nb_etalons (int, optional): Nombre d'étalons utilisés (1 ou 2). None si
        calibration d'usine.

Returns:
    None
"""
    BASE = Path(__file__).parent.parent     
    now = datetime.datetime.now()
    if nb_etalons == 1:
        nom_fichier = now.strftime(f"Calibration à {nb_etalons} étalons %d %B, %Hh%M.csv")
    elif nb_etalons == 2:
        nom_fichier = now.strftime(f"Calibration à {nb_etalons} étalons %d %B, %Hh%M.csv")
    elif nb_etalons is None :
        nom_fichier = now.strftime(f"Calibration d'usine %d %B, %Hh%M.csv")
    chemin = BASE/"Data"/"data_calibration"/nom_fichier      
    if tendance is None :
        resultat = np.atleast_2d(C0) #  garantit un array 2D pour savetxt
        with open(chemin, 'w', newline='', encoding='utf-8') as f:  #encodage explicite
            np.savetxt(f, resultat, fmt='%.2f', header=f"Donnees Calibration à {nb_etalons} étalons(Co,tendance)") 
    else : 
        slope, intercept = tendance.coeffs
        resultat = np.atleast_2d([C0, slope, intercept]) #  array 2D avec C0, slope et intercept
        with open(chemin, 'w', newline='', encoding='utf-8') as f:  #encodage explicite
            np.savetxt(f, resultat, fmt='%.2f', header=f"Donnees Calibration à {nb_etalons},tendance : E = {slope:.2f}*V + {intercept:.2f}") 

def enregistrement_cal2_pdf (fig) :
    """_summary_
Enregistre le graphique de calibration à 2 étalons sous forme d'image PDF
horodatée dans le dossier Data/data_figures/data_figures_calibration/.

Args:
    fig (matplotlib.figure.Figure): Figure matplotlib à sauvegarder.

Returns:
    str: Message de confirmation d'enregistrement.
"""
    BASE = Path(__file__).parent.parent
    now = datetime.datetime.now()
    nom_fichier = now.strftime("Graphique Calibration 2 étalons %d %B, %Hh%M.pdf")
    chemin = BASE/"Data"/'data_figures'/'data_figures_calibration'/nom_fichier      
    fig.savefig(chemin,bbox_inches='tight')
    return 'Le fichier pdf a bien été enregistré.'
# =======================================================================================================
# Calibration à 2 étalons :

def calibration_2_etalons(s, E1=None, E2=None,V1=None, V2=None) :
    """_summary_
Effectue une calibration à deux étalons par régression linéaire.
Demande à l'utilisateur les potentiels des deux solutions étalons, acquiert
les mesures sur chacune d'elles, puis calcule la droite de tendance par
régression linéaire (scipy.stats.linregress) entre les tensions moyennes
mesurées et les potentiels théoriques. Avertit si le R² est inférieur à 0.9.

Remarque : avec seulement 2 points, R² vaut toujours 1 par construction
mathématique — l'avertissement R² < 0.9 ne peut donc jamais se déclencher.

Args:
    s (serial.Serial): Objet de connexion série avec l'Arduino.
    E1 (float, optional): Potentiel théorique de la solution étalon 1 (en mV).
    E2 (float, optional): Potentiel théorique de la solution étalon 2 (en mV).
    V1 (list[float], optional): Tensions brutes mesurées sur l'étalon 1.
    V2 (list[float], optional): Tensions brutes mesurées sur l'étalon 2.
    V_real1 : tension convertit en mV 
    V_real2 : tension convertit en mV
E1 et E2 sont demandé à l'utilisateur si non fournis, V1 et V2 sont acquises via mes.data() si non fournies
V_real1 et V_real2 sont acquise via V1 et V2

Returns:
    tuple: (C0, V1_moy, V2_moy, tendance, r_squared, E1, E2)
        - C0 (float): Intercept de la droite, utilisé comme offset de calibration (en mV).
        - V1_moy (float): Tension moyenne mesurée sur l'étalon 1 (en mV).
        - V2_moy (float): Tension moyenne mesurée sur l'étalon 2 (en mV).
        - tendance (np.poly1d): Droite de calibration sous forme de polynôme.
        - r_squared (float): Coefficient de détermination R² de la régression.
        - E1 (float): Potentiel théorique de l'étalon 1 (en mV).
        - E2 (float): Potentiel théorique de l'étalon 2 (en mV).
"""
    if E1 is None and V1 is None:
        E1 = float(input('Potentiel de la solution étalon 1 (mV) : '))
        input('Placer votre sonde dans la solution étalon 1, quand vous êtes prêt, écrivez OK ===>')
        print('Début des mesures...')
        T, V1, _ = mes.data(s, N=100)
        print('Fin des mesures')
    if E2 is None and V2 is None:
        E2 = float(input('Potentiel de la solution étalon 2 (mV) : '))
        input('Nettoyer et sécher votre sonde, puis la placer dans la solution étalon 2 , quand vous êtes prêt, écrivez OK ===>')
        print('Début des mesures...')
        T, V2,_ = mes.data(s, N=100)
        print('Fin des mesures')

    V1_moy = np.mean(V1)
    V2_moy = np.mean(V2)

    # Conversion en mV 
    V1_real = (2 - V1_moy) * 1000
    V2_real = (2 - V2_moy) * 1000
    a = (E2 - E1)/ (V2_real-V1_real)
    C0 = E1 -a*V1_real
    tendance   = np.poly1d([a,C0])
    print(f'pente = {a}')
    print(f'C0 ={C0}')
    print(f'Équation : E = {a:.4f} * V_real + {C0:.2f}')
    print(V1_real)
    print(V2_real)
    return a,C0,E1,E2,V1_real,V2_real,tendance


#Graphique de la tendance de l'étalonnage. 
def graphe_cal2(tendance,a, C0, E1, E2, V1_real,V2_real):
    """__summary__
    Affiche le graphique de la droite de calibration à 2 étalons.
    Trace la droite de calibration E = a * V_real + C0 ainsi que les deux points
    étalons, avec l'équation de la droite en légende.

    Args:
        tendance (np.poly1d): Droite de calibration sous forme de polynôme,
            construite à partir de a et C0 via np.poly1d([a, C0]).
        a (float): Pente de la droite de calibration (sans unité, idéalement ≈ 1).
        C0 (float): Intercept de la droite de calibration (en mV).
        E1 (float): Potentiel théorique de la solution étalon 1 (en mV).
        E2 (float): Potentiel théorique de la solution étalon 2 (en mV).
        V1_real (float): Tension mesurée convertie de l'étalon 1 (en mV),
            obtenue via (2 - V1_moy) * 1000.
        V2_real (float): Tension mesurée convertie de l'étalon 2 (en mV),
            obtenue via (2 - V2_moy) * 1000.

    Returns:
        matplotlib.figure.Figure: Figure matplotlib du graphique de calibration.
    """
    fig,ax = plt.subplots()
    # Axe X : de part et d'autre des deux mesures pour voir la droite
    x_plot = np.linspace(min(V1_real, V2_real) - 20, max(V1_real, V2_real) + 20, 100)
    signe = '+' if C0 >= 0 else '-'
    ax.plot(x_plot, tendance(x_plot), label=f"E = {a:.2f}·V {signe} {abs(C0):.2f}")
    # Points étalons : x = tension mesurée, y = potentiel théorique
    ax.scatter([V1_real, V2_real], [E1, E2], color='red', zorder=5, label='Étalons')

    ax.set_xlabel('Tension mesurée V (mV)')
    ax.set_ylabel('Potentiel réel E (mV)')
    ax.set_title('Courbe de calibration à 2 étalons')
    ax.legend()
    ax.grid()
    plt.show()
    return fig


