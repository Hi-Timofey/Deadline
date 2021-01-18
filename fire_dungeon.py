import pygame
from pygame import *
from utils import *
from camera import Camera

# Объявляем переменные
from blocks import Platform
from player import Player

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 600  # Высота
# Группируем ширину и высоту в одну переменную
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    # Не движемся дальше нижней границы
    t = max(-(camera.height-WIN_HEIGHT), t)
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


class FireDungeon():

    def __init__(self):
        # создаем героя по (x,y) координатам
        self.player = Player(55, 55, True)
        self.timer = pygame.time.Clock()
        self.entities = pygame.sprite.Group()  # Все объекты

    def run_game(self):
        # Default - player is NOT moving anywhere
        left = right = False
        up = False
        down = True

        platforms = []  # то, во что мы будем врезаться или опираться
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
        pygame.init()  # Инициация PyGame, обязательная строчка
        screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
        pygame.display.set_caption("Fire Dungeon")  # Пишем в шапку
        bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
        # будем использовать как фон
        # Заливаем поверхность сплошным цветом
        bg.fill(Color(BACKGROUND_COLOR))
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

        camera = Camera(
            camera_configure,
            total_level_width,
            total_level_height)
        while True:  # Основной цикл программы
            self.timer.tick(60)
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == QUIT:
                    pygame.quit()

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
                    down = True

            # Каждую итерацию необходимо всё перерисовывать
            screen.blit(bg, (0, 0))

            # hero.draw(screen)  # отображение

            self.entities.update(left, right, up, down, platforms)
            self.player.update(left, right, up, down,
                               platforms)  # передвижение
            # центризируем камеру относительно персонажа
            camera.update(self.player)
            for e in self.entities:
                screen.blit(e.image, camera.apply(e))
            pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    fd = FireDungeon()
    fd.run_game()
