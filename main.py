import pygame
from Player import Player
from map import Map
from CameraGroup import CameraGroup
from mobs import Flying_eye, Goblin
from projectile import Flying_eye_projectile, Goblin_projectile
from math import sqrt

WIDTH = 1280
HEIGHT = 720
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (47, 79, 79)


class GameManager:
    def __init__(self):
        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.entities = pygame.sprite.Group()
        self.state = "in_menu"
        self.map = None
        self.visible_sprites = None
        self.player = None
        self.mob1 = None
        #self.check = Flying_eye_projectile((WIDTH / 2, HEIGHT / 2 + 10), (WIDTH / 2, HEIGHT / 2))

    def init_map(self):
        tmp = Map()
        tmp.create_wall_sprites()
        self.visible_sprites = tmp.visible_sprites
        self.map = tmp.get_map()
        # tmp.draw_in_terminal()

        self.player = Player(tmp.get_spawn_coord_in_room(), tmp.obstacle_sprites)
        self.mob1 = Flying_eye(tmp.get_spawn_coord_in_room(), (self.player.coordx, self.player.coordy))
        self.visible_sprites.add(self.player)
        self.visible_sprites.add(self.mob1)
        self.set_state("game_running")

    def set_state(self, state):
        self.state = state

    def run(self):
        self.init_map()

        # Отрисовка карты в консоль
        print('-' * 150)
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                print(' ' if self.map[y][x] is True else '#', end=' ')
            print()
        print('-' * 150)

        running = True
        while running:
            # Держим цикл на правильной скорости
            self.clock.tick(FPS)
            # Ввод процесса (события)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False

            if (
            sqrt((self.player.coordx - self.mob1.coordx) ** 2 + (self.player.coordy - self.mob1.coordy) ** 2)) <= 160:
                if self.mob1.projectile.status == 'explode':
                    self.mob1.projectile.kill()
                    self.mob1.create_projectile((self.mob1.coordx, self.mob1.coordy),
                                                       (self.player.coordx, self.player.coordy))
                else:
                    self.visible_sprites.add(self.mob1.projectile)

            # Обновление
            # self.entities.update()
            self.visible_sprites.update()
            # Рендеринг
            self.screen.fill(BLACK)
            # self.screen.blit()
            # self.map_surface.draw(self.screen)

            self.visible_sprites.custom_draw(self.player)

            # self.entities.draw(self.screen)

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    Manager = GameManager()
    Manager.run()
