import streamlit as st
from utils.auth import init_session, check_idle_timeout, logout, now_ist
from utils.styling import apply_theme

st.set_page_config(page_title="Avni Badminton Academy", page_icon="🏸", layout="wide")
apply_theme()

init_session()
check_idle_timeout()

if st.session_state.role is None:
    st.title("Avni Badminton Academy")

    with st.form("login_form"):
        role_choice = st.selectbox("Role", ["Admin", "Coach"])
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if role_choice == "Admin" and password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.role = "admin"
            st.session_state.last_active = now_ist()
            st.rerun()
        elif role_choice == "Coach" and password == st.secrets["COACH_PASSWORD"]:
            st.session_state.role = "coach"
            st.session_state.last_active = now_ist()
            st.rerun()
        else:
            st.error("Incorrect password.")

else:
    admin_pages = [
        st.Page("pages_admin/1_Overview.py", title="Overview"),
        st.Page("pages_admin/2_Pending.py", title="Fees Pending"),
        st.Page("pages_admin/3_Students.py", title="Students Roster"),
        st.Page("pages_admin/4_Coaches.py", title="Coaches List"),
        st.Page("pages_admin/5_Gym.py", title="Gym Roster"),
        st.Page("pages_admin/6_Log.py", title="Transaction Log"),
    ]

    coach_pages = [
        st.Page("pages_coach/1_Pending.py", title="Fees Pending"),
        st.Page("pages_coach/2_Students.py", title="Students Roster"),
        st.Page("pages_coach/3_Gym.py", title="Gym Roster"),
    ]

    pages = admin_pages if st.session_state.role == "admin" else coach_pages

    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state.role}**")
        if st.button("Logout"):
            logout()
            st.rerun()

    nav = st.navigation(pages)
    nav.run()