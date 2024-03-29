import pygame
import sys
import sqlite3

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("data/Background.png")  # Add menu screen
pause = False
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
sound_menu = pygame.mixer.Sound("data/spokoinaia_muzyka_dlia_fona_bez_slov_chill_F75.mp3")
sound_menu.play()
sound_game = pygame.mixer.Sound("data/spokoinaia_muzyka_dlia_fona_bez_slov_chill_vEO.mp3")
level_order = 1
flag = True

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def Levels(start_game, level):
    start_game(screen_size, level)


def get_font(size):
    return pygame.font.Font("data/font.ttf", size)  # Add font


def Music(self):
    global flag
    if self:
        sound_menu.play()
        sound_game.play()
    else:
        sound_menu.stop()
        sound_game.stop()


def LanSWITCH():
    pass


def PauseMenu(start_game):
    global pause
    pause = True
    Main_menu(start_game)
    sound_menu.play()


def EndScreen(start_game):
    ES = pygame.image.load("data/ScreenshotPull.png")
    scale_task = pygame.transform.scale(
        ES, (ES.get_width() * 3,
               ES.get_height() * 3))
    window_rect = ES.get_rect(center=(400, 200))
    while True:
        SCREEN.blit(scale_task, window_rect)
        END_SCREEN_MOUSE_POS = pygame.mouse.get_pos()
        END_SCREEN_TEXT = get_font(80).render("CONGRATULATIONS", True, "#ffe521")
        END_SCREEN_RECT = END_SCREEN_TEXT.get_rect(center=(640, 110))
        SCREEN.blit(END_SCREEN_TEXT, END_SCREEN_RECT)
        QUIT_BUTTON = Button(image=pygame.image.load("data/Quit Rect.png"), pos=(640, 450),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        END_SCREEN_CONT = Button(image=None, pos=(640, 630),
                                 text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        END_SCREEN_CONT.changeColor(END_SCREEN_MOUSE_POS)
        END_SCREEN_CONT.update(SCREEN)
        for button in [END_SCREEN_CONT, QUIT_BUTTON]:
            button.changeColor(END_SCREEN_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if END_SCREEN_CONT.checkForInput(END_SCREEN_MOUSE_POS):
                    Play(start_game)
                    sys.exit()
                if QUIT_BUTTON.checkForInput(END_SCREEN_MOUSE_POS):
                    quit()
            pygame.display.update()


def Resume(start_game):
    RM = pygame.image.load("data/Resume.png")
    while True:
        SCREEN.blit(RM, (0, 0))
        RESUME_MOUSE_POS = pygame.mouse.get_pos()
        RESUME_TEXT = get_font(25).render("Information", True, "Black")
        INSTRUCTION_TITLE1_TEXT = get_font(20).render("Hightecher's---", True, "Black")
        INSTRUCTION_TITLE2_TEXT = get_font(20).render("----------Notes", True, "Black")
        RESUME_TEXT2 = get_font(15).render("Вы когда-нибудь задумывались",
                                           True, "Black")
        RESUME_TEXT3 = get_font(15).render("что делают эти дети из техно-",
                                           True, "Black")
        RESUME_TEXT4 = get_font(15).render("парков? Что-то там бегают,",
                                           True, "Black")   # одним из таких - хайтекером!
        RESUME_TEXT5 = get_font(15).render("пишут, печатают, режут и т.д.",
                                           True, "Black")
        RESUME_TEXT6 = get_font(15).render("В этой игре вы сможете погру-",
                                           True, "Black")
        RESUME_TEXT7 = get_font(15).render("зиться в процесс становления",
                                           True, "Black")
        RESUME_TEXT8 = get_font(15).render("одним из таких - ХАЙТЕКЕРОМ!",
                                           True, "Black")
        INSTRUCTION_TEXT = get_font(15).render("“PLAY” - меню для выбора уро-",
                                               True, "Black")
        INSTRUCTION_TEXT2 = get_font(15).render("вня сложности в предстоящей",
                                                True, "Black")
        INSTRUCTION_TEXT3 = get_font(15).render("игре.",
                                                True, "Black")
        INSTRUCTION_TEXT4 = get_font(15).render("Кнопка “QUIT” - выход из игры.",
                                                True, "Black")
        INSTRUCTION_TEXT5 = get_font(15).render("Желаем удачи! Дополнительную",
                                                True, "Black")
        INSTRUCTION_TEXT6 = get_font(15).render("информацию по разработке можно",
                                                True, "Black")
        INSTRUCTION_TEXT7 = get_font(15).render("узнать здесь…",
                                                True, "Black")
        SIGNATURE_TEXT1 = get_font(15).render("vk.com/bgele",
                                              True, "Green")
        SIGNATURE_TEXT2 = get_font(15).render("vk.com/hackforge_industries",
                                              True, "Green")
        SIGNATURE_TEXT3 = get_font(15).render("vk.com/thesameamiten",
                                              True, "Green")
        RESUME_RECT = RESUME_TEXT.get_rect(center=(300, 95))
        INSTRUCTION_TITLE1_RECT = RESUME_TEXT.get_rect(center=(830, 75))
        INSTRUCTION_TITLE2_RECT = RESUME_TEXT.get_rect(center=(830, 100))
        INSTRUCTION_RECT = RESUME_TEXT.get_rect(center=(770, 205))
        INSTRUCTION_RECT2 = RESUME_TEXT.get_rect(center=(770, 235))
        INSTRUCTION_RECT3 = RESUME_TEXT.get_rect(center=(770, 265))
        INSTRUCTION_RECT4 = RESUME_TEXT.get_rect(center=(770, 295))
        INSTRUCTION_RECT5 = RESUME_TEXT.get_rect(center=(770, 325))
        INSTRUCTION_RECT6 = RESUME_TEXT.get_rect(center=(770, 355))
        INSTRUCTION_RECT7 = RESUME_TEXT.get_rect(center=(770, 385))
        SIGNATURE_RECT1 = RESUME_TEXT.get_rect(center=(770, 415))
        SIGNATURE_RECT2 = RESUME_TEXT.get_rect(center=(770, 445))
        SIGNATURE_RECT3 = RESUME_TEXT.get_rect(center=(770, 475))
        RESUME_RECT2 = RESUME_TEXT2.get_rect(center=(320, 140))
        RESUME_RECT3 = RESUME_TEXT2.get_rect(center=(320, 175))
        RESUME_RECT4 = RESUME_TEXT2.get_rect(center=(320, 205))
        RESUME_RECT5 = RESUME_TEXT2.get_rect(center=(320, 235))
        RESUME_RECT6 = RESUME_TEXT2.get_rect(center=(320, 265))
        RESUME_RECT7 = RESUME_TEXT2.get_rect(center=(320, 295))
        RESUME_RECT8 = RESUME_TEXT2.get_rect(center=(320, 325))
        SCREEN.blit(INSTRUCTION_TITLE1_TEXT, INSTRUCTION_TITLE1_RECT)
        SCREEN.blit(INSTRUCTION_TITLE2_TEXT, INSTRUCTION_TITLE2_RECT)
        SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)
        SCREEN.blit(INSTRUCTION_TEXT2, INSTRUCTION_RECT2)
        SCREEN.blit(INSTRUCTION_TEXT3, INSTRUCTION_RECT3)
        SCREEN.blit(INSTRUCTION_TEXT4, INSTRUCTION_RECT4)
        SCREEN.blit(INSTRUCTION_TEXT5, INSTRUCTION_RECT5)
        SCREEN.blit(INSTRUCTION_TEXT6, INSTRUCTION_RECT6)
        SCREEN.blit(INSTRUCTION_TEXT7, INSTRUCTION_RECT7)
        SCREEN.blit(SIGNATURE_TEXT1, SIGNATURE_RECT1)
        SCREEN.blit(SIGNATURE_TEXT2, SIGNATURE_RECT2)
        SCREEN.blit(SIGNATURE_TEXT3, SIGNATURE_RECT3)
        SCREEN.blit(RESUME_TEXT, RESUME_RECT)
        SCREEN.blit(RESUME_TEXT2, RESUME_RECT2)
        SCREEN.blit(RESUME_TEXT3, RESUME_RECT3)
        SCREEN.blit(RESUME_TEXT4, RESUME_RECT4)
        SCREEN.blit(RESUME_TEXT5, RESUME_RECT5)
        SCREEN.blit(RESUME_TEXT6, RESUME_RECT6)
        SCREEN.blit(RESUME_TEXT7, RESUME_RECT7)
        SCREEN.blit(RESUME_TEXT8, RESUME_RECT8)
        RESUME_BACK = Button(image=None, pos=(840, 640),
                             text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        RESUME_BACK.changeColor(RESUME_MOUSE_POS)
        RESUME_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BACK.checkForInput(RESUME_MOUSE_POS):
                    Setting(start_game)
        pygame.display.update()


def Play(start_game):     # start_game()
    global level_order
    Music(not flag)
    sound_game.play()
    LV = pygame.image.load("data/LevelsBG.png")
    LP = pygame.image.load("data/LevelsPlates.png")
    while True:
        con = sqlite3.connect("data/db")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT time FROM level_score""").fetchall()
        level_score1 = str(result[0][0]) if result[0][0] != 0 else '-'
        level_score2 = str(result[1][0]) if result[1][0] != 0 else '-'
        level_score3 = str(result[2][0]) if result[2][0] != 0 else '-'
        TIME = get_font(15).render('The best speed:', True, "White")

        SCREEN.blit(LV, (0, 0))
        SCREEN.blit(LP, (70, 35))
        SCREEN.blit(LP, (490, 35))
        SCREEN.blit(LP, (910, 35))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        LEVEL1_TEXT = get_font(30).render("Level 1", True, "White")
        LEVEL1_RECT = LEVEL1_TEXT.get_rect(center=(220, 120))
        TIME1 = get_font(22).render(level_score1, True, "White")
        RECT1 = LEVEL1_TEXT.get_rect(center=(220, 170))
        RECT1T = LEVEL1_TEXT.get_rect(center=(310, 200))
        SCREEN.blit(TIME, RECT1)
        SCREEN.blit(TIME1, RECT1T)
        SCREEN.blit(LEVEL1_TEXT, LEVEL1_RECT)

        LEVEL2_TEXT = get_font(30).render("Level 2", True, "White")
        LEVEL2_RECT = LEVEL2_TEXT.get_rect(center=(640, 120))
        TIME2 = get_font(22).render(level_score2, True, "White")
        RECT2 = LEVEL2_TEXT.get_rect(center=(640, 170))
        RECT2T = LEVEL2_TEXT.get_rect(center=(730, 200))
        SCREEN.blit(TIME, RECT2)
        SCREEN.blit(TIME2, RECT2T)
        SCREEN.blit(LEVEL2_TEXT, LEVEL2_RECT)

        LEVEL3_TEXT = get_font(30).render("Level 3", True, "White")
        LEVEL3_RECT = LEVEL3_TEXT.get_rect(center=(1060, 120))
        TIME3 = get_font(22).render(level_score3, True, "White")
        RECT3 = LEVEL3_TEXT.get_rect(center=(1060, 170))
        RECT3T = LEVEL3_TEXT.get_rect(center=(1150, 200))
        SCREEN.blit(TIME, RECT3)
        SCREEN.blit(TIME3, RECT3T)
        SCREEN.blit(LEVEL3_TEXT, LEVEL3_RECT)



        GO1_BUTTON = Button(image=None, pos=(220, 500),
                            text_input="GO", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        GO2_BUTTON = Button(image=None, pos=(640, 500),
                            text_input="GO", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        GO3_BUTTON = Button(image=None, pos=(1060, 500),
                            text_input="GO", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        PLAY_BACK = Button(image=None, pos=(640, 650),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        for button in [GO1_BUTTON, GO2_BUTTON, GO3_BUTTON, PLAY_BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    Main_menu(start_game)
                if GO1_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    level_order = 1
                    Levels(start_game, 1)
                    Music(1)
                    Music(2)
                if GO2_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    level_order = 2
                    Levels(start_game, 2)
                if GO3_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    level_order = 3
                    Levels(start_game, 3)
        pygame.display.update()


def Setting(start_game):
    global flag
    ST = pygame.image.load("data/Settings-screen.png")
    while True:
        SCREEN.blit(ST, (0, 0))
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()
        SETTINGS_TEXT = get_font(100).render("SETTINGS", True, "#ffe521")
        SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(640, 110))     # Text settings
        SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)
        RESUME_BUTTON = Button(image=pygame.image.load("data/Options Rect.png"), pos=(640, 230),
                               text_input="RESUME", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        LANGUAGE_BUTTON = Button(image=pygame.image.load("data/Options Rect.png"), pos=(640, 380),
                                 text_input="LANGUA", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MUSIC_BUTTON = Button(image=pygame.image.load("data/Music icon.png"), pos=(640, 500),
                              text_input=None, font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SETTINGS_BACK = Button(image=None, pos=(640, 630),
                               text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        SETTINGS_BACK.changeColor(SETTINGS_MOUSE_POS)
        SETTINGS_BACK.update(SCREEN)
        for button in [RESUME_BUTTON, SETTINGS_BACK, LANGUAGE_BUTTON, MUSIC_BUTTON]:
            button.changeColor(SETTINGS_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTINGS_BACK.checkForInput(SETTINGS_MOUSE_POS):
                    Main_menu(start_game)
                if RESUME_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    Resume(start_game)
                if LANGUAGE_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    LanSWITCH()
                if MUSIC_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    Music(flag)
            if event.type == pygame.MOUSEBUTTONUP:
                if MUSIC_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    Music(not flag)
                    flag = not flag
        pygame.display.update()


def Main_menu(start_game):
    global pause, level_order
    animation_set = [pygame.image.load(f"data/Animation/{i}.png") for i in range(0, 4)]
    i = 1
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#ffe521")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))
        PLAY_BUTTON = Button(image=pygame.image.load("data/Play Rec.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SETTINGS_BUTTON = Button(image=pygame.image.load("data/Options Rect.png"), pos=(640, 400),
                                 text_input="SETTING", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("data/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(animation_set[i // 13], (100, 600))
        i += 1
        if i == 50:
            i = 1
        for button in [PLAY_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if pause:
                        start_game(screen_size, level_order)
                        sys.exit()
                    else:
                        Play(start_game)
                        sys.exit()
                if SETTINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Setting(start_game)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

