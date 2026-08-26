
import serial 
import time 
import matplotlib.pyplot as plt
import datetime
import numpy as np 
import serial
import serial.tools.list_ports
from pathlib import Path


def connexion_port(br=115200, portIN=''):
    """_summary_
Établit la connexion série avec l'Arduino. Si un port est fourni manuellement,
tente de s'y connecter directement. Sinon, détecte automatiquement le port
Arduino parmi les ports disponibles (Windows et Linux), en cherchant les
identifiants caractéristiques dans le nom du port.

Args:
    br (int): Baudrate de la connexion série. Par défaut 115200.
    portIN (str): Nom du port série à utiliser. Si vide, détection automatique.

Returns:
    tuple[str, serial.Serial | str]:
        - portIN : nom du port détecté ou fourni (ex. 'COM6', '/dev/ttyACM0').
        - s : objet serial.Serial connecté, ou la chaîne 'error' en cas d'échec.
"""
    # Si port fourni manuellement
    if portIN:
        try:
            s = serial.Serial(port=portIN, baudrate=br, timeout=5)
            print(f'Connexion établie avec {portIN}')
            return portIN, s
        except serial.SerialException as e:
            print(f"Erreur: impossible d'ouvrir {portIN}")
            return '', 'error'

    # Détection automatique
    ports = list(serial.tools.list_ports.comports())
    
    for port in ports:
        p = str(port)
        # Windows
        if 'Arduino' in p or'Périphérique série' in p or 'série USB' in p :
            portIN = port.device
            break
        # Linux
        if 'ttyACM' in port.device or 'ttyUSB' in port.device:
            portIN = port.device
            break

    if not portIN:
        print("/!\\ Aucun port Arduino détecté")
        return '', 'error'

    try:
        s = serial.Serial(port=portIN, baudrate=br, timeout=5)
        print(f'Connexion réussie sur {portIN}')
        return portIN, s
    except serial.SerialException as e:
        print(f"Erreur: impossible d'ouvrir {portIN} : {e}")
        return '', 'error'

def data(s, N=None):
    """_summary_
    Acquiert un nombre fixe de mesures depuis le port série, espacées d'un
    intervalle de temps connu (time_inter), et renvoie un temps écoulé en
    secondes pour chaque mesure (plutôt qu'un simple indice d'acquisition).

    Parameters
    ----------
    s : serial.Serial
        Objet Serial ouvert sur lequel lire les mesures.
    N : int, optional
        Nombre de mesures à effectuer. Si None, demandé à l'utilisateur.
    time_inter : float, optional
        Intervalle de temps (en sec) entre deux lectures. Par défaut 0.08 sec.

    Returns:
        tuple[list[float], list[float], list[float]]:
            - T : liste des températures mesurées (en °C).
            - V : liste des tensions mesurées (en V).
            - t_temps : liste des temps écoulés depuis le début (en sec).
    """
    time_inter=0.08
    T = []
    V = []
    t_temps = []
    if N is None:
        N = int(input('Combien de mesures veux-tu faire ? '))

    t0 = time.time()
    for k in range(N):
        s.flushInput()
        time.sleep(time_inter)
        try:
            line = s.readline().decode()
            a = line.strip("\r\n").split(",")
            T.append(float(a[1]))  # a[1] : température, a[0] : tension
            V.append(float(a[0]))
            t_temps.append(time.time() - t0)
        except:
            print("problème de lecture de données")
        
        print(f'\rMesure {k+1}/{N} ({100*(k+1)//N} %)', end='', flush=True)

    return T, V, t_temps


# T,V = data()


def Graphe_T_V(x,y,t_temps):
    """_summary_
    Affiche deux graphiques en nuage de points des tensions mesurées (corrigées en mV) et de températures(°C)
    Crée une nouvelle fenêtre matplotlib intitulée 'Graphique Voltage et Température et trace
    chaque valeur de y en fonction de son indice (axe temporel implicite).

    Args:
        x (list[float]): Liste des températures mesurées à afficher (en °C).
        y (list[float]): Liste des tensions corrigées à afficher (en V ou mV selon calibration).
        t_temps (list[float]): Liste des temps écoulés depuis le début (en sec).
    """
    fig, (ax1 , ax2)  = plt.subplots(1,2)
    ax1.plot(t_temps,y,'o',color='red')
    ax1.set_xlabel("Temps d'acquisition (s)")
    ax1.set_ylabel("Potentiel réel (mV)")

    ax2.plot(t_temps,x,'o', color='blue')
    ax2.set_xlabel("Temps d'acquisition (s)")
    ax2.set_ylabel("Température (°C)")
    plt.show()
    return fig 




import threading

import matplotlib.pyplot as plt
import time

def graphe_live(C0, s):
    T = []
    V = []
    t_T = []   # temps (s) associés à chaque mesure de température
    t_V = []   # temps (s) associés à chaque mesure de tension (après filtrage)
    stop = False

    def on_key(event):
        nonlocal stop
        if event.key == 'q':
            stop = True

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.canvas.mpl_connect('key_press_event', on_key)

    print("Mesure en cours... Appuie sur 'q' dans la fenêtre du graphe pour arrêter.")

    t0 = time.time()  # référence de départ pour l'axe temporel

    while not stop:
        s.flushInput()
        time.sleep(0.5)  # ~ 2 mesures / seconde

        try:
            line = s.readline().decode()
            a = line.strip("\r\n").split(",")

            v_cal = (2 - float(a[0])) * 1000 + C0
        

            t_actuel = time.time() - t0

            T.append(float(a[1]))
            t_T.append(t_actuel)

            V.append(v_cal)
            t_V.append(t_actuel)

            ax1.clear()
            ax1.plot(t_V, V, color='blue')
            ax1.set_title("Tension")
            ax1.set_xlabel("Temps (s)")
            ax1.set_ylabel("Tension calibrée (mV)")

            ax2.clear()
            ax2.plot(t_T, T, color='red')
            ax2.set_title("Température")
            ax2.set_xlabel("Temps (s)")
            ax2.set_ylabel("Température (°C)")

            plt.tight_layout()
            plt.pause(0.01)

        except Exception as e:
            print(f"Problème de lecture des données : {e}")

    plt.ioff()   # ← stop le mode interactif
    plt.close(fig)

    return T, V, t_T, t_V, fig

def informations_1er_ordre (T,V,a) :
    """_summary_
    Calcule et affiche les statistiques de base d'une session de mesures : moyenne et écart-type
    des tensions calibrées et des températures mesurées. Affiche les résultats dans la console.

    Args:
        T (list[float]): Liste des températures mesurées (en °C).
        V (list[float]): Liste des tensions calibrées (en mV).
    """
    moy_V = np.mean(V[int(a):])
    sigma = np.std(V[int(a):])
    moy_T = np.mean(T[int(a):])
    print(f"moyenne Potentiel(mV) = {moy_V}")
    print(f'écart type (écart-type) = {sigma}')
    print(f'moyenne Température (°C)={moy_T}')
    return moy_T , moy_V, sigma 


def enregistrement_csv (T,V_real,moy = None,sigma=None) :
    """_summary_
Enregistre les données de température et de potentiel calibré dans un fichier
CSV horodaté, accompagnées de la moyenne et de l'écart-type des tensions.
Le fichier est sauvegardé dans le dossier Data/data_(T,V)/.

Args:
    T (list[float]): Liste des températures mesurées (en °C).
    V_real (list[float]): Liste des potentiels calibrés (en mV).
    moy (float, optional): Moyenne des tensions calibrées. Calculée automatiquement
        si non fournie.
    sigma (float, optional): Écart-type des tensions calibrées. Calculé
        automatiquement si non fourni.

Returns:
    str: Message de confirmation d'enregistrement.
"""
    BASE = Path(__file__).parent.parent
    now = datetime.datetime.now()
    nom_fichier = now.strftime("Mesure Température et Voltage %d %B, %Hh%M.csv")
    chemin = BASE/"Data"/'data_(T,V)'/nom_fichier      
    n = min(len(T), len(V_real))
    if moy is None:
        moy = np.mean(V_real[:n])
    if sigma is None:
        sigma = np.std(V_real[:n])
    resultat = np.column_stack((T[:n], V_real[:n]))
    with open(chemin, 'w') as f:
        np.savetxt(f,resultat, delimiter=',', fmt='%.2f',header=f'Donnees Temperature / Potentiel(calibré),pour V :  écart type ={sigma} et moyenne = {moy}')
    return 'Le fichier csv a bien été enregistré.'

def enregistrement_pdf (figure) :
    """_summary_
Enregistre le graphique de température et de potentiel sous forme d'image PDF
horodatée dans le dossier Data/data_figures/data_figures_mesures/.

Args:
    figure (matplotlib.figure.Figure): Figure matplotlib à sauvegarder.

Returns:
    str: Message de confirmation d'enregistrement.
"""
    BASE = Path(__file__).parent.parent
    now = datetime.datetime.now()
    nom_fichier = now.strftime("Graphique Température et Potentiel %d %B, %Hh%M.pdf")
    chemin = BASE/"Data"/'data_figures'/'data_figures_mesures'/nom_fichier      
    figure.savefig(chemin,bbox_inches='tight')
    return 'Le fichier pdf a bien été enregistré.'

#derniere option, tracer un graphique à partir d'un fichier csv : 
def graphe_csv():
    """
    Lit un fichier CSV contenant des données de température et de potentiel, puis
    trace un graphique de T et V en fonction du nombre de mesures.
    Le fichier CSV doit être horodaté et contenir deux colonnes : température (°C) et potentiel (mV).
    """
    nom = input("Entrez le nom du fichier csv (avec l'extension .csv ; ex Mesure et ... 15 juin, 18H00.csv): ")
    nom = nom.strip().strip('\'"')

    BASE = Path(__file__).parent.parent
    chemin = BASE / "Data" / "data_(T,V)" / nom

    data = np.loadtxt(chemin, delimiter=',', skiprows=1, encoding='latin-1')
    T = data[:, 0]
    V = data[:, 1]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(V, 'o', color='red')
    ax1.set_xlabel("Nombre de mesure")
    ax1.set_ylabel("Potentiel réel (mV)")
    ax2.plot(T, 'o', color='blue')
    ax2.set_xlabel("Nombre de mesure")
    ax2.set_ylabel("Température (°C)")
    plt.show()

    return 'Le graphique a bien été tracé à partir du fichier csv.'