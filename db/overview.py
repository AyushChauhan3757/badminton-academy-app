# db/overview.py

from db.connection import get_connection
from utils.auth import now_ist


def get_totals():
    """
    Returns a dict with lifetime and this-month totals:
    {
        'lifetime_received': int,
        'lifetime_paid': int,
        'lifetime_profit': int,
        'month_received': int,
        'month_paid': int,
        'month_profit': int,
    }
    """
    conn = get_connection()
    today = now_ist()
    current_month = today.month
    current_year = today.year

    # Lifetime received (all fees ever)
    result = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM payments")
    lifetime_received = result.rows[0][0]

    # Lifetime paid (all salary + expenses ever)
    result = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions")
    lifetime_paid = result.rows[0][0]

    lifetime_profit = lifetime_received - lifetime_paid

    # This month received
    result = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM payments WHERE month = ? AND year = ?",
        [current_month, current_year]
    )
    month_received = result.rows[0][0]

    # This month paid
    result = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?",
        [f"{current_month:02d}", str(current_year)]
    )
    month_paid = result.rows[0][0]

    month_profit = month_received - month_paid

    return {
        'lifetime_received': lifetime_received,
        'lifetime_paid': lifetime_paid,
        'lifetime_profit': lifetime_profit,
        'month_received': month_received,
        'month_paid': month_paid,
        'month_profit': month_profit,
    }


def add_transaction(description, amount):
    """
    Inserts a manual expense transaction (bills etc.).
    Expense-only, per spec — no income entries via this function.
    """
    conn = get_connection()
    now = now_ist()
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    conn.execute("""
        INSERT INTO transactions (type, category, amount, date, description, created_at)
        VALUES ('expense', 'expense', ?, ?, ?, ?)
    """, [amount, today, description, timestamp])


def get_recent_log(limit=10):
    """
    Returns the most recent `limit` rows from the merged fee-payments +
    transactions feed, most recent first. Each row is a dict:
    {
        'date': str,
        'amount': int,
        'category': str,       # 'fee' | 'salary' | 'expense'
        'description': str,    # resolved name (fee) or transaction description
    }
    """
    conn = get_connection()

    result = conn.execute("""
        SELECT p.paid_on AS date, p.amount, 'fee' AS category,
               COALESCE(s.name, g.name) AS description, p.created_at AS created_at
        FROM payments p
        LEFT JOIN students s ON p.payer_type = 'student' AND p.payer_id = s.id
        LEFT JOIN gym_members g ON p.payer_type = 'gym' AND p.payer_id = g.id
        UNION ALL
        SELECT date, amount, category, description, created_at
        FROM transactions
        ORDER BY created_at DESC, date DESC
        LIMIT ?
    """, [limit])

    columns = result.columns
    rows = [dict(zip(columns, row)) for row in result.rows]
    return rows