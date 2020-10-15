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
                    ray = self.camera.matrix[x][y] + (
                            self.camera.matrix[x][y] - self.camera.camera_position) / np.linalg.norm(
                        self.camera.matrix[x][y] - self.camera.camera_position) * depth
                    dist = self.waveguide.sdf_cube(ray)
                    if dist < EPSILON:
                        color = (255, 255, 255)
                        pixels.append((color, x * self.SCALE, y * self.SCALE))
                        break
                    depth += dist
                    if depth > MAX_DEPTH:
                        break
            # print(pixels)
        return pixels
