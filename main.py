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
screen_size = (1400, 800)
screen = pygame.display.set_mode(screen_size)
FPS = 50

player_image = load_image('mar.png')


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
    def __init__(self, image, size, pos, time, material, product):
        super().__init__(tools_group)
        self.image = pygame.transform.scale(image, size)
        # в действии или нет
        self.rect = self.image.get_rect()
        self.busy = False
        self.time = time
        self.materials = material
        self.product = product
        # self.mask = pygame.mask.from_surface(self.image)
        self.x = pos[0]
        self.y = pos[1]
        self.state = True
        self.add(borders)

    def making(self):
        self.busy = True
        # отсчёт времени до self.time


    def fixing(self, time):
        hero.busy = True
        # отсчёт времени до локального time
        self.state = True


tools_group = SpriteGroup()
borders = pygame.sprite.Group()
test = Tools(load_image('test.jpg'), (100, 70), (100, 100), 2, ['PLA'], ['3D stuff'])
staffs = [test]


class Player(Sprite):
    def __init__(self, pos):
        super().__init__(hero_group)
        self.image = player_image
        # в действии или нет
        self.busy = False
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        # self.rect.x = pos[0]
        # self.rect.y = pos[1]
        self.stop = False
        self.last_movement = ''

    def move(self, x, y):
        print(bool(pygame.sprite.spritecollideany(self, borders)), hero.last_movement, self.pos_x, self.pos_x, x, y)
        if not pygame.sprite.spritecollideany(self, borders):
            self.pos_x = x
            self.pos_y = y
            self.rect = self.image.get_rect().move(x, y)
            self.stop = False
        else:

            if (hero.last_movement == 'up' and self.pos_y < y) or (hero.last_movement == 'down' and self.pos_y > y):
                self.pos_x = x
                self.pos_y = y
            if ((hero.last_movement == 'left' and self.pos_x < x) or
                    (hero.last_movement == 'right' and self.pos_x > x)):
                self.pos_x = x
                self.pos_y = y
            self.rect = self.image.get_rect().move(x, y)
            self.stop = True


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    intro_text = ["     Kvant HighTech", "",
                  "     Герой двигается",
                  "     Карта на месте"]

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


def up_dowm_left_right(movement, n, x, y):
    if movement == "up":
        hero.move(x, y - n)
    elif movement == "down":
        hero.move(x, y + n)
    elif movement == "left":
        hero.move(x - n, y)
    elif movement == "right":
        hero.move(x + n, y)
    hero.last_movement = movement


def move(hero, movement, shift):
    x, y = hero.pos_x, hero.pos_y
    if shift:
        up_dowm_left_right(movement, 4, x, y)
    else:
        up_dowm_left_right(movement, 3, x, y)


def placements(tool):
    tool.rect = tool.image.get_rect().move(
        tool.x, tool.y)


hero = Player((0, 0))
start_screen()
for j in staffs:
    placements(j)
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
        move(hero, "up", shift)
    elif keys[pygame.K_s]:
        move(hero, "down", shift)
    elif keys[pygame.K_a]:
        move(hero, "left", shift)
    elif keys[pygame.K_d]:
        move(hero, "right", shift)

    screen.fill(pygame.Color("black"))
    screen.blit(pygame.transform.scale(load_image('Sprite-floor.png'), screen_size), (0, 0))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    tools_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
