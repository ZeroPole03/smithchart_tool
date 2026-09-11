import numpy as np
import matplotlib.pyplot as plt
from .impedance import Impedance


class Capacitor(Impedance):
    def __init__(self, Z0, C, f0):
        self.C = C
        self.f0 = f0
        # Impedancia inicial
        super().__init__(Z0, 0);
        self.Zc = self.getImpedanceCapacitor();
        # Actualizamos la impedancia y Gamma
        self.updateCapacitor()

    # CAPACITANCE
    def setCapacitance(self, Cin):
        self.C = Cin;
        self.updateCapacitor();

    def getCapacitnce(self):
        return self.C;
    # FREQUENCY
    def setFrequency(self, f0):
        self.f0 = f0;
        self.updateCapacitor();

    def getFrequency(self):
        return self.f0;
    # CAPACITOR IMPEDANCE
    def getImpedanceCapacitor(self):
        omega = 2.0 * np.pi * self.f0;
        self.Zc = -1j / (omega * self.C);
        return self.Zc;
    # UPDATE
    def updateCapacitor(self):
        self.Zl = self.getImpedanceCapacitor();
        # Gamma respecto a Z0
        self.Gamma = (self.Zl - self.Z0) / (self.Zl + self.Z0);
        self.gr = np.real(self.Gamma);
        self.gi = np.imag(self.Gamma);
        self.mag = np.abs(self.Gamma);
        self.angle = np.angle(self.Gamma);
        # SWR
        self.swr = (1.0 + np.abs(self.Gamma)) / (1.0 - np.abs(self.Gamma));

    # SMITH CHART
    def addToSmithChart(self,cadena="Capacitor",color='green'):
        self.cadena = cadena;
        plt.scatter(self.gr,self.gi,color=color,zorder=5);
        plt.plot([0, self.gr],[0, self.gi],color=color,lw=2,label=self.cadena);

    # CONSTANT RESISTANCE ARC
    def plotArc(self,theta,color='green'):
        # Resistencia normalizada
        R = np.real(self.Zl) / self.Z0;
        # Reactancia normalizada del capacitor
        X = np.imag(self.Zl) / self.Z0;
        # Gamma actual
        gamma = ((R + 1j * X - 1)/(R + 1j * X + 1));
        # Centro y radio del círculo de resistencia constante
        center_x = R / (R + 1.0);
        radius = 1.0 / (R + 1.0);
        # Ángulo geométrico del punto
        phi = np.angle(gamma - center_x);
        alpha = np.linspace(phi,-np.pi,500);
        gamma_arc = (center_x+radius * np.exp(1j * alpha));
        # Coordenadas del arco
        x = np.real(gamma_arc);
        y = np.imag(gamma_arc);
        plt.plot(x,y,color=color,lw=2);
        return gamma_arc;

    # CAPACITOR TRAJECTORY
    def gammaLine(self,Cmin,Cmax,points=500):
        C = np.linspace(Cmin,Cmax,points);
        omega = 2.0 * np.pi * self.f0;
        Z = (-1j/(omega * C));
        gamma = (Z - self.Z0) / (Z + self.Z0);
        return C, gamma;


