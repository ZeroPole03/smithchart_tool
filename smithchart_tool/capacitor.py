import numpy as np
import matplotlib.pyplot as plt
from .impedance import Impedance


class Capacitor(Impedance):
    def __init__(self, Z0, ZL, C, f0, domain="impedance"):
        self.Z0 = Z0;
        self.ZL = ZL;
        self.C = C;
        self.f0 = f0;
        self.domain = domain.lower();

        if self.domain not in ["impedance", "admittance"]:
            raise ValueError(
                "domain must be 'impedance' or 'admittance'"
            );

        self.Zc = -1j / (2 * np.pi * self.f0 * self.C);
        self.Yc = 1j * 2 * np.pi * self.f0 * self.C;

        if self.domain == "impedance":
            self.Zin = self.ZL;
            self.gammaIn = (self.Zin - self.Z0) / (self.Zin + self.Z0);
            # Series capacitor
            self.Zout = self.Zin + self.Zc;
            self.gammaOut = (self.Zout - self.Z0) / (self.Zout + self.Z0);
        else:
            self.Yin = self.ZL;
            # Parallel capacitor
            self.Yout = self.Yin + self.Yc;
            # Convert back to impedance
            self.Zout = 1 / self.Yout;
            # Gamma in the impedance Smith chart
            self.gammaIn = (1 / self.Yin - self.Z0) / (1 / self.Yin + self.Z0);
            self.gammaOut = (self.Zout - self.Z0) / (self.Zout + self.Z0);


        self.gr = np.real(self.gammaOut);
        self.gi = np.imag(self.gammaOut);
        self.mag = np.abs(self.gammaOut);
        self.angle = np.angle(self.gammaOut);
        self.swr = (
            1 + np.abs(self.gammaOut)
        ) / (
            1 - np.abs(self.gammaOut)
        );

    def setCapacitance(self, Cin):
        self.C = Cin;
        self.Zc = -1j / (2 * np.pi * self.f0 * self.C);
        self.Yc = 1j * 2 * np.pi * self.f0 * self.C;
        self._update();

    def getCapacitnce(self):
        return self.C


    def _update(self):
        if self.domain == "impedance":
            self.Zout = self.Zin + self.Zc;
        else:
            self.Yout = self.Yin + self.Yc;
            self.Zout = 1 / self.Yout;

        self.gammaOut = (self.Zout - self.Z0) / (self.Zout + self.Z0);
        self.gr = np.real(self.gammaOut);
        self.gi = np.imag(self.gammaOut);
        self.mag = np.abs(self.gammaOut);
        self.angle = np.angle(self.gammaOut);
        self.swr = (1 + np.abs(self.gammaOut)) / (1 - np.abs(self.gammaOut));

    def getImpedance(self):
        return self.Zout;

    def getAdmittance(self):
        if self.domain == "admittance":
            return self.Yout;

        return 1 / self.Zout;


    def addToSmithChart(self,theta,cadena="Capacitor",color="#008e8eff"):
        self.cadena = cadena;
        alpha = np.linspace(0.0, 1.0, 1000);
        if self.domain == "impedance":
            Zpath = (self.Zin- 1j * alpha /(2 * np.pi * self.f0 * self.C));
            gamma = (Zpath - self.Z0) / (Zpath + self.Z0);

        else:
            Ypath = (self.Yin+ 1j * alpha *2 * np.pi * self.f0 * self.C);
            # Convert admittance path to impedance
            Zpath = 1 / Ypath;
            gamma = (Zpath - self.Z0) / (Zpath + self.Z0);

        x = np.real(gamma);
        y = np.imag(gamma);
        # Radial line to final point
        plt.plot([0, self.gr],[0, self.gi],color='black');
        # Capacitor trajectory
        plt.plot(x,y,color=color,lw=3,label=self.cadena);
        # Initial point
        plt.scatter(np.real(self.gammaIn),np.imag(self.gammaIn),color='black');
        # Final point
        plt.scatter(self.gr,self.gi,color='black');





