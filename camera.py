import math


class Camera:
    def __init__(self, position, WIDTH, HEIGHT, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, H_WIDTH, H_HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.NUM_RAYS_WIDTH = NUM_RAYS_WIDTH
        self.NUM_RAYS_HEIGHT = NUM_RAYS_HEIGHT
        self.H_WIDTH = H_WIDTH
        self.H_HEIGHT = H_HEIGHT
        self.camera_position = (*position, 1)  # Позиция камеры в СКМ
        self.h_fov = math.pi / 3  # Угол обзора камеры по ширине
        self.v_fov = self.h_fov * (self.HEIGHT / self.WIDTH)  # Угол обзора камеры по высоте
        self.Z_DISTANCE = self.NUM_RAYS_HEIGHT / math.tan(self.h_fov / 2)
        self.matrix = [[0] * self.NUM_RAYS_HEIGHT for i in range(self.NUM_RAYS_WIDTH)]
        self.pos_matrix = (self.H_WIDTH, -self.H_HEIGHT, -self.Z_DISTANCE, 1)  # Матрица в СК камеры

        for x in range(self.NUM_RAYS_WIDTH):
            for y in range(self.NUM_RAYS_HEIGHT):
                pos = self.normalize_vector3(self.subtraction_vectors3([x, -y, 0, 1], self.pos_matrix))  # матрица в координатах камеры
                #print(pos)

                #self.matrix[x][y] = self.sum_of_vectors3(self.camera_position, pos) # Матрица в СКМ пересчитанная в нормальный вид
                self.matrix[x][y] = self.transfer_to_WCS(pos)
                #print(self.matrix[x][y])


    def normalize_vector3(self, v):
        len_v = 1 / math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
        return (v[0] * len_v, v[1] * len_v, v[2] * len_v, 1)

    def sum_of_vectors3(self, v1, v2):
        return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2], 1)

    def subtraction_vectors3(self, v1, v2):
        return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2], 1)

    def multiple_vector_and_matrix3(self, v, m):
        x = (v[0] * m[0][0] + v[1] * m[0][1] + v[2] * m[0][2] + v[3] * m[0][3])
        y = (v[0] * m[1][0] + v[1] * m[1][1] + v[2] * m[1][2] + v[3] * m[1][3])
        z = (v[0] * m[2][0] + v[1] * m[2][1] + v[2] * m[2][2] + v[3] * m[2][3])
        s = (v[0] * m[3][0] + v[1] * m[3][1] + v[2] * m[3][2] + v[3] * m[3][3])
        return (x, y, z, s)

    def transfer_to_WCS_rotate_X(self, ray):
        cosf = -self.camera_position[2] / math.sqrt(self.camera_position[1] ** 2 + self.camera_position[2] ** 2)
        sinf = -self.camera_position[1] / math.sqrt(self.camera_position[1] ** 2 + self.camera_position[2] ** 2)
        column1 = (1, 0, 0, 0)
        column2 = (0, cosf, sinf, 0)
        column3 = (0, -sinf, cosf, 0)
        column4 = (0, 0, 0, 1)
        matrix = (column1, column2, column3, column4)
        return self.multiple_vector_and_matrix3(ray, matrix)

    def transfer_to_WCS_rotate_Y(self, ray):
        cost = -self.camera_position[2] / math.sqrt(self.camera_position[0] ** 2 + self.camera_position[2] ** 2)
        sint = -self.camera_position[0] / math.sqrt(self.camera_position[0] ** 2 + self.camera_position[2] ** 2)
        column1 = (cost, 0, sint, self.camera_position[0])
        column2 = (0, 1, 0, 0)
        column3 = (-sint, 0, cost, 0)
        column4 = (0, 0, 0, 1)
        matrix = (column1, column2, column3, column4)
        return self.multiple_vector_and_matrix3(ray, matrix)

    def transfer_to_WCS_shift(self, ray):
        column1 = (0, 0, 0, self.camera_position[0])
        column2 = (0, 1, 0, self.camera_position[1])
        column3 = (0, 0, 0, self.camera_position[2])
        column4 = (0, 0, 0, 1)
        matrix = (column1, column2, column3, column4)
        return self.multiple_vector_and_matrix3(ray, matrix)

    def transfer_to_WCS(self, ray):
        cost = -self.camera_position[2] / math.sqrt(self.camera_position[0] ** 2 + self.camera_position[2] ** 2)
        sint = -self.camera_position[0] / math.sqrt(self.camera_position[0] ** 2 + self.camera_position[2] ** 2)
        cosf = -self.camera_position[2] / math.sqrt(self.camera_position[1] ** 2 + self.camera_position[2] ** 2)
        sinf = -self.camera_position[1] / math.sqrt(self.camera_position[1] ** 2 + self.camera_position[2] ** 2)
        column1 = ( cost,          0, sint*cosf, self.camera_position[0])
        column2 = (    0,       cosf,      sinf, self.camera_position[1])
        column3 = (-sint, -sinf*cost, cost*cosf, self.camera_position[2])
        column4 = (    0,          0,         0,                       1)
        matrix = (column1, column2, column3, column4)
        return self.multiple_vector_and_matrix3(ray, matrix)
    # return [campos[0], (pos[1] * cosf + pos[2] * (-sinf) + pos[3]*campos[1]), (pos[1] * sinf + pos[2] * cosf + pos[3] * campos[2])]
