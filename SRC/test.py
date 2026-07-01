import numpy as np
import Mesure as mes 
import matplotlib.pyplot as plt 
import datetime
import locale
import calibration as cal
import keyboard
from pathlib import Path
import serial
import time

BASE = Path(__file__).parent.parent
a= 1.0635316537286654
C0 =-30.07258358321866
V1_real = 470.20000000000016
V2_real = 253.9393939393939
tendance = np.poly1d([a,C0])
E1 = 470
E2 = 240
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

fig = graphe_cal2(tendance,a, C0, E1, E2, V1_real,V2_real)
fig.savefig(BASE/"Data"/"data_figures"/"calibration.pdf")