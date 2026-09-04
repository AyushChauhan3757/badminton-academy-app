import streamlit as st
from utils.auth import require_role

require_role(["admin"])

st.title("Log")
st.write("Page under construction.")