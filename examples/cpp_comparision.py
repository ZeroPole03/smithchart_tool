# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
# cpp_comparision.py

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from smithchart_tool import *


plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 16,
    "axes.labelsize": 20,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
})

# window color setup
plt.rcParams['figure.facecolor'] = '#b3b3b3ff'
plt.rcParams['axes.facecolor'] = '#f4f4f4ff'


plt.figure(figsize=(8, 8))

theta = np.linspace(0, 2*np.pi, 1000)

smith = SmithChart(theta, unitary=False)
smith.plotChart(admittance=False)

cadena = r''

f0 = 3e9
C = 9.9999e-12

# Interconexión de los componentes de la red
Z0 = 50.0

Z1 = Impedance(Z0, 70.561 + 1j*5.052)

TL1 = TransmissionLine(82, Z1, 71.39, f0)
TL1.addToSmithChart(theta, cadena)
Z1.addToSmithChart(cadena)

Cap = Capacitor(Z0, TL1.getImpedance(), C, f0)

Z3 = Impedance(Z0, Cap.getImpedance())
Z3.addToSmithChart(cadena)

Cap.addToSmithChart(theta, cadena)

TL2 = TransmissionLine(77, Z3, 41.86, f0)
TL2.addToSmithChart(theta, cadena)

imp2 = TL2.getImpedance()

stub = OpenStub(77.0, imp2, 11.99, f0)
stub.addToSmithChart(cadena)

imp3 = stub.getImpedance()

Z4 = Impedance(Z0, imp3)

TL3 = TransmissionLine(77, Z4, 40.55, f0)
TL3.addToSmithChart(theta, cadena)
TL3.labelOnChart(True)


# ==========================================================
# CARGAR TRAYECTORIAS GENERADAS POR C++
# ==========================================================

cpp_data = pd.read_csv("cpp_trajectories.csv")


# ==========================================================
# GRAFICAR TRAYECTORIAS DE C++
# ==========================================================

elements = [
    "TL1",
    "CAP",
    "TL2",
    "STUB",
    "TL3"
]

for element in elements:

    data = cpp_data[cpp_data["element"] == element]

    gamma_real = data["real"].to_numpy()
    gamma_imag = data["imag"].to_numpy()

    plt.plot(
        gamma_real,
        gamma_imag,
        linestyle="--",
        linewidth=2,
        label=element + " C++"
    )


# ==========================================================
# Configuración de la ventana del plot
# ==========================================================

plt.ylabel(r'$Im\{\Gamma\}$')
plt.xlabel(r'$Re\{\Gamma\}$')

plt.xlim(-1, 1)
plt.ylim(-1, 1)

ax1 = plt.gca()

plt.legend()

plt.gca().set_aspect('equal')

plt.show()