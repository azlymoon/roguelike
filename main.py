import pygame

import inventory
from Player import Player
from map import Map
from menu import show_menu, print_text, pause
from menu import Button
# from panel import show_panel
from inventory import Inventory, Item
from CameraGroup import CameraGroup
from mobs import Flying_eye, Goblin, Mushroom
from projectile import Flying_eye_projectile, Goblin_projectile, Mushroom_projectile
from math import sqrt
from time import sleep

pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 30

# Р—Р°РґР°РµРј С†РІРµС‚Р°
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
        self.inventory = Inventory(self)
        self.game_running = False
        self.items = {'item': ['helmet', 'chest', 'shield', 'axe', 'sword'],
                      'resource': ['coke']}
        self.state = "menu"
        self.map = None
        self.map_obj = None
        self.visible_sprites = None
        self.obstacle_sprites = None
        self.player = None
        self.mob1 = None
        self.mob2 = None
        self.mob3 = None
        self.mobs = []

    def init_map(self):
        self.map_obj = Map()
        self.map_obj.create_wall_sprites()
        self.visible_sprites = self.map_obj.visible_sprites
        self.map = self.map_obj.get_map()
        self.obstacle_sprites = self.map_obj.obstacle_sprites
        # tmp.draw_in_terminal()
        self.player = Player(self.map_obj.get_spawn_coord_in_room(), self.map_obj.obstacle_sprites, self)
        self.mob1 = Flying_eye(self.map_obj.get_spawn_coord_in_room(), self.player,
                               self.map_obj.obstacle_sprites, self)
        self.mob2 = Goblin(self.map_obj.get_spawn_coord_in_room(), self.player,
                           self.map_obj.obstacle_sprites, self)
        self.mob3 = Mushroom(self.map_obj.get_spawn_coord_in_room(), self.player,
                             self.map_obj.obstacle_sprites, self)
        # axe = inventory.Item(self.map_obj.get_spawn_coord_in_room(), 'axe', './img/axe.png', self.item_sprites)
        # self.visible_sprites.add(axe)
        self.visible_sprites.add(self.player)
        self.visible_sprites.add(self.mob1)
        self.visible_sprites.add(self.mob2)
        self.visible_sprites.add(self.mob3)
        self.mob_sprites.add(self.mob1)
        self.mob_sprites.add(self.mob2)
        self.mob_sprites.add(self.mob3)
        self.mobs.append(self.mob1)
        self.mobs.append(self.mob2)
        self.mobs.append(self.mob3)
        self.player.get_mobs(self.mobs)
        self.init_items()

    def init_items(self):
        for key in self.items.keys():
            for item in self.items[key]:
                self.visible_sprites.add(Item(self.map_obj.get_spawn_coord_in_room(), item, './img/{}.png'.format(item),
                                              self.item_sprites))

    def start_game(self):
        self.state = 'game_running'
        self.run()

    def start_menu(self):
        self.state = 'menu'
        # self.state = 'game_running'
        self.run()

    def run(self):
        if self.state == 'menu':
            self.init_map()
            show_menu(self)
        elif self.state == 'game_running':
            # РћС‚СЂРёСЃРѕРІРєР° РєР°СЂС‚С‹ РІ РєРѕРЅСЃРѕР»СЊ
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
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.game_running = False
                for mob in self.mobs:
                    # print(mob.rect.x, mob.rect.y, self.player.rect.x, self.player.rect.y)
                    # print(sqrt((mob.rect.x - self.player.rect.x) ** 2 + (mob.rect.y - self.player.rect.y) ** 2))
                    if mob.health <= 0:
                        # mob.projectile.kill()
                        # mob.kill()
                        self.mobs.remove(mob)
                    else:

                        # print("СЃС‚Р°С‚СѓСЃ РёР· РјРµРЅСЋ", mob.projectile.status)
                        if mob.projectile is not None:
                            if mob.projectile.status != 'explode':
                                self.visible_sprites.add(mob.projectile)
                            else:
                                mob.projectile.kill()
                if not self.mobs:
                    self.game_running = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pause(self)

                # РћР±РЅРѕРІР»РµРЅРёРµ
                # self.entities.update()
                self.visible_sprites.update()
                # Р РµРЅРґРµСЂРёРЅРі

                self.screen.fill(BLACK)
                # self.screen.fill(BLACK)
                # self.screen.blit()
                # self.map_surface.draw(self.screen)

                self.visible_sprites.custom_draw(self.player)

                # self.inventory.show_health()
                self.inventory.show_panel()

                self.player.check_health()

                # self.inventory.draw_panel(self)

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
                    # self.inventory.draw_whole(self)
                    self.inventory.draw_whole_items(self)
                    # self.inventory.increase_item('shield')
                    # self.inventory.increase_item('sword')
                    # self.inventory.increase_item('axe')
                    # self.inventory.increase_item('helmet')
                    # self.inventory.increase_item('chest')

                # if keys[pygame.K_4]:
                #    self.inventory.increase('coke')
                #    sleep(0.1)

                # self.entities.draw(self.screen)

                # РџРѕСЃР»Рµ РѕС‚СЂРёСЃРѕРІРєРё РІСЃРµРіРѕ, РїРµСЂРµРІРѕСЂР°С‡РёРІР°РµРј СЌРєСЂР°РЅ
                pygame.display.flip()
            pygame.quit()


if __name__ == '__main__':
    pygame.init()
    Manager = GameManager()
    Manager.run()
