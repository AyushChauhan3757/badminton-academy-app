import streamlit as st
from utils.auth import require_role

require_role(["coach"])

st.title("Pending")
st.write("Page under construction.")