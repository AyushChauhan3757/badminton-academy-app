import streamlit as st
from datetime import datetime, timedelta
import pytz

from utils.ui_helpers import render_dialog_icon, render_dialog_message

# ⚠️ TEMPORARY DEV BYPASS — set to False before any real testing or deployment.
from constants import ROLE_ADMIN, ROLE_COACH
DEV_SKIP_LOGIN = True
DEV_SKIP_LOGIN_ROLE = ROLE_ADMIN # change to ROLE_COACH if you want to test coach view instead

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


# -------------------------------------------------------------------------
# Session Timeout popup — shown once, at the moment check_idle_timeout()
# detects the idle window has been exceeded. Replaces the old plain
# st.warning() with the icon-circle + centered message dialog pattern
# (see utils/ui_helpers.py's render_dialog_icon()/render_dialog_message(),
# CSS in utils/styling.py's apply_dialog_styles()). A single OK button
# closes it; since role/last_active are already cleared by the time this
# is called, the next page load has nothing left to detect, so this only
# ever fires once per timeout — no extra "already shown" flag needed.
# -------------------------------------------------------------------------
@st.dialog("Session Timeout")
def session_expired_dialog():
    render_dialog_icon("schedule", "info")
    render_dialog_message(
        "Session Expired",
        "You have been logged out due to inactivity.<br>Please login again to continue."
    )
    if st.button("OK", key="dlg_primary_session_expired_ok", use_container_width=True):
        st.rerun()


def check_idle_timeout():
    if st.session_state.role is not None and st.session_state.last_active is not None:
        idle_for = now_ist() - st.session_state.last_active
        if idle_for > timedelta(minutes=IDLE_TIMEOUT_MINUTES):
            st.session_state.role = None
            st.session_state.last_active = None
            session_expired_dialog()


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