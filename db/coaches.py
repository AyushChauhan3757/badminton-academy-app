from db.connection import get_connection


def get_all_coaches():
    conn = get_connection()
    result = conn.execute("SELECT id, name, phone, salary FROM coaches")
    columns = result.columns
    rows = result.rows
    return [dict(zip(columns, row)) for row in rows]


def add_coach(name, phone, salary):
    conn = get_connection()
    conn.execute(
        "INSERT INTO coaches (name, phone, salary) VALUES (?, ?, ?)",
        [name, phone, salary]
    )


def update_coach(coach_id, name, phone, salary):
    conn = get_connection()
    conn.execute(
        "UPDATE coaches SET name = ?, phone = ?, salary = ? WHERE id = ?",
        [name, phone, salary, coach_id]
    )


def delete_coach(coach_id):
    conn = get_connection()
    conn.execute(
        "DELETE FROM coaches WHERE id = ?",
        [coach_id]
    )