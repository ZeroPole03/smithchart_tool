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

cpp_data = pd.read_csv("examples/cpp_trajectories.csv")


# ==========================================================
# GRAFICAR TRAYECTORIAS DE C++
# ==========================================================

elements = [
    "TL1",
    "CAP",
    "TL2",
    "STUB1",
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


# =========================================================
# C++ Input Gamma response
# =========================================================

gamma_data = np.loadtxt(
    "examples/cpp_Gamma.csv",
    delimiter=",",
    skiprows=1
)

frequency = gamma_data[:, 0] / 1e9
gamma_real = gamma_data[:, 1]
gamma_imag = gamma_data[:, 2]

gamma = gamma_real + 1j*gamma_imag

gamma_db = 20.0 * np.log10(np.abs(gamma))

gamma_phase = np.angle(
    gamma,
    deg=True)

gamma_phase = np.rad2deg(
    np.unwrap(
        np.deg2rad(gamma_phase)
    )
)

fig, ax1 = plt.subplots()

ax1.plot(
    frequency,
    gamma_db,
    lw = 2.0,
    color = 'black',
    label = r'$|\Gamma_{in}|$'
)

ax1.set_xlabel("Frequency (GHz)")
ax1.set_ylabel(r"$|\Gamma_{in}|$ (dB)")
ax1.grid()

ax2 = ax1.twinx()

ax2.plot(
    frequency,
    gamma_phase,
    linestyle = '--',
    lw = 2.0,
    color = 'red',
    label = r'$\angle\,\,\Gamma_{in}$'
)

ax2.set_ylabel(
    r"$\angle\,\,\Gamma_{in}$ [Deg]"
)

#plt.title("Input Reflection Coefficient")

fig.tight_layout()
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc = 'best'
)

# =========================================================
# C++ Transmission response
# =========================================================

transmission_data = np.loadtxt(
    "examples/cpp_Transmission.csv",
    delimiter=",",
    skiprows=1
)

transmission_frequency = (
    transmission_data[:, 0] / 1e9
)

transmission_real = transmission_data[:, 1]
transmission_imag = transmission_data[:, 2]

transmission = (
    transmission_real +
    1j * transmission_imag
)

transmission_mag = np.abs(
    transmission
)

transmission_db = 20.0 * np.log10(
    transmission_mag
)

transmission_phase = np.angle(
    transmission,
    deg=True
)

transmission_phase = np.rad2deg(
    np.unwrap(
        np.deg2rad(transmission_phase)
    )
)

fig, ax1 = plt.subplots()

ax1.plot(
    transmission_frequency,
    transmission_db,
    lw = 2.0,
    color = 'black',
    label = r'T'
)

ax1.set_xlabel("Frequency (GHz)")
ax1.set_ylabel(
    r"$|T|$ (dB)"
)

ax1.grid()

ax2 = ax1.twinx()

ax2.plot(
    transmission_frequency,
    transmission_phase,
    lw = 2.0,
    color = 'red',
    linestyle = '--',
    label = r'$\angle T$'
)

ax2.set_ylabel(
    r"$\angle\,\,T$ [Deg]"
)

#plt.title("Transmission Response")

fig.tight_layout()
ax2.set_ylabel(
    r"$\angle\,\,T$ [Deg]"
)

#plt.title("Transmission Response")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc = 'best'
)

fig.tight_layout()

plt.show()