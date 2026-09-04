import streamlit as st
from utils.auth import require_role
from constants import ROLE_ADMIN
from db.students import get_all_students

require_role([ROLE_ADMIN])

st.title("Students Roster")

students = get_all_students()

if not students:
    st.info("No students added yet.")
else:
    st.dataframe(students, use_container_width=True)