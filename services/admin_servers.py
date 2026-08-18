from services.servers import create_server


def give_server(user_id, plan):

    name = f"PulSar {plan}"

    create_server(
        user_id,
        name,
        plan
    )

    return (
        "✅ Сервер выдан!\n\n"
        f"👤 Пользователь: {user_id}\n"
        f"📦 Тариф: {plan}"
    )
