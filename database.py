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
