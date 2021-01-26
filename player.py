import pygame
import pyganim
from pygame import *

import blocks
from utils import *

# Player basic variables
MOVE_SPEED = 1
PLAYER_WIDTH = 31  # нужен на один пиксель меньше чем размер блока, иначе взаимодействие багует
PLAYER_HEIGHT = 32
PLAYER_COLOR = "#888888"

MOVE_EXTRA_SPEED = 3  # Ускорение
JUMP_EXTRA_POWER = 1  # дополнительная сила прыжка
ANIMATION_SUPER_SPEED_DELAY = 1  # скорость смены кадров при ускорении

# Gravity constants
JUMP_POWER = 10
GRAVITY = 0.35

# Animation constants
ANIMATION_DELAY = 50
'''
TMP = pygame.transform.scale(pygame.image.load(get_data_path('Woodcutter1.png', 'character')), [48, 48])
char = TMP.subsurface(0, 0, 48, 48)
char = pygame.transform.scale(char, (32, 32))
'''

ANIMATION_RIGHT = [(get_data_path('walk-1.png', 'character')),
                   (get_data_path('walk-2.png', 'character')),
                   (get_data_path('walk-3.png', 'character')),
                   (get_data_path('walk-4.png', 'character')),
                   (get_data_path('walk-5.png', 'character')),
                   (get_data_path('walk-6.png', 'character'))]

ANIMATION_DEATH = [(get_data_path('death1.png', 'character')),
                   (get_data_path('death2.png', 'character')),
                   (get_data_path('death3.png', 'character')),
                   (get_data_path('death2.png', 'character')),
                   (get_data_path('death3.png', 'character')),
                   (get_data_path('death2.png', 'character')),
                   (get_data_path('death3.png', 'character')),
                   (get_data_path('death2.png', 'character'))]

ANIMATION_LEFT = [(get_data_path('walk-l1.png', 'character')),
                  (get_data_path('walk-l2.png', 'character')),
                  (get_data_path('walk-l3.png', 'character')),
                  (get_data_path('walk-l4.png', 'character')),
                  (get_data_path('walk-l5.png', 'character')),
                  (get_data_path('walk-l6.png', 'character'))]

ANIMATION_JUMP = [(get_data_path('up1.png', 'character')),
                  (get_data_path('up2.png', 'character')),
                  (get_data_path('up3.png', 'character')),
                  (get_data_path('up4.png', 'character')),
                  (get_data_path('up5.png', 'character')),
                  (get_data_path('up6.png', 'character'))]

ANIMATION_JUMP_LEFT = [(get_data_path('up1.png', 'character')),
                       (get_data_path('up2.png', 'character')),
                       (get_data_path('up3.png', 'character')),
                       (get_data_path('up4.png', 'character')),
                       (get_data_path('up5.png', 'character')),
                       (get_data_path('up6.png', 'character'))]

ANIMATION_JUMP_RIGHT = [(get_data_path('up1.png', 'character')),
                        (get_data_path('up2.png', 'character')),
                        (get_data_path('up3.png', 'character')),
                        (get_data_path('up4.png', 'character')),
                        (get_data_path('up5.png', 'character')),
                        (get_data_path('up6.png', 'character'))]

ANIMATION_STAY = [(pygame.image.load(get_data_path('Woodcutter1.png', 'character')), 1)]


class Player(sprite.Sprite):
    def __init__(self, x, y, gravity=True):
        sprite.Sprite.__init__(self)
        # Starting coordinates
        self.start_x = x
        self.start_y = y
        self.gravity = gravity

        # Setting up basic speed
        self.xvel = 0
        self.yvel = 0
        # параметр жизни персонажа, становиться False при заимодействии с огнём и шипами
        # TODO можно реализовать его как int и сделать несколько жизней со счётчиком
        self.life = True
        self.end = False

        # Set up gravity value whether player need it or not
        if gravity:
            self.on_ground = not gravity

        # Setting image of the player
        self.image = Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(Color(PLAYER_COLOR))
        self.image.set_colorkey(Color(PLAYER_COLOR))
        self.rect = Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image.set_colorkey(Color(PLAYER_COLOR))

        #        Анимация движения вправо
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        #        Анимация движения влево
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        boltAnim = []
        for anim in ANIMATION_DEATH:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimDeath = pyganim.PygAnimation(boltAnim)
        self.boltAnimDeath.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimJumpLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpLeft.play()
        self.boltAnimJumpLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimJumpLeftSuperSpeed.play()

        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimJumpRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpRight.play()
        self.boltAnimJumpRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimJumpRightSuperSpeed.play()

        boltAnim = []
        for anim in ANIMATION_JUMP:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimJump = pyganim.PygAnimation(boltAnim)
        self.boltAnimJump.play()

        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))

    def update(self, left, right, up, down, platforms, running):
        '''
        Updating player sprite on the screen.

        Func updating player coordinates and sprite by
        checking where he is going (left, right, down, up)
        and setiing up speed by OX and OY.

        Also, separated animations for each directions of the player.
        '''
        if not self.life:
            self.image.fill(Color(PLAYER_COLOR))
            self.boltAnimDeath.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(PLAYER_COLOR))
            if running:  # если ускорение
                self.xvel -= MOVE_EXTRA_SPEED  # то передвигаемся быстрее
                if not up:  # и если не прыгаем
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))  # то отображаем быструю анимацию
            elif up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(PLAYER_COLOR))
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            elif up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if self.gravity:
            if up:
                if self.on_ground:  # прыгаем, только когда можем оттолкнуться от земли
                    self.yvel = -JUMP_POWER
                self.image.fill(Color(PLAYER_COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
            if not (left or right):  # стоим, когда нет указаний идти
                self.xvel = 0
                if not up:
                    self.image.fill(Color(PLAYER_COLOR))
                    self.boltAnimStay.blit(self.image, (0, 0))
            if not self.on_ground:
                self.yvel += GRAVITY
        else:
            # In non-gravity mode logic of UP and DOWN same as
            # fot the RIGHT and LEFT, but on OY.
            if up:
                self.yvel = -MOVE_SPEED
                self.image.fill(Color(PLAYER_COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
            if down:
                self.yvel = MOVE_SPEED
                self.image.fill(Color(PLAYER_COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
            if not (up or down or left or right):
                self.xvel = 0
                self.yvel = 0
                self.image.fill(Color(PLAYER_COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        # Don't know whether we are on the floor or not
        if self.gravity:
            self.on_ground = False

        # Moving sprite based on speed and platforms
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def draw(self, screen):
        ''' Drawing player on the screen.
        '''
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collide(self, xvel, yvel, platforms):
        '''Function that checks if player reached the platforms.

        If player coordinates + speed is matches that he would
        run in wall, that function stops him (include logic of gravity)'''
        for p in platforms:
            if sprite.collide_rect(
                    self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, blocks.Door):  # если пересакаемый блок - blocks.BlockDie
                    self.win()  # выходим из лабиринта
                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо
                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево
                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    if self.gravity:
                        self.on_ground = True  # и становится на что-то твердое
                        self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    if self.gravity:
                        self.yvel = 0  # и энергия прыжка пропадает

                if isinstance(p, blocks.BlockDie):  # если пересакаемый блок - blocks.BlockDie
                    self.die()  # умираем

    def die(self):
        self.image.fill(Color(PLAYER_COLOR))
        self.boltAnimDeath.blit(self.image, (0, 0))
        self.life = False

    def win(self):
        self.end = True

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
