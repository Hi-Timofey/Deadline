import pygame
from pygame import sprite, image
import pyganim
from pygame.locals import Color
from pygame.rect import Rect
from pygame.surface import Surface
import pygame.transform
from random import randint
from utils import get_data_path

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

ANIMATION_DELAY = 1
COLOR = "#888888"

ANIMATION_FIRE = [(get_data_path('Fogo_1.png', 'img')),
                  (get_data_path('Fogo_2.png', 'img')),
                  (get_data_path('Fogo_3.png', 'img')),
                  (get_data_path('Fogo_4.png', 'img'))]

walls_source = pygame.transform.scale(pygame.image.load(
    get_data_path('Civilized-no-bg.png', 'texture')), [250, 250])
WALL_TEXTURES = [
    walls_source.subsurface(
        70, 50, 10, 10), walls_source.subsurface(
            80, 50, 10, 10), walls_source.subsurface(
                50, 90, 10, 10), walls_source.subsurface(
                    40, 90, 10, 10), walls_source.subsurface(
                        30, 90, 10, 10)]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pygame.transform.scale(
            WALL_TEXTURES[randint(1, 4)], (32, 32))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_FIRE:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        self.image = pygame.image.load((get_data_path('Fogo_1.png', 'img')))


class Door(Platform):
    # TODO DOCS !

    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        door = walls_source.subsurface(70, 10, 10, 10)
        self.image = pygame.transform.scale(door, (32, 32))


class ClosedDoor(Platform):
    # TODO DOCS !

    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        door = walls_source.subsurface(10, 10, 10, 10)
        self.image = pygame.transform.scale(door, (32, 32))


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y, goX, goY)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
