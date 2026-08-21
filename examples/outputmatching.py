# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
import numpy as np
import matplotlib.pyplot as plt
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

plt.figure(figsize = (8, 8));
theta = np.linspace(0, 2*np.pi, 1000);
smith = SmithChart(theta, unitary = False);
smith.plotChart(admitance = False); cadena = r'';
f0=3e9; Xc = -1j/(2*np.pi*f0*10.0e-12);

# Interconectamos los elementos del circuito
Z0 = 50.0;
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
imp = TL3.getImpedance();
imp += Xc;
Z6 = Impedance(Z0, imp);
Z6.plotCircles(theta);
Z6.addToSmithChart(cadena);
TL4 = TransmissionLine(40, Z6, 11.56, f0);
TL4.addToSmithChart(theta, cadena);
TL4.labelOnChart(True);

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
