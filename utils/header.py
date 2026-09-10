import streamlit as st
from utils.auth import logout, now_ist


def render_header(title):
    """
    Renders the page header: the page's own title on the left,
    and "Welcome, {Role}" + date/time + a Logout button on the right,
    all in a single row. Call this at the top of every page file
    instead of st.title(...).
    """
    col_title, col_welcome, col_logout = st.columns([5, 3, 1])

    with col_title:
        st.title(title)

    with col_welcome:
        st.markdown(
            f"""
            <div style="text-align:right; padding-top:1.6rem;">
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
            logout()
            st.rerun()