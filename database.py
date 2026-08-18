import sqlite3
from datetime import datetime


DB = "pulsar.db"


def connect():
    return sqlite3.connect(DB)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Пользователи
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0
    )
    """)

    # Промокоды
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS promo (
        code TEXT PRIMARY KEY,
        amount INTEGER,
        uses INTEGER DEFAULT 1
    )
    """)

    # Серверы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        plan TEXT,
        status TEXT DEFAULT 'OFF',
        created TEXT,
        days INTEGER DEFAULT 30
    )
    """)

    conn.commit()
    conn.close()


# Пользователи

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

    return result[0] if result else 0



def add_balance(user_id, amount):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE id=?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()



# Серверы

def add_server(user_id, name, plan):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO servers
        (user_id, name, plan, status, created, days)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            name,
            plan,
            "OFF",
            datetime.now().strftime("%d.%m.%Y"),
            30
        )
    )

    conn.commit()
    conn.close()



def get_servers(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, plan, status, created, days
        FROM servers
        WHERE user_id=?
        """,
        (user_id,)
    )

    servers = cursor.fetchall()

    conn.close()

    return servers



def update_server_status(server_id, status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE servers SET status=? WHERE id=?",
        (status, server_id)
    )

    conn.commit()
    conn.close()
