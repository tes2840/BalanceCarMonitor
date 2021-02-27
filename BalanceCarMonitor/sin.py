import numpy as np
from matplotlib import pyplot as plt

class sin:
    def __init__(self):
        # 描画するグラフを用意する
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax_x = np.linspace(0, 2*np.pi, 500)
        self.ax_y = np.sin(self.ax_x)
        self.lines, = self.ax.plot(self.ax_x, self.ax_y)

    def getFig(self):
        return self.fig, self.ax

    def update(self, dt):
        self.ax_x += dt
        self.ax_y = np.sin(self.ax_x)
        self.lines.set_data(self.ax_x, self.ax_y)
        self.ax.set_xlim((self.ax_x.min(), self.ax_x.max()))
        plt.pause(.01)
