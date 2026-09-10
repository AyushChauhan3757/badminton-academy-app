from datetime import date

import streamlit as st

from constants import BATCH_FEES, BATCH_TIMINGS, ROLE_ADMIN
from db.students import add_student, delete_student, get_all_students, update_student
from utils.auth import require_role
from utils.header import render_header

require_role([ROLE_ADMIN])

render_header("Students Roster")

search_name = st.text_input("Search by name")

col1, col2 = st.columns(2)
with col1:
    batch_filter = st.selectbox("Filter by Batch", options=["All"] + list(BATCH_TIMINGS.keys()))
with col2:
    all_timings = sorted({t for timings in BATCH_TIMINGS.values() for t in timings})
    timing_filter = st.selectbox("Filter by Timing", options=["All"] + all_timings)

col3, col4 = st.columns(2)
with col3:
    admission_start = st.date_input("Admission date from", value=None, format="DD/MM/YYYY")
with col4:
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

st.markdown("---")


@st.dialog("Update Student", width="large")
def update_student_dialog(student):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=student["name"])
        batch = st.selectbox(
            "Batch",
            options=list(BATCH_TIMINGS.keys()),
            index=list(BATCH_TIMINGS.keys()).index(student["batch"]),
        )
        is_custom_fee = st.checkbox("Custom Fee", value=bool(student["is_custom_fee"]))
        fee = st.number_input(
            "Fee",
            value=student["fees"] if is_custom_fee else BATCH_FEES[batch],
            disabled=not is_custom_fee,
            key=f"update_fee_{student['id']}_{batch}_{is_custom_fee}",
        )
    with col2:
        admission_date = st.date_input(
            "Admission Date",
            value=date.fromisoformat(student["admission_date"]),
            format="DD/MM/YYYY",
        )
        timing = st.selectbox(
            "Timing",
            options=BATCH_TIMINGS[batch],
            index=BATCH_TIMINGS[batch].index(student["timing"]) if student["timing"] in BATCH_TIMINGS[batch] else 0,
        )
        guardian_name = st.text_input("Guardian Name", value=student["guardian_name"])
        phone = st.text_input("Phone", value=student["phone"])

    if st.button("Save Changes", key="submit_update_student"):
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
            st.success(f"{name} updated.")
            st.rerun()


@st.dialog("Delete Student")
def delete_student_dialog(student):
    st.warning(f"Are you sure you want to delete **{student['name']}**? This cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Delete", key="confirm_delete_student"):
            delete_student(student["id"])
            st.success(f"{student['name']} deleted.")
            st.rerun()
    with col2:
        if st.button("Cancel", key="cancel_delete_student"):
            st.rerun()


if students:
    col_widths = [2, 1.3, 1, 1.5, 1.3, 1.3, 0.8, 1, 1]
    headers = ["Name", "Batch", "Timing", "Guardian Name", "Phone", "Admission Date", "Fees", "", ""]
    header_cols = st.columns(col_widths)
    for col, h in zip(header_cols, headers):
        col.markdown(f"**{h}**")

    for s in students:
        row_cols = st.columns(col_widths)
        row_cols[0].write(s["name"])
        row_cols[1].write(s["batch"])
        row_cols[2].write(s["timing"])
        row_cols[3].write(s["guardian_name"])
        row_cols[4].write(s["phone"])
        row_cols[5].write(s["admission_date"])
        row_cols[6].write(s["fees"])
        if row_cols[7].button("Edit", key=f"edit_{s['id']}"):
            update_student_dialog(s)
        if row_cols[8].button("Delete", key=f"delete_{s['id']}"):
            delete_student_dialog(s)
else:
    st.info("No students added yet.")


@st.dialog("Add Student", width="large")
def add_student_dialog():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        batch = st.selectbox("Batch", options=list(BATCH_TIMINGS.keys()))
        is_custom_fee = st.checkbox("Custom Fee")
        fee = st.number_input(
            "Fee",
            value=BATCH_FEES[batch],
            disabled=not is_custom_fee,
        )
    with col2:
        admission_date = st.date_input("Admission Date", value=date.today(), format="DD/MM/YYYY")
        timing = st.selectbox("Timing", options=BATCH_TIMINGS[batch])
        guardian_name = st.text_input("Guardian Name")
        phone = st.text_input("Phone")

    if st.button("Add Student", key="submit_add_student"):
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
            st.success(f"{name} added.")
            st.rerun()


if st.button("+ Add Student"):
    add_student_dialog()