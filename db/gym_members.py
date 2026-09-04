from db.connection import get_connection


def get_all_gym_members():
    conn = get_connection()
    result = conn.execute("SELECT * FROM gym_members ORDER BY name ASC")
    columns = result.columns
    rows = result.rows
    return [dict(zip(columns, row)) for row in rows]


def add_gym_member(name, phone, joining_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO gym_members (name, phone, joining_date) VALUES (?, ?, ?)",
        [name, phone, str(joining_date)],
    )


def update_gym_member(member_id, name, phone, joining_date):
    conn = get_connection()
    conn.execute(
        "UPDATE gym_members SET name = ?, phone = ?, joining_date = ? WHERE id = ?",
        [name, phone, str(joining_date), member_id],
    )


def delete_gym_member(member_id):
    conn = get_connection()
    conn.execute("DELETE FROM gym_members WHERE id = ?", [member_id])