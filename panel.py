import pygame
from menu import print_text


health_img = pygame.image.load('./img/menu/heart.png')
health_img = pygame.transform.scale(health_img, (32, 32))

weapon_img = pygame.image.load('./img/menu/weapon.png')
weapon_img = pygame.transform.scale(weapon_img, (40, 40))

armour_img = pygame.image.load('./img/menu/armour.png')
armour_img = pygame.transform.scale(armour_img, (34, 34))


def show_panel(GameManager):
    health = 100
    armour = 100
    weapon = 100
    x = y = 15
    step = 45
    # pygame.draw.rect(GameManager.screen, (255, 255, 255), (10, 10, 235, 85))
    # pygame.draw.rect(GameManager.screen, (184, 188, 163), (10, 10, 235, 85), 8)
    # pygame.draw.rect(GameManager.screen, (0, 0, 0), (10, 10, 235, 85), 2)
    GameManager.screen.blit(health_img, (x - 2, y - 2))
    print_text(GameManager, str(health), x + step, y - 5, (255, 255, 255), font_size=30)

    GameManager.screen.blit(weapon_img, (x - 5, y + step - 7))
    print_text(GameManager, str(weapon), x + step, y - 5 + step, (255, 255, 255), font_size=30)

    GameManager.screen.blit(armour_img, (x - 3, y + 2 * step - 2))
    print_text(GameManager, str(armour), x + step, y - 5 + 2 * step, (255, 255, 255), font_size=30)

