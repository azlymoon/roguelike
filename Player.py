import pygame
from support import import_folder
WIDTH = 32
HEIGHT = 32


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, GameManager):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {'idle_left': [], 'idle_right': [], 'idle_up': [], 'idle_down': [],
                           'run_left': [], 'run_right': [], 'run_up': [], 'run_down': [],
                           'attack_left': [], 'attack_right': [], 'attack_up': [], 'attack_down': [],

                           }

        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['idle_right'][self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)

        # player movement

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.health = 100
        self.weapon = 100
        self.armour = 100

        # player status
        self.status = 'idle_right'
        self.attack_status = 0
        self.next_status = 0
        self.coordx = pos[0]
        self.coordy = pos[1]

        self.obstacle_sprites = obstacle_sprites
        self.GameManager = GameManager

    def import_assets(self):
        path = './img/'
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        if self.status != '':
            animation = self.animations[self.status]
            self.frame_index += len(animation) / 20
            if self.frame_index >= len(animation):
                self.frame_index = 0
            self.image = animation[int(self.frame_index)]

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys.count(True) > 0:
            if keys[pygame.K_1]:
                self.attack_status = 1
                self.direction.x = 0
                self.direction.y = 0
            else:
                self.attack_status = 0
                if keys[pygame.K_RIGHT]:
                    self.direction.x = 1
                if keys[pygame.K_LEFT]:
                    self.direction.x = -1
                if keys[pygame.K_UP]:
                    self.direction.y = -1
                if keys[pygame.K_DOWN]:
                    self.direction.y = 1
                if keys[pygame.K_2]:
                    self.health -= 1
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.attack_status = 0

    def get_status(self):
        if self.attack_status == 1:
            if self.status in ['idle_right', 'run_right']:
                self.status = 'attack_right'
                self.next_status = 'idle_right'
                self.attack_status = 0
            elif self.status in ['idle_left', 'run_left']:
                self.status = 'attack_left'
                self.next_status = 'idle_left'
                self.attack_status = 0
            elif self.status in ['idle_up', 'run_up']:
                self.status = 'attack_up'
                self.next_status = 'idle_up'
                self.attack_status = 0
            elif self.status in ['idle_down', 'run_down']:
                self.status = 'attack_down'
                self.next_status = 'idle_down'
                self.attack_status = 0
        else:
            if self.direction.x == 1:
                self.status = 'run_right'
                self.next_status = 'idle_right'
            elif self.direction.x == -1:
                self.status = 'run_left'
                self.next_status = 'idle_left'
            elif self.direction.y == 1:
                self.status = 'run_down'
                self.next_status = 'idle_down'
            elif self.direction.y == -1:
                self.status = 'run_up'
                self.next_status = 'idle_up'

            else:
                if self.next_status == 0:
                    self.status = 'idle_right'
                else:
                    self.status = self.next_status

    def collision_wall(self, direction):
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

    def collision_item(self):
        for sprite in self.GameManager.item_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.name in self.GameManager.items['item']:
                    whole_inventory_for_items = self.GameManager.inventory.whole_inventory_for_items
                    whole_inventory_for_items[whole_inventory_for_items.index(None)] = sprite
                elif sprite.name in self.GameManager.items['resource']:
                    if sprite.name == 'coke':
                        self.health += 50
                sprite.kill()

    def update(self):
        self.get_input()
        self.get_status()
        self.rect.x += self.direction.x * self.speed
        self.coordx += self.direction.x * self.speed
        self.collision_wall('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.coordy += self.direction.y * self.speed
        self.collision_wall('vertical')
        self.collision_item()
        self.animate()
