# Electronics Engineer: Science Faculty
# Universidad Autónoma de San Luis Potosí
# Alan Rodríguez Bojorjes, SLP, México
# 2026
import numpy as np
import matplotlib.pyplot as plt

class SmithChart:
    # Lista para los juegos de círculos
    r = np.linspace(0, 10, 40);
    r1 = np.linspace(0.1, 10, 40); theta = 2 * np.pi;
    unit = True;
    def __init__(self, theta, unitary = True):
        self.theta = theta; self.unit = unitary;


    def plotAdmittance(self, radio = 1, radio1 = 1, h = 0):
        x3 = radio * np.cos(self.theta) - h;
        y3 = radio * np.sin(self.theta);
        x4 = radio1 * np.cos(self.theta) - 1;
        y4 = radio1 * (np.sin(self.theta) - 1);
        y5 = radio1 * (np.sin(self.theta) + 1);
        plt.plot(x3, y3, color = 'gray', lw = 0.5);
        plt.plot(x4, y4, color = 'gray', lw = 0.5);
        plt.plot(x4, y5, color = 'gray', lw = 0.5);



    def plotChart(self, admittance = False):
        if (self.unit):
            x = np.cos(self.theta);
            y = np.sin(self.theta);
            plt.plot(x, y, color = 'gray', lw = 0.5);
        else:
            # Conjunto de círculos de la carta
            for i in range(np.size(self.r)):
                radio = 1/(self.r[i] + 1);
                radio1 = 1/self.r1[i];
                h = self.r[i] * radio
                x = radio * np.cos(self.theta) + h;
                y = radio * np.sin(self.theta);
                x1 = radio1 * np.cos(self.theta) + 1;
                y1 = radio1 * (np.sin(self.theta) + 1);
                y2 = radio1 * (np.sin(self.theta) - 1);
                plt.plot(x, y, color = 'gray', lw = 0.5);
                plt.plot(x1, y1, color = 'gray', lw = 0.5);
                plt.plot(x1, y2, color = 'gray', lw = 0.5);
                if (admittance):
                    self.plotAdmittance(radio, radio1, h);

 