# pages_coach/3_Gym.py

import streamlit as st
from utils.auth import require_role
from constants import ROLE_COACH
from db.gym_members import get_all_gym_members
from utils.header import render_header

require_role([ROLE_COACH])

render_header("Gym Roster")

members = get_all_gym_members()

if not members:
    st.info("No gym members added yet.")
else:
    search = st.text_input("Search by name")

    filtered = members
    if search:
        filtered = [m for m in filtered if search.lower() in m["name"].lower()]

    if not filtered:
        st.info("No gym members match the current search.")
    else:
        roster = [
            {"Name": m["name"], "Phone": m["phone"], "Joining Date": m["joining_date"]}
            for m in filtered
        ]
        st.dataframe(roster, use_container_width=True, hide_index=True)