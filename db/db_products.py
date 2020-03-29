import logging
import sqlite3
import os

class DBProducts:
    def __init__(self, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger("db boobs class")

        dir_db = os.path.abspath(os.curdir)
        self.conn = sqlite3.connect(f'{dir_db}/snowwhitebot.db')
        self.c = self.conn.cursor()

        sql = '''CREATE TABLE IF NOT EXISTS product_price (id integer primary key, product_id integer, price integer)'''
        self.c.execute(sql)
        self.conn.commit()

    def select_last_price_by_product_id(self, product_id):
        sql = '''SELECT price FROM product_price WHERE product_id = ? ORDER BY id DESC LIMIT 1'''
        try:
            self.c.execute(sql, (product_id,))
            self.conn.commit()
            return self.c.fetchone()
        except sqlite3.Error as e:
            print(type(e).__name__)
            print("Database error: %s" % e)

    def update_price_by_product_id(self, product_id, price):
        sql = '''UPDATE product_price SET price = ? WHERE product_id = ?'''
        try:
            self.c.execute(sql, (price, product_id,))
        except sqlite3.Error as e:
            print(type(e).__name__)
            print("Database error: %s" % e)
