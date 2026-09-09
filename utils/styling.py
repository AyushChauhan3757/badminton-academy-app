import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Sidebar container */
        section[data-testid="stSidebar"] {
            background-color: #14304F;
        }

        /* Sidebar nav links (st.Page items) */
        section[data-testid="stSidebar"] a {
            color: #EEF3F9 !important;
            border-radius: 8px;
            font-weight: 500;
        }

        /* Active/selected nav item */
        section[data-testid="stSidebar"] a[aria-current="page"] {
            background-color: #E0AC4B !important;
            color: #14304F !important;
            font-weight: 700;
        }

        /* Sidebar body text (e.g. "Logged in as: admin") */
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span {
            color: #EEF3F9;
        }
        </style>
    """, unsafe_allow_html=True)