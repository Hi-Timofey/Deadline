# -*- coding: utf-8 -*-
import fire_dungeon
from credits import Credits
import pygame
import pygame_menu
from db_related import Scores
from utils import *


pygame.init()

FPS = 60
display_info = pygame.display.Info()
clock = pygame.time.Clock()

window_size = window_width, window_height = 800, 800
game_size = g_width, g_height = 800, 800

main_menu = None
game = False
surface = pygame.display.set_mode(window_size)

background_image = pygame_menu.baseimage.BaseImage(
    image_path=get_data_path('background.png', 'img'))

pygame.mixer.init()


def draw_background():
    background_image.draw(surface)


def start_end_credits():
    credit_list = [
        "CREDITS - The Departed",
        " ",
        "Leonardo DiCaprio - Billy",
        "Matt Damon - Colin Sullivan",
        "Jack Nicholson - Frank Costello",
        "Mark Wahlberg - Dignam",
        "Martin Sheen - Queenan"]
    c = Credits(credit_list, surface, 'Sigma Five.otf')
    c.main()


def start_the_game():
    game = True
    fd = fire_dungeon.FireDungeon(g_width,g_height)
    surface.fill((0,0,0))
    fd.run_game(gravity=False)


def main():
    pygame.mixer.music.load(get_data_path('menu_theme.wav', 'music'))
    pygame.mixer.music.play(-1)

    main_menu = pygame_menu.Menu(300, 300, 'Fire Dungeon',
                                 theme=pygame_menu.themes.THEME_BLUE)
    scores_menu = Scores(window_width, window_height)
    main_menu.add_button('Play', start_the_game)

    main_menu.add_button('Scores', scores_menu.menu)
    main_menu.add_button('About', start_end_credits)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)

    while True:

        draw_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pass

        main_menu.mainloop(surface, draw_background, fps_limit=FPS)

        pygame.display.update()


if __name__ == '__main__':
    main()
