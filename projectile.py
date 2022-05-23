import pygame
from support import import_folder


class Flying_eye_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, player):
        pygame.sprite.Sprite.__init__(self)
        #self.pos = pos
        self.animations = {'explode': [], 'fly': [],
                           }

        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['fly'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.player = player
        self.speed = 15
        self.status = 'fly'
        # self.length1 = self.player.coordx - self.pos[0]
        # self.length2 = self.player.coordy - self.pos[1]
        self.coordx = pos[0]
        self.coordy = pos[1]
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
        if abs(self.coordx - self.player.coordx) < 10 or abs(self.coordy - self.player.coordy) < 10:

            self.status = 'explode'
            self.player.health -= 1
        else:
            self.status = 'fly'

    def update(self):
        self.get_status()
        if self.status != 'explode':
            self.rect.x += self.speed
            self.rect.y += self.speed
            self.coordx += self.speed
            self.coordy += self.speed
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
