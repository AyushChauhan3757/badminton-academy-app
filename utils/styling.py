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

def apply_login_styles():
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] { display: none !important; }
        div[data-testid="stSidebarCollapsedControl"] { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }

        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        /* Full login page */
        .st-key-login_page {
            position: relative !important;
            width: 100% !important;
            min-height: 100vh !important;
            height: 100vh !important;
            background-color: #FFFFFF;
            overflow: hidden !important;
        }

        /* Navy curved shape */
        .st-key-login_page .login-navy-shape {
            position: absolute !important;
            top: -15% !important;
            right: -15% !important;
            width: 62% !important;
            height: 130% !important;
            background: linear-gradient(135deg, #0D2340, #14304F);
            border-radius: 55% 0 0 45% / 50% 0 0 50%;
            z-index: 1 !important;
        }

        /* Illustration - fixed to the right */
        .st-key-login_illustration_panel {
            position: absolute !important;
            top: 50% !important;
            right: 4% !important;
            transform: translateY(-50%) !important;
            width: auto !important;
            height: 65vh !important;
            max-height: 650px !important;
            z-index: 2 !important;
            pointer-events: none !important;
        }

        .st-key-login_illustration_panel img {
            width: auto !important;
            height: 100% !important;
            max-height: 650px !important;
            object-fit: contain !important;
            display: block !important;
        }

        /* Login section - fixed to the left */
        .st-key-login_form_panel {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 52% !important;
            height: 100vh !important;
            min-height: 100vh !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            padding: 3rem 2rem 3rem 5rem !important;
            z-index: 3 !important;
        }

        /* Keep login content compact */
        .st-key-login_form_panel > div {
            max-width: 480px !important;
        }

        .st-key-login_form_panel [data-testid="stImage"] {
            margin-bottom: 0.5rem !important;
        }

        .st-key-login_form_panel [data-testid="stImage"] img {
            width: 180px !important;
            height: auto !important;
        }

        [data-testid="stElementToolbar"] {
            display: none !important;
        }

        /* Login form width */
        .st-key-login_form_panel [data-testid="stForm"] {
            max-width: 480px !important;
            width: 100% !important;
        }

        /* Selectbox */
        div[data-testid="stSelectbox"] > div {
            border: 1px solid #D0D7E2 !important;
            border-radius: 10px !important;
            background-color: #FFFFFF !important;
        }

        div[data-testid="stSelectbox"] [data-rac] {
            background-color: transparent !important;
        }

        /* Password input */
        div[data-testid="stTextInput"] > div {
            border: 1px solid #D0D7E2 !important;
            border-radius: 10px !important;
            background-color: #FFFFFF !important;
        }

        div[data-testid="stTextInput"] input {
            border: none !important;
            background-color: transparent !important;
        }

        /* Login button */
        .st-key-login_submit_btn button {
            background-color: #14304F !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.75rem !important;
            border: none !important;
        }

        .st-key-login_submit_btn button:hover {
            background-color: #1D4C82 !important;
        }

        .st-key-login_submit_btn button p {
            color: #FFFFFF !important;
        }

        /* Footer */
        .login-footer-row {
            display: flex;
            gap: 2rem;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid #E5EAF1;
        }

        .login-footer-item {
            color: #5b6b82;
            font-size: 0.85rem;
            font-weight: 600;
        }

        /* Mobile */
        @media (max-width: 640px) {
            .st-key-login_page {
                height: auto !important;
                min-height: 100vh !important;
                overflow: visible !important;
            }

            .st-key-login_page .login-navy-shape {
                display: none !important;
            }

            .st-key-login_illustration_panel {
                display: none !important;
            }

            .st-key-login_form_panel {
                position: relative !important;
                width: 100% !important;
                height: auto !important;
                min-height: 100vh !important;
                padding: 2.5rem 1.5rem !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)