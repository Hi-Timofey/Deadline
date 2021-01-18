# -*- coding: utf-8 -*-
import pygame
import pygame_menu
from scores import Scores
from utils import *


pygame.init()

FPS = 60
display_info = pygame.display.Info()
clock = pygame.time.Clock()

window_size = w_width, w_height = 1000, 1000
game_size = g_width, g_height = 800, 800

main_menu = None
surface = pygame.display.set_mode((1000, 1000))

background_image = pygame_menu.baseimage.BaseImage(
    image_path=get_data_path('background.png', 'img'))

pygame.mixer.init()


def draw_background():
    background_image.draw(surface)


def start_end_credits():
    from credits import Credits
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
    import fire_dungeon
    fire_dungeon.main()


def main():
    pygame.mixer.music.load(get_data_path('menu_theme.wav', 'music'))
    pygame.mixer.music.play(-1)

    main_menu = pygame_menu.Menu(300, 300, 'Fire Dungeon',
                                 theme=pygame_menu.themes.THEME_BLUE)
    scores_menu = Scores(1000, 1000)
    main_menu.add_button('Play', start_the_game)

    # menu.add_text_input('Name :', default='John Doe')
    # menu.add_selector(
    #     'Difficulty :', [('Hard', 1),
    #                      ('Easy', 2)],
    #     onchange=set_difficulty)

    main_menu.add_button('Scores', scores_menu.menu)
    main_menu.add_button('About', start_end_credits)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)

    while True:

        draw_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        main_menu.mainloop(surface, draw_background, fps_limit=FPS)

        pygame.display.update()


if __name__ == '__main__':
    main()
