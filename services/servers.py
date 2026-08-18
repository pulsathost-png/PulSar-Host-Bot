from database import connect


def create_server(user_id, name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO servers (user_id, name, status)
        VALUES (?, ?, ?)
        """,
        (user_id, name, "OFF")
    )

    conn.commit()
    conn.close()


def get_servers(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, status FROM servers WHERE user_id=?",
        (user_id,)
    )

    servers = cursor.fetchall()

    conn.close()

    return servers


def start_server(server_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE servers SET status=? WHERE id=?",
        ("ON", server_id)
    )

    conn.commit()
    conn.close()


def stop_server(server_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE servers SET status=? WHERE id=?",
        ("OFF", server_id)
    )

    conn.commit()
    conn.close()
