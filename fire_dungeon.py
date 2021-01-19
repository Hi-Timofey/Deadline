import pygame
from pygame import *
from utils import *
from camera import Camera
from blocks import Platform
from player import Player


# Window size
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 600

# Группируем ширину и высоту в одну переменную
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


def camera_configure(camera, target_rect):
    '''
        Creating Rect for moving camera
    '''
    left, top, _, _ = target_rect
    _, _, width, height = camera
    left, top = -left+WIN_WIDTH / 2, -top+WIN_HEIGHT / 2

    # Left walls
    left = min(0, left)

    # Right walls
    left = max(-(camera.width-WIN_WIDTH), left)

    # Top walls
    top = max(-(camera.height-WIN_HEIGHT), top)
    top = min(0, top)

    return Rect(left, top, width, height)


class FireDungeon():

    def __init__(self):
        self.timer = pygame.time.Clock()
        self.entities = pygame.sprite.Group()  # Все объекты
        self.run = True

    def run_game(self, gravity):
        '''
            Main cycle of the game.
        '''
        # Initialize pygame for this level
        screen = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption("Fire Dungeon")
        bg = Surface(WIN_SIZE)
        bg.fill(Color(BACKGROUND_COLOR))

        # Default - player is NOT moving anywhere
        self.player = Player(55, 55, gravity)
        # Directions of the player
        left = right = False
        up = False
        down = gravity

        # Level generating
        platforms = []
        self.entities.add(self.player)
        level = [
            "----------------------------------",
            "-                                -",
            "-                       --       -",
            "--                               -",
            "-            --                  -",
            "-    -       -                   -",
            "--                               -",
            "-                                -",
            "-                   ----     --- -",
            "-                                -",
            "--       -   -                   -",
            "-    -                           -",
            "-                            --- -",
            "-                                -",
            "-                                -",
            "-      ---                       -",
            "-                                -",
            "-   -------         ----         -",
            "-                                -",
            "-                         -      -",
            "-                            --  -",
            "-                                -",
            "-                                -",
            "----------------------------------"]

        # Image for platforms
        platform_img = image.load(
            get_data_path(
                "wall_64x64_1.png",
                'img')).convert()

        x = y = 0  # координаты
        seed = 0
        for row in level:  # вся строка
            for col in row:  # каждый символ
                seed += 1
                if col == "-":
                    pf = Platform(x, y, platform_img)
                    self.entities.add(pf)
                    platforms.append(pf)
                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        # Высчитываем фактическую ширину уровня
        total_level_width = len(level[0]) * PLATFORM_WIDTH
        total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
        running = False
        camera = Camera(
            camera_configure,
            total_level_width,
            total_level_height)

        while self.run:  # Основной цикл программы
            self.timer.tick(60)
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == QUIT:
                    self.run = False

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
            screen.blit(bg, (0, 0))

            # Next - drawing objects
            self.entities.update(left, right, up, down, platforms, running)
            self.player.update(
                left, right, up, down, platforms,running)

            # Centralize camera on player
            camera.update(self.player)
            for e in self.entities:
                screen.blit(e.image, camera.apply(e))

            pygame.display.update()
        return self.run


if __name__ == "__main__":
    fd = FireDungeon()
    fd.run_game(gravity=False)
