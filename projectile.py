import pygame
from support import import_folder
from math import sqrt, copysign


class Flying_eye_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, player, target_coords):
        pygame.sprite.Sprite.__init__(self)
        # self.pos = pos
        self.animations = {'explode': [], 'fly': [],
                           }

        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['fly'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.player = player
        self.speedx = 7
        self.speedy = 7
        self.status = 'fly'
        self.living_time = 0
        self.target_coords = target_coords
        # self.cur_speed=15
        # self.length1 = self.player.coordx - self.pos[0]
        # self.length2 = self.player.coordy - self.pos[1]
        self.coordx = pos[0]
        self.coordy = pos[1]
        self.direction = pygame.math.Vector2(0, 0)
        self.length = sqrt((self.target_coords[0] - self.coordx) ** 2 + (self.target_coords[1] - self.coordy) ** 2)
        # print(type(self.coordx))
        # print(type(self.player.coordx))

    def import_assets(self):
        path = './flying_eye_projectile/'

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

    def get_status(self):
        sign = lambda a: 1 if a > 0 else -1 if a < 0 else 0
        # if self.living_time > self.length / sqrt(self.speedy**2+self.speedx**2):
        #     self.status = 'explode'
        #     self.living_time = 0
        if abs(self.coordx - self.target_coords[0]) >= 5 or abs(
                self.coordy - self.target_coords[1]) >= 5 and self.living_time <self.length/self.speedy:
            self.status = 'fly'
            self.direction.x = sign(self.target_coords[0] - self.coordx)
            self.direction.y = sign(self.target_coords[1] - self.coordy)
            self.living_time += 1
        else:
            if abs(self.player.coordx - self.coordx) <= 3 and abs(self.player.coordy - self.coordy) <= 3:
                self.player.health -= 1
            self.status = 'explode'
            self.living_time=0

        # else:
        #     self.status = 'fly'
        #     self.direction.x = sign(self.target_coords[0] - self.coordx)
        #     self.direction.y = sign(self.target_coords[1] - self.coordy)
        #     self.living_time += 1

    def update(self):
        self.get_status()
        # print("статус из прожектайла", self.status)
        # print("коорды из прожектайла", self.coordx, self.coordy, self.player.coordx, self.player.coordy,
        # self.target_coords)
        if self.status != 'explode':
            self.rect.x += self.direction.x * self.speedx
            self.rect.y += self.direction.y * self.speedy
            self.coordx += self.direction.x * self.speedx
            self.coordy += self.direction.y * self.speedy
        self.animate()


class Goblin_projectile(Flying_eye_projectile):
    def import_assets(self):
        path = './goblin_projectile/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)


class Mushroom_projectile(Flying_eye_projectile):
    def import_assets(self):
        path = './mushroom_projectile/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)
