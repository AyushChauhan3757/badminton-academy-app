from db.connection import get_connection
from utils.auth import now_ist
from constants import GYM_FEE
from datetime import date

def get_pending_fees(month=None, year=None):
    """
    Returns a combined, name-sorted list of students and gym members
    who have NOT paid for the given month/year.
    Defaults to the current IST month/year if not specified.
    Each item: {'payer_type', 'payer_id', 'name', 'amount'}
    """
    if month is None or year is None:
        today = now_ist()
        month = today.month
        year = today.year

    conn = get_connection()

    students_result = conn.execute(
        """
        SELECT s.id, s.name, s.fees
        FROM students s
        WHERE NOT EXISTS (
            SELECT 1 FROM payments p
            WHERE p.payer_type = 'student'
              AND p.payer_id = s.id
              AND p.month = ?
              AND p.year = ?
        )
        """,
        [month, year],
    )
    students_columns = students_result.columns
    students_rows = students_result.rows

    gym_result = conn.execute(
        """
        SELECT g.id, g.name
        FROM gym_members g
        WHERE NOT EXISTS (
            SELECT 1 FROM payments p
            WHERE p.payer_type = 'gym'
              AND p.payer_id = g.id
              AND p.month = ?
              AND p.year = ?
        )
        """,
        [month, year],
    )
    gym_columns = gym_result.columns
    gym_rows = gym_result.rows

    pending = []

    for row in students_rows:
        record = dict(zip(students_columns, row))
        pending.append({
            "payer_type": "student",
            "payer_id": record["id"],
            "name": record["name"],
            "amount": record["fees"],
        })

    for row in gym_rows:
        record = dict(zip(gym_columns, row))
        pending.append({
            "payer_type": "gym",
            "payer_id": record["id"],
            "name": record["name"],
            "amount": GYM_FEE,
        })

    pending.sort(key=lambda x: x["name"].lower())
    return pending


def mark_fee_paid(payer_type, payer_id, amount, month, year, marked_by):
    """
    Records a fee payment. month/year are the period the payment is FOR
    (may be current month, or a prior month for late payments).
    paid_on is always today (IST) — the actual date paid.
    """
    conn = get_connection()
    today = now_ist().date()
    conn.execute(
        """
        INSERT INTO payments (payer_type, payer_id, month, year, amount, paid_on, marked_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [payer_type, payer_id, month, year, amount, str(today), marked_by],
    )


def get_paid_fees(month=None, year=None):
    """
    Returns a combined, name-sorted list of students and gym members
    who HAVE paid for the given month/year.
    Defaults to the current IST month/year if not specified.
    Each item: {'payer_type', 'payer_id', 'name', 'amount', 'paid_on', 'marked_by'}
    """
    if month is None or year is None:
        today = now_ist()
        month = today.month
        year = today.year

    conn = get_connection()

    students_result = conn.execute(
        """
        SELECT s.id, s.name, p.amount, p.paid_on, p.marked_by
        FROM payments p
        JOIN students s ON s.id = p.payer_id
        WHERE p.payer_type = 'student'
          AND p.month = ?
          AND p.year = ?
        """,
        [month, year],
    )
    students_columns = students_result.columns
    students_rows = students_result.rows

    gym_result = conn.execute(
        """
        SELECT g.id, g.name, p.amount, p.paid_on, p.marked_by
        FROM payments p
        JOIN gym_members g ON g.id = p.payer_id
        WHERE p.payer_type = 'gym'
          AND p.month = ?
          AND p.year = ?
        """,
        [month, year],
    )
    gym_columns = gym_result.columns
    gym_rows = gym_result.rows

    paid = []

    for row in students_rows:
        record = dict(zip(students_columns, row))
        paid.append({
            "payer_type": "student",
            "payer_id": record["id"],
            "name": record["name"],
            "amount": record["amount"],
            "paid_on": record["paid_on"],
            "marked_by": record["marked_by"],
        })

    for row in gym_rows:
        record = dict(zip(gym_columns, row))
        paid.append({
            "payer_type": "gym",
            "payer_id": record["id"],
            "name": record["name"],
            "amount": record["amount"],
            "paid_on": record["paid_on"],
            "marked_by": record["marked_by"],
        })

    paid.sort(key=lambda x: x["name"].lower())
    return paid

def get_missed_last_month():
    """
    Returns a merged, name-sorted list of students and gym members
    who have NO payments row for the PREVIOUS IST month/year.
    Same shape as get_pending_fees(), but always targets last month
    (not current), since this is a separate query per spec.
    """
    now = now_ist()
    month = now.month
    year = now.year

    # Roll back one month (handle January -> December of prior year)
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    conn = get_connection()

    # Students missing a payment row for prev_month/prev_year
    student_result = conn.execute(
        """
        SELECT s.id, s.name, s.fees
        FROM students s
        WHERE NOT EXISTS (
            SELECT 1 FROM payments p
            WHERE p.payer_type = 'student'
              AND p.payer_id = s.id
              AND p.month = ?
              AND p.year = ?
        )
        """,
        (prev_month, prev_year)
    )
    students = [
        {'payer_type': 'student', 'payer_id': row[0], 'name': row[1], 'amount': row[2]}
        for row in student_result.rows
    ]

    # Gym members missing a payment row for prev_month/prev_year
    gym_result = conn.execute(
        """
        SELECT g.id, g.name
        FROM gym_members g
        WHERE NOT EXISTS (
            SELECT 1 FROM payments p
            WHERE p.payer_type = 'gym'
              AND p.payer_id = g.id
              AND p.month = ?
              AND p.year = ?
        )
        """,
        (prev_month, prev_year)
    )
    gym_members = [
        {'payer_type': 'gym', 'payer_id': row[0], 'name': row[1], 'amount': GYM_FEE}
        for row in gym_result.rows
    ]

    combined = students + gym_members
    combined.sort(key=lambda x: x['name'])
    return combined, prev_month, prev_year