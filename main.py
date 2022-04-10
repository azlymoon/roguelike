import pygame
from Player import Player
from mobs import *
from projectile import *
from math import sqrt
import time
import threading

WIDTH = 800
HEIGHT = 650
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (47, 79, 79)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player((WIDTH / 2, HEIGHT / 2))
mob1 = Flying_eye((WIDTH / 2, HEIGHT / 4))
mob2 = Skeleton((WIDTH / 4, HEIGHT / 4))
mob3 = Goblin((WIDTH / 4, HEIGHT / 2))
check = Flying_eye_projectile((mob1.coordx, mob1.coordy), (player.coordx, player.coordy))
all_sprites.add(player)
all_sprites.add(mob1)
all_sprites.add(mob2)
all_sprites.add(mob3)

# Цикл игры
running = True
while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    if (sqrt((player.coordx - mob1.coordx) ** 2 + (player.coordy - mob1.coordy) ** 2)) <= 160:
        if check.status == 'explode':
            check.kill()
            check = Flying_eye_projectile((mob1.coordx, mob1.coordy), (player.coordx, player.coordy))
        else:
            all_sprites.add(check)

    # Обновление
    if check.status == 'explode':
        check.kill()
    all_sprites.update()

    # Рендеринг
    screen.fill(GREY)
    left = 0
    top = 0
    wiph = 20
    height = 400
    myImage = pygame.image.load('./img/healthbar/1.png')
    for i in range(0, player.health):
        myRect = (left, top, wiph, height)
        left += wiph

        screen.blit(myImage, myRect)
    all_sprites.draw(screen)
    if player.health <= 0:
        myRect = (0, 0, WIDTH, HEIGHT)
        screen.blit(pygame.image.load('./img/game_over/1.jpg'), myRect)
    pygame.display.flip()

pygame.quit()
