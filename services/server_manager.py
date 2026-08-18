from datetime import datetime
from database import update_server_status, connect


def start(server_id):

    update_server_status(
        server_id,
        "ON"
    )

    save_log(
        server_id,
        "Сервер запущен"
    )

    return "🟢 Сервер запущен"



def stop(server_id):

    update_server_status(
        server_id,
        "OFF"
    )

    save_log(
        server_id,
        "Сервер остановлен"
    )

    return "🔴 Сервер остановлен"



def restart(server_id):

    update_server_status(
        server_id,
        "RESTART"
    )

    save_log(
        server_id,
        "Сервер перезапущен"
    )

    update_server_status(
        server_id,
        "ON"
    )

    return "🔄 Сервер перезапущен"



def save_log(server_id, text):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id INTEGER,
        text TEXT,
        date TEXT
    )
    """)


    cursor.execute(
        """
        INSERT INTO logs
        (server_id, text, date)
        VALUES (?, ?, ?)
        """,
        (
            server_id,
            text,
            datetime.now().strftime("%d.%m.%Y %H:%M")
        )
    )


    conn.commit()
    conn.close()
