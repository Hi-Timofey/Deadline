import pyganim
from pygame import *
from utils import *

# Player basic variables
MOVE_SPEED = 7
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 32
PLAYER_COLOR = "#888888"

# Gravity constants
JUMP_POWER = 10
GRAVITY = 0.35

# Animation constants
ANIMATION_DELAY = 1

ANIMATION_RIGHT = [(get_data_path('r1.png', 'img')),
                   (get_data_path('r2.png', 'img')),
                   (get_data_path('r3.png', 'img')),
                   (get_data_path('r4.png', 'img')),
                   (get_data_path('r5.png', 'img'))]

ANIMATION_LEFT = [(get_data_path('l1.png', 'img')),
                  (get_data_path('l2.png', 'img')),
                  (get_data_path('l3.png', 'img')),
                  (get_data_path('l4.png', 'img')),
                  (get_data_path('l5.png', 'img'))]

ANIMATION_JUMP_LEFT = [(get_data_path('jl.png', 'img'), 1)]
ANIMATION_JUMP_RIGHT = [(get_data_path('jr.png', 'img'), 1)]
ANIMATION_JUMP = [(get_data_path('j.png', 'img'), 1)]
ANIMATION_STAY = [(get_data_path('0.png', 'img'), 1)]


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

        # Set up gravity value whether player need it or not
        if gravity:
            self.on_ground = not gravity

        # Setting image of the player
        self.image = Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(Color(PLAYER_COLOR))
        self.image.set_colorkey(Color(PLAYER_COLOR))
        self.rect = Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image.set_colorkey(Color(PLAYER_COLOR))

        # Animation right
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        # Animation left
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))

    def update(self, left, right, up, down, platforms):
        '''
        Updating player sprite on the screen.

        Func updating player coordinates and sprite by
        checking where he is going (left, right, down, up)
        and setiing up speed by OX and OY.

        Also, separated animations for each directions of the player.
        '''
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(PLAYER_COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(PLAYER_COLOR))
            if up:
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
