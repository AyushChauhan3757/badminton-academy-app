import streamlit as st

from constants import ROLE_ADMIN
from db.coaches import add_coach, delete_coach, get_all_coaches, update_coach
from utils.auth import require_role
from utils.header import render_header
from utils.ui_helpers import render_dialog_icon, render_dialog_message, queue_toast

require_role([ROLE_ADMIN])

render_header("Coaches List")


@st.dialog("Add Coach")
def add_coach_dialog():
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    salary = st.number_input("Salary", min_value=0, step=500)

    b1, b2 = st.columns(2)
    if b1.button("Cancel", key="dlg_secondary_addcoach_cancel", use_container_width=True):
        st.rerun()
    if b2.button("Add Coach", key="dlg_primary_addcoach_save", use_container_width=True):
        if not name.strip():
            st.error("Name is required.")
        else:
            add_coach(name.strip(), phone.strip(), salary)
            queue_toast("Coach Added", name.strip())
            st.rerun()


with st.container(key="students_top_row"):
    col_search, col_add = st.columns([4, 1])
    with col_search:
        search_name = st.text_input("Search by name", placeholder="Search by name", label_visibility="collapsed")
    with col_add:
        if st.button("+ Add Coach", key="btn_add_coach", use_container_width=True):
            add_coach_dialog()

coaches = get_all_coaches()

if search_name:
    coaches = [c for c in coaches if search_name.lower() in c["name"].lower()]

st.markdown("---")


@st.dialog("Edit Coach")
def edit_coach_dialog(coach):
    name = st.text_input("Name", value=coach["name"])
    phone = st.text_input("Phone", value=coach["phone"])
    salary = st.number_input("Salary", min_value=0, step=500, value=coach["salary"])

    b1, b2 = st.columns(2)
    if b1.button("Cancel", key=f"dlg_secondary_updcoach_cancel_{coach['id']}", use_container_width=True):
        st.rerun()
    if b2.button("Save Changes", key=f"dlg_primary_updcoach_save_{coach['id']}", use_container_width=True):
        if not name.strip():
            st.error("Name is required.")
        else:
            update_coach(coach["id"], name.strip(), phone.strip(), salary)
            queue_toast("Coach Updated", name.strip())
            st.rerun()


@st.dialog("Delete Coach")
def delete_coach_dialog(coach):
    render_dialog_icon("delete", "danger")
    render_dialog_message(
        "Delete Record?",
        "This action cannot be undone.<br>"
        f"Are you sure you want to delete <b>{coach['name']}</b>'s record?"
    )
    col_cancel, col_delete = st.columns(2)
    if col_cancel.button("Cancel", key=f"dlg_secondary_delcoach_{coach['id']}", use_container_width=True):
        st.rerun()
    if col_delete.button("Delete", key=f"dlg_danger_delcoach_{coach['id']}", use_container_width=True):
        delete_coach(coach["id"])
        queue_toast("Record Deleted", coach["name"], kind="danger")
        st.rerun()


if coaches:
    col_widths = [2.2, 1.6, 1.6, 1]
    headers = ["Name", "Phone", "Salary", "Actions"]

    with st.container(key="card_coaches_list"):
        with st.container(key="table_coaches_list"):
            with st.container(key="theader_coaches_list"):
                header_cols = st.columns(col_widths)
                for col, h in zip(header_cols, headers):
                    col.markdown(f'<span class="table-header">{h}</span>', unsafe_allow_html=True)

            for c in coaches:
                row_cols = st.columns(col_widths)
                row_cols[0].markdown(c["name"])
                row_cols[1].markdown(c["phone"] or "—")
                row_cols[2].markdown(f"₹{c['salary']}")
                with row_cols[3]:
                    action_cols = st.columns(2)
                    if action_cols[0].button(":material/edit:", key=f"edit_{c['id']}", help="Edit"):
                        edit_coach_dialog(c)
                    if action_cols[1].button(":material/delete:", key=f"delete_{c['id']}", help="Delete"):
                        delete_coach_dialog(c)
else:
    st.info("No coaches added yet." if not search_name else "No coaches match the current search.")