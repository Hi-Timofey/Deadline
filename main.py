# -*- coding: utf-8 -*-
import fire_dungeon
from credits import Credits
import pygame
import pygame_menu
from db_related import Scores
from utils import *
from create_level import create_level
from player import Player
from random import randint

pygame.mixer.pre_init()
pygame.init()

FPS = 60
display_info = pygame.display.Info()
clock = pygame.time.Clock()
window_size = window_width, window_height = 800, 800
game_size = g_width, g_height = 800, 800

surface = pygame.display.set_mode(window_size)

scores_menu, main_menu = None, None
credits, game = False, False

background_image = pygame_menu.baseimage.BaseImage(
    image_path=get_data_path('background.png', 'img'))

pygame.mixer.init()
pygame.mixer.set_num_channels(5)

fd_theme = pygame_menu.themes.THEME_BLUE.copy()
fd_theme.title_shadow=True
fd_theme.background_color = (237,92,41, 80)
fd_theme.title_font_color = (255,255,255)
fd_theme.selection_color = (255,255,255)
fd_theme.widget_font_color = (255,255,255)
fd_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
fd_theme.title_background_color = (252,108,24)
fd_theme.cursor_color = (244, 164, 96)
fd_theme.menubar_close_button = True
fd_theme.title_font = get_font_path('Sigma Five.otf')
fd_theme.widget_font = get_font_path('Sigma Five.otf')
fd_theme.validate()


def draw_background():
    background_image.draw(surface)


def start_the_game_from_menu():

    global game, main_menu
    game = True
    pygame.mixer.Channel(4).set_volume(0.75)
    pygame.mixer.Channel(4).play(
        pygame.mixer.Sound(
            get_data_path(
                'game_sound.ogg',
                'music')),
        loops=-1)

    # TODO Music
    pygame.mixer.Channel(3).pause()
    surface.fill((0, 0, 0))
    LEVEL = randint(1,1000)
    gravity = False
    # Changing values

    # Maze parameters (X * Y)
    level_width = 15
    level_height = 15
    # FIRE SPEED
    fire_speed = 80
    # PLAYER MOVEMENT
    player_mv = 1
    player_mv_extra = 2

    while game:
        player = Player(
            32,
            96,
            move_speed=player_mv,
            mv_extra_multi=player_mv_extra,
            gravity=gravity)

        level = create_level(level_width, level_height, LEVEL)
        fire_dungeon_lvl = fire_dungeon.FireDungeon(
            level,
            player, g_width, g_height, fire_speed, theme=fd_theme)
        result = fire_dungeon_lvl.run_game(False)
        print(result)
        del fire_dungeon_lvl
        del player
        if result == 1:
            game = False
            # Stop soundtrack
            pygame.mixer.Channel(4).stop()
        elif result == 3:
            LEVEL += 1
            if fire_speed != 30:
                fire_speed -= 5
            level_width += 3
            level_height += 3
            if player_mv < 3:
                player_mv += 0.11
            if player_mv_extra == 1:
                player_mv_extra -= 0.05
            game = True
        elif result == 2:
            game = False
            scores_menu.add_score(LEVEL * 100)

            # Stop soundtrack
            pygame.mixer.Channel(4).stop()

        scores_menu.menu.full_reset()
        main_menu.full_reset()
        create_main_menu()
    if not game:
        pygame.mixer.Channel(3).unpause()


def main():
    global main_menu
    pygame.mixer.Channel(3).set_volume(0.75)
    pygame.mixer.Channel(3).play(
        pygame.mixer.Sound(
            get_data_path(
                'menu_theme.wav',
                'music')),
        loops=-1)

    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pass

            if not game:
                main_menu.update(events)

        if not game:
            draw_background()
            main_menu.draw(surface)

        # Credits(credit_list, surface, 'Sigma Five.otf').main()
        pygame.display.update()



def create_main_menu():
    global main_menu, scores_menu

    # if main_menu is not None:
    #     main_menu.full_reset()
    # if scores_menu is not None:
    #     scores_menu.menu.full_reset()

    main_menu = pygame_menu.Menu(300, 300, 'Fire Dungeon',
                                 theme=fd_theme)
    scores_menu = Scores(int(window_width/1.3), int(window_height/1.3), fd_theme)
    scores_menu.menu.set_onclose(create_main_menu)
    main_menu.add_button('Play', start_the_game_from_menu)
    main_menu.add_button('Scores', scores_menu.menu)
    credit_list = [
        "Fire Dungeon - Fire Maze",
        " ",
        " Menues",
        "Timofey Katkov",
        " ",
        "Game play",
        "Daniil Nesterenko",
        "Timofey Katkov",
        " ",
        "Maze",
        "Daniil Nesterenko"
        " ",
        " ",
        "Music",
        "Timofey Katkov, EROZZION Music",
        " ",
        "Thanks for playing"
    ]
    c = Credits(credit_list, surface, 'Sigma Five.otf')
    main_menu.add_button('About', c.main)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)


if __name__ == '__main__':
    create_main_menu()
    main()
