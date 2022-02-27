import pygame
import pyganim
from support import import_folder
WIDTH = 32
HEIGHT = 32


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {'idle': [], 'idle_down': [], 'idle_left': [], 'idle_right': [], 'idle_up': [],
                           'run_down': [],
                           'run_left': [], 'run_right': [], 'run_up': [], 'slice_down': [],
                           'slice_left': [], 'slice_right': [], 'slice_up': []}
        self.import_assets()
        self.frame_index = 0
        self.image = pygame.Surface((WIDTH, HEIGHT))
        # self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        # player status
        self.status = 'idle'
        self.attack_status = 0
        self.next_status = 0

    def import_assets(self):
        # path = '/Users/User/Desktop/ICT/MIEM/kursach/img/'
        path = './img/'
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += 0.5
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        elif keys[pygame.K_1]:
            self.attack_status = 1
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.attack_status = 0

    def get_status(self):
        if self.attack_status == 1:
            if self.status == 'idle_right':
                self.status = 'slice_left'
                self.next_status = 'idle_right'
                self.attack_status = 0
            elif self.status == 'idle_left':
                self.status = 'slice_right'
                self.next_status = 'idle_left'
                self.attack_status = 0
            elif self.status == 'idle_down':
                self.status = 'slice_down'
                self.next_status = 'idle_down'
                self.attack_status = 0
            elif self.status == 'idle_up':
                self.status = 'slice_up'
                self.next_status = 'idle_up'
                self.attack_status = 0
        else:
            if self.direction.x == 1:
                self.status = 'run_right'
                self.next_status = 'idle_right'
            elif self.direction.x == -1:
                self.status = 'run_left'
                self.next_status = 'idle_left'
            else:
                if self.direction.y == 1:
                    self.status = 'run_down'
                    self.next_status = 'idle_down'
                elif self.direction.y == -1:
                    self.status = 'run_up'
                    self.next_status = 'idle_up'
                else:
                    if self.next_status == 0:
                        self.status = 'idle'
                    else:
                        self.status = self.next_status

    def update(self):
        self.get_input()
        self.get_status()
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.animate()
