import streamlit as st
from utils.auth import require_role

require_role(["coach"])

st.title("Gym Roster")
st.write("Page under construction.")