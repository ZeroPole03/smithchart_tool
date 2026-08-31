# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
import numpy as np
import matplotlib.pyplot as plt

class Impedance:
    # z0 = 50.0 + 0*1j; Zl = 1 + 1j; zn = 0.5 + 1j * 0.5; 
    # gi = 1; gr = 1; gamma0 = 0.5 + 1j * 0.5; resis = 0.5;
    # react = 0.5; gammain = 0.5 + 1j * 0.5; Zin = 50 + 1j* 50;
    # phase = 0; angle = np.pi; cadena = '';
    c = 3e8;
    def __init__(self, z0, Zl):
        self.z0 = z0; 
        self.Zl = Zl;
        self.zn = self.Zl * (1 / self.z0);
        self.resis = np.real(self.zn);
        self.react = np.imag(self.zn);
        self.gr = (self.react**2 + self.resis**2 - 1) / ((self.resis + 1)**2 + self.react**2);
        self.gi = 2 * self.react / ((self.resis + 1)**2 + self.react**2);
        self.gamma0 = self.gr + 1j * self.gi;
        self.angle = np.angle(self.gamma0);

    def getGamma(self):
        return self.gamma0;

    def labelOnChart(self, band, x0 = -0.95, y0 = 0.95):
        if(band):
            if(self.react < 0):
                plt.annotate(r'$Z_{in}= %.2f - j%.2f\,\Omega$' % (self.resis*self.z0, -1*self.z0*self.react),
                            xy = (x0, y0), 
                            xytext = (x0, y0),
                            textcoords = 'offset points',
                            ha = 'left',
                            va = 'center');
                plt.annotate(r'$|\Gamma|\angle\theta= %.2f\angle %.2f$' % (np.abs(self.gamma0), np.angle(self.gamma0, deg = True)),
                            xy = (-0.95, -0.85),
                            xytext = (-0.95, -0.85),
                            textcoords = 'offset points',
                            ha = 'left',
                            va = 'center');
            else:
                plt.annotate(r'$Z_{in}= %.2f+ j%.2f\,\Omega$' % (self.resis*self.z0, self.z0*self.react),
                            xy = (x0, y0), 
                            xytext = (x0, y0),
                            textcoords = 'offset points',
                            ha = 'left',
                            va = 'center'); 
                plt.annotate(r'$|\Gamma|\angle\theta= %.2f\angle %.2f$' % (np.abs(self.gamma0), np.angle(self.gamma0, deg = True)),
                            xy = (-0.95, -0.85),
                            xytext = (-0.95, -0.85),
                            textcoords = 'offset points',
                            ha = 'left',
                            va = 'center');


    def getImpedance(self):
        return self.Zl

    def getAdmitance(self):
        return 1/self.Zl

    def __add__(self, other):
        if hasattr(other, "getImpedance"):
            other = other.getImpedance()
        return self.getImpedance() + other


    def __sub__(self, other):
        if hasattr(other, "getImpedance"):
            other = other.getImpedance()
        return self.getImpedance() - other


    def __mul__(self, other):
        if hasattr(other, "getImpedance"):
            other = other.getImpedance()
        return self.getImpedance() * other


    def __truediv__(self, other):
        if hasattr(other, "getImpedance"):
            other = other.getImpedance()
        return self.getImpedance() / other


    def __radd__(self, other):
        return other + self.getImpedance()


    def __rsub__(self, other):
        return other - self.getImpedance()


    def __rmul__(self, other):
        return other * self.getImpedance()


    def __rtruediv__(self, other):
        return other / self.getImpedance()


    def __repr__(self):
        return f"{self.getImpedance():.4f}"


    def printImpedance(self):
        print("Impedancia de carga Normalizada: ", self.zn);



    def addToSmithChart(self, cadena):
        self.cadena = cadena;
        plt.scatter(self.gr, self.gi, color = 'black');
        plt.plot([0, self.gr], [0, self.gi], 
                    color = 'black', 
                    label = self.cadena);   

    def plotCircles(self, theta, color1 = 'black', color2 = 'black'):
        if(self.react < 1e-4):
            # Radios de círculos de ZL
            radio2 = 1/(self.resis + 1);
            # Resistiva de entrada 
            x3 = radio2 * np.cos(theta) + self.resis/(self.resis + 1);
            y3 = radio2 * np.sin(theta);
            # Círculo resistivo de entrada
            plt.plot(x3, y3, color = color1, lw = 2);
        else:
            # Radios de círculos de ZL
            radio2 = 1/(self.resis + 1);
            radio3 = 1/self.react;
            # Resistiva de entrada 
            x3 = radio2 * np.cos(theta) + self.resis/(self.resis + 1);
            y3 = radio2 * np.sin(theta);
            # Reactiva de entrada 
            x4 = radio3 * np.cos(theta) + 1;
            y4 = radio3 * np.sin(theta) + 1/self.react;
            # Círculo resistivo de entrada
            plt.plot(x3, y3, color = color1, lw = 2);
            # Círculo reactivo de entrada
            plt.plot(x4, y4, color = color2, lw = 2);


    def printSWR(self):
        swr = (1 + np.abs(self.gamma0))/(1 - np.abs(self.gamma0));
        print("------------------------------------------------------------")
        print("Valor de SWR: ", f'{swr:.3f}');

    def getSWR(self):
        swr = (1 + np.abs(self.gamma0))/(1 - np.abs(self.gamma0));
        return swr;

