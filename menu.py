import pygame


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (13, 162, 58)
        self.active_clr = (23, 204, 58)

    def draw(self, GameManager, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(GameManager.screen, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
              # pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(GameManager.screen, self.inactive_clr, (x, y, self.width, self.height))

        print_text(GameManager, message=message, x=x+10, y=y+10, font_size=font_size)


def show_menu(GameManager):
    menu_bckgr = pygame.image.load('./img/menu/menu.jpg')
    menu_bckgr = pygame.transform.scale(menu_bckgr, (1280, 720))

    start_btn = Button(265, 80)
    quit_btn = Button(245, 80)

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        GameManager.screen.blit(menu_bckgr, (0, 0))
        start_btn.draw(GameManager, 270, 200, 'start game', GameManager.start_game, 50)
        quit_btn.draw(GameManager, 280, 300, 'quit game', quit, 50)

        # pygame.GameManager.screen.update()
        pygame.display.flip()
        GameManager.clock.tick(30)


def print_text(GameManager, message, x, y, font_color=(0, 0, 0), font_type='./img/menu/Empirecrown.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    GameManager.screen.blit(text, (x, y))


def pause(GameManager):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text(GameManager, 'paused. press ENTER to continue', 160, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        # pygame.screen.update()
        pygame.display.flip()
