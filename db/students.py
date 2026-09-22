from db.connection import get_connection
from utils.auth import now_ist

def get_all_students():
    """Fetch all students, ordered by name."""
    conn = get_connection()
    result = conn.execute("SELECT id, name, admission_date, batch, timing, fees, is_custom_fee, guardian_name, phone FROM students ORDER BY name ASC")
    return result.rows

def add_student(name, admission_date, batch, timing, fee, is_custom_fee, guardian_name, phone):
    conn = get_connection()
    result = conn.execute(
        """
        INSERT INTO students (name, admission_date, batch, timing, fees, is_custom_fee, guardian_name, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [name, admission_date, batch, timing, fee, int(is_custom_fee), guardian_name, phone],
    )

    student_id = result.last_insert_rowid

    now = now_ist()
    conn.execute(
        """
        INSERT INTO payments (payer_type, payer_id, month, year, amount, paid_on, marked_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        ["student", student_id, now.month, now.year, fee, str(admission_date), "admin", now.strftime("%Y-%m-%d %H:%M:%S")],
    )

def update_student(student_id, name, admission_date, batch, timing, fee, is_custom_fee, guardian_name, phone):
    conn = get_connection()
    conn.execute(
        """
        UPDATE students
        SET name = ?, admission_date = ?, batch = ?, timing = ?, fees = ?,
            is_custom_fee = ?, guardian_name = ?, phone = ?
        WHERE id = ?
        """,
        [name, admission_date, batch, timing, fee, int(is_custom_fee), guardian_name, phone, student_id],
    )

def delete_student(student_id):
    conn = get_connection()
    conn.execute("DELETE FROM students WHERE id = ?", [student_id])