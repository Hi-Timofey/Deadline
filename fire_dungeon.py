import pygame
from pygame import *
from utils import *
from camera import Camera
from blocks import Platform, BlockDie, Door, ClosedDoor
from player import Player
from create_level import create_level
from fire import Fire, show_matrix


BACKGROUND_COLOR = "#000000"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
FIRE_START = [2, 1]


class FireDungeon():

    def __init__(self, level, player, game_width, game_height,
                 game_over_func=None, gravity=False):
        self.timer = pygame.time.Clock()
        self.entities = pygame.sprite.Group()  # Все объекты
        self.run = True
        self.paused = False
        # Window size
        self.WIN_SIZE = self.WIN_WIDTH, self.WIN_HEIGHT = game_width, game_height
        # Группируем ширину и высоту в одну переменную
        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
        # Game
        self.level = level
        self.fire_counter = 0
        self.game_over_func = game_over_func
        self.platforms = []
        self.seed = 0
        self.x = self.y = 0  # координаты
        self.player = player
        self.entities.add(self.player)
        # Высчитываем фактическую ширину уровня
        self.total_level_width = len(self.level[0]) * PLATFORM_WIDTH
        self.total_level_height = len(self.level) * PLATFORM_HEIGHT  # высоту
        # Camera for player
        self.camera = Camera(
            self._camera_configure,
            self.total_level_width,
            self.total_level_height)

    def run_game(self, gravity):
        '''
            Main cycle of the game.
        '''
        # Initialize pygame for this level
        self.screen = pygame.display.set_mode(self.WIN_SIZE)
        pygame.display.set_caption("Fire Dungeon")
        bg = Surface(self.WIN_SIZE)
        bg.fill(Color(BACKGROUND_COLOR))

        # Directions of the player
        left = right = False
        up = False
        down = gravity
        self.level[FIRE_START[0]][FIRE_START[1]] = "!"
        # Image for platforms
        # все анимированные объекты, за исключением героя
        animatedEntities = pygame.sprite.Group()
        for row in self.level:  # вся строка
            for col in row:  # каждый символ
                self.seed += 1
                if col == "#":
                    pf = Platform(self.x, self.y)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                if col == "!":
                    bd = BlockDie(self.x, self.y)
                    self.entities.add(bd)
                    self.platforms.append(bd)
                if col == "C":
                    pf = ClosedDoor(self.x, self.y)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                if col == "E":
                    pf = Door(self.x, self.y)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                self.x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            self.y += PLATFORM_HEIGHT  # то же самое и с высотой
            self.x = 0  # на каждой новой строчке начинаем с нуля

        running = False
        self.fire_list_coords = [FIRE_START]

        exit_code = 0
        while self.run:  # Основной цикл программы
            self.timer.tick(60)
            self._fire_cycle()

            for e in pygame.event.get():  # Обрабатываем события
                if e.type == QUIT:
                    self.run = False
                # Player died
                if not self.player.life:
                    self.run = False
                    exit_code = 2

                # Player ended this level
                if self.player.end:
                    self.run = False
                    exit_code = 3

                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    print('escape')
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False

                if e.type == KEYDOWN and e.key == K_LSHIFT:
                    running = True
                if e.type == KEYUP and e.key == K_LSHIFT:
                    running = False

            # First - backgorund drawing
            self.screen.blit(bg, (0, 0))

            # Next - drawing objects
            animatedEntities.update()
            self.entities.update(
                left, right, up, down, self.platforms, running)
            self.player.update(
                left, right, up, down, self.platforms, running)

            # Centralize camera on player
            self.camera.update(self.player)
            for e in self.entities:
                self.screen.blit(e.image, self.camera.apply(e))

            pygame.display.update()
        if self.game_over_func is not None:
            self.game_over_func()

        # 2 - died ; 3 - finished
        return exit_code

    def _fire_cycle(self):
        self.fire_counter += 1
        self.y = 0
        if self.fire_counter == 120:
            print(self.fire_list_coords)
            for y_new, x_new in self.fire_list_coords:
                f = Fire(x_new, y_new)
                f.update(self.level, self.fire_list_coords)
                print()
                print(self.fire_list_coords)
            self.fire_counter = 0
            for row in self.level:  # вся строка
                for col in row:  # каждый символ
                    self.seed += 1
                    if col == "!":
                        bd = BlockDie(self.x, self.y)
                        self.entities.add(bd)
                        self.platforms.append(bd)
                    self.x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
                self.y += PLATFORM_HEIGHT  # то же самое и с высотой
                self.x = 0  # на каждой новой строчке начинаем с нуля

    def _camera_configure(self, camera, target_rect):
        '''
            Creating Rect for moving camera
        '''
        left, top, _, _ = target_rect
        _, _, width, height = camera
        left, top = -left + self.WIN_WIDTH / 2, -top + self.WIN_HEIGHT / 2

        # Left walls
        left = min(0, left)

        # Right walls
        left = max(-(camera.width - self.WIN_WIDTH), left)

        # Top walls
        top = max(-(camera.height - self.WIN_HEIGHT), top)
        top = min(0, top)

        return Rect(left, top, width, height)


if __name__ == "__main__":
    gravity = False
    pl = Player(65, 64, gravity)
    level = create_level(31, 31, 1)
    fd = FireDungeon(level, pl, 800, 800)
    result = fd.run_game(gravity=False)
    if result == 2:
        print('-' * 10, 'DIED', '-' * 10)
    if result == 3:
        print('-' * 10, 'COMPLETED', '-' * 10)
