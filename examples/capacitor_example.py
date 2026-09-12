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
# Window plot parameters
plt.rcParams['figure.facecolor'] = '#b3b3b3ff';
plt.rcParams['axes.facecolor'] = '#f4f4f4ff';

# We plot the Chart First
plt.figure(figsize = (8, 8));
theta = np.linspace(0, 2*np.pi, 1000);
Chart = SmithChart(theta, unitary = False); cadena = r'';
Chart.plotChart(admittance = False); f0 = 3e9;
length = 0.081*360.0;
Z0 = 50.0; L = 4.054e-9;
Xl = 1j*2*np.pi*f0*L;

imp = 150 + 1j*50;
Z = Impedance(Z0, imp);
imp1 = Z.getImpedance();
Adm1 = Admittance(Z0, Z);
Adm1.addToSmithChart(theta);
Z.plotCircles(theta);
Cap1 = Capacitor(Z0, 1/imp1, 1e-12, f0, domain = "admittance");
Cap1.addToSmithChart(theta, r'1 pF');
imp2 = Cap1.getImpedance();
TL1 = TransmissionLine(70, Impedance(Z0, imp2), 20, f0);
TL1.addToSmithChart(theta, "");
imp3 = TL1.getImpedance();
TL1.plotImpedanceCircles(theta, "");
Cap2 = Capacitor(Z0, imp3, 2e-12, f0);
Cap2.addToSmithChart(theta, r'2 pF');



# Plotting window configuration
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
plt.show()