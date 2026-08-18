from database import connect


def create_promo(code, amount, uses):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO promo (code, amount, uses) VALUES (?, ?, ?)",
        (code, amount, uses)
    )

    conn.commit()
    conn.close()


def get_promo(code):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM promo WHERE code=?",
        (code,)
    )

    promo = cursor.fetchone()

    conn.close()

    return promo


def use_promo(code):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE promo SET uses = uses - 1 WHERE code=?",
        (code,)
    )

    conn.commit()
    conn.close()
