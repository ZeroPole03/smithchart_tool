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
Chart = SmithChart(theta, unitary = True); cadena = r'';
Chart.plotChart(admittance = False); f0 = 3e9;
length = 0.081*360.0;
Z0 = 50.0; L = 4.054e-9;
Xl = 1j*2*np.pi*f0*L;

# We define our load impedance
imp = 150 + 1j*50;
ZL = Impedance(Z0, imp);
YL = Admittance(Z0, ZL);
YL.addToSmithChart(theta);
ZL.addToSmithChart(cadena);
ZL.plotCircles(theta);
#ZL.labelOnChart(True);
stub = OpenStub(50, imp, length, f0);
stub.addToSmithChart(cadena);
#stub.labelOnChart();
# Adding series inductor to complete matching
imp2 = stub.getImpedance(); 
imp2 += Xl;
#Showing new Impedance in the SmithChart
ZL2 = Impedance(Z0, imp2);
ZL2.addToSmithChart(cadena);
ZL2.plotCircles(theta);
ZL2.labelOnChart(True);


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