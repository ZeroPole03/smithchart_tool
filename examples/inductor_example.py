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

# Window plot color parameters
plt.rcParams['figure.facecolor'] = '#b3b3b3ff';
plt.rcParams['axes.facecolor'] = '#f4f4f4ff';

# We put initialize and plot the SmithChart
plt.figure(figsize=(8, 8));
theta = np.linspace(0, 2.0*np.pi, 1000);
Chart = SmithChart(theta, unitary = True);
Chart.plotChart(); f0 = 3e9; cadena = '';

# Lumped parameters and characteristic impedance
Z0 = 50.0; L = 8.054e-9;

# We create a Load Impedance
imp = 50 + 1j*50;

# We create the lumped objects 
Load = Impedance(Z0, imp);
L1 = Inductor(Z0, imp, L, f0);

# Plot whithin the Smith Chart
Load.addToSmithChart(cadena);
Load.plotCircles(theta);
L1.addToSmithChart(theta);
L1.labelOnChart(False);



# Plotting window configuration
plt.ylabel(r'$Im\{\Gamma\}$');
plt.xlabel(r'$Re\{\Gamma\}$');
plt.xlim(-1, 1);
plt.ylim(-1, 1);
ax1 = plt.gca();   # eje actual
#ax2 = ax1.twinx()   # eje Y derecho
#ax2.set_ylim(1, -1)  # invertido
#plt.title('Smith Chart');
plt.legend();
#plt.grid();
plt.gca().set_aspect('equal');
plt.show()



