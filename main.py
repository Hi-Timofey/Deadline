# -*- coding: utf-8 -*-
import fire_dungeon
import json
import datetime
from credits import Credits
import pygame
import pygame_menu
from db_related import Scores, Saves
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

saves_menu, scores_menu, main_menu = None, None, None
credits, game = False, False

background_image = pygame_menu.baseimage.BaseImage(
    image_path=get_data_path('background.png', 'img'))

pygame.mixer.init()
pygame.mixer.set_num_channels(5)

fd_theme = pygame_menu.themes.THEME_BLUE.copy()
fd_theme.title_shadow = True
fd_theme.background_color = (237, 92, 41, 80)
fd_theme.title_font_color = (255, 255, 255)
fd_theme.selection_color = (255, 255, 255)
fd_theme.widget_font_color = (255, 255, 255)
fd_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
fd_theme.title_background_color = (252, 108, 24)
fd_theme.cursor_color = (244, 164, 96)
fd_theme.menubar_close_button = True
fd_theme.title_font = get_font_path('Sigma Five.otf')
fd_theme.widget_font = get_font_path('Sigma Five.otf')
fd_theme.validate()


def draw_background():
    background_image.draw(surface)


def start_game(save=None):

    global game, main_menu, saves_menu
    game = True

    # Music
    pygame.mixer.Channel(4).set_volume(0.75)
    pygame.mixer.Channel(4).play(
        pygame.mixer.Sound(
            get_data_path(
                'game_sound.ogg',
                'music')),
        loops=-1)

    pygame.mixer.Channel(3).pause()
    surface.fill((0, 0, 0))

    # Level number
    LEVEL = 1
    # Maze parameters (X * Y)
    level_width = 15
    level_height = 15

    # FIRE
    fire_speed = 80
    fire_list_coords = None
    fire_delay = 227 + 1

    # PLAYER MOVEMENT
    player_mv = 1
    player_mv_extra = 2

    # Player
    gravity = False
    player_x = 32
    player_y = 96

    fire_dungeon_lvl = None

    # Loading save if it exists
    if save is not None:
        LEVEL = save['level_num']
        gravity = save['gravity']
        level_width = save['level_width']
        level_height = save['level_height']
        fire_speed = save['fire_speed']
        player_mv = save['player_mv']
        player_mv_extra = save['player_mv_extra']
        player_x = save['player_x']
        player_y = save['player_y']
        fire_list_coords = save['fire_coords']
        fire_delay = 0

    while game:

        player = Player(
            player_x,
            player_y,
            move_speed=player_mv,
            mv_extra_multi=player_mv_extra,
            gravity=gravity)

        if save is None:
            level = create_level(level_width, level_height, LEVEL)
        else:
            level = save['level']

        fire_dungeon_lvl = fire_dungeon.FireDungeon(
            level, player, g_width, g_height, fire_speed, theme=fd_theme,
            fire_list_coords=fire_list_coords, fire_delay=fire_delay)

        # After finishing loaded level need to set defult values for next
        # levels
        if save is not None:
            save = None
            player_x = 32
            player_y = 96
            fire_delay = 227 + 1

        result = fire_dungeon_lvl.run_game(False)

        if result == 1:
            game = False
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
        elif result == 7:
            game = False
            date = datetime.date.today()
            time = datetime.datetime.now().time()
            save = {
                # Time of saving
                f'date': f'{date}_{str(time)[:8]}',
                # Data to create level
                'level_num': LEVEL,
                'level_width': level_width, 'level_height': level_height,
                'level': fire_dungeon_lvl.get_level(),
                'fire_coords': fire_dungeon_lvl.fire_list_coords,
                # 'seed' : fire_dungeon_lvl.seed,

                # Player information
                'gravity': gravity,
                'fire_speed': fire_speed,
                'player_mv': player_mv,
                'player_mv_extra': player_mv_extra,
                'player_x': player.rect.x,
                'player_y': player.rect.y
            }
            saves_menu.add_new_save(save)


        # Reseting menu if player want to clear it
        saves_menu.menu.full_reset()
        scores_menu.menu.full_reset()
        main_menu.full_reset()
        create_main_menu()

    del fire_dungeon_lvl
    del player
    if not game:
        pygame.mixer.Channel(4).stop()
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

        pygame.display.update()


def start_game_from_save(*args, **kwargs):

    print(args, kwargs)
    pass


def create_main_menu():
    global main_menu, scores_menu, saves_menu

    # Main menu
    main_menu = pygame_menu.Menu(300, 300, 'Fire Dungeon',
                                 theme=fd_theme)

    # Table of SCORES
    scores_menu = Scores(
        int(window_width / 1.3),
        int(window_height / 1.3),
        fd_theme)
    scores_menu.menu.set_onclose(create_main_menu)

    # Table of SAVES
    saves_menu = Saves(
        int(window_width / 1.3),
        int(window_height / 1.3),
        start_game, fd_theme)

    main_menu.add_button('Play', start_game)
    main_menu.add_button('Scores', scores_menu.menu)
    main_menu.add_button('Saves', saves_menu.menu)
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
