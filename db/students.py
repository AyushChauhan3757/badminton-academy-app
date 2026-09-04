from db.connection import get_connection

def get_all_students():
    """Fetch all students, ordered by name."""
    conn = get_connection()
    result = conn.execute("SELECT id, name, admission_date, batch, timing, fees, is_custom_fee, guardian_name, phone FROM students ORDER BY name ASC")
    return result.rows

def add_student(name, admission_date, batch, timing, fee, is_custom_fee, guardian_name, phone):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO students (name, admission_date, batch, timing, fees, is_custom_fee, guardian_name, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [name, admission_date, batch, timing, fee, int(is_custom_fee), guardian_name, phone],
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