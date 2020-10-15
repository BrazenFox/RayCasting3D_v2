from collections import defaultdict
from multiprocessing import Pool
from camera import Camera
import pygame
from waveguide import WaveGuide
from ray_casting import RayCasting
import sys
from time import time

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Ray Casting')

    WIDTH = 1280
    HEIGHT = 720
    RES = WIDTH, HEIGHT
    SCALE = 4
    NUM_RAYS_WIDTH = int(WIDTH / SCALE)  # Количество лучей в ширину
    NUM_RAYS_HEIGHT = int(HEIGHT / SCALE)  # Количество лучей в высоту
    H_WIDTH = NUM_RAYS_WIDTH // 2
    H_HEIGHT = NUM_RAYS_HEIGHT // 2
    FPS = 60

    screen = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(True)
    keydown_handlers = defaultdict(list)
    keyup_handlers = defaultdict(list)
    mouse_handlers = []

    camera = Camera([5, 5, -10], WIDTH, HEIGHT, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, H_WIDTH, H_HEIGHT)
    waveguide = WaveGuide([0, 0, 0], [1, 1, 2])
    multiple_processing = RayCasting(camera, waveguide, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, SCALE)

    with Pool(processes=8) as pool:
        start = time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill(pygame.Color('darkslategray'))
            pixels = multiple_processing.multiprocessing()

            min_power = pixels[0][0]
            max_power = pixels[0][0]

            for power,x,y in pixels:
                if power > max_power:
                    max_power = power
                if power < min_power:
                    min_power = power

            dispersion = max_power - min_power

            print("min_power: ", min_power, "max_power: ", max_power)

            for power, x, y in pixels:
                color1 = 200. / dispersion * (power-min_power)
                color2 = 200. / dispersion * (power-min_power)
                color3 = 100 - 100. / dispersion * (power-min_power)
                color = (color1, color2, color3)

                pygame.draw.rect(screen, color, (x, y, SCALE, SCALE))
            pygame.display.flip()
            clock.tick()
