import pygame
from menu import print_text

health_img = pygame.image.load('./img/menu/heart.png')
health_img = pygame.transform.scale(health_img, (32, 32))

weapon_img = pygame.image.load('./img/menu/weapon.png')
weapon_img = pygame.transform.scale(weapon_img, (40, 40))

armour_img = pygame.image.load('./img/menu/armour.png')
armour_img = pygame.transform.scale(armour_img, (34, 34))


class Resource:
    def __init__(self, name, image_path):
        self.name = name
        self.amount = 0
        self.image = pygame.image.load(image_path)


class Item(pygame.sprite.Sprite):
    def __init__(self, pos, name, image_path1, item_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pos = pos
        self.image = pygame.image.load(image_path1)
        self.rect = self.image.get_rect(topleft=pos)
        self.item_sprites = item_sprites
        self.add_to_item_sprites()

    def add_to_item_sprites(self):
        self.item_sprites.add(self)


class Inventory:
    def __init__(self, GameManager):
        self.whole_inventory_for_items = [None] * 12
        self.start_cell = 0
        self.end_cell = 0
        self.start_cell1 = 0
        self.end_cell1 = 0
        self.GameManager = GameManager
        self.weapon_buf = False
        self.armour_buf = False

    def draw_whole_items(self, GameManager):
        x = 655
        y = 255
        side = 60
        step = 75

        # отрисовка инвентаря для оружия и брони на 10 ячеек
        pygame.draw.rect(GameManager.screen, (175, 190, 202), (640, 240, 165, 240))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (640, 240, 165, 240), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (640, 240, 165, 240), 2)

        pygame.draw.rect(GameManager.screen, (175, 190, 202), (820, 220, 165, 260))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (820, 220, 165, 260), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (820, 220, 165, 260), 2)

        # отрисовка текста для брони
        print_text(GameManager, "armour", 835, 226, (0, 0, 0), font_size=18)

        # отрисовка текста для оружия
        print_text(GameManager, "weapon", 910, 226, (0, 0, 0), font_size=18)

        for cell1 in self.whole_inventory_for_items:
            # print(cell.amount)
            pygame.draw.rect(GameManager.screen, (200, 215, 227), (x, y, side, side))
            if cell1 is not None:
                GameManager.screen.blit(cell1.image, (x + 5, y + 5))

            y += step

            if y == 480:
                y = 255
                if x == 730:
                    x = 760
                    x += step
                else:
                    x += step

        pygame.draw.rect(GameManager.screen, (175, 190, 202), (905, 325, 75, 75))

        # отрисовка текста для щита
        print_text(GameManager, "shield", 913, 379, (0, 0, 0), font_size=18)

    def set_start_cell(self, mouse_x, mouse_y):
        start_x = 655
        start_y = 255
        step = 85
        side = 60

        for y in range(0, 3):
            for x in range(0, 4):
                cell_x = start_x + x * step
                cell_y = start_y + y * step

                if cell_x <= mouse_x <= cell_x + side and cell_y <= mouse_y <= cell_y + side:
                    self.start_cell = x * 3 + y
                    print("Start " + str(x * 3 + y))
                    return

    def set_end_cell(self, mouse_x, mouse_y):
        start_x = 655
        start_y = 255
        step = 85
        side = 60

        for y in range(0, 3):
            for x in range(0, 4):
                cell_x = start_x + x * step
                cell_y = start_y + y * step

                if cell_x <= mouse_x <= cell_x + side and cell_y <= mouse_y <= cell_y + side:
                    self.end_cell = x * 3 + y
                    print("End " + str(x * 3 + y))
                    self.swap_cells()
                    # for item in self.GameManager.item_sprites:
                    #     if item.name in self.GameManager.items['item']:
                    #         if item.name in ['axe', 'sword'] and self.end_cell == 9:
                    #             self.swap_cells()
                    #             self.change_weapon()
                    print(self.whole_inventory_for_items[self.start_cell])
                    if self.whole_inventory_for_items[self.end_cell] is not None:
                        print(self.whole_inventory_for_items[self.end_cell].name)
                    # if self.whole_inventory_for_items[self.start_cell] is not None:
                    #     if self.whole_inventory_for_items[self.start_cell].name in ['axe', 'sword'] and self.end_cell == 9:
                    #         self.swap_cells()
                    #         self.change_weapon()
                    if self.end_cell == 9 or self.start_cell == 9:
                        self.change_weapon()

                    return

    def swap_cells(self):
        # temp = self.whole_inventory_for_items[self.end_cell]
        # self.whole_inventory_for_items[self.end_cell] = self.whole_inventory_for_items[self.start_cell]
        # self.whole_inventory_for_items[self.start_cell] = temp

        self.whole_inventory_for_items[self.start_cell], self.whole_inventory_for_items[self.end_cell] =\
            self.whole_inventory_for_items[self.end_cell], self.whole_inventory_for_items[self.start_cell]

        # self.change_armour()

    def change_weapon(self):
        if self.end_cell == 9:
            if self.whole_inventory_for_items[9] is not None:
                if self.whole_inventory_for_items[9].name in ['axe', 'sword'] and self.weapon_buf is False:
                    self.GameManager.player.weapon += 80
                    self.weapon_buf = True
        if self.start_cell == 9 and self.weapon_buf is True:
            if self.whole_inventory_for_items[9] is not None:
                if self.whole_inventory_for_items[9].name not in ['axe', 'sword']:
                    self.GameManager.player.weapon -= 80
                    self.weapon_buf = False
            else:
                self.GameManager.player.weapon -= 80
                self.weapon_buf = False

    def change_armour(self):
        if self.end_cell == 11:
            if self.whole_inventory_for_items[11] is not None:
                self.GameManager.player.armour += 50
        if self.start_cell == 11:
            self.GameManager.player.armour -= 50

        if self.end_cell == 6:
            if self.whole_inventory_for_items[6] is not None:
                self.GameManager.player.armour += 70
        if self.start_cell == 6:
            self.GameManager.player.armour -= 70

        if self.end_cell == 7:
            if self.whole_inventory_for_items[7] is not None:
                self.GameManager.player.armour += 100
        if self.start_cell == 7:
            self.GameManager.player.armour -= 100

    def show_panel(self):
        x = y = 15
        step = 45
        self.GameManager.screen.blit(health_img, (x - 2, y - 2))
        print_text(self.GameManager, str(self.GameManager.player.health), x + step, y - 5, (255, 255, 255),
                   font_size=30)

        self.GameManager.screen.blit(weapon_img, (x - 5, y + step - 7))
        print_text(self.GameManager, str(self.GameManager.player.weapon), x + step, y - 5 + step,
                   (255, 255, 255), font_size=30)

        self.GameManager.screen.blit(armour_img, (x - 3, y + 2 * step - 2))
        print_text(self.GameManager, str(self.GameManager.player.armour), x + step, y - 5 + 2 * step,
                   (255, 255, 255), font_size=30)
