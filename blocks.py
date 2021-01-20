import pygame
from pygame import sprite, image
import pyganim
from pygame.locals import Color
from pygame.rect import Rect
from pygame.surface import Surface
from random import randint

from utils import get_data_path

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
# ANIMATION_BLOCKTELEPORT = [
#             (get_data_path("sjf2r.png", 'img')),
#             (get_data_path("sjf2r.png", 'img'))]
COLOR = "#888888"


class Platform(sprite.Sprite):
    def __init__(self, x, y, image):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image
        # self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y, image):
        img = image
        self.image = Surface(
            (PLATFORM_WIDTH, PLATFORM_HEIGHT),
            pygame.SRCALPHA)
        Platform.__init__(self, x, y, image)

        self.image = img


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
