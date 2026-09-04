import streamlit as st
from datetime import datetime
from utils.auth import require_role
from constants import ROLE_ADMIN
from db.gym_members import (
    get_all_gym_members,
    add_gym_member,
    update_gym_member,
    delete_gym_member,
)

require_role([ROLE_ADMIN])

st.title("Gym Roster")


@st.dialog("Add Gym Member")
def add_gym_member_dialog():
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    joining_date = st.date_input("Joining Date", format="DD/MM/YYYY")

    if st.button("Add", type="primary"):
        if not name:
            st.error("Name is required.")
        else:
            add_gym_member(name, phone, joining_date)
            st.rerun()


@st.dialog("Edit Gym Member")
def edit_gym_member_dialog(member):
    name = st.text_input("Name", value=member["name"])
    phone = st.text_input("Phone", value=member["phone"] or "")
    joining_date = st.date_input(
        "Joining Date",
        value=member["joining_date"],
        format="DD/MM/YYYY",
    )

    if st.button("Save", type="primary"):
        if not name:
            st.error("Name is required.")
        else:
            update_gym_member(member["id"], name, phone, joining_date)
            st.rerun()


@st.dialog("Delete Gym Member")
def delete_gym_member_dialog(member):
    st.write(f"Are you sure you want to delete **{member['name']}**?")
    col1, col2 = st.columns(2)
    if col1.button("Yes, Delete", type="primary"):
        delete_gym_member(member["id"])
        st.rerun()
    if col2.button("Cancel"):
        st.rerun()


if st.button("+ Add Gym Member"):
    add_gym_member_dialog()

gym_members = get_all_gym_members()

search = st.text_input("Search by name")

col1, col2 = st.columns(2)
start_date = col1.date_input("Joining date from", value=None, format="DD/MM/YYYY")
end_date = col2.date_input("Joining date to", value=None, format="DD/MM/YYYY")

filtered = gym_members
if search:
    filtered = [g for g in filtered if search.lower() in g["name"].lower()]
if start_date:
    filtered = [
        g for g in filtered
        if datetime.strptime(g["joining_date"], "%Y-%m-%d").date() >= start_date
    ]
if end_date:
    filtered = [
        g for g in filtered
        if datetime.strptime(g["joining_date"], "%Y-%m-%d").date() <= end_date
    ]

if not filtered:
    st.info("No gym members added yet." if not gym_members else "No matches found.")
else:
    header_cols = st.columns([3, 2, 2, 1, 1])
    header_cols[0].markdown("**Name**")
    header_cols[1].markdown("**Phone**")
    header_cols[2].markdown("**Joining Date**")

    for member in filtered:
        row_cols = st.columns([3, 2, 2, 1, 1])
        row_cols[0].write(member["name"])
        row_cols[1].write(member["phone"] or "—")
        row_cols[2].write(member["joining_date"])
        if row_cols[3].button("Edit", key=f"edit_{member['id']}"):
            edit_gym_member_dialog(member)
        if row_cols[4].button("Delete", key=f"delete_{member['id']}"):
            delete_gym_member_dialog(member)