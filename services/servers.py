from database import (
    add_server,
    get_servers,
    update_server_status
)


def create_server(user_id, name, plan):
    add_server(
        user_id,
        name,
        plan
    )


def user_servers(user_id):
    return get_servers(user_id)


def start_server(server_id):
    update_server_status(
        server_id,
        "ON"
    )


def stop_server(server_id):
    update_server_status(
        server_id,
        "OFF"
    )


def restart_server(server_id):
    update_server_status(
        server_id,
        "RESTART"
    )
