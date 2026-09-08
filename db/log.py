from db.connection import get_connection

PAGE_SIZE = 20

def _base_query(category_filter=None):
    """
    Builds the merged UNION ALL query, optionally filtered by category.
    category_filter: None (all), 'fee' (fees only), or 'bill' (bills/salary only)
    """
    fee_select = """
        SELECT
            p.paid_on AS date,
            p.amount AS amount,
            'fee' AS category,
            p.payer_type AS payer_type,
            COALESCE(s.name, gm.name, 'Deleted student/member') AS description,
            p.created_at AS created_at
        FROM payments p
        LEFT JOIN students s ON p.payer_type = 'student' AND p.payer_id = s.id
        LEFT JOIN gym_members gm ON p.payer_type = 'gym' AND p.payer_id = gm.id
    """
    bill_select = """
        SELECT
            t.date AS date,
            t.amount AS amount,
            t.category AS category,
            NULL AS payer_type,
            t.description AS description,
            t.created_at AS created_at
        FROM transactions t
    """

    if category_filter == "fee":
        return f"SELECT * FROM ({fee_select})"
    elif category_filter == "bill":
        return f"SELECT * FROM ({bill_select})"
    else:
        return f"SELECT * FROM ({fee_select} UNION ALL {bill_select})"


def _apply_date_filter(query, start_date, end_date):
    """Appends a WHERE clause filtering on date, if start/end provided."""
    conditions = []
    if start_date:
        conditions.append(f"date >= '{start_date}'")
    if end_date:
        conditions.append(f"date <= '{end_date}'")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    return query


def get_log_page(page=1, page_size=PAGE_SIZE, category_filter=None, start_date=None, end_date=None):
    """
    Returns one page of the merged activity log (fee payments + transactions),
    most recent first. page is 1-indexed.
    category_filter: None (all), 'fee', or 'bill'
    start_date / end_date: ISO date strings ('YYYY-MM-DD') or None
    """
    conn = get_connection()
    offset = (page - 1) * page_size

    inner = f"SELECT * FROM ({_base_query(category_filter)})"
    inner = _apply_date_filter(inner, start_date, end_date)

    query = f"""
        {inner}
        ORDER BY created_at DESC, date DESC
        LIMIT ? OFFSET ?
    """
    result = conn.execute(query, [page_size, offset])
    columns = result.columns
    rows = [dict(zip(columns, row)) for row in result.rows]
    return rows


def get_log_total_count(category_filter=None, start_date=None, end_date=None):
    """Returns total row count for the given filters, for pagination controls."""
    conn = get_connection()
    inner = f"SELECT * FROM ({_base_query(category_filter)})"
    inner = _apply_date_filter(inner, start_date, end_date)
    query = f"SELECT COUNT(*) FROM ({inner})"
    result = conn.execute(query)
    return result.rows[0][0]