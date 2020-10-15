import math
# from numpy.linalg import norm
import numpy as np



class Camera:
    def __init__(self, position, WIDTH, HEIGHT, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, H_WIDTH, H_HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.NUM_RAYS_WIDTH = NUM_RAYS_WIDTH
        self.NUM_RAYS_HEIGHT = NUM_RAYS_HEIGHT
        self.H_WIDTH = H_WIDTH
        self.H_HEIGHT = H_HEIGHT
        self.camera_position = np.array([*position])  # Позиция камеры в СКМ
        self.h_fov = math.pi / 3  # Угол обзора камеры по ширине
        self.v_fov = self.h_fov * (self.HEIGHT / self.WIDTH)  # Угол обзора камеры по высоте
        self.Z_DISTANCE = self.NUM_RAYS_HEIGHT / math.tan(self.h_fov / 2)
        self.matrix = [[0] * self.NUM_RAYS_HEIGHT for i in range(self.NUM_RAYS_WIDTH)]
        self.pos_matrix = np.array([self.H_WIDTH, -self.H_HEIGHT, -self.Z_DISTANCE])  # Матрица в СК камеры

        for x in range(self.NUM_RAYS_WIDTH):
            for y in range(self.NUM_RAYS_HEIGHT):
                pos =([x,-y,0] - self.pos_matrix)
                self.matrix[x][y] = self.camera_position + pos/np.linalg.norm(pos) # Матрица в СКМ пересчитанная в нормальный вид


    def  intermediate_matrix(self):
        print(self.matrix[0][0])
        m = np.linalg.norm(self.matrix - self.camera_position)
        print(m[0][0])
        return np.linalg.norm(self.matrix - self.camera_position)