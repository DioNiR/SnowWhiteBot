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


        sql = '''CREATE TABLE IF NOT EXISTS questions (id integer primary key, message_id integer, author_id integer, question_text text)'''
        self.c.execute(sql)
        self.conn.commit()

        sql = '''CREATE TABLE IF NOT EXISTS answers (id integer primary key, question_id integer, message_id integer, answer_text text, points integer default 1)'''
        self.c.execute(sql)
        self.conn.commit()

        sql = '''CREATE TABLE IF NOT EXISTS question_votes (id integer primary key, question_id integer, answer_id integer, user_id integer, points integer default 1)'''
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

    def insert_question(self, question_text, message_id, author_id):
        sql = '''INSERT INTO questions('author_id', 'message_id', 'question_text') VALUES (?, ?, ?)'''
        self.c.execute(sql, (author_id, message_id, question_text))
        self.conn.commit()
        return self.c.lastrowid

    def insert_answer(self, question_id, message_id, answer_text):
        try:
            sql = '''INSERT INTO answers('question_id','message_id', 'answer_text') VALUES (?, ?, ?)'''
            self.c.execute(sql, (question_id, message_id, answer_text))
            self.conn.commit()
            return self.c.lastrowid
        except sqlite3.Error as e:
            print(type(e).__name__)

    def select_question_answers(self, question_id):
        try:
            sql = '''SELECT * FROM answers WHERE question_id = ?'''
            self.c.execute(sql, (question_id,))
            return self.c.fetchall()
        except sqlite3.Error as e:
            print(type(e).__name__)

    def select_question_by_message_id(self, message_id):
        sql = '''SELECT * FROM questions WHERE message_id = ?'''
        self.c.execute(sql, (message_id,))
        return self.c.fetchone()

    def select_answer_by_message_id(self, message_id):
        sql = '''SELECT * FROM answers WHERE message_id = ?'''
        self.c.execute(sql, (message_id,))
        return self.c.fetchone()

    def update_answer_points_by_id(self, answer_id, points):
        sql = '''UPDATE answers SET points = ? WHERE id = ?'''
        self.c.execute(sql, (points, answer_id))

    def get_answer_points_by_id(self, answer_id):
        sql = '''SELECT points FROM answers WHERE id = ?'''
        self.c.execute(sql, (answer_id,))
        return self.c.fetchone()

    def select_questions_by_author(self, author_id):
        sql = '''SELECT * FROM questions WHERE author_id = ?'''
        self.c.execute(sql, (author_id,))
        return self.c.fetchall()

    def select_questions_not_votes(self, user_id):
        sql = '''
            SELECT * FROM questions WHERE id NOT IN (SELECT question_id FROM question_votes WHERE user_id = ?)
        '''

    def select_random_questions(self, user_id):
        sql = '''
            SELECT * FROM questions WHERE id NOT IN (SELECT question_id FROM question_votes WHERE user_id = ?) ORDER BY RANDOM() LIMIT 1
        '''
        try:
            self.c.execute(sql, (user_id,))

        except sqlite3.Error as e:
            print(e)

        return self.c.fetchall()

    def ckeck_answer_user_vote(self, question_id, answer_id, user_id):
        sql = '''SELECT * FROM question_votes WHERE question_id = ? AND user_id = ?'''
        self.c.execute(sql, (question_id, user_id))
        return self.c.fetchone()

    def add_answer_vote(self, question_id, answer_id, user_id, points = 1):
        try:
            sql = '''INSERT INTO question_votes('question_id','answer_id', 'user_id', 'points') VALUES (?, ?, ?, ?)'''
            self.c.execute(sql, (question_id, answer_id, user_id, points))
            self.conn.commit()
            return self.c.lastrowid
        except sqlite3.Error as e:
            print(type(e).__name__)
            print("Database error: %s" % e)
