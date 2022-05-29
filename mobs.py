import math

import pygame
from support import import_folder
from projectile import Flying_eye_projectile, Goblin_projectile, Mushroom_projectile
from math import sqrt, floor
import random


class Flying_eye(pygame.sprite.Sprite):
    def __init__(self, pos, player, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {'idle_left': [], 'idle_right': [],
                           'run_left': [], 'run_right': [],
                           'attack_left': [], 'attack_right': []

                           }

        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['idle_right'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.player = player
        # mob movement

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.health = 1
        self.coordx = pos[0]
        self.coordy = pos[1]

        # mob status
        self.status = 'idle_right'
        self.attack_status = 0
        self.next_status = 0
        # self.projectile = Flying_eye_projectile(pos=pos, player=player,
        # target_coords=(self.player.coordx, self.player.coordy))
        self.projectile = None

        # self.projectile.status = 'ex'
        self.obstacle_sprites = obstacle_sprites
        self.move_time = 1

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

        if self.move_time % 151 == 0:
            self.direction.x = random.randint(-1, 1)
            self.direction.y = random.randint(-1, 1)
            self.move_time = 0
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.move_time += 1

    def get_status(self):
        # print(self.projectile.status)
        # print(self.frame_index)
        # if 40 > sqrt(
        #         (self.coordx - self.player.coordx) ** 2 + (self.coordy - self.player.coordy) ** 2) > 10 and \
        #         math.floor(self.frame_index) == len(self.animations)-1:
        # print(self.projectile.status)
        print(sqrt(
            (self.coordx - self.player.coordx) ** 2 + (self.coordy - self.player.coordy) ** 2))
        if 200 > sqrt((self.coordx - self.player.coordx) ** 2 + (self.coordy - self.player.coordy) ** 2) > 40 and \
                math.floor(self.frame_index) == len(self.animations) - 1:
            if self.projectile is None:
                self.create_projectile([self.coordx, self.coordy], self.player,
                                       (self.player.coordx, self.player.coordy))

            else:
                if self.projectile.status == 'explode':
                    self.create_projectile([self.coordx, self.coordy], self.player,
                                           (self.player.coordx, self.player.coordy))
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

    def create_projectile(self, mob_coords, player_coords, target_coords):
        self.projectile = Flying_eye_projectile(mob_coords, self.player, target_coords)

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

    def update(self):
        # print(self.coordx, self.coordy, self.player.coordx, self.player.coordy)
        # self.get_input()
        self.get_status()
        # print(self.status)
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')
        self.coordx += self.direction.x * self.speed
        self.coordy += self.direction.y * self.speed
        self.animate()


class Goblin(Flying_eye):
    def __init__(self, pos, player, obstacle_sprites):
        super().__init__(pos=pos, player=player, obstacle_sprites=obstacle_sprites)
        # self.projectile = Goblin_projectile(pos=pos, player=self.player, target_coords=(player.coordx, player.coordy))

    def import_assets(self):
        path = './goblin/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def create_projectile(self, mob_coords, player_coords, target_coords):
        self.projectile = Goblin_projectile(mob_coords, self.player, target_coords)


class Mushroom(Flying_eye):
    def __init__(self, pos, player, obstacle_sprites):
        super().__init__(pos=pos, player=player, obstacle_sprites=obstacle_sprites)
        # self.projectile = Mushroom_projectile(pos=pos, player=self.player,
        # target_coords=(self.player.coordx, self.player.coordy))

    def import_assets(self):
        path = './mushroom/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def create_projectile(self, mob_coords, player_coords, target_coords):
        self.projectile = Mushroom_projectile(mob_coords, self.player, target_coords)
