import logging
import sqlite3
import os

class DBBoobsVote:
    def __init__(self, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger("db boobs class")

        dir_db = os.path.abspath(os.curdir)
        self.conn = sqlite3.connect(f'{dir_db}/snowwhitebot.db')
        self.c = self.conn.cursor()