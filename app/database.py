import sqlite3

def start_db():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            userid INTEGER UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, user_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    try:
        curr.execute('INSERT INTO users (username, userid) VALUES (?, ?)', (username, user_id))
    except:
        pass
    conn.commit()
    conn.close()