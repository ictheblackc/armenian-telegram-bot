import os
import sqlite3


class Database:
    """Class for database work."""
    def __init__(self, name):
        self.name = name

    def create_db(self):
        connection = sqlite3.connect(f'{self.name}.sqlite3')
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            is_bot INTEGER,
            first_name VARCHAR,
            last_name VARCHAR,
            username VARCHAR,
            language_code VARCHAR,
            is_premium INTEGER
        );
        """
        connection.execute(sql)
        sql = """
        CREATE TABLE IF NOT EXISTS words (
            word VARCHAR,
            translation VARCHAR
        );
        """
        connection.execute(sql)
        connection.close()

    def insert_user(self, user_id, is_bot, first_name, last_name, username, language_code, is_premium):
        connection = sqlite3.connect(f'{self.name}.sqlite3')
        sql = f"""
        INSERT OR IGNORE INTO users (
            id,
            is_bot,
            first_name,
            last_name,
            username,
            language_code,
            is_premium
        ) VALUES (
            '{user_id}',
            '{is_bot}',
            '{first_name}',
            '{last_name}',
            '{username}',
            '{language_code}',
            '{is_premium}'
        );
        """
        connection.execute(sql)
        connection.commit()
        connection.close()

    def insert_word(self, word, translation):
        connection = sqlite3.connect(f'{self.name}.sqlite3')
        sql = f"""
        INSERT OR IGNORE INTO words (
            word,
            translation
        ) VALUES (
            '{word}',
            '{translation}'
        );
        """
        connection.execute(sql)
        connection.commit()
        connection.close()

    def get_random_word(self):
        connection = sqlite3.connect(f'{self.name}.sqlite3')
        sql = """
        SELECT * FROM words ORDER BY RANDOM() LIMIT 1;
        """
        cursor = connection.execute(sql)
        for row in cursor:
            random_word = row
        connection.close()
        return random_word

    # def get_random_words(self, limit):
    #     connection = sqlite3.connect(f'{self.name}.sqlite3')
    #     sql = f"""
    #     SELECT * FROM words ORDER BY RANDOM() LIMIT {limit};
    #     """
    #     random_words = connection.execute(sql)
    #     print(random_words[0])
    #     connection.close()
    #     return random_words
