import random

import pygame
from Player import Player
from map import Map
from menu import show_menu, pause
from inventory import Inventory, Item
from mobs import Flying_eye, Goblin, Mushroom

pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (47, 79, 79)


class GameManager:
    def __init__(self):
        pygame.display.set_caption("Escape the Castle")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.entities = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        self.inventory = None
        self.game_running = False
        self.items = {'item': ['helmet', 'chest', 'shield', 'axe', 'sword'],
                      'resource': ['coke', 'coin']}
        self.state = "menu"
        self.count_mobs = None
        self.map = None
        self.map_obj = None
        self.visible_sprites = None
        self.obstacle_sprites = None
        self.player = None
        self.count_coin = None
        self.mobs = []
        self.mobs_dictionary = ["Flying_eye", "Goblin", "Mushroom"]

        self.file = './music/1.mp3'
        self.music_menu = './music/2.mp3'
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_menu)

    def init_map(self):
        self.map_obj = Map(self)
        self.inventory = Inventory(self)
        self.map_obj.create_wall_sprites()
        self.visible_sprites = self.map_obj.visible_sprites
        self.map = self.map_obj.get_map()
        self.obstacle_sprites = self.map_obj.obstacle_sprites
        self.player = Player(self.map_obj.get_spawn_coord_in_room(), self.map_obj.obstacle_sprites, self)

        self.visible_sprites.add(self.player)
        # self.count_mobs = random.randint(7, 13)
        self.count_mobs = 1
        self.count_coin = 5
        self.init_items()
        self.init_mobs()
        self.player.get_mobs(self.mobs)

    def init_mobs(self):
        for i in range(self.count_mobs):
            name = random.choice(self.mobs_dictionary)
            if name == "Flying_eye":
                mob = Flying_eye(self.map_obj.get_spawn_coord_in_room(), self.player,
                                 self.map_obj.obstacle_sprites, self)
                self.visible_sprites.add(mob)
                self.mob_sprites.add(mob)
                self.mobs.append(mob)
            elif name == "Goblin":
                mob = Goblin(self.map_obj.get_spawn_coord_in_room(), self.player,
                             self.map_obj.obstacle_sprites, self)
                self.visible_sprites.add(mob)
                self.mob_sprites.add(mob)
                self.mobs.append(mob)
            elif name == "Mushroom":
                mob = Mushroom(self.map_obj.get_spawn_coord_in_room(), self.player,
                               self.map_obj.obstacle_sprites, self)
                self.visible_sprites.add(mob)
                self.mob_sprites.add(mob)
                self.mobs.append(mob)

    def init_items(self):
        for key in self.items.keys():
            for item in self.items[key]:
                if item != 'coin':
                    self.visible_sprites.add(
                        Item(self.map_obj.get_spawn_coord_in_room(), item, './img/{}.png'.format(item),
                             self.item_sprites))
                else:
                    for _ in range(self.count_coin):
                        self.visible_sprites.add(
                            Item(self.map_obj.get_spawn_coord_in_room(), item, './img/{}.png'.format(item),
                                 self.item_sprites))

    def start_game(self):
        self.state = 'game_running'
        self.run()

    def start_menu(self):
        self.state = 'menu'
        self.run()

    def start_new_lvl(self):
        self.state = 'new_lvl'
        self.run()

    def run(self):
        if self.state == 'menu':
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.music_menu)
            pygame.mixer.music.play(-1)
            show_menu(self)
        elif self.state == 'new_lvl':
            pygame.mixer.music.stop()
            self.init_map()
            self.state = 'game_running'
            self.run()
        elif self.state == 'game_running':
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.file)
            pygame.mixer.music.play(-1)
            print('-' * 150)
            for y in range(len(self.map)):
                for x in range(len(self.map[0])):
                    print(' ' if self.map[y][x] is True else '#', end=' ')
                print()
            print('-' * 150)

            self.game_running = True
            hold_left = False

            while self.game_running:
                self.clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_running = False
                for mob in self.mobs:
                    if mob.health <= 0:
                        self.mobs.remove(mob)

                    else:
                        if mob.projectile is not None:
                            if mob.projectile.status != 'explode':
                                self.visible_sprites.add(mob.projectile)
                            else:
                                mob.projectile.kill()
                if not self.mob_sprites:
                    self.mobs.clear()
                    self.start_new_lvl()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pause(self)

                self.visible_sprites.update()
                self.screen.fill(BLACK)
                self.visible_sprites.custom_draw(self.player)
                self.inventory.show_panel()
                self.player.check_health()
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                if click[0] and not hold_left:
                    print(mouse)
                    self.inventory.set_start_cell(mouse[0], mouse[1])
                    hold_left = True
                if hold_left and not click[0]:
                    print(mouse)
                    self.inventory.set_end_cell(mouse[0], mouse[1])
                    hold_left = False

                if keys[pygame.K_e]:
                    self.inventory.draw_whole_items(self)
                pygame.display.flip()
            pygame.quit()


if __name__ == '__main__':
    pygame.init()
    Manager = GameManager()
    Manager.run()
