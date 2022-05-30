import pygame
from support import import_folder
from math import sqrt


class Flying_eye_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, GameManager):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {'explode': [], 'fly': []}
        self.GameManager = GameManager
        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['fly'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.status = 'fly'
        self.living_time = 0
        self.target_coords = (GameManager.player.rect.x, GameManager.player.rect.y)
        self.direction = pygame.math.Vector2(0, 0)

        self.length = sqrt((self.target_coords[0] - self.rect.x) ** 2 + (self.target_coords[1] - self.rect.y) ** 2)
        self.add_to_projectile_sprites()
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2((GameManager.player.rect.x, GameManager.player.rect.y)) - self.pos
        self.speed = 7

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

    def collision_wall(self):
        for wall in self.GameManager.obstacle_sprites:
            if wall.rect.colliderect(self.rect):
                self.status = 'explode'
                self.kill()

    def update(self):
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
