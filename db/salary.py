from db.connection import get_connection
from utils.auth import now_ist


def get_salary_status(coach_id, month=None, year=None):
    """
    Returns True if the given coach has a salary_payouts row for the given
    month/year (i.e. already paid), False otherwise.
    Defaults to current IST month/year if not provided.
    """
    if month is None or year is None:
        today = now_ist()
        month = today.month
        year = today.year

    conn = get_connection()
    result = conn.execute(
        "SELECT id FROM salary_payouts WHERE coach_id = ? AND month = ? AND year = ?",
        (coach_id, month, year)
    )
    return len(result.rows) > 0

def clear_coach_salary(coach_id, coach_name, salary_amount, month=None, year=None):
    """
    Marks a coach's salary as paid for the given month/year.
    Inserts into salary_payouts AND transactions (dual-write per spec).
    Defaults to current IST month/year if not provided.
    """
    if month is None or year is None:
        today = now_ist()
        month = today.month
        year = today.year

    today_date = now_ist().date().isoformat()

    conn = get_connection()
    conn.execute(
        "INSERT INTO salary_payouts (coach_id, month, year, amount, paid_on) VALUES (?, ?, ?, ?, ?)",
        (coach_id, month, year, salary_amount, today_date)
    )
    conn.execute(
        "INSERT INTO transactions (type, category, amount, date, description) VALUES (?, ?, ?, ?, ?)",
        ('expense', 'salary', salary_amount, today_date, coach_name)
    )