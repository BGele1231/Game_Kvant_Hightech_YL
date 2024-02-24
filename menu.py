import pygame
import sys
from main import start_game

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("data/Background.png")   # Add menu screen


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


def get_font(size):
    return pygame.font.Font("data/font.ttf", size)  # Add font


def Music():
    pass


def LanSWINTCH():
    pass


def Levels():
    start_game()


def Resume():
    RM = pygame.image.load("data/Resume.png")
    while True:
        SCREEN.blit(RM, (0, 0))
        RESUME_MOUSE_POS = pygame.mouse.get_pos()
        RESUME_TEXT = get_font(25).render("Information", True, "Black")
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
        RESUME_RECT = RESUME_TEXT.get_rect(center=(300, 95))
        RESUME_RECT2 = RESUME_TEXT2.get_rect(center=(320, 140))
        RESUME_RECT3 = RESUME_TEXT2.get_rect(center=(320, 175))
        RESUME_RECT4 = RESUME_TEXT2.get_rect(center=(320, 205))
        RESUME_RECT5 = RESUME_TEXT2.get_rect(center=(320, 235))
        RESUME_RECT6 = RESUME_TEXT2.get_rect(center=(320, 265))
        RESUME_RECT7 = RESUME_TEXT2.get_rect(center=(320, 295))
        RESUME_RECT8 = RESUME_TEXT2.get_rect(center=(320, 325))
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
                    Setting()
        pygame.display.update()


def Play():     # start_game()
    LV = pygame.image.load("data/LevelsBG.png")
    LP = pygame.image.load("data/LevelsPlates.png")
    while True:
        SCREEN.blit(LV, (0, 0))
        SCREEN.blit(LP, (70, 35))
        SCREEN.blit(LP, (490, 35))
        SCREEN.blit(LP, (910, 35))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        LEVEL1_TEXT = get_font(30).render("Level 1", True, "White")
        LEVEL1_RECT = LEVEL1_TEXT.get_rect(center=(220, 120))
        SCREEN.blit(LEVEL1_TEXT, LEVEL1_RECT)
        LEVEL2_TEXT = get_font(30).render("Level 2", True, "White")
        LEVEL2_RECT = LEVEL2_TEXT.get_rect(center=(640, 120))
        SCREEN.blit(LEVEL2_TEXT, LEVEL2_RECT)
        LEVEL3_TEXT = get_font(30).render("Level 3", True, "White")
        LEVEL3_RECT = LEVEL3_TEXT.get_rect(center=(1060, 120))
        SCREEN.blit(LEVEL3_TEXT, LEVEL3_RECT)
        GO1_BUTTON = Button(image=None, pos=(220, 500),
                            text_input="GO", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        GO2_BUTTON = Button(image=None, pos=(640, 500),
                            text_input="GO", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        GO3_BUTTON = Button(image=None, pos=(1060, 500),
                            text_input="GO", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        PLAY_BACK = Button(image=None, pos=(640, 630),
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
                    Main_menu()
                if GO1_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    Levels()
        pygame.display.update()


def Setting():
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
                    Main_menu()
                if RESUME_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    Resume()
                if LANGUAGE_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    LanSWINTCH()
                if MUSIC_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    Music()
        pygame.display.update()


def Main_menu():
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
        for button in [PLAY_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Play()
                    sys.exit()
                if SETTINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Setting()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


Main_menu()
