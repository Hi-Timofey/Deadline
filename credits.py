#!/usr/bin/python
import pygame
from pygame.locals import *



class Credits():

    def __init__(self, credit_list,surface, font='Arial'):
        self.credit_list = credit_list
        self.surface = surface
        self.font = pygame.font.SysFont(font, 40)
        self.run = True
        self.clock = pygame.time.Clock()

    def main(self):
        screen_r = self.surface.get_rect()

        texts = []
        # we render the text once, since it's easier to work with surfaces
        # also, font rendering is a performance killer
        for i, line in enumerate(self.credit_list):
            s = self.font.render(line, 1, (240,240,240))
            # we also create a Rect for each Surface.
            # whenever you use rects with surfaces, it may be a good idea to use sprites instead
            # we give each rect the correct starting position
            r = s.get_rect(
                centerx=screen_r.centerx,
                y=screen_r.bottom + i * 45)
            texts.append((r, s))

        while self.run:
            for e in pygame.event.get():
                if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            self.surface.fill((0,0, 0))

            for r, s in texts:
                # now we just move each rect by one pixel each frame
                r.move_ip(0, -1)
                # and drawing is as simple as this
                self.surface.blit(s, r)

            # if all rects have left the screen, we exit
            if not screen_r.collidelistall([r for (r, _) in texts]):
                return

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    main()
