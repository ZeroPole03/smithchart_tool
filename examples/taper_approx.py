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
plt.rcParams['figure.facecolor'] = '#b3b3b3ff';
plt.rcParams['axes.facecolor'] = '#f4f4f4ff';

plt.figure(figsize = (8, 8));
theta = np.linspace(0, 2*np.pi, 1000);
smith = SmithChart(theta, unitary = False);
smith.plotChart(admittance = False); cadena = r'';


# Taper length: 180°
N = 100;
length = 180;
dtheta = length/N;
# Initial conditions 
f0 = 3e9;
Z0 = 50;
Zk = Impedance(Z0, 150);
#Zk.addToSmithChart(cadena);
#Zk.plotCircles(theta);
impNew = 0;

# Linear Taper section approximation through TLines junction
for k in range(N):
    x = (k + 0.5) / N;
    Z0k = 150 + (50 - 150) * x;
    TLk = TransmissionLine(Z0k, Zk, dtheta, f0);
    TLk.addToSmithChart(theta, cadena);
    impNew = TLk.getImpedance();
    Zk = Impedance(Z0, impNew);

TLk.labelOnChart(True, 0.1, 0.15);
Zk.plotCircles(theta);
print("For", N,  "midpoint Sections we obatain: ");
TLk.printImpedance();



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