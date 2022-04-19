import pygame
from Player import Player
from map import Map
from CameraGroup import CameraGroup
from mobs import Flying_eye, Goblin, Mushroom
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


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (13, 162, 58)
        self.active_clr = (23, 204, 58)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(GameManager.screen, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
              # pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(GameManager.screen, self.inactive_clr, (x, y, self.width, self.height))

        print_text(message=message, x=x+10, y=y+10, font_size=font_size)


def show_menu():
    menu_bckgr = pygame.image.load('menu.jpg')
    menu_bckgr = pygame.transform.scale(menu_bckgr, (1280, 720))

    start_btn = Button(265, 80)
    quit_btn = Button(245, 80)

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        GameManager.screen.blit(menu_bckgr, (0, 0))
        start_btn.draw(270, 200, 'start game', GameManager.run, 50)
        quit_btn.draw(280, 300, 'quit game', quit, 50)

        pygame.GameManager.screen.update()
        GameManager.clock.tick(30)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='Empirecrown.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    GameManager.screen.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('paused. press ENTER to continue', 160, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.screen.update()


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
        self.mob1 = Flying_eye(tmp.get_spawn_coord_in_room(), (self.player.coordx, self.player.coordy))
        self.mob2 = Goblin(tmp.get_spawn_coord_in_room(), (self.player.coordx, self.player.coordy))
        self.mob3 = Mushroom(tmp.get_spawn_coord_in_room(), (self.player.coordx, self.player.coordy))
        self.visible_sprites.add(self.player)
        self.visible_sprites.add(self.mob1)
        self.visible_sprites.add(self.mob2)
        self.visible_sprites.add(self.mob3)
        self.mobs.append(self.mob1)
        self.mobs.append(self.mob2)
        self.mobs.append(self.mob3)
        self.set_state("game_running")

    def set_state(self, state):
        self.state = state

    def run(self):
        show_menu()
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
            for mob in self.mobs:
                if mob.projectile.status == "explode":
                    mob.projectile.kill()
                if (
                        sqrt((self.player.coordx - mob.coordx) ** 2 + (self.player.coordy - mob.coordy) ** 2)) <= 160:
                    if mob.projectile.status == 'explode':
                        mob.create_projectile((mob.coordx, mob.coordy), (self.player.coordx, self.player.coordy))
                    else:
                        self.visible_sprites.add(mob.projectile)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pause()

            # Обновление
            # self.entities.update()
            self.visible_sprites.update()
            # Рендеринг
            # self.screen.fill(BLACK)
            # self.screen.blit()
            # self.map_surface.draw(self.screen)

            self.visible_sprites.custom_draw(self.player)

            # self.entities.draw(self.screen)

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()
        pygame.quit()

show_menu()
