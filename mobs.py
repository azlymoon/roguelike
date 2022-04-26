import pygame
from support import import_folder
from projectile import Flying_eye_projectile, Goblin_projectile, Mushroom_projectile
from math import sqrt


class Flying_eye(pygame.sprite.Sprite):
    def __init__(self, pos, player_pos, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {'idle_left': [], 'idle_right': [],
                           'run_left': [], 'run_right': [],
                           'attack_left': [], 'attack_right': []

                           }

        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['idle_right'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # mob movement

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.health = 1
        self.coordx = pos[0]
        self.coordy = pos[1]
        self.playerx = player_pos[0]
        self.playery = player_pos[1]
        # mob status
        self.status = 'idle_right'
        self.attack_status = 0
        self.next_status = 0
        self.projectile = Flying_eye_projectile(pos, player_pos)
        self.obstacle_sprites = obstacle_sprites

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        elif keys[pygame.K_SPACE]:
            self.attack_status = 1
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.attack_status = 0

    def get_status(self):
        if sqrt((self.coordx - self.playerx) ** 2 + (self.coordy - self.playery) ** 2) < 160:
            self.attack_status = 1
            # self.projectile = Flying_eye_projectile((self.coordx, self.coordy), player_pos)
            # self.projectile.status = 'fly'
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

    def create_projectile(self, mob_coords, player_coords):
        self.projectile = Flying_eye_projectile(mob_coords, player_coords)

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
        self.get_input()
        self.get_status()
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')
        self.coordx += self.direction.x * self.speed
        self.coordy += self.direction.y * self.speed
        self.animate()


# class Skeleton(Flying_eye):
#     def import_assets(self):
#         path = './img_mobs/skeleton/'
#
#         for animation in self.animations.keys():
#             full_path = path + animation
#             self.animations[animation] = import_folder(full_path)


class Goblin(Flying_eye):
    def __init__(self, pos, player_pos, obstacle_sprites):
        super().__init__(pos=pos, player_pos=player_pos, obstacle_sprites=obstacle_sprites)
        self.projectile = Goblin_projectile(pos=pos, player_pos=player_pos)

    def import_assets(self):
        path = './goblin/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def create_projectile(self, mob_coords, player_coords):
        self.projectile = Goblin_projectile(mob_coords, player_coords)


class Mushroom(Flying_eye):
    def __init__(self, pos, player_pos, obstacle_sprites):
        super().__init__(pos=pos, player_pos=player_pos, obstacle_sprites=obstacle_sprites)
        self.projectile = Mushroom_projectile(pos=pos, player_pos=player_pos)

    def import_assets(self):
        path = './mushroom/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def create_projectile(self, mob_coords, player_coords):
        self.projectile = Mushroom_projectile(mob_coords, player_coords)