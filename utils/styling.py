import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .block-container {
            padding-top: 0rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container > div:first-child {
            margin-top: 0 !important;
        }

        [data-testid="stAppViewContainer"] h1 {
            font-size: 3.2rem !important;
        }

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

        [data-testid="stSidebarHeader"] {
            margin-bottom: -2rem !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
            padding-top: 0 !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #14304F;
        }

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

        section[data-testid="stSidebar"] a[aria-current="page"] {
            background-color: #E0AC4B !important;
            color: #14304F !important;
            font-weight: 700;
        }

        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span {
            color: #EEF3F9;
        }

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

        div[data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        [data-testid="stSidebarHeader"] button[data-testid="stLogoLink"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarHeader"] button[data-testid="stLogoLink"]:hover {
            background-color: transparent !important;
        }

        [data-testid="stHeader"] [data-testid="stHeaderLogo"] {
            display: none !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5EAF1 !important;
            border-radius: 16px !important;
            box-shadow: 0 2px 8px rgba(20, 48, 79, 0.06) !important;
            padding: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    apply_kpi_card_styles()
    apply_table_card_styles()


def apply_kpi_card_styles():
    st.markdown("""
    <style>
    div[class*="st-key-kpi_"] {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 2px 8px rgba(20, 48, 79, 0.08);
        border: none !important;
        display: flex;
        align-items: center;
    }
    div[class*="st-key-kpi_"] .kpi-row {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        width: 100%;
    }
    div[class*="st-key-kpi_"] .kpi-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 56px;
        height: 56px;
        min-width: 56px;
        border-radius: 50%;
    }
    div[class*="st-key-kpi_"] .kpi-icon .material-symbols-outlined {
        font-size: 28px;
    }
    div[class*="st-key-kpi_"] .kpi-text {
        display: flex;
        flex-direction: column;
    }
    div[class*="st-key-kpi_"] .kpi-label {
        font-size: 1rem;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    div[class*="st-key-kpi_"] .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }
    div[class*="st-key-kpi_"] [data-testid="stMarkdownContainer"],
    div[class*="st-key-kpi_"] [data-testid="stMarkdown"] {
        margin: 0 !important;
        padding: 0 !important;
        width: 100%;
    }
    div[class*="st-key-kpi_"] > div {
        width: 100%;
    }

    /* Color-coded card backgrounds by metric type - matched by key substring so
       this covers both the desktop cards (kpi_lifetime_received, kpi_month_paid,
       etc.) and the mobile cards (kpi_m_received_life, kpi_m_paid_month, etc.)
       with one set of rules. */
    div[class*="st-key-kpi_"][class*="_received"] {
        background-color: #EAF1FB !important;
    }
    div[class*="st-key-kpi_"][class*="_paid"] {
        background-color: #FBE7E6 !important;
    }
    div[class*="st-key-kpi_"][class*="_profit"] {
        background-color: #E3F5EA !important;
    }

    /* Desktop: keep the existing 3+3 Lifetime/This Month layout, hide the paired mobile version */
    @media (min-width: 641px) {
        div[class*="st-key-kpi_section_mobile"] {
            display: none !important;
        }
    }

    /* Mobile: hide the desktop 3+3 layout, show the paired Lifetime/This Month
       version instead (Received|Received, Paid|Paid, Profit|Profit rows).
       flex-direction must be forced back to row here because Streamlit's own
       mobile CSS switches these horizontal blocks to column layout by default. */
    @media (max-width: 640px) {
        div[class*="st-key-kpi_"] .kpi-icon {
            display: none !important;
        }
        div[class*="st-key-kpi_section_desktop"] {
            display: none !important;
        }
        div[class*="st-key-kpi_section_mobile"] [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 0.75rem !important;
        }
        div[class*="st-key-kpi_section_mobile"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
        div[class*="st-key-kpi_section_mobile"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            width: 50% !important;
            flex: 1 1 0 !important;
            min-width: 0 !important;
        }
        div[class*="st-key-kpi_m_"] {
            padding: 0.9rem 0.7rem !important;
        }
    }

    /* Dedicated classes for mobile KPI cards - defined outside the media query
       (the section itself is already hidden on desktop via display:none above,
       so no need to re-scope by width) to avoid any cascade/specificity fight
       with the desktop .kpi-value/.kpi-label rules. */
    .kpi-value-mobile {
        font-size: 1.15rem;
        font-weight: 800;
        line-height: 1.2;
        white-space: nowrap;
        overflow: hidden;
    }
    .kpi-label-mobile {
        font-size: 0.8rem;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 0.3rem;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_table_card_styles():
    st.markdown("""
    <style>
    div[class*="st-key-card_"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 1.8rem 2rem;
        box-shadow: 0 2px 8px rgba(20, 48, 79, 0.08);
        border: 1px solid #E5EAF1 !important;
    }

    .table-header {
        font-size: 1rem;
        font-weight: 800;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    /* Kill default gap on the vertical wrapper around each column's content
    inside the card - this was pushing "View Full Log" down and out of
    alignment with "+ Add Transaction" next to it. */
    div[class*="st-key-card_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"],
    div[class*="st-key-card_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        justify-content: center !important;
    }
    div[class*="st-key-table_"] {
        gap: 0 !important;
    }

    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] {
        margin-bottom: 0 !important;
        border-bottom: 1px solid #B9C4D3 !important;
        align-items: stretch !important;
        gap: 0 !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] [data-testid="stElementContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] [data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[class*="st-key-table_"] p {
        font-size: 1.15rem !important;
        line-height: 1.6 !important;
        margin-bottom: 0 !important;
    }

    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-right: 1px solid #B9C4D3 !important;
        padding: 0.85rem 0.75rem !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child,
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
        border-right: none !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"] p,
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] p,
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"] span,
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] span,
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"] .table-header,
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] .table-header {
        text-align: center !important;
        width: 100%;
    }

    /* Outer border around the whole table */
    div[class*="st-key-table_"] {
        border: 1px solid #8FA0B8 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Header row - darker divider lines than the data rows */
    div[class*="st-key-theader_"] [data-testid="stHorizontalBlock"] {
        border-bottom: 2px solid #8FA0B8 !important;
    }
    div[class*="st-key-theader_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
    div[class*="st-key-theader_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        border-right: 2px solid #8FA0B8 !important;
    }

    .st-key-btn_add_transaction button {
        background-color: #14304F !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 3rem !important;
        font-weight: 600 !important;
        width: 360px !important;
        max-width: 100% !important;
    }
    .st-key-btn_add_transaction button p {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
    .st-key-btn_add_transaction button:hover {
        background-color: #1D4C82 !important;
    }

    div[class*="st-key-card_"] div.stPageLink a {
        justify-content: center !important;
        text-decoration: none !important;
    }
    div[class*="st-key-card_"] div.stPageLink a,
    div[class*="st-key-card_"] div.stPageLink a * {
        color: #14304F !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
    }

    /* Mobile: force table rows back to row-direction (Streamlit defaults to
       column-stacking horizontal blocks under 640px) and shrink text/padding
       so all 4 columns can fit side by side on a phone screen. */
    @media (max-width: 640px) {
        div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }
        div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
        div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            width: auto !important;
            flex: 1 1 0 !important;
            min-width: 0 !important;
            padding: 0.4rem 0.25rem !important;
        }
        div[class*="st-key-table_"] p,
        div[class*="st-key-table_"] .table-header {
            font-size: 0.68rem !important;
            line-height: 1.25 !important;
            word-break: break-word !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def apply_login_styles():
    st.markdown("""
        <style>
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            margin: 0 !important;
            padding: 0 !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        section[data-testid="stSidebar"] { display: none !important; }
        div[data-testid="stSidebarCollapsedControl"] { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }

        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        .st-key-login_page {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background-image: url('app/static/login_background.png');
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            overflow: hidden !important;
            z-index: 9999 !important;
        }

        .st-key-login_form_panel {
            position: absolute !important;
            top: 50% !important;
            left: 8% !important;
            transform: translateY(-50%) !important;
            width: 420px !important;
            max-width: 90vw !important;
            background-color: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px !important;
            padding: 2.5rem 2rem !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.15) !important;
            z-index: 3 !important;
            align-items: center !important;
        }

        .st-key-login_form_panel [data-testid="stImage"] {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
        .st-key-login_form_panel [data-testid="stImage"] img {
            width: 180px !important;
            height: auto !important;
        }

        [data-testid="stElementToolbar"] {
            display: none !important;
        }

        .st-key-login_form_panel [data-testid="stForm"] {
            width: 100% !important;
        }

        div[data-testid="stSelectbox"] > div {
            border: 1px solid #D0D7E2 !important;
            border-radius: 10px !important;
            background-color: #FFFFFF !important;
        }
        div[data-testid="stSelectbox"] [data-rac] {
            background-color: transparent !important;
        }

        div[data-testid="stTextInput"] > div {
            border: 1px solid #D0D7E2 !important;
            border-radius: 10px !important;
            background-color: #FFFFFF !important;
        }
        div[data-testid="stTextInput"] input {
            border: none !important;
            background-color: transparent !important;
        }

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

        .login-footer-row {
            display: flex;
            gap: 2rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #E5EAF1;
        }
        .login-footer-item {
            color: #14304F;
            font-size: 0.9rem;
            font-weight: 700;
        }

        @media (max-width: 640px) {
            .st-key-login_page {
                position: absolute !important;
                background-image: none !important;
                background-color: #14304F !important;
                height: auto !important;
                min-height: 100vh !important;
                overflow: visible !important;
            }
            .st-key-login_form_panel {
                position: relative !important;
                top: 0 !important;
                left: 0 !important;
                transform: none !important;
                width: 90% !important;
                margin: 5vh auto !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)