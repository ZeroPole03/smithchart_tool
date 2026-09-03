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

# We plot the Chart First
plt.figure(figsize = (8, 8));
theta = np.linspace(0, 2*np.pi, 1000);
Chart = SmithChart(theta, unitary = False); cadena = r'';
Chart.plotChart(admittance = False);
Z0 = 50.0;
imp = 150 + 1j*50;
ZL = Impedance(Z0, imp);
YL = Admittance(Z0, ZL);
YL.addToSmithChart(theta);
ZL.addToSmithChart(cadena);
ZL.plotCircles(theta);
ZL.labelOnChart(True);


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