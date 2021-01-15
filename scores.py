import os
import sqlite3 as sql
import pygame
import pygame_menu


class Scores():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.path = os.path.join('data', 'db.db')
        self.cur = None
        self.db_connect = None

        if not Scores.isSQLite3(self.path):
            self.create_default_base()

        self.create_menu()

    def create_menu(self):
        data = self.get_all_data(ordered=True)
        self.menu = pygame_menu.Menu(
            self.height,
            self.width,
            'Dungeon Scores ',
            theme=pygame_menu.themes.THEME_BLUE,
            columns=2,
            onclose=pygame_menu.events.EXIT,
            rows=1 + len(data))

        self.menu.add_label('Score', max_char=-1, font_size=28)
        for d in data:
            self.menu.add_label(d[0], max_char=-1, font_size=16)

        self.menu.add_label('Data', max_char=-1, font_size=28)
        for d in data:
            self.menu.add_label(d[1], max_char=-1, font_size=16)

    def menu_off(self):
        self.menu.disable()

    def menu_on(self):
        self.menu.enable()

    def is_enabled(self):
        return self.menu.is_enabled()

    def update(self, events):
        return self.menu.update(events)

    def draw(self, surface):
        return self.menu.draw(surface)

    # --- DATABASE ---

    def create_default_table(self):
        '''Creates the default database with "Files" table'''

        self._start()
        query_table = '''
        CREATE TABLE "scores" (
	"id"	INTEGER NOT NULL UNIQUE,
	"score"	INTEGER NOT NULL DEFAULT 0,
	"data"	TEXT NOT NULL DEFAULT '01.01.2021 13:00',
	PRIMARY KEY("score")
                );
        '''
        self.cur.execute(query_table)
        self.db_connect.commit()
        self._stop()

    def _start(self):
        self.db_connect = sql.connect(self.path)
        self.cur = self.db_connect.cursor()

    def _stop(self):
        self.cur = None
        self.db_connect.close()

    def isSQLite3(filename):
        if not os.path.isfile(filename):
            return False
        if os.path.getsize(
                filename) < 100:  # SQLite database file header is 100 bytes
            return False

        with open(filename, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == b'SQLite format 3\x00'

    def get_all_data(self, ordered=True):
        self._start()

        if ordered:
            response = self.cur.execute(
                '''select distinct score, data from scores
                                    order by score asc''').fetchall()
        else:
            response = self.cur.execute(
                'select distinct score, data from scores').fetchall()

        self._stop()
        return response


    def add_score(self, score, date):
         self._start()
         self.cur.execute(f"insert into scores values({int(score)}, '{date}')")
         self.db_connect.commit()
         self._stop()


    def delete_all_scores(self):
        self._start()

        query = f"delete from scores"
        self.cur.execute(query)

        self.db_connect.commit()
        self._stop()


if __name__ == '__main__':

    height = 600
    width = 600
    pygame.init()
    surface = pygame.display.set_mode((width, height))

    menu = Scores(width, height)
    # menu.set_up(width, height)
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()
