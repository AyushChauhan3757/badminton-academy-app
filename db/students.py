from db.connection import get_connection

def get_all_students():
    """Fetch all students, ordered by name."""
    conn = get_connection()
    result = conn.execute("SELECT id, name, admission_date, batch, timing, fees, is_custom_fee, guardian_name, phone FROM students ORDER BY name ASC")
    return result.rows