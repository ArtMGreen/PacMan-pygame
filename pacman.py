import sys
import pygame

pygame.init()
pygame.key.set_repeat(0, 70)

FPS = 60
WIDTH = 1080
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):    # загрузка всех изображений
    image = pygame.image.load(name)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():    # начальный экран
    intro_text = ["PACMAN"]
    fon = pygame.transform.scale(load_image('data/fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    # мини-цикл для начального экрана
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):    # загрузка уровней
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('data/wall.png'), 'empty': load_image('data/path.png')}
player_images = {('right', 0): load_image('data/pacman.png'),
                 ('right', 1): load_image('data/pacman_closed.png'),
                 ('left', 0): load_image('data/pacman_left.png'),
                 ('left', 1): load_image('data/pacman_closed.png'),
                 ('up', 0): load_image('data/pacman_up.png'),
                 ('up', 1): load_image('data/pacman_closed.png'),
                 ('down', 0): load_image('data/pacman_down.png'),
                 ('down', 1): load_image('data/pacman_closed.png'),
                 (None, 0): load_image('data/pacman.png'),
                 (None, 1): load_image('data/pacman_closed.png')}

tile_width = tile_height = 32


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_images[('right', 0)]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.frame = 0
        self.animtime = 0

    def animate(self, direction):
        self.animtime += clock.get_time()
        if self.animtime >= 100:
            self.animtime -= 100
            self.frame = (self.frame + 1) % 2
            self.image = player_images[(direction, self.frame)]
        if direction == 'left':
            player.rect.x -= 2
        elif direction == 'right':
            player.rect.x += 2
        elif direction == 'up':
            player.rect.y -= 2
        elif direction == 'down':
            player.rect.y += 2


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


start_screen()

player, level_x, level_y = generate_level(load_level('data/map.txt'))
running = True
direction = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = 'left'
            if event.key == pygame.K_RIGHT:
                direction = 'right'
            if event.key == pygame.K_UP:
                direction = 'up'
            if event.key == pygame.K_DOWN:
                direction = 'down'
    player.animate(direction)
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)
terminate()
