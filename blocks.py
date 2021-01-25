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
# ANIMATION_BLOCKTELEPORT = [
#             (get_data_path("sjf2r.png", 'img')),
#             (get_data_path("sjf2r.png", 'img'))]
COLOR = "#888888"

ANIMATION_FIRE = [(get_data_path('Fogo_1.png', 'img')),
                  (get_data_path('Fogo_2.png', 'img')),
                  (get_data_path('Fogo_3.png', 'img')),
                  (get_data_path('Fogo_4.png', 'img'))]

TMP = pygame.transform.scale(pygame.image.load(get_data_path('Civilized-no-bg.png', 'texture')), [250, 250])
WALL_TEXTURES = [TMP.subsurface(70, 50, 10, 10), TMP.subsurface(80, 50, 10, 10), TMP.subsurface(50, 90, 10, 10),
                 TMP.subsurface(40, 90, 10, 10), TMP.subsurface(30, 90, 10, 10)]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        wall_textures = []
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        '''
        tmp = pygame.transform.scale(pygame.image.load(get_data_path('Civilized.png', 'texture')), [250, 250])
        wall_textures.append(tmp.subsurface(70, 50, 10, 10))
        wall_textures.append(tmp.subsurface(80, 50, 10, 10))
        wall_textures.append(tmp.subsurface(50, 80, 10, 10))
        wall_textures.append(tmp.subsurface(40, 80, 10, 10))
        wall_textures.append(tmp.subsurface(60, 80, 10, 10))
        '''
        img = pygame.transform.scale(WALL_TEXTURES[randint(1, 4)], (32, 32))
        self.image = img
        '''
        picture = image.load(
            get_data_path(f"wall_64x64_{randint(1, 15)}.png",
                          'img')).convert()
        img = pygame.transform.scale(picture, (32, 32))
        self.image = img
        '''
        # self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_FIRE:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        img = pygame.image.load((get_data_path('Fogo_1.png', 'img')))
        self.image = img


class Door(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        door = TMP.subsurface(70, 10, 10, 10)
        img = pygame.transform.scale(door, (32, 32))
        self.image = img


class ClosedDoor(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        door = TMP.subsurface(10, 10, 10, 10)
        img = pygame.transform.scale(door, (32, 32))
        self.image = img


'''
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
'''


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
