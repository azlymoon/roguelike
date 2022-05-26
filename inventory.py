import pygame
from menu import print_text


class Resource:
    def __init__(self, name, image_path):
        self.name = name
        self.amount = 0
        self.image = pygame.image.load(image_path)

class Item:
    def __init__(self, name1, image_path1):
        self.name1 = name1
        self.image1 = pygame.image.load(image_path1)


class Inventory:
    def __init__(self):
        self.resources = {
            'coke': Resource('coke', './img/coke.png')
        }
        self.items = {
            'helmet': Item('helmet', './img/helmet.png'),
            'chest': Item('chest', './img/chest.png'),
            'shield': Item('shield', './img/shield.png'),
            'axe': Item('axe', './img/axe.png'),
            'sword': Item('sword', './img/sword.png')
        }

        # self.inventory_panel = [None] * 3
        self.whole_inventory = [None] * 4
        self.whole_inventory_for_items = [None] * 12
        self.start_cell = 0
        self.end_cell = 0
        self.start_cell1 = 0
        self.end_cell1 = 0

    def get_amount(self, name):
        try:
            return self.resources[name].amount
        except KeyError:
            return -1

    def increase(self, name):
        # self.resources[name].amount += 1
        # print(self.resources[name].amount)
        # self.update_whole()
        if self.resources[name] not in self.whole_inventory:
            self.whole_inventory[self.whole_inventory.index(None)] = self.resources[name]
        self.resources[name].amount += 1
        # print(self.resources[name].amount)

    def increase_item(self, name1):
        # self.resources[name].amount += 1
        # print(self.resources[name].amount)
        # self.update_whole()
        if self.items[name1] not in self.whole_inventory_for_items:
            self.whole_inventory_for_items[self.whole_inventory_for_items.index(None)] = self.items[name1]

    # def update_whole(self):
    #     for name, resource in self.resources.items():
    #         if resource.amount != 0 and resource not in self.whole_inventory:
    #             # self.whole_inventory.insert(self.whole_inventory.index(None), resource)
    #             print(resource.amount)
    #             self.whole_inventory[self.whole_inventory.index(None)] = resource
    #             # self.whole_inventory.remove(None)
    #         # print(self.resources[name].amount)
    #     # print()

    def draw_whole(self, GameManager):
        x = 655
        y = 515
        side = 60
        step = 75

        # отрисовка основного инвентаря на 4 ячейки
        pygame.draw.rect(GameManager.screen, (175, 190, 202), (640, 500, 315, 100))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (640, 500, 315, 100), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (640, 500, 315, 100), 2)

        for cell in self.whole_inventory:
            # print(cell.amount)
            pygame.draw.rect(GameManager.screen, (200, 215, 227), (x, y, side, side))
            if cell is not None:
                GameManager.screen.blit(cell.image, (x + 5, y + 5))
                print_text(GameManager, str(cell.amount), x + 27, y + 60, (0, 0, 0), font_size=18)

            x += step

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
                GameManager.screen.blit(cell1.image1, (x + 5, y + 5))

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

    # def draw_whole_armour(self, GameManager):

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
                # print("Cell #{0} is ({1}, {2})".format(y * 4 + x, x, y))
                # print("x: [{0}, {1}], y: [{2}, {3}]".format(cell_x, cell_x + side, cell_y, cell_y + side))

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
                    return

    def swap_cells(self):
        temp = self.whole_inventory_for_items[self.end_cell]
        self.whole_inventory_for_items[self.end_cell] = self.whole_inventory_for_items[self.start_cell]
        self.whole_inventory_for_items[self.start_cell] = temp
