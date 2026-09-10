import streamlit as st
from utils.auth import require_role
from constants import ROLE_ADMIN
from db.coaches import get_all_coaches, add_coach, update_coach, delete_coach
from db.salary import get_salary_status, clear_coach_salary
from utils.header import render_header

require_role([ROLE_ADMIN])

render_header("Coaches List")

if st.button("+ Add Coach"):
    st.session_state.show_add_coach = True

@st.dialog("Add Coach")
def add_coach_dialog():
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    salary = st.number_input("Salary", min_value=0, step=500)

    if st.button("Save"):
        if not name:
            st.error("Name is required.")
        else:
            add_coach(name, phone, salary)
            st.session_state.show_add_coach = False
            st.rerun()

if st.session_state.get("show_add_coach"):
    add_coach_dialog()


@st.dialog("Edit Coach")
def edit_coach_dialog(coach):
    name = st.text_input("Name", value=coach["name"])
    phone = st.text_input("Phone", value=coach["phone"])
    salary = st.number_input("Salary", min_value=0, step=500, value=coach["salary"])

    if st.button("Save Changes"):
        if not name:
            st.error("Name is required.")
        else:
            update_coach(coach["id"], name, phone, salary)
            st.session_state.edit_coach_id = None
            st.rerun()


@st.dialog("Delete Coach")
def delete_coach_dialog(coach):
    st.write(f"Are you sure you want to delete **{coach['name']}**?")
    col1, col2 = st.columns(2)
    if col1.button("Yes, Delete"):
        delete_coach(coach["id"])
        st.session_state.delete_coach_id = None
        st.rerun()
    if col2.button("Cancel"):
        st.session_state.delete_coach_id = None
        st.rerun()


@st.dialog("Confirm Salary Payment")
def mark_salary_paid_dialog(coach):
    st.write(f"Mark **{coach['name']}**'s salary of ₹{coach['salary']} as paid for this month?")
    col1, col2 = st.columns(2)
    if col1.button("Yes, Mark Paid"):
        clear_coach_salary(coach["id"], coach["name"], coach["salary"])
        st.session_state.mark_paid_coach_id = None
        st.rerun()
    if col2.button("Cancel"):
        st.session_state.mark_paid_coach_id = None
        st.rerun()


coaches = get_all_coaches()

if not coaches:
    st.info("No coaches added yet.")
else:
    for coach in coaches:
        cols = st.columns([0.25, 0.2, 0.15, 0.15, 0.125, 0.125])
        cols[0].write(coach["name"])
        cols[1].write(coach["phone"])
        cols[2].write(f"₹{coach['salary']}")

        paid = get_salary_status(coach["id"])
        if paid:
            cols[3].markdown("✅ Paid")
        else:
            if cols[3].button("🔴 Mark Paid", key=f"markpaid_{coach['id']}"):
                st.session_state.mark_paid_coach_id = coach["id"]

        if cols[4].button("Edit", key=f"edit_{coach['id']}"):
            st.session_state.edit_coach_id = coach["id"]
        if cols[5].button("Delete", key=f"delete_{coach['id']}"):
            st.session_state.delete_coach_id = coach["id"]

    if st.session_state.get("edit_coach_id"):
        coach = next((c for c in coaches if c["id"] == st.session_state.edit_coach_id), None)
        if coach:
            edit_coach_dialog(coach)

    if st.session_state.get("delete_coach_id"):
        coach = next((c for c in coaches if c["id"] == st.session_state.delete_coach_id), None)
        if coach:
            delete_coach_dialog(coach)

    if st.session_state.get("mark_paid_coach_id"):
        coach = next((c for c in coaches if c["id"] == st.session_state.mark_paid_coach_id), None)
        if coach:
            mark_salary_paid_dialog(coach)