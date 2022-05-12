import pygame
from Player import Player
from map import Map
from menu import show_menu, print_text, pause
from CameraGroup import CameraGroup
from mobs import Flying_eye, Goblin, Mushroom
from projectile import Flying_eye_projectile, Goblin_projectile, Mushroom_projectile
from math import sqrt

pygame.init()

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
        self.state = "menu"
        self.map = None
        self.visible_sprites = None
        self.player = None
        self.mob1 = None
        self.mob2 = None
        self.mob3 = None
        self.mobs = []

    def init_map(self):
        tmp = Map()
        tmp.create_wall_sprites()
        self.visible_sprites = tmp.visible_sprites
        self.map = tmp.get_map()
        # tmp.draw_in_terminal()

        self.player = Player(tmp.get_spawn_coord_in_room(), tmp.obstacle_sprites)
        self.mob1 = Flying_eye(tmp.get_spawn_coord_in_room(), (self.player.coordx, self.player.coordy), tmp.obstacle_sprites)
        self.mob2 = Goblin(tmp.get_spawn_coord_in_room(), (self.player.coordx, self.player.coordy), tmp.obstacle_sprites)
        self.mob3 = Mushroom(tmp.get_spawn_coord_in_room(), (self.player.coordx, self.player.coordy), tmp.obstacle_sprites)
        self.visible_sprites.add(self.player)
        self.visible_sprites.add(self.mob1)
        self.visible_sprites.add(self.mob2)
        self.visible_sprites.add(self.mob3)
        self.mobs.append(self.mob1)
        self.mobs.append(self.mob2)
        self.mobs.append(self.mob3)

    def start_game(self):
        self.state = 'game_running'
        self.run()

    def run(self):
        if self.state == 'menu':
            self.init_map()
            show_menu(self)
        elif self.state == 'game_running':
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
                for mob in self.mobs:
                    if mob.projectile.status == "explode":
                        mob.projectile.kill()
                    if (sqrt((self.player.coordx - mob.coordx) ** 2 + (self.player.coordy - mob.coordy) ** 2)) <= 160:
                        if mob.projectile.status == 'explode':
                            mob.create_projectile((mob.coordx, mob.coordy), (self.player.coordx, self.player.coordy))
                        else:
                            self.visible_sprites.add(mob.projectile)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pause(self)

                # Обновление
                # self.entities.update()
                self.visible_sprites.update()
                # Рендеринг

                self.screen.fill(BLACK)
                # self.screen.fill(BLACK)
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
