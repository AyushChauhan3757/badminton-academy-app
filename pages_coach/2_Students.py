import streamlit as st

from constants import BATCH_TIMINGS, ROLE_COACH
from db.students import get_all_students
from utils.auth import require_role
from utils.header import render_header
from utils.ui_helpers import batch_pill, timing_pill

require_role([ROLE_COACH])

render_header("Students Roster")

PAGE_SIZE = 10

# Read-only page: no Add/Edit/Delete anywhere. Fees, guardian name and admission
# date are deliberately not shown (spec Permission Model); phone IS shown (Entry 23).

with st.container(key="students_top_row"):
    search_name = st.text_input("Search by name", placeholder="Search by name", label_visibility="collapsed")

with st.container(key="students_filters_row"):
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        batch_filter = st.selectbox("Filter by Batch", options=["All"] + list(BATCH_TIMINGS.keys()))
    with fcol2:
        all_timings = sorted({t for timings in BATCH_TIMINGS.values() for t in timings})
        timing_filter = st.selectbox("Filter by Timing", options=["All"] + all_timings)

students = get_all_students()

if search_name:
    students = [s for s in students if search_name.lower() in s["name"].lower()]
if batch_filter != "All":
    students = [s for s in students if s["batch"] == batch_filter]
if timing_filter != "All":
    students = [s for s in students if s["timing"] == timing_filter]

# Reset to page 1 whenever the active filter/search combination changes
filter_signature = (search_name, batch_filter, timing_filter)
if st.session_state.get("coach_students_filter_signature") != filter_signature:
    st.session_state["coach_students_filter_signature"] = filter_signature
    st.session_state["coach_students_page"] = 1

if "coach_students_page" not in st.session_state:
    st.session_state["coach_students_page"] = 1

total_students = len(students)
total_pages = max(1, (total_students + PAGE_SIZE - 1) // PAGE_SIZE)
st.session_state["coach_students_page"] = min(st.session_state["coach_students_page"], total_pages)
current_page = st.session_state["coach_students_page"]

start_idx = (current_page - 1) * PAGE_SIZE
paginated_students = students[start_idx:start_idx + PAGE_SIZE]

st.markdown("---")

if paginated_students:
    col_widths = [1.6, 1.4, 0.9, 1.3]
    headers = ["Name", "Batch", "Timing", "Phone"]

    # Distinct keys (not *_students_roster) so the Admin table's 8-column mobile
    # fixed-width rules don't apply to this 4-column table.
    with st.container(key="card_coach_students"):
        with st.container(key="table_coach_students"):
            with st.container(key="theader_coach_students"):
                header_cols = st.columns(col_widths)
                for col, h in zip(header_cols, headers):
                    col.markdown(f'<span class="table-header">{h}</span>', unsafe_allow_html=True)

            for s in paginated_students:
                row_cols = st.columns(col_widths)
                row_cols[0].markdown(s["name"])
                row_cols[1].markdown(batch_pill(s["batch"]), unsafe_allow_html=True)
                row_cols[2].markdown(timing_pill(s["timing"]), unsafe_allow_html=True)
                row_cols[3].markdown(s["phone"] or "")

    with st.container(key="pagination_coach_students"):
        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            if st.button("← Previous", key="coach_students_prev_page", disabled=(current_page <= 1)):
                st.session_state["coach_students_page"] = current_page - 1
                st.rerun()
        with pcol2:
            st.markdown(f"<div class='pagination-label'>Page {current_page} of {total_pages}</div>", unsafe_allow_html=True)
        with pcol3:
            if st.button("Next →", key="coach_students_next_page", disabled=(current_page >= total_pages)):
                st.session_state["coach_students_page"] = current_page + 1
                st.rerun()
else:
    st.info("No students added yet." if total_students == 0 else "No students match the current filters.")