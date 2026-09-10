import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
from skrf import Frequency
from skrf.media import MLine
from smithchart_tool import *
# CONFIGURACIÓN DE LA FIGURA
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 16,
    "axes.labelsize": 20,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
})

er = 3.66              # Permitividad relativa RO4350B
h = 0.762e-3           # Altura del sustrato [m]
t = 18e-6              # Espesor del cobre [m]
f0 = 3e9               # Frecuencia central [Hz]
# Resistividad aproximada del cobre
rho_cu = 1.68e-8       # Ohm*m
# FUNCIÓN: IMPEDANCIA DE UNA MICROSTRIP
def microstrip_z0(width, h, t, er, f0):
    freq = Frequency(f0 / 1e9,f0 / 1e9,1,unit='GHz');
    line = MLine(frequency=freq,z0_port=50,w=width,
        h=h,
        t=t,
        ep_r=er,
        mu_r=1,
        rho=rho_cu,
        model='hammerstadjensen',
        disp='none'
    )
    z0 = np.real(line.z0_characteristic[0]);
    ep_eff = np.real(line.ep_reff_f[0]);
    return z0, ep_eff;

# FUNCIÓN: SÍNTESIS DE WIDTH PARA UNA IMPEDANCIA OBJETIVO
def synthesize_width(
        Z_target,
        h,
        t,
        er,
        f0,
        w_min=None,
        w_max=None,
        tolerance=1e-4,
        max_iterations=100):
    """
    Encuentra el ancho W de una microstrip que produzca
    aproximadamente Z_target utilizando Hammerstad-Jensen
    mediante búsqueda binaria.
    tolerance:
        Error relativo permitido.
    """
    if w_min is None:
        w_min = h * 1e-3;

    if w_max is None:
        w_max = h * 100.0;
    # Calculamos impedancias en los extremos
    Z_min, _ = microstrip_z0(w_max, h, t, er, f0);
    Z_max, _ = microstrip_z0(w_min, h, t, er, f0);
    # Comprobamos que el objetivo está dentro del rango
    if not (Z_min <= Z_target <= Z_max):
        raise ValueError(
            f"Z_target = {Z_target:.3f} Ohm está fuera "
            f"del rango sintetizable.\n"
            f"Rango aproximado: "
            f"{Z_min:.3f} - {Z_max:.3f} Ohm"
        )

    # Búsqueda binaria
    for _ in range(max_iterations):
        w_mid = 0.5 * (w_min + w_max);
        Z_mid, _ = microstrip_z0(w_mid, h, t, er, f0);
        error = abs(Z_mid - Z_target) / Z_target;
        if error < tolerance:
            break;
        # Si Z_mid es demasiado alta,
        # necesitamos una pista más ancha.
        if Z_mid > Z_target:
            w_min = w_mid
        else:
            w_max = w_mid

    # Permitividad efectiva final
    Z_final, ep_eff = microstrip_z0(w_mid, h, t, er, f0);
    return w_mid, Z_final, ep_eff


# FUNCIÓN: CONVERTIR ÁNGULO ELÉCTRICO A LONGITUD FÍSICA
def electrical_length_to_physical(
        theta_deg,
        f0,
        ep_eff):
    """
    Convierte longitud eléctrica theta [deg]
    a longitud física [m].
    theta = beta * L
    beta = 2*pi*f0*sqrt(ep_eff)/c
    """

    c = 299792458.0;
    theta_rad = np.deg2rad(theta_deg);
    beta = (2.0 * np.pi *f0 *np.sqrt(ep_eff)/ c);
    length = theta_rad / beta;
    return length;

# FIGURA DEL SMITH CHART

plt.figure(figsize=(8, 8));
theta = np.linspace(0,2*np.pi,1000);
Chart = SmithChart(theta,unitary=False);
cadena = r'';
Chart.plotChart(admittance=False);
# PARÁMETROS DEL TAPER
# Longitud eléctrica total
length = 183.0;       # grados
# Número de secciones
N = 100
# Ángulo eléctrico de cada sección
dtheta = length / N;

# IMPEDANCIA INICIAL# 
Z0 = 50
Z_start = 90
Z_end = 50

# CARGA INICIAL
Zk = Impedance(Z0,Z_start);
Zk.addToSmithChart(cadena);
Zk.plotCircles(theta);
impNew = 0;

# ARRAYS PARA LA GEOMETRÍA FÍSICA
Z_sections = [];
width_sections = [];
length_sections = [];
theta_sections = [];
ep_eff_sections = [];
position_sections = [];
physical_position = 0.0;

# TAPER EXPONENCIAL
for k in range(N):
    x = (k + 0.25) / N
    Z0k = (Z_start *(Z_end / Z_start)**x);
    # Guardamos impedancia objetivo
    Z_sections.append(Z0k);
    # TRANSMISSION LINE ORIGINAL
    TLk = TransmissionLine(Z0k,Zk,dtheta,f0);
    TLk.addToSmithChart(theta,cadena);
    # IMPEDANCIA DE SALIDA DE LA SECCIÓN
    impNew = TLk.getImpedance();
    Zk = Impedance(Z0,impNew);
    # SÍNTESIS FÍSICA
    try:
        width, Z_calc, ep_eff = synthesize_width(Z0k,h,t,er,f0);

    except ValueError as error:
        print(f"Error en sección {k}:");
        print(error);
        raise
    # Convertimos la longitud eléctrica
    # de la sección a longitud física
    physical_length = electrical_length_to_physical(dtheta,f0,ep_eff);
    # Guardamos resultados
    width_sections.append(width);
    length_sections.append(physical_length);
    theta_sections.append(dtheta);
    ep_eff_sections.append(ep_eff);
    position_sections.append(physical_position);
    physical_position += physical_length;


# RESULTADOS DEL TAPER
width_sections = np.array(width_sections);
length_sections = np.array(length_sections);
Z_sections = np.array(Z_sections);
ep_eff_sections = np.array(ep_eff_sections);
position_sections = np.array(position_sections);

# RESULTADOS
print()
print("============================================")
print("         MICROSTRIP TAPER")
print("============================================")

print(f"Number of sections : {N}");
print(f"Electrical length  : {length:.3f} deg");
print(
    f"Physical length    : "
    f"{np.sum(length_sections)*1e3:.3f} mm"
)

print(
    f"Initial impedance  : "
    f"{Z_sections[0]:.3f} Ohm"
)

print(
    f"Final impedance    : "
    f"{Z_sections[-1]:.3f} Ohm"
)

print(
    f"Initial width      : "
    f"{width_sections[0]*1e3:.4f} mm"
)

print(
    f"Final width        : "
    f"{width_sections[-1]*1e3:.4f} mm"
)

print(
    f"Minimum width      : "
    f"{np.min(width_sections)*1e3:.4f} mm"
)

print(
    f"Maximum width      : "
    f"{np.max(width_sections)*1e3:.4f} mm"
)

print()

# SMITH CHART

TLk.labelOnChart(True,0.1,0.15);
Zk.plotCircles(theta);
print("For ",N," sections we obtain:");
TLk.printImpedance();
plt.ylabel(r'$Im\{\Gamma\}$');
plt.xlabel(r'$Re\{\Gamma\}$');
plt.xlim(-1, 1);
plt.ylim(-1, 1);
plt.legend();
plt.gca().set_aspect('equal');
plt.show();


# FIGURA FÍSICA DEL TAPER
fig, ax = plt.subplots(figsize=(14, 4));
# Convertimos metros -> milímetros
width_mm = width_sections * 1e3;
length_mm = length_sections * 1e3;
# Posición acumulada en mm
x_position_mm = np.concatenate(([0],np.cumsum(length_mm)));
# Dibujamos cada sección
for k in range(N):
    x0 = x_position_mm[k];
    Lk = length_mm[k];
    Wk = width_mm[k];
    rectangle = plt.Rectangle(
        (
            x0,
            -Wk / 2
        ),
        Lk,
        Wk,
        linewidth=0,
        edgecolor=None,
        facecolor='#3a34eb'
    )
    ax.add_patch(rectangle);

# Eje central
ax.axhline(0,color='black',linewidth=0.8,linestyle='--');
ax.set_xlabel(r'Physical position $z$ [mm]');
ax.set_ylabel(r'Width $W$ [mm]');
ax.set_xlim(0,np.sum(length_mm));
max_width_mm = np.max(width_mm);
ax.set_ylim(-max_width_mm * 0.75,max_width_mm * 0.75);
ax.set_title(r'Physical approximation of the exponential taper');
ax.grid(True, alpha=0.25);
plt.tight_layout();
plt.show();


# PERFIL Z0 VS POSICIÓN
fig, ax = plt.subplots(figsize=(10, 5));
# Posición central de cada sección
section_centers = (position_sections + length_sections / 2.0);

# Perfil continuo
z_continuous = np.linspace(0,np.sum(length_sections),1000);
x_continuous = (z_continuous /np.sum(length_sections));
Z_continuous = (Z_start *(Z_end / Z_start)**x_continuous);
# Perfil continuo

ax.plot(z_continuous * 1e3,Z_continuous,linewidth=2,label=r'Continuous exponential profile');

# Secciones discretas
ax.scatter(section_centers * 1e3,Z_sections,s=8,label=r'Discrete sections');
ax.set_xlabel(r'Physical position $z$ [mm]');
ax.set_ylabel(r'Characteristic impedance $Z_0$ [$\Omega$]');
ax.set_title(r'Exponential taper discretization');
ax.grid(True,alpha=0.25);
ax.legend();
plt.tight_layout();
plt.show();