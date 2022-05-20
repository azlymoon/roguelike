import pygame
from menu import print_text


class Resource:
    def __init__(self, name, image_path):
        self.name = name
        self.amount = 0
        self.image = pygame.image.load(image_path)


class Inventory:
    def __init__(self):
        self.resources = {
            'sword': Resource('sword', './img/sword.png'),
            'shield': Resource('shield', './img/shield.png'),
            'coke': Resource('coke', './img/coke.png')
        }

        self.inventory_panel = [None] * 3
        self.whole_inventory = [None] * 6

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
        print(self.resources[name].amount)

    def update_whole(self):
        for name, resource in self.resources.items():
            if resource.amount != 0 and resource not in self.whole_inventory:
                # self.whole_inventory.insert(self.whole_inventory.index(None), resource)
                print(resource.amount)
                self.whole_inventory[self.whole_inventory.index(None)] = resource
                # self.whole_inventory.remove(None)
            # print(self.resources[name].amount)
        # print()

    def draw_whole(self, GameManager):
        x = 30
        y = 550
        side = 60
        step = 75

        pygame.draw.rect(GameManager.screen, (175, 190, 202), (x - 15, y - 15, 240, 165))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (x - 15, y - 15, 240, 165), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (x - 15, y - 15, 240, 165), 2)

        for cell in self.whole_inventory:
            # print(cell.amount)
            pygame.draw.rect(GameManager.screen, (200, 215, 227), (x, y, side, side))
            if cell is not None:
                GameManager.screen.blit(cell.image, (x + 15, y + 5))
                print_text(GameManager, str(cell.amount), x + 37, y + 58, font_size=17)

            x += step

            if x == 255:
                x = 30
                y += step

    def draw_panel(self, GameManager):
        x = 500
        y = 625
        side = 60
        step = 75

        pygame.draw.rect(GameManager.screen, (175, 190, 202), (x - 15, y - 15, 240, 90))
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (x - 15, y - 15, 240, 90), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (x - 15, y - 15, 240, 90), 2)
        for cell in self.inventory_panel:
            pygame.draw.rect(GameManager.screen, (200, 215, 227), (x, y, side, side))
            if cell is not None:
                GameManager.screen.blit(cell.image, (x + 15, y + 5))
                print_text(GameManager, str(cell.amount), x + 37, y + 58, font_size=17)

            x += step
