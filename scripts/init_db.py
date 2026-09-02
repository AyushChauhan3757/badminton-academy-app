"""
One-time (but safe to re-run) script to create all tables in the Turso database.
Reads TURSO_DATABASE_URL and TURSO_AUTH_TOKEN from environment variables.
Run with: python scripts/init_db.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_connection


def main():
    client = get_connection()

    with open(os.path.join(os.path.dirname(__file__), "..", "db", "schema.sql")) as f:
        schema_sql = f.read()

    # Split on semicolons to run each statement separately
    statements = [s.strip() for s in schema_sql.split(";") if s.strip()]

    for stmt in statements:
        client.execute(stmt)
        print(f"Ran: {stmt[:60]}...")

    print("\nAll tables created successfully.")
    client.close()


if __name__ == "__main__":
    main()