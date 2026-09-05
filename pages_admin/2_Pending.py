import streamlit as st
from utils.auth import require_role
from constants import ROLE_ADMIN
from db.payments import get_pending_fees

require_role([ROLE_ADMIN])

st.title("Fees Pending")

pending = get_pending_fees()
students_pending = [p for p in pending if p["payer_type"] == "student"]
gym_pending = [p for p in pending if p["payer_type"] == "gym"]

col_students, col_gym = st.columns(2)

with col_students:
    st.subheader("Students")
    if not students_pending:
        st.info("No pending student fees.")
    else:
        for person in students_pending:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(person["name"])
            with c2:
                st.write(f"₹{person['amount']}")

with col_gym:
    st.subheader("Gym Members")
    if not gym_pending:
        st.info("No pending gym fees.")
    else:
        for person in gym_pending:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(person["name"])
            with c2:
                st.write(f"₹{person['amount']}")