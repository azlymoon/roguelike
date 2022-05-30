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
        self.map_obj = Map(self)
        self.inventory = Inventory(self)
        self.map_obj.create_wall_sprites()
        self.visible_sprites = self.map_obj.visible_sprites
        self.map = self.map_obj.get_map()
        self.obstacle_sprites = self.map_obj.obstacle_sprites
        self.player = Player(self.map_obj.get_spawn_coord_in_room(), self.map_obj.obstacle_sprites, self)
        self.mob1 = Flying_eye(self.map_obj.get_spawn_coord_in_room(), self.player,
                               self.map_obj.obstacle_sprites, self)
        self.mob2 = Goblin(self.map_obj.get_spawn_coord_in_room(), self.player,
                           self.map_obj.obstacle_sprites, self)
        self.mob3 = Mushroom(self.map_obj.get_spawn_coord_in_room(), self.player,
                             self.map_obj.obstacle_sprites, self)
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

    def start_new_lvl(self):
        self.state = 'new_lvl'
        self.run()

    def run(self):
        if self.state == 'menu':
            self.init_map()
            show_menu(self)
        elif self.state == 'new_lvl':
            self.init_map()
            self.state = 'game_running'
            self.run()
        elif self.state == 'game_running':
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
                if not self.mobs:
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
