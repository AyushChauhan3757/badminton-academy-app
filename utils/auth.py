import streamlit as st
from datetime import datetime, timedelta
import pytz

# ⚠️ TEMPORARY DEV BYPASS — set to False before any real testing or deployment.
from constants import ROLE_ADMIN, ROLE_COACH
DEV_SKIP_LOGIN = True
DEV_SKIP_LOGIN_ROLE = ROLE_COACH  # change to ROLE_COACH if you want to test coach view instead

IST = pytz.timezone("Asia/Kolkata")
IDLE_TIMEOUT_MINUTES = 30


def now_ist():
    return datetime.now(IST)


def init_session():
    if DEV_SKIP_LOGIN and "role" not in st.session_state:
        st.session_state.role = DEV_SKIP_LOGIN_ROLE
        st.session_state.last_active = now_ist()
        return
    if "role" not in st.session_state:
        st.session_state.role = None
    if "last_active" not in st.session_state:
        st.session_state.last_active = None


def check_idle_timeout():
    if st.session_state.role is not None and st.session_state.last_active is not None:
        idle_for = now_ist() - st.session_state.last_active
        if idle_for > timedelta(minutes=IDLE_TIMEOUT_MINUTES):
            st.session_state.role = None
            st.session_state.last_active = None
            st.warning("Session timed out due to inactivity. Please log in again.")


def require_role(allowed_roles):
    """Call at the top of every page. Stops the page from rendering
    if the user isn't logged in with an allowed role."""
    init_session()
    check_idle_timeout()

    if st.session_state.role not in allowed_roles:
        st.error("You must be logged in with the correct role to view this page.")
        st.stop()

    st.session_state.last_active = now_ist()


def logout():
    st.session_state.role = None
    st.session_state.last_active = None