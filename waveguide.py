import math
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