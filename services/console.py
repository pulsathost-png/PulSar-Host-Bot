from database import connect


def get_server(server_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM servers WHERE id=?",
        (server_id,)
    )

    server = cursor.fetchone()

    conn.close()

    return server


def send_command(server_id, command):
    # Пока тестовая консоль
    # позже подключим настоящий сервер

    return (
        f"📟 Сервер ID: {server_id}\n"
        f"▶ Команда: {command}\n\n"
        f"✅ Команда выполнена"
    )
