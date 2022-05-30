import math

import pygame
from support import import_folder
from projectile import Flying_eye_projectile, Goblin_projectile, Mushroom_projectile
from math import sqrt
import random


class Flying_eye(pygame.sprite.Sprite):
    def __init__(self, pos, player, obstacle_sprites, GameManager):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {'idle_left': [], 'idle_right': [],
                           'run_left': [], 'run_right': [],
                           'attack_left': [], 'attack_right': []

                           }
        self.GameManager = GameManager
        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['idle_right'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.player = player
        # mob movement

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.health = 1000

        # mob status
        self.status = 'idle_right'
        self.attack_status = 0
        self.next_status = 0
        self.projectile = None
        self.obstacle_sprites = obstacle_sprites
        self.move_time = 30

    def import_assets(self):
        path = './flying_eye/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        if self.status != '':
            animation = self.animations[self.status]
            self.frame_index += 0.15
            if self.frame_index >= len(animation):
                self.frame_index = 0
            self.image = animation[int(self.frame_index)]

    def get_input(self):
        print(self.move_time % 30)
        if self.move_time % 30 == 0:
            self.direction.x = random.randint(-1, 1)
            self.direction.y = random.randint(-1, 1)
            self.move_time = 1
        else:
            print(self.move_time)
            self.move_time += 1

    def get_status(self):
        if 200 > sqrt((self.rect.x - self.player.rect.x) ** 2 + (self.rect.y - self.rect.y) ** 2) > 40 and \
                math.floor(self.frame_index) == len(self.animations) - 1:
            if self.projectile is None:
                self.create_projectile()

            else:
                if self.projectile.status == 'explode':
                    self.create_projectile()
        self.attack_status = 1
        if self.attack_status == 1:
            if self.status == 'idle_right':
                self.status = 'attack_right'
                self.next_status = 'idle_right'
                self.attack_status = 0
            elif self.status == 'idle_left':
                self.status = 'attack_left'
                self.next_status = 'idle_left'
                self.attack_status = 0

        else:
            if self.direction.x == 1:
                self.status = 'run_right'
                self.next_status = 'idle_right'
            elif self.direction.x == -1:
                self.status = 'run_left'
                self.next_status = 'idle_left'
            elif self.direction.y == 1 and self.status == 'idle_right':
                self.status = 'run_right'
                self.next_status = 'idle_right'
            elif self.direction.y == -1 and self.status == 'idle_right':
                self.status = 'run_right'
                self.next_status = 'idle_right'
            elif self.direction.y == 1 and self.status == 'idle_left':
                self.status = 'run_left'
                self.next_status = 'idle_left'
            elif self.direction.y == -1 and self.status == 'idle_left':
                self.status = 'run_left'
                self.next_status = 'idle_left'

            else:
                if self.next_status == 0:
                    self.status = 'idle_right'
                else:
                    self.status = self.next_status

    def create_projectile(self):
        self.projectile = Flying_eye_projectile([self.rect.x, self.rect.y], self.GameManager)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def check_health(self):
        if self.health <= 0:
            print(self.health)
            self.kill()

    def update(self):
        self.get_input()
        self.get_status()
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')
        self.animate()


class Goblin(Flying_eye):
    def __init__(self, pos, player, obstacle_sprites, GameManager):
        super().__init__(pos=pos, player=player, obstacle_sprites=obstacle_sprites,
                         GameManager=GameManager)

    def import_assets(self):
        path = './goblin/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def create_projectile(self):
        self.projectile = Goblin_projectile([self.rect.x, self.rect.y], self.GameManager)


class Mushroom(Flying_eye):
    def __init__(self, pos, player, obstacle_sprites, GameManager):
        super().__init__(pos=pos, player=player, obstacle_sprites=obstacle_sprites,
                         GameManager=GameManager)

    def import_assets(self):
        path = './mushroom/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def create_projectile(self):
        self.projectile = Mushroom_projectile([self.rect.x, self.rect.y], self.GameManager)
