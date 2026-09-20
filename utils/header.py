import streamlit as st
from utils.auth import logout, now_ist
from utils.ui_helpers import render_dialog_icon, render_dialog_message


# -------------------------------------------------------------------------
# Logout Confirmation popup — replaces the previous instant-logout
# behavior with a confirm step. Uses the same icon-circle + centered
# message + button-variant dialog pattern as the rest of the app (see
# utils/ui_helpers.py's render_dialog_icon()/render_dialog_message(),
# CSS in utils/styling.py's apply_dialog_styles()). Keyed by title so
# a call from any page's header gets unique widget keys.
# -------------------------------------------------------------------------
def _confirm_logout_dialog(title):
    @st.dialog("Logout Confirmation")
    def confirm_logout():
        render_dialog_icon("logout", "info")
        render_dialog_message("Logout?", "Are you sure you want to logout?")
        col_cancel, col_logout = st.columns(2)
        if col_cancel.button("Cancel", key=f"dlg_secondary_logout_cancel_{title}", use_container_width=True):
            st.rerun()
        if col_logout.button("Logout", key=f"dlg_primary_logout_confirm_{title}", use_container_width=True):
            logout()
            st.rerun()

    confirm_logout()


def render_header(title):
    """
    Renders the page header: the page's own title on the left,
    and "Welcome, {Role}" + date/time + a Logout button on the right,
    all in a single row. Call this at the top of every page file
    instead of st.title(...).
    """
    header_row = st.container(key="page_header")
    col_title, col_welcome, col_logout = header_row.columns([5, 3, 1])

    with col_title:
        st.title(title)

    with col_welcome:
        st.markdown(
            f"""
            <div class="header-welcome-block" style="text-align:right; padding-top:1.6rem;">
                <span style="font-weight:700; font-size:1.05rem; color:#14304F;">
                    Welcome, {st.session_state.role.capitalize()}
                </span><br>
                <span style="font-size:0.85rem; color:#6B7280;">
                    {now_ist().strftime('%A, %d %B %Y | %I:%M %p')}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_logout:
        st.markdown("<div style='padding-top:1.6rem;'></div>", unsafe_allow_html=True)
        if st.button("Logout", key=f"header_logout_btn_{title}"):
            _confirm_logout_dialog(title)