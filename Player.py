import pygame
from support import import_folder
from menu import print_text
import sys

WIDTH = 32
HEIGHT = 32


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, GameManager):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {'idle_left': [], 'idle_right': [], 'idle_up': [], 'idle_down': [],
                           'run_left': [], 'run_right': [], 'run_up': [], 'run_down': [],
                           'attack_left': [], 'attack_right': [], 'attack_up': [], 'attack_down': []}

        self.import_assets()
        self.frame_index = 0
        self.image = self.animations['idle_right'][self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)
        self.mobs = None
        # player movement

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.health = 100
        self.weapon = 100
        self.armour = 100
        self.coin = 0
        self.enemy = 0

        # player status
        self.status = 'idle_right'
        self.attack_status = 0
        self.next_status = 0
        self.GameManager = GameManager

        self.obstacle_sprites = obstacle_sprites
        self.GameManager = GameManager

    def import_assets(self):
        path = './img/'
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def give_pos_player(self):
        return [self.rect.x, self.rect.y]

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
                    self.direction.y = 0
                if keys[pygame.K_LEFT]:
                    self.direction.x = -1
                    self.direction.y = 0
                if keys[pygame.K_UP]:
                    self.direction.y = -1
                    self.direction.x = 0
                if keys[pygame.K_DOWN]:
                    self.direction.y = 1
                    self.direction.x = 0
                if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                    self.direction.x = 1
                    self.direction.y = -1
                if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                    self.direction.x = 1
                    self.direction.y = 1
                if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                    self.direction.x = -1
                    self.direction.y = -1
                if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                    self.direction.x = -1
                    self.direction.y = 1
                if keys[pygame.K_2]:
                    self.health -= 1
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.attack_status = 0

    def get_mobs(self, mobs):
        self.mobs = mobs

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
        for item in self.GameManager.item_sprites:
            if item.rect.colliderect(self.rect):
                if item.name in self.GameManager.items['item']:
                    whole_inventory_for_items = self.GameManager.inventory.whole_inventory_for_items
                    whole_inventory_for_items[whole_inventory_for_items.index(None)] = item
                elif item.name in self.GameManager.items['resource']:
                    if item.name == 'coke':
                        self.health += 50
                    if item.name == 'coin':
                        self.coin += 1
                item.kill()

    def collision_mob(self):

        for mob in self.GameManager.mob_sprites:
            if mob.rect.colliderect(self.rect) and self.status in ['attack_left', 'attack_up',
                                                                   'attack_down', 'attack_right']:
                mob.health -= self.weapon
                mob.check_health()

    def collision_projectile(self):
        for projectile in self.GameManager.projectile_sprites:
            if projectile.rect.colliderect(self.rect):
                if self.armour >= 20:
                    self.armour -= 20
                elif self.armour > 0:
                    self.armour -= self.armour
                else:
                    self.health -= 10
                projectile.status = 'explode'
                projectile.kill()

    def check_health(self):
        if self.health <= 0:
            self.game_over_menu()

    def game_over_menu(self):
        dead = True
        while dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.draw.rect(self.GameManager.screen, (255, 255, 255), (290, 360, 700, 213))
            pygame.draw.rect(self.GameManager.screen, (184, 188, 163), (290, 360, 700, 213), 8)
            pygame.draw.rect(self.GameManager.screen, (0, 0, 0), (290, 360, 700, 213), 2)
            print_text(self.GameManager, 'you dead. game over.', 88, 150, (255, 255, 255), font_size=115)
            print_text(self.GameManager, 'press SPACE to restart', 308, 380, (0, 0, 0))
            print_text(self.GameManager, 'or press TAB to quit.', 370, 460, (0, 0, 0))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_SPACE]:
                dead = False
                self.GameManager.start_new_lvl()

            pygame.display.flip()

    def update(self):
        self.check_health()
        self.get_input()
        self.get_status()
        self.rect.x += self.direction.x * self.speed
        self.collision_wall('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision_wall('vertical')
        self.collision_item()
        self.collision_mob()
        self.collision_projectile()
        self.animate()
