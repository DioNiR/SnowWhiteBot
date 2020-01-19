import logging
import sqlite3
import os

class db:
    def __init__(self, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger("db class")

        dir_db = os.path.abspath(os.curdir)
        self.conn = sqlite3.connect(f'{dir_db}/snowwhitebot.db')
        self.c = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS chat_members (id integer primary key, chat_id integer, user_id integer, user_name text)'''
        self.c.execute(sql)
        self.conn.commit()

        sql = '''CREATE TABLE IF NOT EXISTS images (id integer primary key, images_key text)'''
        self.c.execute(sql)
        self.conn.commit()


        sql = '''CREATE TABLE IF NOT EXISTS chats (id integer primary key, chat_id integer, chat_name text)'''
        self.c.execute(sql)
        self.conn.commit()


    def insert_chat(self, chat_id, chat_name):
        """Метод добавления чата в БД

        Keyword arguments:
        chat_id -- id чата
        chat_name -- название чата

        """

        self.logger.info('insert_chat')

        sql = '''INSERT INTO chats(chat_id, chat_name) VALUES(?, ?)'''
        self.c.execute(sql, (chat_id, chat_name))
        self.conn.commit()

        self.logger.info(f'chat_id: {chat_id}')
        self.logger.info(f'chat_name: {chat_name}')
        self.logger.info(self.c.lastrowid)

        return self.c.lastrowid

    def select_chat_by_chat_id(self, chat_id):
        """Метод поиск чата по id чата, не путать id бд

        Keyword arguments:
        chat_id -- id чата

        """
        self.logger.info('select_chat_by_chat_id')

        sql = '''SELECT * FROM chats WHERE chat_id = ?'''
        self.c.execute(sql, (chat_id, ))

        self.logger.info(f'chat_id: {chat_id}')
        self.logger.info(self.c.fetchone())

        return self.c.fetchone()

    def get_chats(self):
        """Метод получения данных всех добавленных чатов"""
        self.logger.info('get_chats')

        sql = '''SELECT * FROM chats'''
        self.c.execute(sql)
        return self.c.fetchall()


    def insert_chat_members_data(self, chat_id, user_id, user_name):
        sql = '''INSERT INTO chat_members(chat_id, user_id, user_name) VALUES(?, ?, ?)'''
        self.c.execute(sql, (chat_id, user_id, user_name))
        self.conn.commit()

        return self.c.lastrowid

    def select_chat_members_by_user_id(self, chat_id, user_id):
        sql = '''SELECT * FROM chat_members WHERE chat_id = ? AND user_id = ?'''
        self.c.execute(sql, (chat_id, user_id))
        return self.c.fetchone()

    def select_chat_members_by_chat_id(self, chat_id):
        sql = '''SELECT * FROM chat_members WHERE chat_id = ?'''
        self.c.execute(sql, (chat_id, ))
        return self.c.fetchall()

    def select_product_by_id(self, product_id):
        sql = '''SELECT * FROM product WHERE id = ?'''
        self.c.execute(sql, (product_id))
        return self.c.fetchall() 

    def select_product_by_key(self, product_key):
        sql = '''SELECT * FROM product WHERE sky = ?'''
        self.c.execute(sql, (product_key))
        return self.c.fetchall()

    def insert_product_data(self, category_id, sku, name, url):
        sql = '''INSERT INTO products(category_id, sku, name, url) VALUES(?, ?, ?, ?)'''
        self.c.execute(sql, (category_id, sku, name, url))
        self.conn.commit()

        return self.c.lastrowid