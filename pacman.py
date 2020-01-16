import sys
import pygame
from random import choice


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
points_group = pygame.sprite.Group()

up_borders = pygame.sprite.Group()
down_borders = pygame.sprite.Group()
left_borders = pygame.sprite.Group()
right_borders = pygame.sprite.Group()


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
ghost_images = {'grey': load_image('data/grey_monster.png'),
                'pink': load_image('data/pink_monster.png'),
                'red': load_image('data/red_monster.png'),
                'blue': load_image('data/blue_monster.png')}

tile_width = tile_height = 32


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            Border(tile_width * pos_x, tile_height * pos_y - 1, tile_width * pos_x + 31, tile_height * pos_y - 1, up_borders)
            Border(tile_width * pos_x, tile_height * pos_y + 32, tile_width * pos_x + 31, tile_height * pos_y + 32, down_borders)
            Border(tile_width * pos_x + 32, tile_height * pos_y, tile_width * pos_x + 32, tile_height * pos_y + 31, right_borders)
            Border(tile_width * pos_x - 1, tile_height * pos_y, tile_width * pos_x - 1, tile_height * pos_y + 31, left_borders)
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type):
        super().__init__(player_group, all_sprites)
        self.image = ghost_images[type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.direction = None

    def able_to_move(self, direction):
        if (((pygame.sprite.spritecollideany(self, up_borders) and direction == 'down') or
             (pygame.sprite.spritecollideany(self, down_borders) and direction == 'up') or
             (pygame.sprite.spritecollideany(self, left_borders) and direction == 'right') or
             (pygame.sprite.spritecollideany(self, right_borders) and direction == 'left'))):
            return False
        return True

    def move(self):
        if self.direction == 'left':
            self.rect.x -= 1
        elif self.direction == 'right':
            self.rect.x += 1
        elif self.direction == 'up':
            self.rect.y -= 1
        elif self.direction == 'down':
            self.rect.y += 1

    def find_direction(self):
        if self.rect.x < player.rect.x and self.able_to_move('right'):
            self.direction = 'right'
        if self.rect.x > player.rect.x and self.able_to_move('left'):
            self.direction = 'left'
        if self.rect.y < player.rect.y and self.able_to_move('down'):
            self.direction = 'down'
        if self.rect.y > player.rect.y and self.able_to_move('up'):
            self.direction = 'up'
        else:
            directions = ['up', 'down', 'right', 'left']
            for direction in directions:
                if not self.able_to_move(direction):
                    directions.remove(direction)
            self.direction = choice(directions)


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

    def able_to_move(self, direction):
        if (((pygame.sprite.spritecollideany(self, up_borders) and direction == 'down') or
             (pygame.sprite.spritecollideany(self, down_borders) and direction == 'up') or
             (pygame.sprite.spritecollideany(self, left_borders) and direction == 'right') or
             (pygame.sprite.spritecollideany(self, right_borders) and direction == 'left'))):
            return False
        return True

    def move(self, direction):
        if direction == 'left':
            self.rect.x -= 2
        elif direction == 'right':
            self.rect.x += 2
        elif direction == 'up':
            self.rect.y -= 2
        elif direction == 'down':
            self.rect.y += 2
        if pygame.sprite.spritecollideany(self, points_group):
            pygame.sprite.spritecollideany(self, points_group).kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, group):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Point(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(points_group, all_sprites)
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("pink"), (3, 3), 3)
        self.rect = pygame.Rect(tile_width * pos_x + 12, tile_height * pos_y + 12, 6, 6)


def generate_level(level):
    new_player, x, y, ghosts = None, None, None, [None] * 4
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
                Point(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'R':
                Tile('empty', x, y)
                red = Ghost(x, y, 'red')
            elif level[y][x] == 'G':
                Tile('empty', x, y)
                grey = Ghost(x, y, 'grey')
            elif level[y][x] == 'P':
                Tile('empty', x, y)
                pink = Ghost(x, y, 'pink')
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                blue = Ghost(x, y, 'blue')
    return new_player, x, y, [red, grey, pink, blue]


start_screen()

player, level_x, level_y, ghosts = generate_level(load_level('data/map.txt'))
running = True
direction = None
next_direction = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                next_direction = 'left'
            if event.key == pygame.K_RIGHT:
                next_direction = 'right'
            if event.key == pygame.K_UP:
                next_direction = 'up'
            if event.key == pygame.K_DOWN:
                next_direction = 'down'
    if player.able_to_move(next_direction):
        direction = next_direction
    player.animate(direction)
    if player.able_to_move(direction):
        player.move(direction)
    for ghost in ghosts:
        if not ghost.able_to_move(ghost.direction) or ghost.direction is None:
            ghost.find_direction()
        ghost.move()
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    points_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    if not bool(points_group):
        break
    clock.tick(60)
terminate()
