import sqlite3
import logging

db = sqlite3.connect('database/bot.db')

def setup_database():
    with db as conn :
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id INTEGER PRIMARY KEY,
                     coin INTEGER DEFAULT 0,
                     day_traffic_limit INTEGER DEFAULT 5,
                     used_traffic INTEGER DEFAULT 0,
                     large_file BOOLEAN DEFAULT TRUE,
                     join_date TEXT DEFAULT CURRENT_TIMESTAMP)
                     ''')
        conn.commit()
    logging.info('Database setup OK')


def create_user (user):
    with db as conn:
        conn.execute('''INSERT OR IGNORE INTO users (user_id)
                        VALUES(?)
                     ''', (user,))
        conn.commit()