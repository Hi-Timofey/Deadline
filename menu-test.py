import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 600))


def draw_background():
    pass


def set_difficulty(value, difficulty):
    pass


def start_the_game():
    pass


if __name__ == '__main__':

    menu = pygame_menu.Menu(600, 600, 'Fire Dungeon',
                            theme=pygame_menu.themes.THEME_BLUE)

    # menu.add_button('Play', start_the_game)

    # menu.add_text_input('Name :', default='John Doe')
    # menu.add_selector(
    #     'Difficulty :', [('Hard', 1),
    #                      ('Easy', 2)],
    #     onchange=set_difficulty)

    menu.add_button('Scores', )
    menu.add_button('Quit', pygame_menu.events.EXIT)

    while True:

        draw_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()
