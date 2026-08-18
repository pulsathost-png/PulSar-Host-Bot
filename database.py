import sqlite3

DB = "pulsar.db"


def connect():
    return sqlite3.connect(DB)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS promo (
        code TEXT PRIMARY KEY,
        amount INTEGER,
        uses INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        status TEXT DEFAULT 'OFF'
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
        (user_id, username)
    )

    conn.commit()
    conn.close()


def get_balance(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0


def add_balance(user_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE id=?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()
