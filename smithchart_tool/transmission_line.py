# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
import numpy as np
import matplotlib.pyplot as plt
from .impedance import Impedance

class TransmissionLine:
    length = 1e-2; rin = 1.0; xin = 1.0; 
    ginr = 1.0; giin = 1.0; lamda = 6e-2; f0 = 2.5e9;
    alpha = 0.0; Zin = 0.0; Gin = 1.0 + 1j; cadena = ''; 
    swr = 0; e = 1; phase = 0; load = 1.0 + 1.0j;
    caplength = 1e-2; Z0 = 50 + 1j*0; 

    def __init__(self, Z0, Impedance, deg, f0):
        self.load = Impedance;
        self.f0 = f0;
        self.Z0 = Z0;
        # Fase eléctrica (2βl)
        self.phase = 2.0 * deg;
        # Coeficiente de reflexión referido a la impedancia
        # característica de la línea
        self.gammaLine = (self.load.Zl - self.Z0) / (self.load.Zl + self.Z0);
        # Coeficiente propagado hacia la entrada de la línea
        self.gammaRot = self.gammaLine * np.exp(-1j * self.phase);
        # Transformación entre la carta de Smith de 50 Ω
        # y la carta natural de la línea
        self.k = (self.Z0 - 50.0) / (self.Z0 + 50.0);
        # Coeficiente de reflexión mostrado en la carta de 50 Ω
        self.Gin = (self.k + self.gammaRot) / (1 + self.k * self.gammaRot);
        # Componentes cartesianas
        self.ginr = np.real(self.Gin);
        self.giin = np.imag(self.Gin);
        # Magnitud y fase
        self.mag = np.abs(self.Gin);
        self.angle = np.angle(self.Gin);
        # Parámetro para dibujar el arco
        self.alpha = np.linspace(0.0, self.phase, 1000);
        # SWR respecto a la impedancia característica de la línea
        self.swr = (1 + np.abs(self.gammaLine)) / (1 - np.abs(self.gammaLine));

    def addToSmithChart(self, theta, cadena, color1 = '#18156b', color2 = '#18156b'):
        self.cadena = cadena;
        # Determinamos la impedancia de entrada
        self.rin = (1 - self.ginr**2 - self.giin**2) / ((1 - self.ginr)**2 + self.giin**2);
        self.xin = 2 * self.giin / ((1 - self.ginr)**2 + self.giin**2);
        self.Zin = self.rin + 1j*self.xin;
        self.Zin *= 50.0;
        # Arco de la línea sobre la carta de 50 Ω
        gamma = self.gammaLine * np.exp(-1j*self.alpha);
        gamma = (self.k + gamma)/(1 + self.k*gamma);
        x5 = np.real(gamma);
        y5 = np.imag(gamma);
        #x5 = 0.2424242424 + self.load.getSWR() + abs(self.load.gamma0) * np.cos(self.alpha);
        # Punto de coeficiente a la entrada
        plt.scatter(self.ginr, self.giin, color = color1, lw = 2);
        # Vector de coeficiente a la entrada
        plt.plot([0, self.ginr],[0, self.giin], color = color2, label = self.cadena);
        # arco con la fase de \Gamma_{in}
        plt.plot(x5, y5, color = '#3a34eb', lw = 3);

    def plotImpedanceCircles(self, theta, cadena, color1 = '#18156b', color2 = '#18156b'):
        self.cadena = cadena;
        # Determinamos la impedancia de entrada
        self.rin = (1 - self.ginr**2 - self.giin**2) / ((1 - self.ginr)**2 + self.giin**2);
        self.xin = 2 * self.giin / ((1 - self.ginr)**2 + self.giin**2);
        self.Zin = self.rin + 1j*self.xin;
        self.Zin *= 50.0;
        # creamos los círculos reactivos y resistivos de entrada
        xr = (1/(self.rin + 1)) * np.cos(theta) + self.rin/(self.rin + 1);
        yr = (1/(self.rin + 1)) * np.sin(theta);
        yi = (1/self.xin) * (np.cos(theta) + 1);
        xi = (1/self.xin) * np.sin(theta) + 1;
        # Círculo resistivo de impedancia de entrada
        plt.plot(xr, yr, color = color1, lw = 2);
        # Círculo reactivo de impedancia de entrada
        plt.plot(xi, yi, color = color2, lw = 2);

    def labelOnChart(self, band):
        if(band):
            if(np.imag(self.Zin) < 0):
                plt.annotate(r'$Z_{in}= %.2f - j%.2f\,\Omega$' % (np.real(self.Zin), -1*np.imag(self.Zin)),
                            xy = (-0.95, 0.85), 
                            xytext = (-0.95, 0.85),
                            textcoords = 'offset points',
                            ha = 'left',
                            va = 'center');
            else:
                plt.annotate(r'$Z_{in}= %.2f + j%.2f\,\Omega$' % (np.real(self.Zin), np.imag(self.Zin)),
                                xy = (-0.95, 0.85), 
                                xytext = (-0.95, 0.85),
                                textcoords = 'offset points',
                                ha = 'left',
                                va = 'center');

            plt.annotate(r'$|\Gamma_{in}|\angle\theta-\phi= %.2f\angle %.2f$' % (np.abs(self.Gin), np.angle(self.Gin, deg = True)),
                xy = (-0.95, -0.95), 
                xytext = (-0.95, -0.95),
                textcoords = 'offset points',
                ha = 'left',
                va = 'center');

    def showAngle(self):
        x = 0.05 * np.cos(self.alpha);
        y = 0.05 * np.sin(self.alpha);
        x1 = 0.065 * np.cos((self.load.angle - self.phase) * 0.5);
        y1 = 0.065 * np.sin((self.load.angle - self.phase) * 0.5);
        plt.plot(x, y, color = 'black', lw = 1);
        plt.annotate(r'$\angle %.2f $' % (np.abs(np.angle(self.Gin, deg = True)) + np.abs(np.angle(self.load.gamma0, deg = True))),
                    xy = (x1, y1),
                    xytext = (x1, y1),
                    ha = 'left',
                    va = 'center');

    def printImpedance(self):
        print("------------------------------------------------------------");
        print('Impedancia normalizada de entrada calculada: ')
        print('Z_in = ',f'{(self.rin + 1j*self.xin):.3f}','Ohms')
        print('Z_in = ', f'{np.abs(self.rin + 1j*self.xin):.3f}', '<' , f'{np.angle(self.rin + 1j*self.xin, deg = True):.3f}');

    def printGamma(self):
        print("------------------------------------------------------------");
        print('Coeficiente a la entrada: ', f'{self.Gin:.3f}');
        print('Fasor de coeficiente: ', f'{np.abs(self.Gin):.3f}', ' < ', f'{np.angle(self.Gin, deg = True):.3f}');

    def printSWR(self):
        print("------------------------------------------------------------");
        print("El SWR de la carga: ", 
            self.load.Zl, " es: ", self.swr);

    def openCapacitanceLine(self, cap = 2e-12, z0 = 50.0, plot = True):
        d1 = self.lamda / (2 * np.pi);
        d1 *= np.atan(2 * np.pi * self.f0 * z0 * cap);
        period = self.lamda * 0.5;
        print("------------------------------------------------------------");
        print("La distancia para la capacitancia en circuito abierto es: "); 
        print(f'{(d1*1e3):.3f}', " + n", f'{(period*1e3):.3f}', " mm");

        if (plot):
            rad2 = -1/np.tan((2 * np.pi/self.lamda) * d1);
            gamr = (rad2**2 - 1) / (1 + rad2**2);
            gami = 2 * rad2 / (1 + rad2**2);
            plt.scatter(gamr, gami, color = 'blue');
        else: 
            pass

    def openInductanceLine(self, L = 10e-9, z0 = 50.0, plot = True):
        d2 = self.lamda / (2 * np.pi);
        d2 *= (np.pi - np.atan(z0/(2*np.pi*f0*L)));
        period = self.lamda * 0.5;
        print("------------------------------------------------------------");
        print("La distancia para la inductancia en circuito abierto es: ", f'{L:.5f}', " es:");
        print(f'{(d2*1e3):.3f}', " + n", f'{(period*1e3):.3f}', " mm");
        if (plot):
            rad2 = -1/np.tan((2 * np.pi/self.lamda) * d2);
            gamr = (rad2**2 - 1) / (1 + rad2**2);
            gami = 2 * rad2 / (1 + rad2**2);
            plt.scatter(gamr, gami, color = 'red');
        else: 
            pass

    def shortCapacitanceLine(self, cap = 5e-12, z0 = 50.0, plot = True):
        d1 = self.lamda / (2 * np.pi);
        d1 *= (np.pi - np.atan(1/(2*np.pi*self.f0*cap*z0)));
        period = self.lamda * 0.5;
        print("------------------------------------------------------------");
        print("La distancia para la capacitancia en circuito abierto es: "); 
        print(f'{(d1*1e3):.3f}', " + n", f'{(period*1e3):.3f}', " mm");

        if (plot):
            rad2 = -1/np.tan((2 * np.pi/self.lamda) * d1);
            gamr = (rad2**2 - 1) / (1 + rad2**2);
            gami = 2 * rad2 / (1 + rad2**2);
            plt.scatter(gamr, gami, color = 'blue');
        else: 
            pass 

    def shortInductanceLine(self, L = 10e-9, z0 = 50.0, plot = True):
        d2 = self.lamda / (2 * np.pi);
        d2 *= np.atan((2*np.pi*f0*L)/z0);
        period = self.lamda * 0.5;
        print("------------------------------------------------------------");
        print("La distancia para la inductancia en circuito abierto es: ", f'{L:.5f}', " es:");
        print(f'{(d2*1e3):.3f}', " + n", f'{(period*1e3):.3f}', " mm");
        if (plot):
            rad2 = -1/np.tan((2 * np.pi/self.lamda) * d2);
            gamr = (rad2**2 - 1) / (1 + rad2**2);
            gami = 2 * rad2 / (1 + rad2**2);
            plt.scatter(gamr, gami, color = 'red');
        else: 
            pass

    def getImpedance(self):
        return self.Zin;

    def getAdmitance(self):
        return 1/self.Zin;

    def getGamma(self):
        return self.Gin;

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

