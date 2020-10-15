from multiprocessing import Pool
from threading import Thread
from constants import *


class RayCasting:
    def __init__(self, camera, waveguide, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, SCALE):
        """Инициализация потока"""
        self.camera = camera
        self.waveguide = waveguide
        self.NUM_RAYS_WIDTH = NUM_RAYS_WIDTH
        self.NUM_RAYS_HEIGHT = NUM_RAYS_HEIGHT
        self.SCALE = SCALE

    def multiprocessing(self):
        with Pool(processes=8) as pool:
            p1 = pool.apply_async(self.ray_casting, (0,))
            p2 = pool.apply_async(self.ray_casting, (1,))
            p3 = pool.apply_async(self.ray_casting, (2,))
            p4 = pool.apply_async(self.ray_casting, (3,))
            p5 = pool.apply_async(self.ray_casting, (4,))
            p6 = pool.apply_async(self.ray_casting, (5,))
            p7 = pool.apply_async(self.ray_casting, (6,))
            p8 = pool.apply_async(self.ray_casting, (7,))
            return p1.get() + p2.get() + p3.get() + p4.get() + p5.get() + p6.get() + p7.get() + p8.get()

    def ray_casting(self, process):
        """Запуск потока"""
        pixels = []
        for x in range(process, self.NUM_RAYS_WIDTH, 8):
            for y in range(0, self.NUM_RAYS_HEIGHT, 1):
                depth = 0
                for i in range(MAX_STEPS):
                    ray = self.sum_of_vectors3(self.camera.matrix[x][y], self.multiple_vector_and_number3(self.normalize_vector3(self.subtraction_vectors3(self.camera.matrix[x][y], self.camera.camera_position)), depth))
                    dist = self.waveguide.sdf_cube(ray)
                    if dist < EPSILON:
                        power = self.waveguide.field_power(ray)
                        pixels.append((power, x * self.SCALE, y * self.SCALE))
                        break
                    depth += dist
                    if depth > MAX_DEPTH:
                        break
            # print(pixels)
        return pixels

    def subtraction_vectors3(self, v1, v2):
        return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

    def sum_of_vectors3(self, v1, v2):
        return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

    def normalize_vector3(self, vec):
        len_vec = 1 / math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
        return (vec[0] * len_vec, vec[1] * len_vec, vec[2] * len_vec)

    def multiple_vector_and_number3(self, v1, n):
        return (v1[0] * n, v1[1] * n, v1[2] * n)
