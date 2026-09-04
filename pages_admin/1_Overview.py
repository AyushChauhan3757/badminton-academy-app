import streamlit as st
from utils.auth import require_role

require_role(["admin"])

st.title("Overview")
st.write("Page under construction.")