import pygame
import sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("data/Background.png")   # Add menu screen


def get_font(size):
    return pygame.font.Font("data/", size)  # Add font


def Play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()


def Options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 460))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    Main_menu()

        pygame.display.update()


def Main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        PLAY_BUTTON = Button()
        OPTIONS_BUTTON = Button()
        QUIT_BUTTON = Button()
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


Main_menu()
