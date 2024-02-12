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
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (1500, 900)
screen = pygame.display.set_mode(screen_size)
FPS = 50
OVERLAP = 30  # на сколько пикселей герой может перекрывать другие спрайты
ACCESS_ZONE = 25  # отступ для зоны доступа инструментов


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
    def __init__(self, image, dedicated_image, size, pos, time, recipes, redundant_height=0):
        super().__init__(tools_group)
        self.image = pygame.transform.scale(image, size)
        self.first_image = pygame.transform.scale(image, size)
        self.second_image = pygame.transform.scale(dedicated_image, size)
        # в действии или нет
        self.rect = pygame.Rect((*pos, *size))
        self.size = size
        self.busy = False  # занят изготовлением или нет
        self.time = time
        self.recipes = recipes  # словарь, ключ - продукт, значение - материал
        # self.mask = pygame.mask.from_surface(self.image)
        self.x = pos[0]
        self.y = pos[1]
        self.access = False  # персонаж в зоне доступа инструмента или нет
        self.state = True  # сломан или нет
        # self.add(borders)
        self.redundant_height = redundant_height
        self.access_rect = pygame.Rect((self.x - ACCESS_ZONE, self.y - ACCESS_ZONE,
                                       size[0] + ACCESS_ZONE * 2, size[1] + ACCESS_ZONE * 2))

    def making(self):
        if self.access and not self.busy:
            self.busy = True
            if hero.active_inventory in self.recipes:
                product = self.recipes[hero.active_inventory]
                # отсчёт времени до self.time
                print('Making')
                if hero.inventory1 == '':
                    hero.inventory1 = product
                elif hero.inventory2 == '':
                    hero.inventory2 = product
                return True
            return ''  # доделать ВЫВОД НА ЭКРАН, что нет свободного места
        else:
            return False

    def fixing(self, time):
        if self.access:
            hero.busy = True
            # отсчёт времени до локального time
            self.state = True


sprite_group = SpriteGroup()
tools_group = SpriteGroup()
# borders = pygame.sprite.Group()
flsun = Tools(load_image('flsun.png'), load_image('flsun_dedicated.png'), (200, 170),
             (350, 630), 2, {'PLA': '3D stuff'}, 55)
staffs = [flsun]


class Storage(Tools):
    def __init__(self, image, dedicated_image, size, pos, products, redundant_height=0):
        materials = dict()
        for k in products:
            materials[k] = ''
        super().__init__(image, dedicated_image, size, pos, 0, materials, redundant_height)


class Player(Sprite):
    def __init__(self, pos, size):
        super().__init__(hero_group)
        self.image = pygame.transform.scale(player_image, size)
        # в действии или нет
        self.busy = False
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos[0]
        self.y = pos[1]
        # self.rect.x = pos[0]
        # self.rect.y = pos[1]
        self.inventory1 = ''
        self.inventory2 = ''
        self.active_inventory = True  # True - inventory1, False - inventory2
        self.top_bottom = False

    def move(self, x, y):
        global access_tools
        access_tools = []
        for i in staffs:
            # print(x, y, self.rect.size[0], self.rect.size[1], i.x, i.y, i.size[0], i.size[1])
            if (((x > i.x + i.size[0] or i.x > x + self.rect.size[0]) or
                    (y > i.y + i.size[1] - OVERLAP)) and
                    0 <= x <= screen_size[0] - self.rect.size[0] and 0 <= y <= screen_size[1] - self.rect.size[1]):
                hero.top_bottom = False
                self.x = x
                self.y = y
                self.rect = self.image.get_rect().move(x, y)
            elif (((x > i.x + i.size[0] or i.x > x + self.rect.size[0]) or
                    (i.y + i.redundant_height > y + self.rect.size[1])) and
                  0 <= x <= screen_size[0] - self.rect.size[0] and 0 <= y <= screen_size[1] - self.rect.size[1]):
                hero.top_bottom = True
                self.x = x
                self.y = y
                self.rect = self.image.get_rect().move(x, y)
            middle_x = (x + self.rect.size[0]) // 2
            middle_y = (y + self.rect.size[1]) // 2

            if i.access_rect.colliderect(self.rect):
                access_tools.append(i)
                i.access = True
                i.image = i.second_image
            else:
                i.image = i.first_image
                i.access = False


access_tools = []
player_image = load_image('character_front.png')
player_image_lateral = load_image('character_lateral.png')
player_image_back = load_image('character_back.png')
player_size = (120, 150)
hero_group = SpriteGroup()
hero = Player((0, 0), player_size)


def terminate():
    pygame.quit()
    sys.exit





def start_screen():
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
    for j in access_tools:
        if j.making():
            break
        print('check')


clock = pygame.time.Clock()
start_screen()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    screen.fill(pygame.Color("black"))
    screen.blit(pygame.transform.scale(load_image('Sprite-floor.png'), screen_size), (0, 0))
    if hero.top_bottom:
        hero_group.draw(screen)
        tools_group.draw(screen)
    else:
        tools_group.draw(screen)
        hero_group.draw(screen)
    # sprite_group.draw(screen)
    # pygame.draw.rect(screen, (255, 255, 255), test.access_rect)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
