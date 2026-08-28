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
# window color setup
plt.rcParams['figure.facecolor'] = '#b3b3b3ff'
plt.rcParams['axes.facecolor'] = '#f4f4f4ff'

plt.figure(figsize = (8, 8));
theta = np.linspace(0, 2*np.pi, 1000);
smith = SmithChart(theta, unitary = False);
smith.plotChart(admittance = False); cadena = r'';
f0=3e9; Xc = -1j/(2*np.pi*f0*9.9999e-12);

# Interconexión de los componentes de la red
Z0 = 50.0;
Z1 = Impedance(Z0, 70.561+1j*5.052); 
#Z1.plotCircles(theta);
TL1 = TransmissionLine(82, Z1, 71.39, f0);
#TL1.plotImpedanceCircles(theta, cadena);
TL1.addToSmithChart(theta, cadena);
Z1.addToSmithChart(cadena);
imp = TL1.getImpedance();
imp += Xc;
Z3 = Impedance(Z0, imp);
Z3.addToSmithChart(cadena);
Z3.plotCircles(theta);
TL2 = TransmissionLine(77, Z3, 41.86, f0);
#TL2.plotImpedanceCircles(theta, cadena);
TL2.addToSmithChart(theta, cadena);
imp2 = TL2.getImpedance();
stub = OpenStub(77.0, imp2, 11.99, f0);
stub.addToSmithChart(cadena);
#stub.plotImpedanceCircles(theta);
imp3 = stub.getImpedance();
Z4 = Impedance(Z0, imp3);
TL3 = TransmissionLine(77, Z4, 40.55, f0);
#TL3.plotImpedanceCircles(theta, cadena);
TL3.addToSmithChart(theta, cadena);
TL3.labelOnChart(True);

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