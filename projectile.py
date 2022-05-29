import pygame
from support import import_folder
from math import sqrt, copysign


class Flying_eye_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, GameManager):
        pygame.sprite.Sprite.__init__(self)
        # self.pos = pos
        self.animations = {'explode': [], 'fly': [],
                           }
        self.GameManager = GameManager
        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['fly'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.status = 'fly'
        self.living_time = 0
        self.target_coords = (GameManager.player.rect.x, GameManager.player.rect.y)
        # self.cur_speed=15
        # self.length1 = self.player.coordx - self.pos[0]
        # self.length2 = self.player.coordy - self.pos[1]
        self.direction = pygame.math.Vector2(0, 0)

        self.length = sqrt((self.target_coords[0] - self.rect.x) ** 2 + (self.target_coords[1] - self.rect.y) ** 2)
        # print(type(self.coordx))
        # print(type(self.player.coordx))
        self.add_to_projectile_sprites()
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2((GameManager.player.rect.x, GameManager.player.rect.y)) - self.pos
        sign = lambda a: 1 if a > 0 else -1 if a < 0 else 0
        # self.direction.x = sign(self.target_coords[0] - self.rect.x)
        # self.direction.y = sign(self.target_coords[1] - self.rect.y)
        self.speed = 7
        # self.speedy = 7

    def add_to_projectile_sprites(self):
        self.GameManager.projectile_sprites.add(self)

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

    # def get_status(self):

        # if self.living_time > self.length / sqrt(self.speedy**2+self.speedx**2):
        #     self.status = 'explode'
        #     self.living_time = 0
        # if self.living_time < self.length / self.speed:
        #     self.status = 'fly'
        #     self.living_time += 1
        # else:
        #     # if abs(self.player.coordx - self.coordx) <= 3 and abs(self.player.coordy - self.coordy) <= 3:
        #     #     self.player.health -= 1
        #     self.status = 'explode'

        # else:
        #     self.status = 'fly'
        #     self.direction.x = sign(self.target_coords[0] - self.coordx)
        #     self.direction.y = sign(self.target_coords[1] - self.coordy)
        #     self.living_time += 1

    def collision_wall(self):
        for wall in self.GameManager.obstacle_sprites:
            if wall.rect.colliderect(self.rect):
                self.status = 'explode'
                self.kill()

    def update(self):
        # self.get_status()
        # print("статус из прожектайла", self.status)
        # print("коорды из прожектайла", self.coordx, self.coordy, self.player.coordx, self.player.coordy,
        # self.target_coords)
        self.collision_wall()
        if self.status != 'explode':
            self.pos += self.direction.normalize() * self.speed
            self.rect.center = (round(self.pos.x), round(self.pos.y))
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
