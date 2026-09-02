import os
import libsql_client


def get_connection():
    """
    Returns a libSQL client connected to the Turso database.
    Reads credentials from environment variables (used by init_db.py)
    or Streamlit secrets (used by the app itself).
    """
    url = os.environ.get("TURSO_DATABASE_URL")
    auth_token = os.environ.get("TURSO_AUTH_TOKEN")

    if not url or not auth_token:
        import streamlit as st
        url = st.secrets["TURSO_DATABASE_URL"]
        auth_token = st.secrets["TURSO_AUTH_TOKEN"]

    return libsql_client.create_client_sync(
        url=url,
        auth_token=auth_token,
    )