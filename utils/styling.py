import streamlit as st


# =============================================================================
# apply_theme()
# Entry point — called once per page (from app.py). Injects the global/base
# CSS directly, then calls each specialized styling function in turn.
# =============================================================================

def apply_theme():
    st.markdown("""
        <style>
        /* ---------------------------------------------------------------
           FONTS
        --------------------------------------------------------------- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* ---------------------------------------------------------------
        Icon-only buttons (:material/... syntax) — must keep the
        Material Symbols ligature font; the global Plus Jakarta Sans
        override above otherwise breaks the icon glyph rendering.
        --------------------------------------------------------------- */
        span[data-testid="stIconMaterial"] {
            font-family: 'Material Symbols Outlined' !important;
        }

        /* ---------------------------------------------------------------
           GLOBAL PAGE LAYOUT
        --------------------------------------------------------------- */
        .block-container {
            padding-top: 0rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container > div:first-child {
            margin-top: 0 !important;
        }
        [data-testid="stAppViewContainer"] h1 {
            font-size: 3.2rem !important;
        }

        /* ---------------------------------------------------------------
        ICON BUTTONS — Streamlit's in-button Material icon syntax
        (:material/edit:, :material/delete:, etc.) renders as
        <span role="img" aria-label="... icon">, using font
        "Material Symbols Rounded" inline — this font was never
        imported, so the ligature silently failed to render.
        --------------------------------------------------------------- */
        span[role="img"][translate="no"] {
            font-family: 'Material Symbols Rounded' !important;
            font-size: 1.3rem !important;
            color: #14304F !important;
        }
        div[class*="st-key-edit_"] span[role="img"][translate="no"] {
            color: #1D4C82 !important;
        }
        div[class*="st-key-delete_"] span[role="img"][translate="no"] {
            color: #E0524A !important;
        }

        /* ---------------------------------------------------------------
           SIDEBAR — logo sizing/centering
        --------------------------------------------------------------- */
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
            margin-bottom: -2rem !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
            padding-top: 0 !important;
        }

        /* ---------------------------------------------------------------
           SIDEBAR — background + nav links
        --------------------------------------------------------------- */
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

        /* ---------------------------------------------------------------
           SIDEBAR — buttons (Logout, etc.)
        --------------------------------------------------------------- */
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

        /* ---------------------------------------------------------------
           SIDEBAR — collapse button (hidden entirely, not restyled —
           see build log Entry 26) + logo-as-link on non-home pages
           (Entry 27/28: Streamlit swaps the plain <img> logo for a
           <button data-testid="stLogoLink"> on every page except the
           current session's home page, which the general sidebar-button
           rule above was painting white — these two rules undo that)
        --------------------------------------------------------------- */
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

        /* ---------------------------------------------------------------
           TOP HEADER BAR — hide the small logo icon that appears here
           when the sidebar is collapsed (Entry 27/28)
        --------------------------------------------------------------- */
        [data-testid="stHeader"] [data-testid="stHeaderLogo"] {
            display: none !important;
        }

        /* ---------------------------------------------------------------
           LEGACY generic bordered-container rule. Superseded in practice
           by the explicit kpi_/card_ key-based rules below (Entry 28+),
           but left in place as a fallback for any st.container(border=True)
           that doesn't yet have a dedicated key.
        --------------------------------------------------------------- */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5EAF1 !important;
            border-radius: 16px !important;
            box-shadow: 0 2px 8px rgba(20, 48, 79, 0.06) !important;
            padding: 1rem !important;
        }
        /* ---------------------------------------------------------------
           PAGE HEADER (title / Welcome+time / Logout, via
           utils/header.py's render_header()) — mobile only.
           Desktop keeps the existing single-row 3-column layout
           untouched; on mobile, title stays on its own full-width
           line, but Welcome+time and Logout are forced back into one
           shared row (Welcome left, Logout right) instead of each
           stacking as separate full-width rows.
        --------------------------------------------------------------- */
        @media (max-width: 640px) {
            div[class*="st-key-page_header"] [data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: wrap !important;
                align-items: center !important;
            }
            div[class*="st-key-page_header"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1),
            div[class*="st-key-page_header"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) {
                flex: 1 1 100% !important;
                width: 100% !important;
            }
            div[class*="st-key-page_header"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2),
            div[class*="st-key-page_header"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) {
                flex: 1 1 65% !important;
                max-width: 65% !important;
                min-width: 0 !important;
                width: auto !important;
            }
            div[class*="st-key-page_header"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3),
            div[class*="st-key-page_header"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3) {
                flex: 0 0 auto !important;
                width: auto !important;
                min-width: 0 !important;
            }
            .header-welcome-block {
                text-align: left !important;
                padding-top: 0 !important;
            }
        }
        @media (max-width: 640px) {
            .stApp, [data-testid="stAppViewContainer"], .block-container {
                overflow-x: hidden !important;
                max-width: 100vw !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    apply_kpi_card_styles()
    apply_table_card_styles()
    apply_tab_styles()
    apply_filter_control_styles()


# =============================================================================
# apply_kpi_card_styles()
# Styles any st.container(border=True, key="kpi_...") — small metric cards
# with an icon-left / label-value-right layout (Overview page KPI rows).
# Includes the desktop 3-across layout and the paired mobile layout.
# =============================================================================

def apply_kpi_card_styles():
    st.markdown("""
    <style>
    /* ---------------------------------------------------------------
       KPI CARD — base shape (desktop + mobile)
    --------------------------------------------------------------- */
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

    /* ---------------------------------------------------------------
       KPI CARD — color-coded backgrounds by metric type, matched by
       key substring so this covers both desktop cards
       (kpi_lifetime_received, kpi_month_paid, ...) and mobile cards
       (kpi_m_received_life, kpi_m_paid_month, ...) with one rule set.
    --------------------------------------------------------------- */
    div[class*="st-key-kpi_"][class*="_received"] {
        background-color: #EAF1FB !important;
    }
    div[class*="st-key-kpi_"][class*="_paid"] {
        background-color: #FBE7E6 !important;
    }
    div[class*="st-key-kpi_"][class*="_profit"] {
        background-color: #E3F5EA !important;
    }

    /* ---------------------------------------------------------------
       KPI CARD — desktop vs mobile layout swap.
       Desktop: keep the 3+3 Lifetime/This Month rows, hide the mobile
       paired layout. Mobile: hide desktop rows, show the paired
       Lifetime/This Month layout instead (flex-direction must be
       forced back to row — Streamlit's own mobile CSS switches
       horizontal blocks to column layout by default under 640px).
    --------------------------------------------------------------- */
    @media (min-width: 641px) {
        div[class*="st-key-kpi_section_mobile"] {
            display: none !important;
        }
    }
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

    /* ---------------------------------------------------------------
       KPI CARD — dedicated mobile-only text classes. Defined outside
       the media query (the section itself is already display:none'd
       on desktop above) to avoid any cascade/specificity fight with
       the desktop .kpi-value/.kpi-label rules.
    --------------------------------------------------------------- */
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


# =============================================================================
# apply_table_card_styles()
# Styles any st.container(border=True, key="card_...") — larger table/list
# panels — plus the nested "table_" (rows) and "theader_" (header row)
# containers used inside them, and the small reusable text/pill/button
# helper classes (.table-header, .status-*, .batch-*, .card-subheading,
# btn_markpaid_/btn_takeaction_ buttons).
# =============================================================================

def apply_table_card_styles():
    st.markdown("""
    <style>
    /* ---------------------------------------------------------------
       CARD — outer panel shape
    --------------------------------------------------------------- */
    div[class*="st-key-card_"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 1.8rem 2rem;
        box-shadow: 0 2px 8px rgba(20, 48, 79, 0.08);
        border: 1px solid #E5EAF1 !important;
    }

    /* ---------------------------------------------------------------
       TEXT HELPERS — column headers, status labels, small subheading
       used above a table inside a card (e.g. "August 2026" on the
       Missed Last Month tab)
    --------------------------------------------------------------- */
    .table-header {
        font-size: 1rem;
        font-weight: 800;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .card-subheading {
        display: block;
        font-size: 1.1rem;
        font-weight: 700;
        color: #14304F;
        margin-bottom: 0.5rem;
    }
    .status-paid {
        color: #22A06B;
        font-weight: 700;
    }
    .status-pending {
        color: #E0524A;
        font-weight: 700;
    }

    /* ---------------------------------------------------------------
       BATCH / TYPE PILLS — used on Fees Pending & Missed Last Month
       tables to color-code a student's batch (or "Gym"/"Student")
    --------------------------------------------------------------- */
    .batch-pill {
        display: inline-block;
        padding: 0.25rem 0.9rem;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 700;
        white-space: nowrap;
    }
    .batch-beginner {
        background-color: #EAF1FB;
        color: #1D4C82;
    }
    .batch-advanced-1 {
        background-color: #FBF0DC;
        color: #A9711B;
    }
    .batch-advanced-2 {
        background-color: #F3E8FB;
        color: #7B3FA0;
    }
    .batch-gym {
        background-color: #E3F5EA;
        color: #22A06B;
    }
    .batch-student {
        background-color: #FDEEDC;
        color: #B4530A;
    }
    .timing-4-5 {
        background-color: #E9F7F6;
        color: #0E7C86;
    }
    .timing-5-6 {
        background-color: #FDEEDC;
        color: #B4530A;
    }
    .timing-6-7 {
        background-color: #F3E8FB;
        color: #7B3FA0;
    }
    .timing-4-6 {
        background-color: #EAF1FB;
        color: #1D4C82;
    }

    /* ---------------------------------------------------------------
       ROW-ACTION BUTTONS — "Mark Paid" (red outline — represents an
       outstanding payment) and "Take Action" (neutral — may resolve
       to a payment OR a delete on the Missed Last Month tab). Both
       are centered within their table cell.

       FIX (this pass): these buttons had regressed to tiny centered
       squares with faint, unreadable 0.62rem text on DESKTOP. Root
       cause was two-fold:
         1) The button-text font-size rule below was accidentally
            written outside any @media query, so the mobile-only
            0.62rem size was applying on desktop too.
         2. div[class*="st-key-table_"] button[data-testid^="stBaseButton"]
            (further down this file) used the generic "table_" selector
            instead of scoping to table_students_roster specifically —
            because it carries an extra attribute selector, it has
            HIGHER CSS specificity than these btn_markpaid_/btn_takeaction_
            rules and was winning regardless of source order, forcing
            EVERY button inside ANY table_ container (including these)
            down to a fixed 2.1rem x 2.1rem square meant only for the
            Students Roster's Edit/Delete icon buttons.
       Fixed by: (a) giving these buttons explicit width/weight/color
       here with normal specificity, and (b) rescoping the offending
       rule down below to table_students_roster only, so it no longer
       reaches these buttons at all. Desktop sizing now stays legible;
       the mobile-specific shrink (still wanted on phones) lives ONLY
       inside the existing @media (max-width: 640px) block further
       down and is no longer duplicated up here.
    --------------------------------------------------------------- */
    div[class*="st-key-btn_markpaid_"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div[class*="st-key-btn_markpaid_"] button {
        background-color: transparent !important;
        border: 1.5px solid #E0524A !important;
        border-radius: 8px !important;
        width: 100% !important;
        min-width: 0 !important;
        height: auto !important;
        padding: 0.4rem 0.6rem !important;
    }
    div[class*="st-key-btn_markpaid_"] button p {
        color: #E0524A !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }
    div[class*="st-key-btn_markpaid_"] button:hover {
        background-color: #FBE7E6 !important;
    }

    div[class*="st-key-btn_takeaction_"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div[class*="st-key-btn_takeaction_"] button {
        width: 100% !important;
        min-width: 0 !important;
        height: auto !important;
        padding: 0.4rem 0.6rem !important;
    }
    div[class*="st-key-btn_takeaction_"] button p {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }

    /* ---------------------------------------------------------------
       "+ Add Transaction" button (Overview page)
    --------------------------------------------------------------- */
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

    /* ---------------------------------------------------------------
       "View Full Log" page-link (Overview page) — div.stPageLink a is
       the confirmed-correct selector (Entry 33); earlier
       stPageLink-NavLink/kind="secondary" guesses never matched.
    --------------------------------------------------------------- */
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

    /* ---------------------------------------------------------------
       CARD — kill default Streamlit gaps so button/link rows inside
       a card line up cleanly (e.g. "+ Add Transaction" / "View Full
       Log →" sitting on the same row, Entry 33)
    --------------------------------------------------------------- */
    div[class*="st-key-card_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"],
    div[class*="st-key-card_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        justify-content: center !important;
    }
    div[class*="st-key-table_"] {
        gap: 0 !important;
    }

    /* ---------------------------------------------------------------
       TABLE ROWS — the "table_" container wraps just the header +
       data rows inside a card, so border/divider/centering CSS stays
       scoped to actual rows without leaking onto sibling buttons/links
       that share the same outer "card_" panel (three-tier nesting
       pattern: card_ > table_ > theader_, Entry 33).
    --------------------------------------------------------------- */
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] {
        margin-bottom: 0 !important;
        border-bottom: 1px solid #B9C4D3 !important;
        align-items: stretch !important;
        gap: 0 !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-right: 1px solid #B9C4D3 !important;
        padding: 0.45rem 0.75rem !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"],
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        min-height: unset !important;
        height: auto !important;
        width: 100% !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] [data-testid="stElementContainer"] {
        margin: 0 !important;
        padding: 0 !important;
        height: auto !important;
        min-height: unset !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] [data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[class*="st-key-table_"] p {
        font-size: 1.05rem !important;
        line-height: 1.3 !important;
        margin-bottom: 0 !important;
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

    /* ---------------------------------------------------------------
       BUTTONS INSIDE TABLE ROWS — Streamlit's own button wrapper
       (.stButton) and the <button> itself carry default padding/
       min-height that made button rows visibly taller than plain-
       text rows; this collapses them down to match. Kept generic
       (applies to any table_ container) since it's just padding/
       height normalization, not a fixed-size override.
    --------------------------------------------------------------- */
    div[class*="st-key-table_"] .stButton {
        min-height: unset !important;
        height: auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div[class*="st-key-table_"] .stButton button {
        padding: 0.35rem 0.9rem !important;
        line-height: 1.2 !important;
        min-height: unset !important;
        height: auto !important;
    }

    /* -----------------------------------------------------------
       FIX (this pass): this fixed-square button-size rule is for
       the Students Roster's Edit/Delete ICON buttons only. It was
       previously written against the generic "table_" selector,
       which — because it carries an extra attribute selector — has
       higher specificity than the btn_markpaid_/btn_takeaction_
       rules above and was silently shrinking Mark Paid / Take
       Action buttons on the Pending page into 2.1rem squares too.
       Rescoped to table_students_roster only so it can no longer
       reach any other page's buttons.
    ----------------------------------------------------------- */
    div[class*="st-key-table_students_roster"] button[data-testid^="stBaseButton"] {
        min-height: unset !important;
        height: 2.1rem !important;
        width: 2.1rem !important;
        padding: 0.3rem !important;
        line-height: 1.2 !important;
        flex-shrink: 0 !important;
        min-width: 34px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] {
        display: flex !important;
        gap: 0.5rem !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        align-items: center !important;
        width: auto !important;
        min-width: 0 !important;
        border-bottom: none !important;
    }
    div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
    div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: 0 !important;
        padding: 0 !important;
        border-right: none !important;
    }
    div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] [data-testid="stVerticalBlock"] {
        height: auto !important;
        min-height: unset !important;
    }
    div[class*="st-key-table_"] .stButton button p {
        line-height: 1.2 !important;
        margin: 0 !important;
    }

    /* Outer border around the whole table */
    div[class*="st-key-table_"] {
        border: 1px solid #8FA0B8 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Header row — darker divider lines than the data rows */
    div[class*="st-key-theader_"] [data-testid="stHorizontalBlock"] {
        border-bottom: 2px solid #8FA0B8 !important;
    }
    div[class*="st-key-theader_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
    div[class*="st-key-theader_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        border-right: 2px solid #8FA0B8 !important;
    }

    /* ---------------------------------------------------------------
       MOBILE — force table rows back to row-direction (Streamlit
       defaults to column-stacking horizontal blocks under 640px) and
       shrink text/padding so all columns fit side by side on a phone.
       This generic block is fine to keep un-scoped: it only affects
       tables that DON'T also have the students_roster-specific fixed
       pixel-width block further below (which overrides it there).
    --------------------------------------------------------------- */
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
        .batch-pill {
            font-size: 0.62rem !important;
            padding: 0.15rem 0.5rem !important;
            white-space: normal !important;
            word-break: normal !important;
            overflow-wrap: break-word !important;
        }
        /* Mark Paid / Take Action: mobile-only shrink lives HERE and
           only here now — no longer duplicated outside this media
           query, which was what broke desktop sizing (see fix note
           above). */
        div[class*="st-key-btn_markpaid_"] button,
        div[class*="st-key-btn_takeaction_"] button {
            font-size: 0.7rem !important;
            padding: 0.35rem 0.4rem !important;
            white-space: normal !important;
            line-height: 1.2 !important;
            width: 100% !important;
        }
        div[class*="st-key-btn_markpaid_"] button p,
        div[class*="st-key-btn_takeaction_"] button p {
            white-space: normal !important;
            font-size: 0.7rem !important;
            font-weight: 700 !important;
        }
        div[class*="st-key-table_"] [data-testid="stHorizontalBlock"] {
            min-height: 3.4rem !important;
        }
    }
    /* ---------------------------------------------------------------
       PAGINATION CONTROLS — Previous/Next + "Page X of Y", used
       below any paginated table (Students Roster, and future
       paginated tables)
    --------------------------------------------------------------- */
    div[class*="st-key-pagination_"] {
        margin-top: 0.75rem !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    div[class*="st-key-pagination_"] [data-testid="stHorizontalBlock"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 0.75rem !important;
        flex-wrap: nowrap !important;
        max-width: 100% !important;
    }
    div[class*="st-key-pagination_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
    div[class*="st-key-pagination_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[class*="st-key-pagination_"] button {
        background-color: #1D4C82 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
    }
    div[class*="st-key-pagination_"] button p {
        color: #FFFFFF !important;
    }
    div[class*="st-key-pagination_"] button:hover:not(:disabled) {
        background-color: #14304F !important;
    }
    div[class*="st-key-pagination_"] button:disabled {
        background-color: #D7E1EE !important;
        opacity: 1 !important;
    }
    div[class*="st-key-pagination_"] button:disabled p {
        color: #9AA6B5 !important;
    }
    .pagination-label {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        font-weight: 700;
        color: #14304F;
        font-size: 1.05rem;
        white-space: nowrap;
    }
    /* ---------------------------------------------------------------
       MOBILE — Students Roster table specifically: too many columns
       to shrink-to-fit without mangling text, so give it a fixed
       comfortable width and let the card scroll horizontally instead.

       FIX (this pass, overlap bug): the nth-child(1)-(8) width rules
       below apply to ANY [data-testid="stHorizontalBlock"] inside
       table_students_roster — but the nested Edit/Delete
       st.columns(2) is ALSO a stHorizontalBlock with its own columns
       1 and 2. That meant Edit was inheriting the Name column's
       160px width and Delete was inheriting the Batch column's
       150px width, which is exactly the "Edit covers Date, table
       breaks near Delete" overlap reported. Fixed by re-asserting
       auto/fit-content sizing on any NESTED stHorizontalBlock's
       columns, placed AFTER the nth-child rules so it wins (same
       specificity, later in source order).

       FIX (this pass, pagination-pushed-offscreen bug): a flex item
       with overflow-x:auto still won't scroll and instead expands
       past its container if it doesn't also get min-width:0 (the
       default flex min-width is content-based, not 0). That let this
       900px-wide table push the whole card — and everything below it,
       including the pagination row — wider than the viewport. Fixed
       by forcing min-width:0 + box-sizing on this container and its
       ancestor card, in addition to the existing overflow-x:auto.

       FIX (this pass, border-completeness bug): the outer row was
       computing to an exact 900px box (matching min-width) even
       though the real content — all 8 columns summed via
       getBoundingClientRect() — measured 945px. `width: max-content`
       was NOT resolving to that true content width in this flex/
       scroll context (confirmed via console: computed width landed
       on exactly 900px, the min-width floor, not 945px). Since
       border-bottom paints along the row's own box, it stopped 45px
       short of where the Actions column's border-right actually
       rendered — that 45px gap is what looked like a missing/
       incomplete border once scrolled to the right edge. Fixed by
       replacing the unreliable `width: max-content` with a hardcoded
       `950px` (content width + a small buffer) on both width and
       min-width, so the row box is always guaranteed wide enough for
       its own border to reach past the last column. If a future
       column is added/removed from this table, this value may need
       revisiting (sum of column widths below + ~5-10px buffer).
    --------------------------------------------------------------- */
    @media (max-width: 640px) {
        div[class*="st-key-card_students_roster"] {
            min-width: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            overflow-x: hidden !important;
        }
        div[class*="st-key-table_students_roster"] {
            overflow-x: auto !important;
            overflow-y: visible !important;
            -webkit-overflow-scrolling: touch !important;
            min-width: 0 !important;
            max-width: 100% !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            min-width: 945px !important;
            width: 945px !important;
        }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) { flex: 0 0 160px !important; width: 160px !important; }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) { flex: 0 0 150px !important; width: 150px !important; }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3) { flex: 0 0 85px !important; width: 85px !important; }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(4) { flex: 0 0 140px !important; width: 140px !important; }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(5),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(5) { flex: 0 0 120px !important; width: 120px !important; }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(6) { flex: 0 0 120px !important; width: 120px !important; }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(7) { flex: 0 0 80px !important; width: 80px !important; }
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(8),
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(8) { flex: 0 0 90px !important; width: 90px !important; }

        /* Re-assert AFTER the nth-child rules above: the nested
           Edit/Delete columns must NOT inherit those fixed widths —
           this is the fix for the overlap bug described above. */
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 0 0 auto !important;
            width: auto !important;
            min-width: 0 !important;
        }
        /* The nested block ITSELF (not just its column children) was
           also inheriting min-width:900px from the outer row rule
           above via plain descendant matching — width:auto alone
           doesn't cancel a min-width constraint, which is what was
           still leaving a large empty gap before the Edit/Delete
           buttons. Explicitly zero it here. */
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] {
            min-width: 0 !important;
            width: auto !important;
            flex: 0 0 auto !important;
        }

        div[class*="st-key-table_students_roster"] p,
        div[class*="st-key-table_students_roster"] .table-header {
            font-size: 0.8rem !important;
            white-space: normal !important;
        }
        div[class*="st-key-table_students_roster"] .batch-pill {
            white-space: nowrap !important;
            font-size: 0.75rem !important;
        }

        /* On mobile the table scrolls horizontally, but the table's
           outer rounded border (border + border-radius, set on the
           static, non-scrolling table_ box) doesn't travel with the
           scrolled content — by the time you scroll right to see
           Actions, you've scrolled past where that border was drawn,
           so the row/header appear to have no closing border at all
           ("cell borders ending"). The generic :last-child rule
           (which removes border-right on the last column, correct
           for the STATIC/unscrolled case) is what's removing the one
           border that would otherwise close off the row visually
           while scrolled. Re-enable it here, scoped to Students
           Roster's mobile view only, for both data rows and header. */
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child,
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
            border-right: 1px solid #8FA0B8 !important;
        }
        div[class*="st-key-theader_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child,
        div[class*="st-key-theader_students_roster"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
            border-right: 2px solid #8FA0B8 !important;
        }
        /* FIX (this pass): the two :last-child re-enable rules above
           are descendant selectors — they don't care HOW DEEP the
           stHorizontalBlock is, only that the column is the last
           child of *some* stHorizontalBlock inside the table. That
           means they also matched the last child of the NESTED
           Edit/Delete stHorizontalBlock (i.e. the Delete button's
           own column), incorrectly re-adding a border-right onto
           Delete itself — the stray vertical line reported right
           after the Delete button. This rule is written with one
           extra [data-testid="stHorizontalBlock"] token, giving it
           higher specificity than the two rules above regardless of
           source order, so it reliably wins and cancels the border
           on the nested column specifically, leaving the OUTER
           Actions column's re-enabled border-right (the one that's
           actually needed to close off the row) untouched. */
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child,
        div[class*="st-key-table_students_roster"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
            border-right: none !important;
        }
    }

    /* ---------------------------------------------------------------
       MOBILE — pagination row: Streamlit's default column-stacking
       for horizontal blocks under 640px breaks the centered row and
       stretches buttons full-width; force it back to a compact row.
       Also hardened with min-width:0/max-width so it can never be
       pushed off-screen by a sibling table expanding above it.
    --------------------------------------------------------------- */
    @media (max-width: 640px) {
        div[class*="st-key-pagination_"] {
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }
        div[class*="st-key-pagination_"] [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            min-width: 0 !important;
            max-width: 100% !important;
        }
        div[class*="st-key-pagination_"] [data-testid="stHorizontalBlock"] > div[data-testid="column"],
        div[class*="st-key-pagination_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            min-width: 0 !important;
        }
        div[class*="st-key-pagination_"] button {
            padding: 0.45rem 0.9rem !important;
            font-size: 0.85rem !important;
        }
    }
    @media (max-width: 640px) {
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .block-container,
        [data-testid="stVerticalBlock"] {
            min-width: 0 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# apply_tab_styles()
# Styles st.tabs() — full-width, equally-divided segmented-button tab bar
# (Coach Salary Pending / Fees Pending / Students Missed Last Month, and
# any future st.tabs() usage elsewhere in the app).
# =============================================================================

def apply_tab_styles():
    st.markdown("""
    <style>
    /* Kill default underline/border chrome around the tab list itself
       (this Streamlit version uses react-aria-components, not baseweb —
       real selectors confirmed via DevTools, see build log Entry 34+) */
    div[data-testid="stTabs"] div[data-rac][data-orientation="horizontal"] {
        border-bottom: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stTabs"] > div {
        border-bottom: none !important;
        box-shadow: none !important;
    }

    /* The tab-list track — full width, equal 3-way flex split, light
       background so the active pill stands out against it */
    div[data-testid="stTabs"] [role="tablist"] {
        display: flex !important;
        width: 100% !important;
        gap: 0.4rem !important;
        background-color: #EEF3F9 !important;
        border-radius: 12px !important;
        padding: 6px !important;
        border-bottom: none !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Each individual tab */
    div[data-testid="stTab"] {
        flex: 1 1 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        background-color: transparent !important;
        border-radius: 9px !important;
        padding: 0.7rem 1rem !important;
    }
    div[data-testid="stTab"],
    div[data-testid="stTab"] p,
    div[data-testid="stTab"] span {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #14304F !important;
    }
    div[data-testid="stTab"][aria-selected="true"] {
        background-color: #14304F !important;
    }
    div[data-testid="stTab"][aria-selected="true"] p,
    div[data-testid="stTab"][aria-selected="true"] span {
        color: #FFFFFF !important;
    }

    /* Hide react-aria's own underline-indicator element — a solid pill
       fill (above) replaces it, so no separate indicator is needed */
    [data-testid="stTabHighlight"] {
        display: none !important;
    }
    .react-aria-SelectionIndicator {
        display: none !important;
    }
    @media (max-width: 640px) {
        div[data-testid="stTabs"] [role="tablist"] {
            overflow-x: hidden !important;
            flex-wrap: nowrap !important;
        }
        div[data-testid="stTab"] {
            flex: 1 1 0 !important;
            min-width: 0 !important;
            padding: 0.5rem 0.2rem !important;
        }
        div[data-testid="stTab"],
        div[data-testid="stTab"] p,
        div[data-testid="stTab"] span {
            font-size: 0.7rem !important;
            white-space: normal !important;
            line-height: 1.15 !important;
            text-align: center !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# apply_login_styles()
# Login page only — full-bleed background image with a frosted-glass
# left-positioned form card. Called from the login screen, not apply_theme().
# =============================================================================

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

        /* Full-viewport background image container (position: fixed with
           explicit 100vw/100vh — NOT position: relative + min-height,
           which caused a white-border clipping bug, see Entry 30) */
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

        /* Frosted-glass form card, left-positioned, vertically centered */
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

        /* Form field styling — react-aria-components selectbox, not
           baseweb (see Entry 29) */
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

        /* Mobile — solid navy background instead of the image, card
           becomes a normal in-flow block instead of absolutely
           positioned. position: absolute (not the base rule's fixed)
           lets the page grow past 100vh and scroll — see Entry 31's
           scroll-trap fix; do not remove without re-testing on a real
           narrow device. */
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

# ============================================================
# Filter / Search Controls (search bar, dropdowns, date pickers,
# "+ Add X" primary buttons) — shared across roster-style pages
# ============================================================
def apply_filter_control_styles():
    st.markdown("""
        <style>
        div[data-testid="stTextInput"] input,
        div[data-testid="stDateInput"] input {
            background-color: #FFFFFF !important;
            border: 1px solid #D7E1EE !important;
            border-radius: 10px !important;
            padding: 0.55rem 0.9rem !important;
            font-size: 0.95rem !important;
        }
        div[data-testid="stSelectbox"] {
            border-radius: 10px !important;
        }

        div[class*="st-key-btn_add_student"] button,
        div[class*="st-key-btn_add_gym"] button,
        div[class*="st-key-btn_add_coach"] button {
            background-color: #1D4C82 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.4rem !important;
            width: 100% !important;
        }
        div[class*="st-key-btn_add_student"] button:hover,
        div[class*="st-key-btn_add_gym"] button:hover,
        div[class*="st-key-btn_add_coach"] button:hover {
            background-color: #14304F !important;
        }
        </style>
    """, unsafe_allow_html=True)