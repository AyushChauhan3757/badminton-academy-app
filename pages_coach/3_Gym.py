# pages_coach/3_Gym.py

from datetime import date

import streamlit as st

from constants import ROLE_COACH
from db.gym_members import get_all_gym_members
from utils.auth import require_role
from utils.header import render_header

require_role([ROLE_COACH])

render_header("Gym Roster")

PAGE_SIZE = 10

with st.container(key="students_top_row"):
    search_name = st.text_input(
        "Search by name", placeholder="Search by name", label_visibility="collapsed"
    )

gym_members = get_all_gym_members()

if search_name:
    gym_members = [g for g in gym_members if search_name.lower() in g["name"].lower()]

filter_signature = (search_name,)
if st.session_state.get("coach_gym_filter_signature") != filter_signature:
    st.session_state["coach_gym_filter_signature"] = filter_signature
    st.session_state["coach_gym_page"] = 1

if "coach_gym_page" not in st.session_state:
    st.session_state["coach_gym_page"] = 1

total_members = len(gym_members)
total_pages = max(1, (total_members + PAGE_SIZE - 1) // PAGE_SIZE)
st.session_state["coach_gym_page"] = min(st.session_state["coach_gym_page"], total_pages)
current_page = st.session_state["coach_gym_page"]

start_idx = (current_page - 1) * PAGE_SIZE
end_idx = start_idx + PAGE_SIZE
paginated_members = gym_members[start_idx:end_idx]

st.markdown("---")

if paginated_members:
    col_widths = [2.5, 2, 2]
    headers = ["Name", "Phone", "Joining Date"]

    with st.container(key="card_coach_gym"):
        with st.container(key="table_coach_gym"):
            with st.container(key="theader_coach_gym"):
                header_cols = st.columns(col_widths)
                for col, h in zip(header_cols, headers):
                    col.markdown(f'<span class="table-header">{h}</span>', unsafe_allow_html=True)

            for m in paginated_members:
                row_cols = st.columns(col_widths)
                row_cols[0].markdown(m["name"])
                row_cols[1].markdown(m["phone"] or "—")
                row_cols[2].markdown(date.fromisoformat(m["joining_date"]).strftime("%d/%m/%Y"))

    with st.container(key="pagination_coach_gym"):
        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            if st.button("← Previous", key="coach_gym_prev_page", disabled=(current_page <= 1)):
                st.session_state["coach_gym_page"] = current_page - 1
                st.rerun()
        with pcol2:
            st.markdown(
                f"<div class='pagination-label'>Page {current_page} of {total_pages}</div>",
                unsafe_allow_html=True,
            )
        with pcol3:
            if st.button("Next →", key="coach_gym_next_page", disabled=(current_page >= total_pages)):
                st.session_state["coach_gym_page"] = current_page + 1
                st.rerun()
else:
    st.info("No gym members added yet." if total_members == 0 else "No gym members match the current search.")