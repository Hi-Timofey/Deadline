import os
import sqlite3 as sql
import pygame
import pygame_menu
import datetime


class FireDB():

    def __init__(self, width, height, theme=None):
        self.width = width
        self.height = height
        self.theme = theme
        self.path = os.path.join('data', 'db.db')
        self.cur = None
        self.db_connect = None

        if not Scores.isSQLite3(self.path):
            self.create_default_base()

        self.create_menu()
    # --- DATABASE ---

    def create_default_table(self):
        '''
        Creates the default database.

        Creates db with SCORES table which contains
        player scores and dates of them ; SAVES with
        player not ended games.
        '''

        self._start()
        query_table = '''
        CREATE TABLE "scores" (
	"id"	INTEGER,
	"score"	INTEGER NOT NULL DEFAULT 0,
	"date"	TEXT NOT NULL DEFAULT '01.01.2021 13:00',
	PRIMARY KEY("id" AUTOINCREMENT)
);
        '''
        # query_table += '''
        # CREATE TABLE "scores" (
        # "id"	INTEGER NOT NULL UNIQUE,
        # "score"	INTEGER NOT NULL DEFAULT 0,
        # "data"	TEXT NOT NULL DEFAULT '01.01.2021 13:00',
        # PRIMARY KEY("score")
        #         );'''
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


class Scores(FireDB):

    def create_menu(self):
        data = self.get_all_data(ordered=True)
        data_length = len(data)
        if self.theme is None:
            self.theme = pygame_menu.themes.THEME_BLUE
        if data_length > 0:
            self.menu = pygame_menu.Menu(
                self.height,
                self.width,
                'Dungeon Scores ',
                theme=self.theme,
                columns=2,
                onclose=pygame_menu.events.EXIT,
                rows=2 + data_length)

            scores_lbl = []
            self.menu.add_label('Score', max_char=-1, font_size=22)
            for d in data:
                scores_lbl.append(self.menu.add_label(d[0], max_char=-1, font_size=30))

            self.menu.add_button('Quit', pygame_menu.events.RESET)

            self.menu.add_label('Data', max_char=-1, font_size=22)
            for d in data:
                scores_lbl.append(self.menu.add_label(d[1], max_char=-1, font_size=30))

            self.clear_btn = self.menu.add_button('Clear', self.delete_all_scores)
            self.scores_lbl = scores_lbl

        else:
            self.menu = pygame_menu.Menu(
                self.height,
                self.width,
                'Dungeon Scores ',
                theme=self.theme,
                columns=2,
                onclose=pygame_menu.events.EXIT,
                rows=2)
            self.menu.add_label('Score', max_char=-1, font_size=28)
            self.menu.add_button('No', pygame_menu.events.RESET)
            self.menu.add_label('Records', max_char=-1, font_size=28)
            self.menu.add_button('Data', pygame_menu.events.RESET)

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

    def get_all_data(self, ordered=True):
        self._start()

        if ordered:
            response = self.cur.execute(
                '''select distinct score, date from scores
                                    order by score DESC''').fetchall()
        else:
            response = self.cur.execute(
                'select distinct score, date from scores').fetchall()

        self._stop()
        return response

    def add_score(self, score):
        self._start()
        date = datetime.date.today()
        time = datetime.datetime.now().time()
        query = f"insert into scores(id, score, date) values(null, {int(score)}, '{date} {str(time)[:8]}')"
        self.cur.execute(query)
        self.db_connect.commit()
        self._stop()

    def delete_all_scores(self):
        self._start()

        query = f"delete from scores"
        self.cur.execute(query)

        self.db_connect.commit()
        self._stop()
        self.create_menu()
        self.menu.full_reset()
        # Just hides the lbl from player view
        for score in self.scores_lbl:
            score.hide()




class Saves(FireDB):

    def get_all_data(self, ordered=True):
        pass
        # self._start()

        # if ordered:
        #     response = self.cur.execute(
        #         '''select distinct score, data from scores
        #                             order by score asc''').fetchall()
        # else:
        #     response = self.cur.execute(
        #         'select distinct score, data from scores').fetchall()

        # self._stop()
        # return response

    def add_score(self, score, date):
        pass
        # self._start()
        # self.cur.execute(f"insert into scores values({int(score)}, '{date}')")
        # self.db_connect.commit()
        # self._stop()

    def delete_all_scores(self):
        pass
        # self._start()

        # query = f"delete from scores"
        # self.cur.execute(query)

        # self.db_connect.commit()
        # self._stop()


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
