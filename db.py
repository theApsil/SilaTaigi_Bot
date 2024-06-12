import sqlite3


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            bonus_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def add_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


def update_user_bonus(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET bonus_count = bonus_count + 1 WHERE user_id = ?', (user_id,))
    cursor.execute('SELECT bonus_count FROM users WHERE user_id = ?', (user_id,))
    bonus_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return bonus_count


def get_user_bonus(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT bonus_count FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def reset_user_bonus(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET bonus_count = 0 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
