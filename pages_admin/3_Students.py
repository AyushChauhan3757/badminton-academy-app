from datetime import date

import streamlit as st

from constants import BATCH_FEES, BATCH_TIMINGS, ROLE_ADMIN
from db.students import add_student, delete_student, get_all_students, update_student
from utils.auth import require_role
from utils.header import render_header
from utils.ui_helpers import (
    batch_pill,
    timing_pill,
    render_dialog_icon,
    render_dialog_message,
    queue_toast,
    tint_dialog_selects,
)

require_role([ROLE_ADMIN])

render_header("Students Roster")

PAGE_SIZE = 10

@st.dialog("Add Student", width="medium")
def add_student_dialog():
    c1, c2 = st.columns(2)
    name = c1.text_input("Name")
    phone = c2.text_input("Phone")

    c1, c2 = st.columns(2)
    with c1:
        with st.container(key="dlg_batch_add"):
            batch = st.selectbox("Batch", options=list(BATCH_TIMINGS.keys()))
    with c2:
        with st.container(key="dlg_timing_add"):
            timing = st.selectbox("Timing", options=BATCH_TIMINGS[batch])

    c1, c2 = st.columns(2)
    admission_date = c1.date_input("Admission Date", value=date.today(), format="DD/MM/YYYY")
    guardian_name = c2.text_input("Guardian Name")

    c1, c2 = st.columns(2)
    is_custom_fee = c2.checkbox("Custom Fee", key="dlg_customfee_add")
    fee = c1.number_input(
        "Fee (₹)",
        value=BATCH_FEES[batch],
        disabled=not is_custom_fee,
    )

    b1, b2 = st.columns(2)
    if b1.button("Cancel", key="dlg_secondary_addstudent_cancel", use_container_width=True):
        st.rerun()
    if b2.button("Add Student", key="dlg_primary_addstudent_save", use_container_width=True):
        if not name.strip():
            st.error("Name is required.")
        else:
            add_student(
                name=name.strip(),
                admission_date=str(admission_date),
                batch=batch,
                timing=timing,
                fee=fee,
                is_custom_fee=is_custom_fee,
                guardian_name=guardian_name.strip(),
                phone=phone.strip(),
            )
            queue_toast("Student Added", name.strip())
            st.rerun()

    tint_dialog_selects(batch, timing, "add")


with st.container(key="students_top_row"):
    col_search, col_add = st.columns([4, 1])
    with col_search:
        search_name = st.text_input("Search by name", placeholder="Search by name", label_visibility="collapsed")
    with col_add:
        if st.button("+ Add Student", key="btn_add_student", use_container_width=True):
            add_student_dialog()

with st.container(key="students_filters_row"):
    fcol1, fcol2, fcol3, fcol4 = st.columns(4)
    with fcol1:
        batch_filter = st.selectbox("Filter by Batch", options=["All"] + list(BATCH_TIMINGS.keys()))
    with fcol2:
        all_timings = sorted({t for timings in BATCH_TIMINGS.values() for t in timings})
        timing_filter = st.selectbox("Filter by Timing", options=["All"] + all_timings)
    with fcol3:
        admission_start = st.date_input("Admission date from", value=None, format="DD/MM/YYYY")
    with fcol4:
        admission_end = st.date_input("Admission date to", value=None, format="DD/MM/YYYY")

students = get_all_students()

if search_name:
    students = [s for s in students if search_name.lower() in s["name"].lower()]
if batch_filter != "All":
    students = [s for s in students if s["batch"] == batch_filter]
if timing_filter != "All":
    students = [s for s in students if s["timing"] == timing_filter]
if admission_start:
    students = [s for s in students if date.fromisoformat(s["admission_date"]) >= admission_start]
if admission_end:
    students = [s for s in students if date.fromisoformat(s["admission_date"]) <= admission_end]

# Reset to page 1 whenever the active filter/search combination changes
filter_signature = (search_name, batch_filter, timing_filter, admission_start, admission_end)
if st.session_state.get("students_filter_signature") != filter_signature:
    st.session_state["students_filter_signature"] = filter_signature
    st.session_state["students_page"] = 1

if "students_page" not in st.session_state:
    st.session_state["students_page"] = 1

total_students = len(students)
total_pages = max(1, (total_students + PAGE_SIZE - 1) // PAGE_SIZE)
st.session_state["students_page"] = min(st.session_state["students_page"], total_pages)
current_page = st.session_state["students_page"]

start_idx = (current_page - 1) * PAGE_SIZE
end_idx = start_idx + PAGE_SIZE
paginated_students = students[start_idx:end_idx]

st.markdown("---")

@st.dialog("Update Student", width="medium")
def update_student_dialog(student):
    c1, c2 = st.columns(2)
    name = c1.text_input("Name", value=student["name"])
    phone = c2.text_input("Phone", value=student["phone"])

    c1, c2 = st.columns(2)
    with c1:
        with st.container(key="dlg_batch_upd"):
            batch = st.selectbox(
                "Batch",
                options=list(BATCH_TIMINGS.keys()),
                index=list(BATCH_TIMINGS.keys()).index(student["batch"]),
            )
    with c2:
        with st.container(key="dlg_timing_upd"):
            timing = st.selectbox(
                "Timing",
                options=BATCH_TIMINGS[batch],
                index=BATCH_TIMINGS[batch].index(student["timing"]) if student["timing"] in BATCH_TIMINGS[batch] else 0,
            )

    c1, c2 = st.columns(2)
    admission_date = c1.date_input(
        "Admission Date",
        value=date.fromisoformat(student["admission_date"]),
        format="DD/MM/YYYY",
    )
    guardian_name = c2.text_input("Guardian Name", value=student["guardian_name"])

    c1, c2 = st.columns(2)
    is_custom_fee = c2.checkbox(
        "Custom Fee",
        value=bool(student["is_custom_fee"]),
        key=f"dlg_customfee_upd_{student['id']}",
    )
    fee = c1.number_input(
        "Fee (₹)",
        value=student["fees"] if is_custom_fee else BATCH_FEES[batch],
        disabled=not is_custom_fee,
        key=f"update_fee_{student['id']}_{batch}_{is_custom_fee}",
    )

    b1, b2 = st.columns(2)
    if b1.button("Cancel", key=f"dlg_secondary_updstudent_cancel_{student['id']}", use_container_width=True):
        st.rerun()
    if b2.button("Save Changes", key=f"dlg_primary_updstudent_save_{student['id']}", use_container_width=True):
        if not name.strip():
            st.error("Name is required.")
        else:
            update_student(
                student_id=student["id"],
                name=name.strip(),
                admission_date=str(admission_date),
                batch=batch,
                timing=timing,
                fee=fee,
                is_custom_fee=is_custom_fee,
                guardian_name=guardian_name.strip(),
                phone=phone.strip(),
            )
            queue_toast("Student Updated", name.strip())
            st.rerun()

    tint_dialog_selects(batch, timing, "upd")


@st.dialog("Delete Student")
def delete_student_dialog(student):
    render_dialog_icon("delete", "danger")
    render_dialog_message(
        "Delete Record?",
        "This action cannot be undone.<br>"
        f"Are you sure you want to delete <b>{student['name']}</b>'s record?"
    )
    col_cancel, col_delete = st.columns(2)
    if col_cancel.button("Cancel", key=f"dlg_secondary_delstudent_{student['id']}", use_container_width=True):
        st.rerun()
    if col_delete.button("Delete", key=f"dlg_danger_delstudent_{student['id']}", use_container_width=True):
        delete_student(student["id"])
        queue_toast("Record Deleted", student["name"], kind="danger")
        st.rerun()


if paginated_students:
    col_widths = [1.5, 1.4, 0.8, 1.3, 1.1, 1.1, 0.7, 0.8]
    headers = ["Name", "Batch", "Timing", "Guardian Name", "Phone", "Admission Date", "Fees", "Actions"]

    with st.container(key="card_students_roster"):
        with st.container(key="table_students_roster"):
            with st.container(key="theader_students_roster"):
                header_cols = st.columns(col_widths)
                for col, h in zip(header_cols, headers):
                    col.markdown(f'<span class="table-header">{h}</span>', unsafe_allow_html=True)

            for s in paginated_students:
                row_cols = st.columns(col_widths)
                row_cols[0].markdown(s["name"])
                row_cols[1].markdown(batch_pill(s["batch"]), unsafe_allow_html=True)
                row_cols[2].markdown(timing_pill(s["timing"]), unsafe_allow_html=True)
                row_cols[3].markdown(s["guardian_name"])
                row_cols[4].markdown(s["phone"])
                row_cols[5].markdown(date.fromisoformat(s["admission_date"]).strftime("%d/%m/%Y"))
                row_cols[6].markdown(f"₹{s['fees']}")
                with row_cols[7]:
                    action_cols = st.columns(2)
                    if action_cols[0].button(":material/edit:", key=f"edit_{s['id']}", help="Edit"):
                        update_student_dialog(s)
                    if action_cols[1].button(":material/delete:", key=f"delete_{s['id']}", help="Delete"):
                        delete_student_dialog(s)

    with st.container(key="pagination_students"):
        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            if st.button("← Previous", key="students_prev_page", disabled=(current_page <= 1)):
                st.session_state["students_page"] = current_page - 1
                st.rerun()
        with pcol2:
            st.markdown(f"<div class='pagination-label'>Page {current_page} of {total_pages}</div>", unsafe_allow_html=True)
        with pcol3:
            if st.button("Next →", key="students_next_page", disabled=(current_page >= total_pages)):
                st.session_state["students_page"] = current_page + 1
                st.rerun()
else:
    st.info("No students added yet." if total_students == 0 else "No students match the current filters.")