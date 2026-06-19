import numpy as np 
from pathlib import Path

BASE = Path(__file__).parent.parent
#air , boitier fonctionnel
data_bon_e = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 18 June, 15h32.csv", delimiter="," , skiprows=1)
T_bon_e = data_bon_e[:,0]

#eau, boitier fonctionnel
data_bon_a = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 18 June, 15h35.csv", delimiter="," , skiprows=1)
T_bon_a = data_bon_a[:,0]

#air, boitier défaillant
data_nul_a = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 18 June, 15h39.csv", delimiter="," , skiprows=1)
T_nul_a = data_nul_a[:,0]

#eau , boitier défaillant
data_nul_e = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 18 June, 15h39.csv", delimiter="," , skiprows=1)
T_nul_e = data_nul_e[:,0]
n = min(len(T_bon_e), len(T_nul_e))

n = min(len(T_bon_a), len(T_nul_a))

diff_e = T_bon_e[:n] - T_nul_e[:n]  


print(f"moyenn diff_e = {np.mean(diff_e)} et sigma_a = {np.std(diff_e)}")

diff_a =  T_bon_a[:n] - T_nul_a[:n]


print(f"moyenn diff_a = {np.mean(diff_a)} et sigma_a = {np.std(diff_a)}")