'''
import pyganim
from pygame import *
from utils import *

BACKGROUND_COLOR = "#004400"
FIRE_WIDTH = 32
FIRE_HEIGHT = 32
FIRE_COLOR = "#000000"
FIRE_SPEED = 2
from time import sleep


class Fire(sprite.Sprite):
    def __init__(self, x, y, level):
        sprite.Sprite.__init__(self)
        # Starting coordinates
        self.start_x = x
        self.start_y = y

        # drawing fire
        self.image = Surface((FIRE_WIDTH, FIRE_HEIGHT))
        self.image.fill(Color(FIRE_COLOR))
        self.image.set_colorkey(Color(FIRE_COLOR))
        self.rect = Rect(x, y, FIRE_WIDTH, FIRE_HEIGHT)
        self.image.set_colorkey(Color(FIRE_COLOR))
        #
        self.xvel = FIRE_SPEED
        self.yvel = FIRE_SPEED

    def update(self, x, y, platforms, level):  # по принципу героя

        self.image.fill(Color(FIRE_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        while True:
            if level[y + 1][x + 1] == '0' or level[y + 1][x + 1] == ' ':
                level[y + 1][x + 1] = '!'
            if level[y][x + 1] == '0' or level[y][x + 1] == ' ':
                level[y][x + 1] = '!'
            if level[y + 1][x] == '0' or level[y + 1][x] == ' ':
                level[y + 1][x] = '!'

            if level[y - 1][x - 1] == '0' or level[y - 1][x - 1] == ' ':
                level[y - 1][x - 1] = '!'
            if level[y][x - 1] == '0' or level[y][x - 1] == ' ':
                level[y][x - 1] = '!'
            if level[y - 1][x] == '0' or level[y - 1][x] == ' ':
                level[y - 1][x] = '!'

            if level[y + 1][x - 1] == '0' or level[y + 1][x - 1] == ' ':
                level[y + 1][x - 1] = '!'
            if level[y - 1][x + 1] == '0' or level[y - 1][x + 1] == ' ':
                level[y - 1][x + 1] = '!'

            sleep(2)
'''

def show_matrix(matrix):
    char_border = '#'
    print(char_border * (int(len(matrix[0])) + 2))
    for _ in range(len(matrix)):
        print(char_border, end='')
        for i in range(len(matrix[_])):
            pp = str(matrix[_][i]).replace('0', ' ')
            pp = str(matrix[_][i]).replace('1', '#')
            print(pp, end="")
        print(char_border)
    print(char_border * (len(matrix[0]) + 2))

if __name__ == '__main__':
    level = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
             [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
             [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
             [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
             [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
             [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
             [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
             [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
             [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
             [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]]

    for y, line in enumerate(level):
        for x, char in enumerate(line):
            # front
            if y + 1 < len(level):
                if str(level[y + 1][x]) == '0' or str(level[y + 1][x]) == ' ':
                    level[y + 1][x] = '!'
            if x + 1 < len(line):
                if str(level[y][x + 1]) == '0' or str(level[y][x + 1]) == ' ':
                    level[y][x + 1] = '!'
            if x + 1 < len(line) and y + 1 < len(level):
                if str(level[y + 1][x + 1]) == '0' or str(level[y + 1][x + 1]) == ' ':
                    level[y + 1][x + 1] = '!'
            # back
            if x > 0:
                if str(level[y][x - 1]) == '0' or str(level[y][x - 1]) == ' ':
                    level[y][x - 1] = '!'
            if y > 0:
                if str(level[y - 1][x]) == '0' or str(level[y - 1][x]) == ' ':
                    level[y - 1][x] = '!'
            if y > 0 and x > 0:
                if str(level[y - 1][x - 1]) == '0' or str(level[y - 1][x - 1]) == ' ':
                    level[y - 1][x - 1] = '!'
            # diagonal
            if x > 0 and y+1 < len(level):
                if str(level[y + 1][x - 1]) == '0' or str(level[y + 1][x - 1]) == ' ':
                    level[y + 1][x - 1] = '!'
            if y > 0 and x+1 < len(line):
                if str(level[y - 1][x + 1]) == '0' or str(level[y - 1][x + 1]) == ' ':
                    level[y - 1][x + 1] = '!'
    show_matrix(level)

def restruct(level):