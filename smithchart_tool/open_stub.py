# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
import numpy as np
import matplotlib.pyplot as plt

class OpenStub:
    c = 3e8;
    def __init__(self, z0=50.0, ZL=0.5+1j*0.5, theta_deg=90, f0=2.4e9):
        self.z0 = z0;
        self.f0 = f0;
        self.theta_deg = theta_deg;
        self.Zload = complex(ZL);
        self.Yload = 1/self.Zload;
        self.theta = np.deg2rad(theta_deg);
        self.lamda = self.c/self.f0;
        self.beta = 2*np.pi/self.lamda;
        self.length = self.theta/self.beta;
        self.Zstub = -1j*self.z0/np.tan(self.theta);
        self.Ystub = 1/self.Zstub;
        self.Yin = self.Yload + self.Ystub;
        self.Zin = 1/self.Yin;
        # self.zn = self.Zin/self.z0
        self.gammaStub = (self.Zin-self.z0)/(self.Zin+self.z0);
        #self.yn = self.Yin*self.z0;
        self.k = (self.z0-50.0)/(self.z0+50.0);
        self.alpha = np.linspace(1e-6, self.theta, 1000);
        Zstub = -1j*self.z0/np.tan(self.alpha);
        Ystub = 1/Zstub;
        Yeq = self.Yload + Ystub;
        Zeq = 1/Yeq;
        gammaStub = (Zeq-self.z0)/(Zeq+self.z0);
        self.gammaArc = (self.k + gammaStub)/(1 + self.k*gammaStub);
        self.gamma = (self.k+self.gammaStub)/(1+self.k*self.gammaStub);
        self.gr = np.real(self.gamma);
        self.gi = np.imag(self.gamma);
        # self.r = np.real(self.zn);
        # self.x = np.imag(self.zn);
        # self.gr = (self.r**2+self.x**2-1)/((self.r+1)**2+self.x**2)
        # self.gi = 2*self.x/((self.r+1)**2+self.x**2)
        #self.gamma = self.gr + 1j*self.gi
        self.zn = (1+self.gamma)/(1-self.gamma);
        self.Zdisplay = 50.0*self.zn;
        self.mag = np.abs(self.gamma)
        self.angle = np.angle(self.gamma)
        self.cadena = "";
        self.yn = 1/self.zn;
        self.g = np.real(self.yn);
        self.b = np.imag(self.yn);
        self.r = np.real(self.zn);
        self.x = np.imag(self.zn);

    def getImpedance(self):
        return self.Zin

    ###########################################################

    def getAdmitance(self):
        return self.Yin

    ###########################################################

    def getGamma(self):
        return self.gamma

    ###########################################################

    def getLoadImpedance(self):
        return self.Zload

    ###########################################################

    def getLoadAdmitance(self):
        return self.Yload

    ###########################################################

    def getStubImpedance(self):
        return self.Zstub

    ###########################################################

    def getStubAdmitance(self):
        return self.Ystub

    ###########################################################

    def getSWR(self):

        swr = (1+np.abs(self.gamma))/(
              1-np.abs(self.gamma))

        return swr

    ###########################################################

    def printSWR(self):

        print("------------------------------------------");
        print("SWR =",self.getSWR());

    ###########################################################

    def printImpedance(self):
        print("------------------------------------------");
        print("Carga");
        print(self.Zload);

        print("------------------------------------------");
        print("Stub");
        print(self.Zstub);

        print("------------------------------------------");
        print("Impedancia equivalente");
        print(self.Zin);

        print("Normalizada");
        print(self.zn);

    ###########################################################

    def printAdmitance(self):
        print("------------------------------------------");
        print("Admitancia carga");
        print(self.Yload);
        print("------------------------------------------");
        print("Admitancia stub");
        print(self.Ystub);

        print("------------------------------------------");
        print("Admitancia equivalente");
        print(self.Yin);
        print("Normalizada");
        print(self.yn);

    ###########################################################

    def addToSmithChart(self, cadena="", color='green'):
        self.cadena = cadena;
        # Arco del stub
        plt.plot(np.real(self.gammaArc), np.imag(self.gammaArc), color=color, lw=3);
        # Punto final
        plt.scatter(self.gr, self.gi, color='black');
        # Vector
        plt.plot([0, self.gr], [0, self.gi], color='black', label=self.cadena);

    ###########################################################

    def plotImpedanceCircles(self, theta, colorR='black', colorX='black'):
        radioR = 1/(self.r + 1);
        xR = radioR*np.cos(theta) + self.r/(self.r + 1);
        yR = radioR*np.sin(theta);
        plt.plot(xR, yR, color=colorR, lw=2);
        if np.abs(self.x) > 1e-10:
            radioX = 1/self.x;
            xX = radioX*np.cos(theta) + 1;
            yX = radioX*np.sin(theta) + 1/self.x;
            plt.plot(xX, yX, color=colorX, lw=2);

    ###########################################################

    def plotAdmitanceCircles(self, theta, colorG='red', colorB='red'):
        radioG = 1/(self.g + 1);
        xG = radioG*(np.cos(theta) - self.g);
        yG = radioG*np.sin(theta);
        plt.plot(xG, yG, color=colorG, lw=2);
        if np.abs(self.b) > 1e-10:
            radioB = 1/self.b;
            xB = radioB*np.cos(theta) - 1;
            yB = radioB*(np.sin(theta) - 1);
            plt.plot(xB, yB, color=colorB, lw=2);
    ###########################################################
    def labelOnChart(self, band=True):
        if not band:
            return
        # Impedancia equivalente
        if np.imag(self.Zin) < 0:
            plt.annotate(
                r'$Z_{eq}= %.2f-j%.2f\,\Omega$'
                %(np.real(self.Zin),
                  -np.imag(self.Zin)),
                xy=(-0.95,0.95),
                xytext=(-0.95,0.95),
                textcoords='offset points',
                ha='left');
        else:
            plt.annotate(
                r'$Z_{eq}= %.2f+j%.2f\,\Omega$'
                %(np.real(self.Zin),
                  np.imag(self.Zin)),
                xy=(-0.95,0.95),
                xytext=(-0.95,0.95),
                textcoords='offset points',
                ha='left');
        # Admitancia equivalente
        if np.imag(self.Yin) < 0:

            plt.annotate(
                r'$Y_{eq}= %.4f-j%.4f\,S$'
                %(np.real(self.Yin),
                  -np.imag(self.Yin)),
                xy=(-0.95,0.82),
                xytext=(-0.95,0.82),
                textcoords='offset points',
                ha='left');
        else:
            plt.annotate(
                r'$Y_{eq}= %.4f+j%.4f\,S$'
                %(np.real(self.Yin),
                  np.imag(self.Yin)),
                xy=(-0.95,0.82),
                xytext=(-0.95,0.82),
                textcoords='offset points',
                ha='left');
        # Información del stub
        if np.imag(self.Zstub) < 0:

            texto = r'$Z_{stub}=%.2f-j%.2f\,\Omega$' % (
                np.real(self.Zstub),
                -np.imag(self.Zstub));

        else:

            texto = r'$Z_{stub}=%.2f+j%.2f\,\Omega$' % (
                np.real(self.Zstub),
                np.imag(self.Zstub));

        plt.annotate(
            texto,
            xy=(-0.95,0.69),
            xytext=(-0.95,0.69),
            textcoords='offset points',
            ha='left');
        # Gamma
        plt.annotate(
            r'$|\Gamma|=%.3f\angle%.2f^\circ$'
            %(self.mag,
              np.angle(self.gamma,deg=True)),
            xy=(-0.95,-0.90),
            xytext=(-0.95,-0.90),
            textcoords='offset points',
            ha='left');

    ###########################################################
    def __add__(self, other):

        if hasattr(other, "getImpedance"):
            other = other.getImpedance();

        return self.getImpedance() + other;

    ###########################################################

    def __sub__(self, other):

        if hasattr(other, "getImpedance"):
            other = other.getImpedance()

        return self.getImpedance() - other;

    ###########################################################

    def __mul__(self, other):

        if hasattr(other, "getImpedance"):
            other = other.getImpedance()

        return self.getImpedance() * other;

    ###########################################################

    def __truediv__(self, other):

        if hasattr(other, "getImpedance"):
            other = other.getImpedance();

        return self.getImpedance() / other;

    ###########################################################

    def __radd__(self, other):
        return other + self.getImpedance();

    ###########################################################

    def __rsub__(self, other):
        return other - self.getImpedance();

    ###########################################################

    def __rmul__(self, other):
        return other * self.getImpedance();

    ###########################################################

    def __rtruediv__(self, other):
        return other / self.getImpedance();

    ###########################################################

    def __repr__(self):
        return f"{self.getImpedance():.4f}";

 