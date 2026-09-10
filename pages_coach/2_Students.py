# pages_coach/2_Students.py

import streamlit as st
from utils.auth import require_role
from constants import ROLE_COACH, BATCH_TIMINGS
from db.students import get_all_students
from utils.header import render_header

require_role([ROLE_COACH])

render_header("Students Roster")

students = get_all_students()

if not students:
    st.info("No students added yet.")
else:
    # --- Filters ---
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search by name")
    with col2:
        batch_filter = st.selectbox("Filter by Batch", ["All"] + list(BATCH_TIMINGS.keys()))
    with col3:
        # Timing options depend on batch filter; if "All", show every timing across all batches
        if batch_filter != "All":
            timing_options = ["All"] + BATCH_TIMINGS[batch_filter]
        else:
            all_timings = sorted({t for timings in BATCH_TIMINGS.values() for t in timings})
            timing_options = ["All"] + all_timings
        timing_filter = st.selectbox("Filter by Timing", timing_options)

    # --- Apply filters ---
    filtered = students
    if search:
        filtered = [s for s in filtered if search.lower() in s["name"].lower()]
    if batch_filter != "All":
        filtered = [s for s in filtered if s["batch"] == batch_filter]
    if timing_filter != "All":
        filtered = [s for s in filtered if s["timing"] == timing_filter]

    # --- Display ---
    if not filtered:
        st.info("No students match the current filters.")
    else:
        roster = [
            {"Name": s["name"], "Batch": s["batch"], "Timing": s["timing"]}
            for s in filtered
        ]
        st.dataframe(roster, use_container_width=True, hide_index=True)