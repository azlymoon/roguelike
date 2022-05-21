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
            'helmet': Item('coke', './img/helmet.png'),
            'chest': Item('coke', './img/chest.png'),
            'shield': Item('coke', './img/shield.png'),
            'axe': Item('coke', './img/axe.png'),
            'sword': Item('coke', './img/sword.png')
        }

        # self.inventory_panel = [None] * 3
        self.whole_inventory = [None] * 4
        self.whole_inventory_for_items = [None] * 6
        self.whole_inventory_for_armour = [None] * 4
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
        x = 945
        y = 295
        side = 60
        step = 75

        # отрисовка основного инвентаря на 8 ячеек
        pygame.draw.rect(GameManager.screen, (175, 190, 202), (930, 280, 315, 100))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (930, 280, 315, 100), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (930, 280, 315, 100), 2)

        # отрисовка ячейки для оружия
        pygame.draw.rect(GameManager.screen, (175, 190, 202), (710, 295, 90, 105))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (710, 295, 90, 105), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (710, 295, 90, 105), 2)
        pygame.draw.rect(GameManager.screen, (200, 215, 227), (725, 310, side, side))
        print_text(GameManager, "weapon", 725, 369, font_size=18)

        # отрисовка ячейки для щита
        pygame.draw.rect(GameManager.screen, (175, 190, 202), (710, 430, 90, 105))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (710, 430, 90, 105), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (710, 430, 90, 105), 2)
        pygame.draw.rect(GameManager.screen, (200, 215, 227), (725, 460, side, side))
        print_text(GameManager, "shield", 729, 437, font_size=18)

        for cell in self.whole_inventory:
            # print(cell.amount)
            pygame.draw.rect(GameManager.screen, (200, 215, 227), (x, y, side, side))
            if cell is not None:
                GameManager.screen.blit(cell.image, (x + 5, y + 5))
                print_text(GameManager, str(cell.amount), x + 27, y + 60, font_size=18)

            x += step

    def draw_whole_items(self, GameManager):
        x = 945
        y = 415
        side = 60
        step = 75

        # отрисовка основного инвентаря на 8 ячеек
        pygame.draw.rect(GameManager.screen, (175, 190, 202), (930, 400, 240, 165))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (930, 400, 240, 165), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (930, 400, 240, 165), 2)

        for cell1 in self.whole_inventory_for_items:
            # print(cell.amount)
            pygame.draw.rect(GameManager.screen, (200, 215, 227), (x, y, side, side))
            if cell1 is not None:
                GameManager.screen.blit(cell1.image1, (x + 5, y + 5))

            x += step

            if x == 1170:
                x = 945
                y += step

    def draw_whole_armour(self, GameManager):
        x = 825
        y = 235
        side = 60
        step = 75

        # отрисовка амуниции на 4 ячейки
        pygame.draw.rect(GameManager.screen, (175, 190, 202), (810, 205, 90, 330))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (810, 205, 90, 330), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (810, 205, 90, 330), 2)
        print_text(GameManager, "armour", 825, 210, font_size=18)

        for cell2 in self.whole_inventory_for_armour:
            # print(cell.amount)
            pygame.draw.rect(GameManager.screen, (200, 215, 227), (x, y, side, side))

            y += step

    def set_start_cell(self, mouse_x, mouse_y):
        start_x = 945
        start_y = 415
        step = 75
        side = 60

        for y in range(0, 2):
            for x in range(0, 3):
                cell_x = start_x + x * step
                cell_y = start_y + y * step

                if cell_x <= mouse_x <= cell_x + side and cell_y <= mouse_y <= cell_y + side:
                    self.start_cell = y * 3 + x
                    print("Start " + str(y * 3 + x))
                    return
                # print("Cell #{0} is ({1}, {2})".format(y * 4 + x, x, y))
                # print("x: [{0}, {1}], y: [{2}, {3}]".format(cell_x, cell_x + side, cell_y, cell_y + side))

        start_x1 = 825
        start_y1 = 235
        step = 75
        side = 60

        for y1 in range(0, 4):
            for x1 in range(0, 1):
                cell_x1 = start_x1 + x1 * step
                cell_y1 = start_y1 + y1 * step

                if cell_x1 <= mouse_x <= cell_x1 + side and cell_y1 <= mouse_y <= cell_y1 + side:
                    self.start_cell = y1
                    print("End " + str(y1))
                    return

    def set_end_cell(self, mouse_x, mouse_y):
        start_x = 945
        start_y = 415
        step = 75
        side = 60

        for y in range(0, 2):
            for x in range(0, 3):
                cell_x = start_x + x * step
                cell_y = start_y + y * step

                if cell_x <= mouse_x <= cell_x + side and cell_y <= mouse_y <= cell_y + side:
                    self.end_cell = y * 3 + x
                    print("End " + str(y * 3 + x))
                    self.swap_cells()
                    return

        start_x1 = 825
        start_y1 = 235
        step = 75
        side = 60

        for y1 in range(0, 4):
            for x1 in range(0, 1):
                cell_x1 = start_x1 + x1 * step
                cell_y1 = start_y1 + y1 * step

                if cell_x1 <= mouse_x <= cell_x1 + side and cell_y1 <= mouse_y <= cell_y1 + side:
                    self.end_cell1 = y1
                    print("End " + str(y1))
                    self.swap_cells_armour()
                    return

    def swap_cells(self):
        temp = self.whole_inventory_for_items[self.end_cell]
        self.whole_inventory_for_items[self.end_cell] = self.whole_inventory_for_items[self.start_cell]
        self.whole_inventory_for_items[self.start_cell] = temp

    def swap_cells_armour(self):
        temp1 = self.whole_inventory_for_armour[self.end_cell1]
        self.whole_inventory_for_armour[self.end_cell1] = self.whole_inventory_for_armour[self.start_cell1]
        self.whole_inventory_for_armour[self.start_cell1] = temp1
