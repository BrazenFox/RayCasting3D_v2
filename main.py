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

    WIDTH = 800
    HEIGHT = 600
    RES = WIDTH, HEIGHT
    SCALE = 1                           #Разрешение (на сколько четкая будет картинка)
    NUM_RAYS_WIDTH = int(WIDTH / SCALE)  # Количество лучей в ширину
    NUM_RAYS_HEIGHT = int(HEIGHT / SCALE)  # Количество лучей в высоту
    H_WIDTH = NUM_RAYS_WIDTH // 2       #Вычисляем центр матрицы по y
    H_HEIGHT = NUM_RAYS_HEIGHT // 2     #Вычисляем центр матрицы по x
    FPS = 60

    screen = pygame.display.set_mode(RES) #создаем окно
    clock = pygame.time.Clock()           #считаем время

    pygame.mouse.set_visible(True)   #отображение курсора в окне
    keydown_handlers = defaultdict(list) #массив событий при нажатии кнопки (сейчас не используется)
    keyup_handlers = defaultdict(list)   #массив событий при отпускании кнопки (сейчас не используется)
    mouse_handlers = []                 #массив наших событий (сейчас не используется)

    camera = Camera([5, 5, -10], WIDTH, HEIGHT, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, H_WIDTH, H_HEIGHT) #Создаем камеру с координатами, направленная на объект
    waveguide = WaveGuide([0, 0, 0], [1, 1, 2])                                                     #cоздаем параллелепипед с центром и размерами
    multiple_processing = RayCasting(camera, waveguide, NUM_RAYS_WIDTH, NUM_RAYS_HEIGHT, SCALE)     #создаем класс вычислений пикселей

    start = time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(pygame.Color('darkslategray'))                                              #Заливаем экран (фон) цветом
        pixels = multiple_processing.multiprocessing()                                          #Вычисляем пиксели

        min_power = pixels[0][0]                                                                #Вычисляем минимум поля
        max_power = pixels[0][0]                                                                #Вычисляем максимум поля

        for power, x, y in pixels:
            if power > max_power:
                max_power = power
            if power < min_power:
                min_power = power

        dispersion = max_power - min_power                                                      #Вычисляем разброс значений

        #print("min_power: ", min_power, "max_power: ", max_power)
        for power, x, y in pixels:
            '''color1 = 255. / dispersion * (power-min_power)
            color2 = 200. / dispersion * (power-min_power)
            color3 = 150 - 150. / dispersion * (power-min_power)
            color = (color1, color2, color3)'''
            color = waveguide.color_fader(dispersion+1, power - min_power)
            #color =(255,255,255)
            pygame.draw.rect(screen, color, (x, y, SCALE, SCALE))
        pygame.display.flip()
        clock.tick()

    pygame.quit()
    sys.exit()