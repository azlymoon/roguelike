import pygame


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (184, 188, 163)
        self.active_clr = (255, 253, 208)

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

        print_text(GameManager, message=message, x=x+20, y=y+14, font_size=font_size)


def show_menu(GameManager):
    menu_bckgr = pygame.image.load('./img/menu/menu.jpg')
    menu_bckgr = pygame.transform.scale(menu_bckgr, (1280, 720))

    start_btn = Button(480, 150)
    quit_btn = Button(440, 150)

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        GameManager.screen.blit(menu_bckgr, (0, 0))
        start_btn.draw(GameManager, 400, 150, 'start game', GameManager.start_game, 90)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (400, 150, 480, 150), 8)
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (400, 150, 480, 150), 2)
        quit_btn.draw(GameManager, 420, 370, 'quit game', quit, 90)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (420, 370, 440, 150), 8)
        pygame.draw.rect(GameManager.screen, (255, 255, 255), (420, 370, 440, 150), 2)

        # pygame.GameManager.screen.update()
        pygame.display.flip()
        GameManager.clock.tick(30)


def print_text(GameManager, message, x, y, font_color=(0, 0, 0), font_type='./img/menu/Empirecrown.ttf', font_size=64):
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

        pygame.draw.rect(GameManager.screen, (255, 255, 255), (140, 240, 1000, 213))
        pygame.draw.rect(GameManager.screen, (184, 188, 163), (140, 240, 1000, 213), 8)
        pygame.draw.rect(GameManager.screen, (0, 0, 0), (140, 240, 1000, 213), 2)
        print_text(GameManager, 'paused. press ENTER to continue', 166, 260)
        print_text(GameManager, 'or press SPACE to quit.', 322, 340)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        if keys[pygame.K_SPACE]:
            quit()

        # pygame.screen.update()
        pygame.display.flip()
