import numpy as np
import matplotlib.pyplot as plt
from .impedance import Impedance


class Capacitor(Impedance):

    def __init__(self, Z0, ZL, C, f0):
        self.Z0 = Z0;
        self.ZL = ZL;
        self.C = C;
        self.f0 = f0;
        # Impedancia inicial
        self.Zin = ZL;
        # Impedancia del capacitor
        self.Zc = -1j / (2 * np.pi * self.f0 * self.C);
        # Impedancia resultante
        self.Zout = self.Zin + self.Zc;
        # Coeficiente de reflexión inicial
        self.gammaIn = (self.Zin - self.Z0) / (self.Zin + self.Z0);
        # Coeficiente de reflexión final
        self.Gamma = (self.Zout - self.Z0) / (self.Zout + self.Z0);
        self.gr = np.real(self.Gamma);
        self.gi = np.imag(self.Gamma);
        self.mag = np.abs(self.Gamma);
        self.angle = np.angle(self.Gamma);
        self.swr = (1 + np.abs(self.Gamma)) / (1 - np.abs(self.Gamma));

    def setCapacitance(self, Cin):
        self.C = Cin;
        self.Zc = -1j / (2 * np.pi * self.f0 * self.C);
        self.Zout = self.Zin + self.Zc;
        self.Gamma = (self.Zout - self.Z0) / (self.Zout + self.Z0);
        self.gr = np.real(self.Gamma);
        self.gi = np.imag(self.Gamma);

    def getCapacitnce(self):
        return self.C

    def getImpedance(self):
        return self.Zout

    def addToSmithChart(self,theta,cadena="",color1="#00d7f3ff"):
        self.cadena = cadena;
        # Parámetro geométrico para recorrer
        # desde la impedancia inicial hasta la final
        alpha = np.linspace(0.0, 1.0, 1000);
        # Trayectoria de impedancia
        Zpath = (self.Zin- 1j * alpha /(2 * np.pi * self.f0 * self.C));
        # Transformación a Gamma
        gamma = (Zpath - self.Z0) / (Zpath + self.Z0);
        x = np.real(gamma);
        y = np.imag(gamma);
        # Punto inicial
        plt.scatter(np.real(self.gammaIn),np.imag(self.gammaIn),color='black');
        # Punto final
        plt.scatter(self.gr,self.gi,color='black');
        # Línea desde el centro hasta el punto final
        plt.plot([0, self.gr],[0, self.gi],color='black',label=self.cadena);
        # Arco del capacitor
        plt.plot(x,y,color=color1,lw=3);



