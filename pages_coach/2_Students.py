import streamlit as st
from utils.auth import require_role

require_role(["coach"])

st.title("Students")
st.write("Page under construction.")