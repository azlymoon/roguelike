import pygame
from support import import_folder
from math import sqrt


class Flying_eye_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, player_pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.player_pos = player_pos
        self.animations = {'explode': [], 'fly': [],
                           }

        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['fly'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = 15
        self.status = 'fly'
        self.length1 = self.player_pos[0] - self.pos[0]
        self.length2 = self.player_pos[1] - self.pos[1]
        self.coordx = self.pos[0]
        self.coordy = self.pos[1]

    def import_assets(self):
        path = './img/img_mobs/flying_eye_projectile/'


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

    def get_status(self, pos, player_pos):

        if (abs(self.coordx - self.player_pos[0]) < 10) and (abs(self.coordy - self.player_pos[1]) < 10):
            self.status = 'explode'
        else:
            self.status = 'fly'

    def update(self):
        #self.get_status(pos=self.pos, player_pos=self.player_pos)
        if self.status != 'explode':
            self.rect.x += self.length1 / self.speed
            self.rect.y += self.length2 / self.speed
            self.coordx += self.length1 / self.speed
            self.coordy += self.length2 / self.speed
        self.animate()


class Goblin_projectile(Flying_eye_projectile):
    def import_assets(self):
        path = '.img/img_mobs/goblin_projectile/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)
