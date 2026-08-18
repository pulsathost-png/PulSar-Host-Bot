from database import connect
from datetime import datetime


def save_console_log(server_id, command):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS console_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id INTEGER,
        command TEXT,
        date TEXT
    )
    """)

    cursor.execute(
        """
        INSERT INTO console_logs
        (server_id, command, date)
        VALUES (?, ?, ?)
        """,
        (
            server_id,
            command,
            datetime.now().strftime("%d.%m.%Y %H:%M")
        )
    )

    conn.commit()
    conn.close()



def execute_command(server_id, command):

    save_console_log(
        server_id,
        command
    )

    # Пока тестовая обработка
    if command == "status":
        return "🟢 Сервер работает\nИгроков: 0"

    elif command == "stop":
        return "⏹ Сервер остановлен"

    elif command == "restart":
        return "🔄 Сервер перезапущен"

    else:
        return (
            f"📟 Выполнена команда:\n"
            f"{command}"
        )
