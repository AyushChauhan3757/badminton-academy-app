import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Reduce default top padding of the main content area */
        .block-container {
            padding-top: 2rem !important;
        }

        /* Increase page title size (e.g. "Overview", "Fees Pending") */
        [data-testid="stAppViewContainer"] h1 {
            font-size: 3.2rem !important;
        }

        /* Enlarge the sidebar logo + its container */
        [data-testid="stSidebar"] [data-testid="stLogo"] {
            height: 16rem !important;
        }
        [data-testid="stSidebar"] img {
            height: 16rem !important;
            width: auto !important;
            max-height: none !important;
            display: block !important;
            margin: 0 auto !important;
        }
        [data-testid="stSidebarHeader"] {
            height: auto !important;
            padding-top: 1rem !important;
            padding-bottom: 0 !important;
            display: flex !important;
            justify-content: center !important;
        }

        /* Reduce gap between logo and nav list */
        [data-testid="stSidebarHeader"] {
            margin-bottom: -2rem !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
            padding-top: 0 !important;
        }

        /* Sidebar container */
        section[data-testid="stSidebar"] {
            background-color: #14304F;
        }

                /* Sidebar nav links (st.Page items) - font size + spacing */
        section[data-testid="stSidebar"] a {
            color: #EEF3F9 !important;
            border-radius: 8px;
            font-weight: 500;
            font-size: 1.25rem !important;
            padding: 0.75rem 1rem !important;
            margin-bottom: 0.175rem !important;
        }
        section[data-testid="stSidebar"] a span,
        section[data-testid="stSidebar"] a p {
            font-size: 1.25rem !important;
        }

        /* Active/selected nav item */
        section[data-testid="stSidebar"] a[aria-current="page"] {
            background-color: #E0AC4B !important;
            color: #14304F !important;
            font-weight: 700;
        }

        /* Sidebar body text */
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span {
            color: #EEF3F9;
        }

        /* Sidebar buttons (e.g. Logout) */
        section[data-testid="stSidebar"] button {
            background-color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] button p {
            color: #14304F !important;
        }
        section[data-testid="stSidebar"] button:hover {
            background-color: #E0AC4B !important;
        }
        section[data-testid="stSidebar"] button:hover p {
            color: #14304F !important;
        }

        /* Hide Streamlit's sidebar collapse button entirely - sidebar should not be collapsible on desktop */
        div[data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        /* Logo becomes a clickable button on non-home pages - strip button styling from it */
        [data-testid="stSidebarHeader"] button[data-testid="stLogoLink"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarHeader"] button[data-testid="stLogoLink"]:hover {
            background-color: transparent !important;
        }

        /* Hide the logo Streamlit relocates into the top header when the sidebar is collapsed (e.g. on mobile) */
        [data-testid="stHeader"] [data-testid="stHeaderLogo"] {
            display: none !important;
        }

        /* Card-style bordered containers (used for KPI cards, table panels, etc.) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5EAF1 !important;
            border-radius: 16px !important;
            box-shadow: 0 2px 8px rgba(20, 48, 79, 0.06) !important;
            padding: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)