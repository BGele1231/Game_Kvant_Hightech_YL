import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


FPS = 50
OVERLAP = 60  # на сколько пикселей герой может перекрывать другие спрайты
ACCESS_ZONE = 10  # отступ для зоны доступа инструментов
PLAYER_CONST = 7  # отступ внутрь прямоугольника для пересечений access_rect


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tools(Sprite):
    def __init__(self, image, dedicated_image, size, pos, time, recipes, access_sides, redundant_height=0):
        super().__init__(tools_group)
        self.image = pygame.transform.scale(image, size)
        self.first_image = pygame.transform.scale(image, size)  # обычное изображение
        self.second_image = pygame.transform.scale(dedicated_image, size)  # с обводкой
        self.rect = pygame.Rect((*pos, *size))
        self.size = size
        self.busy = False  # занят изготовлением или нет
        self.time = time
        self.recipes = recipes  # словарь, ключ - материал, значение - продукт
        self.x = pos[0]
        self.y = pos[1]
        self.access = False  # персонаж в зоне доступа инструмента или нет
        self.state = True  # сломан или нет
        self.redundant_height = redundant_height

        x_ac, y_ac, x_ac_size, y_ac_size = self.x, self.y + redundant_height, size[0], size[1] - OVERLAP
        if 'top' in access_sides:
            y_ac = self.y - ACCESS_ZONE + redundant_height
            if 'bottom' in access_sides:
                y_ac_size = size[1] + ACCESS_ZONE * 2 - OVERLAP
            else:
                y_ac_size = size[1] + ACCESS_ZONE - OVERLAP
        else:
            if 'bottom' in access_sides:
                y_ac_size = size[1] + ACCESS_ZONE - OVERLAP
        if 'left' in access_sides:
            x_ac = self.x - ACCESS_ZONE
            if 'right' in access_sides:
                x_ac_size = size[0] + ACCESS_ZONE * 2
            else:
                x_ac_size = size[0] + ACCESS_ZONE
        else:
            if 'bottom' in access_sides:
                x_ac_size = size[0] + ACCESS_ZONE
        self.access_rect = pygame.Rect(x_ac, y_ac, x_ac_size, y_ac_size)

    def making(self):
        if not self.state:
            return "it's broken"
        if not self.busy:
            self.busy = True
            if hero.active_inventory and hero.inventory1 in self.recipes.keys():
                product = self.recipes[hero.inventory1]
                hero.inventory1 = product
                return False
            elif not hero.active_inventory and hero.inventory2 in self.recipes.keys():
                product = self.recipes[hero.inventory2]
                hero.inventory2 = product
                return False
            # отсчёт времени до self.time
            # изменить после таймера self.busy
            print('Making')
            return "I can't take more/I am shorthanded"  # доделать ВЫВОД НА ЭКРАН, что нет свободного места
        else:
            return "it works"

    def fixing(self, time):
        if self.access:
            hero.busy = True
            # отсчёт времени до локального time
            self.state = True


class Storage(Tools):
    def __init__(self, image, dedicated_image, size, pos, product, access_sides, redundant_height=0):
        super().__init__(image, dedicated_image, size, pos, 0, {'': product}, access_sides, redundant_height)

    def making(self):
        # где-то тут выбор точного материала
        if hero.active_inventory and hero.inventory1 == '':
            product = self.recipes.get(hero.inventory1)
            hero.inventory1 = product
            return False
        elif not hero.active_inventory and hero.inventory2 == '':
            product = self.recipes.get(hero.inventory2)
            hero.inventory2 = product
            return False
        return "I can't take more/I am shorthanded"  # доделать ВЫВОД НА ЭКРАН, что нет свободного места


class Player(Sprite):
    def __init__(self, pos, size):
        super().__init__(hero_group)
        self.image = pygame.transform.scale(player_image, size)
        self.size = size
        self.busy = False  # в действии или нет
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos[0]
        self.y = pos[1]
        self.inventory1 = ''
        self.inventory2 = ''
        self.active_inventory = True  # True - inventory1, False - inventory2
        # self.top_bottom = False
        self.access_rect = pygame.Rect(self.x + PLAYER_CONST, self.y + PLAYER_CONST,
                                      size[0] - PLAYER_CONST, size[1] - PLAYER_CONST)

    def move(self, x, y):
        global access_tools
        access_tools = []
        flag = False
        for i in staffs:
            # print(x, y, self.rect.size[0], self.rect.size[1], i.x, i.y, i.size[0], i.size[1])
            if (((x > i.x + i.size[0] or i.x > x + self.rect.size[0]) or
                 ((y > i.y + i.size[1] - OVERLAP) or (i.y + i.redundant_height > y + self.rect.size[1]))) and
                    0 <= x <= screen_size[0] - self.rect.size[0] and
                    0 <= y <= screen_size[1] - self.rect.size[1]):
                # hero.top_bottom = False
                flag = True
            else:
                flag = False
                break
        if flag:
            self.x = x
            self.y = y
            self.rect = self.image.get_rect().move(x, y)
            self.access_rect = pygame.Rect((x + PLAYER_CONST, y + PLAYER_CONST),
                                           (self.size[0] - PLAYER_CONST, self.size[1] - PLAYER_CONST))

        for i in staffs:
            if i.access_rect.colliderect(self.access_rect):
                access_tools.append(i)
                i.access = True
                i.image = i.second_image
            else:
                i.image = i.first_image
                i.access = False





def start_screen(screen_size):
    intro_text = ["     Kvant HighTech", "",
                  "     Использовать английскую раскладку"]

    fon = pygame.transform.scale(load_image('Sprite-floor.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)





def up_down_left_right(movement, n):
    x, y = hero.x, hero.y
    if movement == "up":
        hero.move(x, y - n)
        hero.image = pygame.transform.scale(player_image_back, player_size)
    elif movement == "down":
        hero.move(x, y + n)
        hero.image = pygame.transform.scale(player_image, player_size)
    elif movement == "left":
        hero.move(x - n, y)
        hero.image = pygame.transform.flip(pygame.transform.scale(player_image_lateral, player_size), True, False)
    elif movement == "right":
        hero.move(x + n, y)
        hero.image = pygame.transform.scale(player_image_lateral, player_size)
    elif movement == "up_left":
        hero.move(x - n, y - n)
        hero.image = pygame.transform.flip(pygame.transform.scale(player_image_lateral, player_size), True, False)
    elif movement == "up_right":
        hero.move(x + n, y - n)
        hero.image = pygame.transform.scale(player_image_lateral, player_size)
    elif movement == "down_left":
        hero.move(x - n, y + n)
        hero.image = pygame.transform.flip(pygame.transform.scale(player_image_lateral, player_size), True, False)
    elif movement == "down_right":
        hero.move(x + n, y + n)
        hero.image = pygame.transform.scale(player_image_lateral, player_size)


def move(hero, movement, shift):
    if shift:
        up_down_left_right(movement, 5)
    else:
        up_down_left_right(movement, 3)


def choosing_tools():
    print(access_tools)
    # for j in access_tools:
    k = access_tools[0].making()
    if k:
        pass
        # доделать ВЫВОД НА ЭКРАН, k будет сообщением


def terminate():
    pygame.quit()
    sys.exit


def start_game(screen_size):
    start_screen(screen_size)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                hero.active_inventory = not hero.active_inventory
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            shift = True
        else:
            shift = False
        if keys[pygame.K_w]:
            if keys[pygame.K_a]:
                move(hero, "up_left", shift)
            elif keys[pygame.K_d]:
                move(hero, "up_right", shift)
            else:
                move(hero, "up", shift)
        elif keys[pygame.K_s]:
            if keys[pygame.K_a]:
                move(hero, "down_left", shift)
            elif keys[pygame.K_d]:
                move(hero, "down_right", shift)
            else:
                move(hero, "down", shift)
        elif keys[pygame.K_a]:
            move(hero, "left", shift)
        elif keys[pygame.K_d]:
            move(hero, "right", shift)
        if keys[pygame.K_f]:
            choosing_tools()
        if keys[pygame.K_1]:
            hero.active_inventory = True
        elif keys[pygame.K_2]:
            hero.active_inventory = False

        if keys[pygame.K_TAB]:
            print(hero.inventory1, hero.inventory2)

        screen.fill(pygame.Color("black"))
        screen.blit(pygame.transform.scale(load_image('Sprite-floor.png'), screen_size), (0, 0))
        if hero.y <= middle_coordinates:
            top_tools.draw(screen)
            hero_group.draw(screen)
            workbench_group.draw(screen)
            bottom_tools.draw(screen)
            side_tools.draw(screen)
        else:
            top_tools.draw(screen)
            workbench_group.draw(screen)
            side_tools.draw(screen)
            hero_group.draw(screen)
            bottom_tools.draw(screen)

        # hero_group.draw(screen)
        pygame.draw.rect(screen, (255, 255, 255), hero.access_rect)
        # pygame.draw.rect(screen, (44, 44, 44), flsun.access_rect)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


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


def Play():
    start_game((1400, 800))


def Options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 460))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

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
        PLAY_BUTTON = Button(image=pygame.image.load("data/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("data/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("data/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
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
                    sys.exit()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()

    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")

    BG = pygame.image.load("data/Background.png")  # Add menu screen

    pygame.init()
    screen_size = (1280, 720)
    screen = pygame.display.set_mode(screen_size)

    sprite_group = SpriteGroup()
    tools_group = SpriteGroup()
    flsun = Tools(load_image('test.png'), load_image('flsun_dedicated.png'), (190, 160),
                  (333, 558), 2, {'PLA': '3D stuff'}, "top", 55)
    wanhao = Tools(load_image('wanhao.png'), load_image('wanhao_dedicated.png'), (190, 160),
                   (530, 558), 2, {'PLA': '3D stuff'}, "top", 55)
    her = Tools(load_image('her.png'), load_image('her_dedicated.png'), (200, 190),
                (725, 529), 2, {'PLA': '3D stuff'}, "top", 55)
    garbage = Tools(load_image('garbage.png'), load_image('garbage_dedicated.png'), (130, 170),
                    (935, 539), 2, {'PLA': '3D stuff'}, "top", 55)
    soldering = Tools(load_image('soldering.png'), load_image('soldering_dedicated.png'), (140, 235),
                      (8, 480), 2, {'PLA': '3D stuff'}, "left right", 55)
    sandpaper = Tools(load_image('sandpaper.png'), load_image('sandpaper_dedicated.png'), (130, 180),
                      (21, 280), 2, {'PLA': '3D stuff'}, "left right", 55)
    painting = Tools(load_image('painting.png'), load_image('painting_dedicated.png'), (220, 220),
                     (30, 0), 2, {'PLA': '3D stuff'}, "top bottom", 55)
    trotec = Tools(load_image('trotec.png'), load_image('trotec_dedicated.png'), (230, 170),
                   (270, 50), 2, {'PLA': '3D stuff'}, "top bottom", 55)
    trotec_2 = Tools(load_image('trotec.png'), load_image('trotec_dedicated.png'), (230, 170),
                     (520, 50), 2, {'PLA': '3D stuff'}, "top bottom", 55)
    rack = Tools(load_image('rack.png'), load_image('rack_dedicated.png'), (110, 200),
                 (890, 40), 2, {'PLA': '3D stuff'}, "top bottom", 55)
    buld = Tools(load_image('buld.png'), load_image('buld_dedicated.png'), (260, 170),
                 (990, 70), 2, {'PLA': '3D stuff'}, "top bottom", 55)
    workbench = Tools(load_image('workbench.png'), load_image('workbench_dedicated.png'), (472, 232),
                      (350, 300), 1, {'smth': 'good_smth'}, "left right", 50)
    middle_coordinates = (workbench.y + workbench.size[1]) // 2
    staffs = [workbench, flsun, wanhao, her, garbage, soldering, sandpaper, trotec, trotec_2, buld, rack]
    workbench_group = SpriteGroup()
    bottom_tools = SpriteGroup()
    bottom_tools.add(flsun)
    bottom_tools.add(workbench)
    bottom_tools.add(rack)
    bottom_tools.add(buld)
    bottom_tools.add(trotec_2)
    bottom_tools.add(soldering)
    bottom_tools.add(trotec)

    bottom_tools.add(wanhao)
    bottom_tools.add(sandpaper)
    bottom_tools.add(her)
    bottom_tools.add(garbage)
    top_tools = SpriteGroup()
    side_tools = SpriteGroup()

    access_tools = []
    player_image = load_image('character_front.png')
    player_image_lateral = load_image('character_lateral.png')
    player_image_back = load_image('character_back.png')
    player_size = (100, 130)
    hero_group = SpriteGroup()
    hero = Player((0, 0), player_size)

    clock = pygame.time.Clock()

    Main_menu()