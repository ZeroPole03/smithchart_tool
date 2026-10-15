# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from smithchart_tool import *

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 16,           # Tamaño base general
    "axes.labelsize": 20,      # Etiquetas de los ejes
    "xtick.labelsize": 16,     # Números en el eje X
    "ytick.labelsize": 16,     # Números en el eje Y
    "legend.fontsize": 16,     # Tamaño de las leyendas
})
# window color setup
plt.rcParams['figure.facecolor'] = '#b3b3b3ff'
plt.rcParams['axes.facecolor'] = '#f4f4f4ff'

plt.figure(figsize = (8, 8));
cpp_data = pd.read_csv("examples/cpp_trajectoriesOutput.csv")

elements = ["STUB1", "TL1", "TL2", "TL3", "C1", "TL4"]






theta = np.linspace(0, 2*np.pi, 1000);
smith = SmithChart(theta, unitary = False);
smith.plotChart(admittance = False); cadena = r'';
f0=3e9; 

# Interconectamos los elementos del circuito
Z0 = 50.0; C = 10.0e-12;
Z1 = Impedance(Z0, Z0);
Z1.addToSmithChart(cadena);
imp0 = Z1.getImpedance();
# Open Stub
stub1 = OpenStub(90.0, imp0, 28.49, f0);
stub1.addToSmithChart(cadena);
Z3 = Impedance(Z0, stub1.getImpedance());

TL1 = TransmissionLine(30, Z3, 12.01, f0);
TL1.addToSmithChart(theta, cadena);
Z4 = Impedance(Z0, TL1.getImpedance());

TL2 = TransmissionLine(35.4, Z4, 6.634, f0);
TL2.addToSmithChart(theta, cadena);
Z5 = Impedance(Z0, TL2.getImpedance());

TL3 = TransmissionLine(40, Z5, 7.391, f0);
TL3.addToSmithChart(theta, cadena);

Cap1 = Capacitor(Z0, TL3.getImpedance(), C, f0);
Z6 = Impedance(Z0, Cap1.getImpedance());
Z6.plotCircles(theta);
Z6.addToSmithChart(cadena);

Cap1.addToSmithChart(theta, cadena);
TL4 = TransmissionLine(40, Z6, 11.56, f0);
TL4.addToSmithChart(theta, cadena);
TL4.labelOnChart(True);

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

# Configuración de la ventana del plot
plt.ylabel(r'$Im\{\Gamma\}$');
plt.xlabel(r'$Re\{\Gamma\}$');
plt.xlim(-1, 1);
plt.ylim(-1, 1);
ax1 = plt.gca()      # eje actual
#ax2 = ax1.twinx()   # eje Y derecho
#ax2.set_ylim(1, -1)  # invertido
#plt.title('Carta de Smith');
plt.legend();
#plt.grid();
plt.gca().set_aspect('equal');
plt.show();
