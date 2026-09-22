from datetime import date, datetime

import streamlit as st

from constants import ROLE_ADMIN
from db.gym_members import (
    add_gym_member,
    delete_gym_member,
    get_all_gym_members,
    update_gym_member,
)
from utils.auth import require_role
from utils.header import render_header
from utils.ui_helpers import render_dialog_icon, render_dialog_message, queue_toast

require_role([ROLE_ADMIN])

render_header("Gym Roster")

PAGE_SIZE = 10


@st.dialog("Add Gym Member")
def add_gym_member_dialog():
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    joining_date = st.date_input("Joining Date", value=date.today(), format="DD/MM/YYYY")

    b1, b2 = st.columns(2)
    if b1.button("Cancel", key="dlg_secondary_addgym_cancel", use_container_width=True):
        st.rerun()
    if b2.button("Add Gym Member", key="dlg_primary_addgym_save", use_container_width=True):
        if not name.strip():
            st.error("Name is required.")
        else:
            add_gym_member(name.strip(), phone.strip(), str(joining_date))
            queue_toast("Gym Member Added", name.strip())
            st.rerun()


with st.container(key="students_top_row"):
    col_search, col_add = st.columns([4, 1])
    with col_search:
        search_name = st.text_input("Search by name", placeholder="Search by name", label_visibility="collapsed")
    with col_add:
        if st.button("+ Add Gym Member", key="btn_add_gym", use_container_width=True):
            add_gym_member_dialog()

with st.container(key="students_filters_row"):
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        start_date = st.date_input("Joining date from", value=None, format="DD/MM/YYYY")
    with fcol2:
        end_date = st.date_input("Joining date to", value=None, format="DD/MM/YYYY")

gym_members = get_all_gym_members()

if search_name:
    gym_members = [g for g in gym_members if search_name.lower() in g["name"].lower()]
if start_date:
    gym_members = [
        g for g in gym_members
        if datetime.strptime(g["joining_date"], "%Y-%m-%d").date() >= start_date
    ]
if end_date:
    gym_members = [
        g for g in gym_members
        if datetime.strptime(g["joining_date"], "%Y-%m-%d").date() <= end_date
    ]

filter_signature = (search_name, start_date, end_date)
if st.session_state.get("gym_filter_signature") != filter_signature:
    st.session_state["gym_filter_signature"] = filter_signature
    st.session_state["gym_page"] = 1

if "gym_page" not in st.session_state:
    st.session_state["gym_page"] = 1

total_members = len(gym_members)
total_pages = max(1, (total_members + PAGE_SIZE - 1) // PAGE_SIZE)
st.session_state["gym_page"] = min(st.session_state["gym_page"], total_pages)
current_page = st.session_state["gym_page"]

start_idx = (current_page - 1) * PAGE_SIZE
end_idx = start_idx + PAGE_SIZE
paginated_members = gym_members[start_idx:end_idx]

st.markdown("---")


@st.dialog("Edit Gym Member")
def edit_gym_member_dialog(member):
    name = st.text_input("Name", value=member["name"])
    phone = st.text_input("Phone", value=member["phone"] or "")
    joining_date = st.date_input(
        "Joining Date",
        value=date.fromisoformat(member["joining_date"]),
        format="DD/MM/YYYY",
    )

    b1, b2 = st.columns(2)
    if b1.button("Cancel", key=f"dlg_secondary_updgym_cancel_{member['id']}", use_container_width=True):
        st.rerun()
    if b2.button("Save Changes", key=f"dlg_primary_updgym_save_{member['id']}", use_container_width=True):
        if not name.strip():
            st.error("Name is required.")
        else:
            update_gym_member(member["id"], name.strip(), phone.strip(), str(joining_date))
            queue_toast("Gym Member Updated", name.strip())
            st.rerun()


@st.dialog("Delete Gym Member")
def delete_gym_member_dialog(member):
    render_dialog_icon("delete", "danger")
    render_dialog_message(
        "Delete Record?",
        "This action cannot be undone.<br>"
        f"Are you sure you want to delete <b>{member['name']}</b>'s record?"
    )
    col_cancel, col_delete = st.columns(2)
    if col_cancel.button("Cancel", key=f"dlg_secondary_delgym_{member['id']}", use_container_width=True):
        st.rerun()
    if col_delete.button("Delete", key=f"dlg_danger_delgym_{member['id']}", use_container_width=True):
        delete_gym_member(member["id"])
        queue_toast("Record Deleted", member["name"], kind="danger")
        st.rerun()


if paginated_members:
    col_widths = [2.2, 1.6, 1.6, 1]
    headers = ["Name", "Phone", "Joining Date", "Actions"]

    with st.container(key="card_gym_roster"):
        with st.container(key="table_gym_roster"):
            with st.container(key="theader_gym_roster"):
                header_cols = st.columns(col_widths)
                for col, h in zip(header_cols, headers):
                    col.markdown(f'<span class="table-header">{h}</span>', unsafe_allow_html=True)

            for m in paginated_members:
                row_cols = st.columns(col_widths)
                row_cols[0].markdown(m["name"])
                row_cols[1].markdown(m["phone"] or "—")
                row_cols[2].markdown(date.fromisoformat(m["joining_date"]).strftime("%d/%m/%Y"))
                with row_cols[3]:
                    action_cols = st.columns(2)
                    if action_cols[0].button(":material/edit:", key=f"edit_{m['id']}", help="Edit"):
                        edit_gym_member_dialog(m)
                    if action_cols[1].button(":material/delete:", key=f"delete_{m['id']}", help="Delete"):
                        delete_gym_member_dialog(m)

    with st.container(key="pagination_gym"):
        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            if st.button("← Previous", key="gym_prev_page", disabled=(current_page <= 1)):
                st.session_state["gym_page"] = current_page - 1
                st.rerun()
        with pcol2:
            st.markdown(f"<div class='pagination-label'>Page {current_page} of {total_pages}</div>", unsafe_allow_html=True)
        with pcol3:
            if st.button("Next →", key="gym_next_page", disabled=(current_page >= total_pages)):
                st.session_state["gym_page"] = current_page + 1
                st.rerun()
else:
    st.info("No gym members added yet." if total_members == 0 else "No gym members match the current filters.")