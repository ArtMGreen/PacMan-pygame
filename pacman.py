import sys
import pygame
from random import choice


pygame.init()
pygame.key.set_repeat(0, 70)

FPS = 60
WIDTH = 1080
HEIGHT = 720
tile_width = tile_height = 32
powerful_AI = 0
player_speed = 1
ghost_speed = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

lobster_pacman = pygame.font.Font('data/lobster.ttf', 120)
lobster_big = pygame.font.Font('data/lobster.ttf', 70)
lobster_medium = pygame.font.Font('data/lobster.ttf', 50)
lobster_small = pygame.font.Font('data/lobster.ttf', 30)

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
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
    while True:
        # Выводим изображение на экран
        fon = pygame.transform.scale(load_image('data/fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        # Выводим "PACMAN" на экран
        string = lobster_pacman.render('PACMAN', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 295, 70
        screen.blit(string, rect_str)
        # Выводим кнопку помощи на экран
        string = lobster_big.render('Help', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 350, 350
        screen.blit(string, rect_str)
        # Выводим кнопку настроек на экран
        string = lobster_big.render('Settings', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 500, 350
        screen.blit(string, rect_str)
        # Выводим кнопку старта игры на экран
        string = lobster_big.render('Play', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 470, 450
        screen.blit(string, rect_str)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 475 >= event.pos[0] >= 350 and 435 >= event.pos[1] >= 350:
                    help_screen()
                elif 723 >= event.pos[0] >= 500 and 435 >= event.pos[1] >= 350:
                    settings_screen()
                elif 605 >= event.pos[0] >= 470 and 535 >= event.pos[1] >= 450:
                    return    # начинаем игру
        pygame.display.flip()


def help_screen():
    while True:
        # Выводим изображение на экран
        fon = pygame.transform.scale(load_image('data/fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        # Выводим информацию об управлении на экран
        string = lobster_medium.render('Control is performed using arrow keys', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 70, 100
        screen.blit(string, rect_str)
        # Копирайтики, имя-фамилия и контакты :)
        string = lobster_small.render('© Артем (ArtMGreen) Матевосян', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 70, 400
        screen.blit(string, rect_str)
        string = lobster_small.render('Official PacMan website: pacman.com', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 70, 450
        screen.blit(string, rect_str)
        string = lobster_small.render('github.com/ArtMGreen', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 70, 550
        screen.blit(string, rect_str)
        string = lobster_small.render('vk.com/artmgreen', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 70, 600
        screen.blit(string, rect_str)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def settings_screen():
    global powerful_AI, player_speed, ghost_speed
    y_list = [100, 300, 500]
    list_of_parameters = ["AI", "Player's speed", "Ghosts' speed"]
    while True:
        # Выводим изображение на экран
        fon = pygame.transform.scale(load_image('data/fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        # Выводим названия настроек
        for count in range(3):
            string = lobster_big.render(list_of_parameters[count], 1, (0, 0, 0), (255, 255, 255))
            rect_str = string.get_rect()
            rect_str.x, rect_str.y = 70, y_list[count]
            screen.blit(string, rect_str)
        # Разнообразные перекдючатели настроек
        if powerful_AI:
            string = lobster_big.render('Smart', 1, (0, 0, 0), (255, 255, 255))
            rect_str = string.get_rect()
            rect_str.x, rect_str.y = 170, 100
            screen.blit(string, rect_str)
        else:
            string = lobster_big.render('Original', 1, (0, 0, 0), (255, 255, 255))
            rect_str = string.get_rect()
            rect_str.x, rect_str.y = 170, 100
            screen.blit(string, rect_str)
        string = lobster_big.render(str(player_speed), 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 490, 300
        screen.blit(string, rect_str)
        string = lobster_big.render(str(ghost_speed), 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 460, 500
        screen.blit(string, rect_str)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 415 >= event.pos[0] >= 170 and 185 >= event.pos[1] >= 100:
                    powerful_AI = (powerful_AI + 1) % 2
                elif 528 >= event.pos[0] >= 490 and 385 >= event.pos[1] >= 300:
                    player_speed = (player_speed + 1) % 3
                elif 498 >= event.pos[0] >= 460 and 585 >= event.pos[1] >= 500:
                    ghost_speed = (ghost_speed + 1) % 2
                else:
                    return
        pygame.display.flip()


def winning_screen():
    while True:
        # Выводим изображение на экран
        fon = pygame.transform.scale(load_image('data/fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        # Выводим информацию об управлении на экран
        string = lobster_pacman.render('You won!', 1, (0, 0, 0), (255, 255, 255))
        rect_str = string.get_rect()
        rect_str.x, rect_str.y = 300, 200
        screen.blit(string, rect_str)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


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
        super().__init__(ghost_group, all_sprites)
        self.image = ghost_images[type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = None
        self.AI_count = 0

    def able_to_move(self, direction):
        if (((pygame.sprite.spritecollideany(self, up_borders) and direction == 'down') or
             (pygame.sprite.spritecollideany(self, down_borders) and direction == 'up') or
             (pygame.sprite.spritecollideany(self, left_borders) and direction == 'right') or
             (pygame.sprite.spritecollideany(self, right_borders) and direction == 'left'))):
            return False
        return True

    def move(self):
        if self.direction == 'left':
            self.rect.x -= 2 ** ghost_speed
        if self.direction == 'right':
            self.rect.x += 2 ** ghost_speed
        if self.direction == 'up':
            self.rect.y -= 2 ** ghost_speed
        if self.direction == 'down':
            self.rect.y += 2 ** ghost_speed
        if powerful_AI:
            self.AI_count += 2 ** ghost_speed

    def find_direction(self):
        self.AI_count = 0
        if self.rect.x < player.rect.x and self.able_to_move('right'):
            self.direction = 'right'
        elif self.rect.x > player.rect.x and self.able_to_move('left'):
            self.direction = 'left'
        elif self.rect.y < player.rect.y and self.able_to_move('down'):
            self.direction = 'down'
        elif self.rect.y > player.rect.y and self.able_to_move('up'):
            self.direction = 'up'
        else:
            directions = ['up', 'down', 'right', 'left']
            self.direction = choice([d for d in directions if self.able_to_move(d)])


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_images[('right', 0)]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.frame = 0
        self.animtime = 0

    def animate(self, direction):
        self.animtime += clock.get_time()
        if self.animtime >= 100:
            self.animtime = 0
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
            self.rect.x -= 2 ** player_speed
        elif direction == 'right':
            self.rect.x += 2 ** player_speed
        elif direction == 'up':
            self.rect.y -= 2 ** player_speed
        elif direction == 'down':
            self.rect.y += 2 ** player_speed
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
    new_player, x, y, ghosts = None, None, None, []
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
                ghosts.append(red)
            elif level[y][x] == 'G':
                Tile('empty', x, y)
                grey = Ghost(x, y, 'grey')
                ghosts.append(grey)
            elif level[y][x] == 'P':
                Tile('empty', x, y)
                pink = Ghost(x, y, 'pink')
                ghosts.append(pink)
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                blue = Ghost(x, y, 'blue')
                ghosts.append(blue)
    return new_player, x, y, ghosts


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
        if not ghost.able_to_move(ghost.direction) or ghost.direction is None or ghost.AI_count == 32:
            ghost.find_direction()
        ghost.move()
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    points_group.draw(screen)
    player_group.draw(screen)
    ghost_group.draw(screen)
    pygame.display.flip()
    if not bool(points_group):
        winning_screen()
        break
    if ((pygame.sprite.collide_mask(player, ghosts[0]) or
         pygame.sprite.collide_mask(player, ghosts[1]) or
         pygame.sprite.collide_mask(player, ghosts[2]) or
         pygame.sprite.collide_mask(player, ghosts[3]))):
        break
    clock.tick(60)
terminate()
