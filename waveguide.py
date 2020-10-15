import math
import constants
import matplotlib.colors as cl
import numpy as np
class WaveGuide:
    def __init__(self, position, size):
        self.waveguide_position = [*position]  # Позиция камеры в СКМ
        self.size = size
        '''self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])'''

    def sdf_cube(self, p):
        q = (abs(p[0] + self.waveguide_position[0]) - self.size[0], abs(p[1] + self.waveguide_position[1]) - self.size[1], abs(p[2] + self.waveguide_position[2]) - self.size[2])
        return max((q[0], q[1], q[2], 0)) + min(max(q[0], max(q[1], q[2])), 0)

    def field_power(self, p):
        #print("До ",p)
        p = (p[0] + self.size[0], p[1] + self.size[1], p[2] + self.size[2]+4.5) #+1e-12
        #print("После ",p)
        cc = 3e10  # скорость света в см/с
        ff = 22  # Частота в ГГц
        f = ff * 1e9  # перевод в Гц
        w = 2 * math.pi * f
        lyam = cc / f
        hh = w / cc  # волновое число в волноводе
        # Параметры волновода
        a = self.size[0]*2#+constants.EPSILON*2   # размер волновода по x в см
        b = self.size[1]*2#+constants.EPSILON*2  # размер волновода по y в см
        c = lyam  # размер волновода по z в см
        # Мода
        n = 1
        m = 1
        # время сечения
        tt =0  # время в минус хреналионной степени
        t = tt / 1e12

        kappa = math.sqrt(((math.pi * n / a) ** 2) + ((math.pi * m / b) ** 2))
        kappaX = math.pi * n / a
        kappaY = math.pi * m / b
        f_kr = (cc * kappa) / (2 * math.pi)
        ##########   H   ############
        #return ((abs(math.sin(kappaX * p[0])) ** ((1 / kappaX) ** 2)) / (abs(math.sin(kappaY * p[1])) ** ((1 / kappaY) ** 2))) * math.cos(w * t + math.pi / 2 - hh * p[2])
        ##########    E   ###########
        return abs(math.cos(kappaY * p[1])) * abs(math.cos(kappaX * p[0])) * math.cos(w * t - hh * p[2])

    def color_fader(self, n, x=0):
        colors = ["yellow", "darkcyan", "purple"]
        colors.reverse()
        l = (len(colors) - 1)
        j = (x) / n
        for i in range(l):
            c1 = np.array(cl.to_rgb(colors[i]))
            c2 = np.array(cl.to_rgb(colors[i + 1]))
            if j >= i * (1 / l) and j < (i + 1) * (1 / l):
                color = cl.to_hex((1 - l * (j - i * (1 / l))) * c1 + (l * (j - i * (1 / l))) * c2)
                if color != None:
                    return color
