import pygame

health_img = pygame.image.load('./img/menu/heart.png')
health_img = pygame.transform.scale(health_img, (55, 55))
health = 3


def show_health(GameManager):
    global health
    show = 0
    x = 25
    pygame.draw.rect(GameManager.screen, (255, 255, 255), (10, 10, 235, 85))
    pygame.draw.rect(GameManager.screen, (184, 188, 163), (10, 10, 235, 85), 8)
    pygame.draw.rect(GameManager.screen, (0, 0, 0), (10, 10, 235, 85), 2)
    while show != health:
        GameManager.screen.blit(health_img, (x, 25))
        x += 75
        show += 1
