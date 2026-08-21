# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
import numpy as np
import matplotlib.pyplot as plt
from .impedance import Impedance

class Admittance:
    # g = 1; b = 1; y = 1.0 + 1j; 
    # load = 50.0 + 1j*50.0; z0 = 50.0;
    # angle = 0; mag = 1.0; tl = 1.0 + 1.0j;
    # gin = 1; giin = 1; yin = gin + 1j*giin;
    # grot = 1 + 1j; gammar = 1.0; gammai = 1.0;
    c = 3e8;
    def __init__(self, z0, Impedance):
        self.load = Impedance;
        self.z0 = z0;
        # self.mag = np.abs(self.load.gamma0);
        # self.angle = np.angle(self.load.gamma0) + np.pi;
        gamma = self.load.getGamma();
        self.mag = np.abs(gamma);
        self.angle = np.angle(gamma) + np.pi;
        self.gammar = self.mag * np.cos(self.angle);
        self.gammai = self.mag * np.sin(self.angle);
        self.grot = self.gammar + 1j*self.gammai;
        self.g = (1 - self.gammar**2 - self.gammai**2) / ((self.gammar - 1)**2 + self.gammai**2);
        self.b = 2 * self.gammai / ((self.gammar - 1)**2 + self.gammai**2);
        self.y = self.g + 1j * self.b;
        self.gamma0 = self.gammar + 1j*self.gammai;


    def addToSmithChart(self, theta, color = 'red', color1 = 'red'):
        x = (1 / (self.g + 1)) * (np.cos(theta) - self.g);
        y = (1 / (self.g + 1)) * np.sin(theta);
        x1 = (1 / self.b) * np.cos(theta) - 1;
        y1 = (1 / self.b) * (np.sin(theta) - 1);
        #y2 = (1 / self.load.react) * (np.sin(theta) + 1);
        plt.plot(x, y, color = color, lw = 2);
        plt.plot(x1, y1, color = color, lw = 2);
        #plt.plot(x1, y2, color = color1, lw = 3);
        #plt.plot([0, self.gammar],[0, self.gammai], color = 'red', lw = 2);
        #plt.scatter(self.gammar, self.gammai, color = 'red');


    def printAdmitance(self):
        print("-------------------------------------------------------------");
        print("La admitancia de la impedancia es: ")
        print(f'{(self.y/self.z0):.3f}', " Siemens");
        print("Fasor: ", f'{np.abs(self.y):.3f}', " < ", 
            f'{np.angle(self.y, deg = True):.3f}');

    def getAdmitance(self):
        return self.y

    def getImpedance(self):
        return 1/self.y

    def getLoadAdmitance(self):
        return (self.y/self.z0);

    def getGamma(self):
        return self.gamma0;

    def transToAdmitance(self, TransmissionLine, color1 = 'red', label1 = False):
        self.tl = TransmissionLine;
        self.gin = self.mag * np.cos(self.angle - self.tl.phase);
        self.giin = self.mag * np.sin(self.angle - self.tl.phase);
        conduct = (1 - self.gin**2 - self.giin**2) / ((1 - self.gin)**2 + self.giin**2);
        susep = 2 * self.giin / ((1 - self.gin)**2 + self.giin**2);
        x = (1 / (conduct + 1)) * (np.cos(theta) - conduct);
        y = (1 / (conduct + 1)) * np.sin(theta);
        x1 = (1 / susep) * np.cos(theta) - 1;
        y1 = (1 / susep) * (np.sin(theta) - 1);
        #y2 = (1 / self.load.react) * (np.sin(theta) + 1);
        plt.plot(x, y, color = color1, lw = 2);
        plt.plot(x1, y1, color = color1, lw = 2);
        #plt.plot(x1, y2, color = color1, lw = 3);
        #plt.plot([0, self.gin],[0, self.giin], color = 'red', lw = 2);
        #plt.scatter(self.gin, self.giin, color = 'red');
        if(label1):
            if(susep < 0):
                plt.annotate(r'$Y_{in}= %.3f - j %.3f$' % (conduct/self.z0, -1*susep/self.z0),
                            xy = (-0.95, 0.65),
                            xytext = (-0.95, 0.65),
                            ha = 'left',
                            va = 'center');
            else:
                plt.annotate(r'$Y_{in}= %.3f + j %.3f$' % (conduct/self.z0, susep/self.z0),
                            xy = (-0.95, 0.65),
                            xytext = (-0.95, 0.65),
                            ha = 'left',
                            va = 'center');


        self.yin = conduct + 1j*susep;
        print("------------------------------------------------------------");
        print("La Admitancia normalizada de entrada es: ");
        print(f'{(self.yin):.3f}');
        print("Fasor: ", f'{np.abs(self.yin):.3f}', " < ", f'{np.angle(self.yin, deg = True):.3f}');


    def labelOnChart(self, band = 'True', x0 = -0.95, y0 = 0.75):
        if(self.b < 0):
            plt.annotate(r'$Y_{L}= %.2f - j%.2f\,\Omega$' % (self.g / self.z0, -1*self.b / self.z0),
                        xy = (x0, y0), 
                        xytext = (x0, y0),
                        textcoords = 'offset points',
                        ha = 'left',
                        va = 'center');
        else:
            plt.annotate(r'$Y_{L}= %.2f+ j%.2f\,\Omega$' % (self.g / self.z0, self.b / self.z0),
                        xy = (x0, y0), 
                        xytext = (x0, y0),
                        textcoords = 'offset points',
                        ha = 'left',
                        va = 'center'); 

    def __add__(self, other):
        if hasattr(other, "getAdmitance"):
            other = other.getAdmitance()
        return self.getAdmitance() + other


    def __sub__(self, other):
        if hasattr(other, "getAdmitance"):
            other = other.getAdmitance()
        return self.getAdmitance() - other


    def __mul__(self, other):
        if hasattr(other, "getAdmitance"):
            other = other.getAdmitance()
        return self.getAdmitance() * other


    def __truediv__(self, other):
        if hasattr(other, "getAdmitance"):
            other = other.getAdmitance()
        return self.getAdmitance() / other


    def __radd__(self, other):
        return other + self.getAdmitance()


    def __rsub__(self, other):
        return other - self.getAdmitance()


    def __rmul__(self, other):
        return other * self.getAdmitance()


    def __rtruediv__(self, other):
        return other / self.getAdmitance()


    def __repr__(self):
        return f"{self.getAdmitance():.4e}"

