from collections import defaultdict
from multiprocessing import Pool

import pygame
from camera import Camera
from constants import *
from waveguide import WaveGuide
from ray_casting import RayCasting
#from multiprocessing import Pool
import sys
from time import time



if __name__ == '__main__':
    WIDTH = 1280
    HEIGHT = 720
    RES = WIDTH, HEIGHT
    SCALE = 1
    NUM_RAYS_WIDTH = int(WIDTH / SCALE)  # Количество лучей в ширину
    NUM_RAYS_HEIGHT = int(HEIGHT / SCALE)  # Количество лучей в высоту
    H_WIDTH = NUM_RAYS_WIDTH // 2
    H_HEIGHT = NUM_RAYS_HEIGHT // 2
    FPS = 60

    pygame.init()
    pygame.display.set_caption('Ray marching')
    screen = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(True)
    keydown_handlers = defaultdict(list)
    keyup_handlers = defaultdict(list)
    mouse_handlers = []

    camera = Camera([0, 0, -15], WIDTH, HEIGHT, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, H_WIDTH, H_HEIGHT)
    waveguide = WaveGuide([0, 0, 0], [2, 2, 2])

    with Pool(processes=8) as pool:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            multiple_processing = RayCasting(camera, waveguide, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, SCALE)
            pixels = multiple_processing.multiprocessing()
            screen.fill(pygame.Color('darkslategray'))
            for color, x, y in pixels:
                print(1)
                pygame.draw.rect(screen, color, (x, y, SCALE, SCALE))


            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()
