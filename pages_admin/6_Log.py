import streamlit as st
from datetime import date, timedelta
from utils.auth import require_role, now_ist
from constants import ROLE_ADMIN
from db.log import get_log_page, get_log_total_count, PAGE_SIZE
from utils.header import render_header

require_role([ROLE_ADMIN])

render_header("Activity Log")

# --- Session state defaults ---
if "log_page" not in st.session_state:
    st.session_state.log_page = 1
if "log_category_filter" not in st.session_state:
    st.session_state.log_category_filter = "All"
if "log_start_date" not in st.session_state:
    st.session_state.log_start_date = None
if "log_end_date" not in st.session_state:
    st.session_state.log_end_date = None
if "log_active_preset" not in st.session_state:
    st.session_state.log_active_preset = None  # 'this_month' | 'last_month' | 'last_year' | 'custom' | None
if "log_search" not in st.session_state:
    st.session_state.log_search = ""

today = now_ist().date()


def _reset_to_page_1():
    st.session_state.log_page = 1


def _first_day_of_month(d):
    return d.replace(day=1)


def _last_day_of_prev_month(d):
    return _first_day_of_month(d) - timedelta(days=1)


def _btn_type(preset_name):
    return "primary" if st.session_state.log_active_preset == preset_name else "secondary"


# --- Search bar ---
with st.container(key="log_top_row"):
    search_text = st.text_input(
        "Search",
        placeholder="Search by name or description...",
        label_visibility="collapsed",
        key="log_search_input",
    )

if search_text != st.session_state.log_search:
    st.session_state.log_search = search_text
    _reset_to_page_1()

# --- Date range presets ---
with st.container(key="log_presets_row"):
    preset_cols = st.columns(4)

    with preset_cols[0]:
        if st.button("This month", type=_btn_type("this_month"), key="log_btn_this_month", use_container_width=True):
            st.session_state.log_start_date = _first_day_of_month(today)
            st.session_state.log_end_date = today
            st.session_state.log_active_preset = "this_month"
            _reset_to_page_1()
            st.rerun()

    with preset_cols[1]:
        if st.button("Last month", type=_btn_type("last_month"), key="log_btn_last_month", use_container_width=True):
            last_month_end = _last_day_of_prev_month(today)
            st.session_state.log_start_date = _first_day_of_month(last_month_end)
            st.session_state.log_end_date = last_month_end
            st.session_state.log_active_preset = "last_month"
            _reset_to_page_1()
            st.rerun()

    with preset_cols[2]:
        if st.button("Last year", type=_btn_type("last_year"), key="log_btn_last_year", use_container_width=True):
            prev_year = today.year - 1
            st.session_state.log_start_date = date(prev_year, 1, 1)
            st.session_state.log_end_date = date(prev_year, 12, 31)
            st.session_state.log_active_preset = "last_year"
            _reset_to_page_1()
            st.rerun()

    with preset_cols[3]:
        if st.button("Reset", type="secondary", key="log_btn_reset", use_container_width=True):
            st.session_state.log_start_date = None
            st.session_state.log_end_date = None
            st.session_state.log_active_preset = None
            _reset_to_page_1()
            st.rerun()

# --- Category + custom date range ---
filter_options = {
    "All": None,
    "Fees only": "fee",
    "Bills/Salary only": "bill",
}

with st.container(key="log_filters_row"):
    filter_cols = st.columns([1.2, 1, 1])

    with filter_cols[0]:
        selected_label = st.selectbox(
            "Category",
            options=list(filter_options.keys()),
            index=list(filter_options.keys()).index(st.session_state.log_category_filter),
        )
    with filter_cols[1]:
        custom_start = st.date_input(
            "From", value=st.session_state.log_start_date, format="DD/MM/YYYY", key="log_from_input"
        )
    with filter_cols[2]:
        custom_end = st.date_input(
            "To", value=st.session_state.log_end_date, format="DD/MM/YYYY", key="log_to_input"
        )

if selected_label != st.session_state.log_category_filter:
    st.session_state.log_category_filter = selected_label
    _reset_to_page_1()

if custom_start != st.session_state.log_start_date or custom_end != st.session_state.log_end_date:
    st.session_state.log_start_date = custom_start
    st.session_state.log_end_date = custom_end
    st.session_state.log_active_preset = "custom"
    _reset_to_page_1()

category_filter = filter_options[st.session_state.log_category_filter]
start_date_str = st.session_state.log_start_date.isoformat() if st.session_state.log_start_date else None
end_date_str = st.session_state.log_end_date.isoformat() if st.session_state.log_end_date else None

# --- Data ---
total_count = get_log_total_count(
    category_filter=category_filter,
    start_date=start_date_str,
    end_date=end_date_str,
    search=st.session_state.log_search,
)
total_pages = max(1, (total_count + PAGE_SIZE - 1) // PAGE_SIZE)

if st.session_state.log_page > total_pages:
    st.session_state.log_page = total_pages

rows = get_log_page(
    page=st.session_state.log_page,
    category_filter=category_filter,
    start_date=start_date_str,
    end_date=end_date_str,
    search=st.session_state.log_search,
)

COL_WIDTHS = [1.2, 1.2, 2.6, 1.4]

# --- Table card ---
with st.container(key="card_log"):
    st.subheader("All Activity")

    if not rows:
        st.info("No activity found for this filter.")
    else:
        with st.container(key="table_log"):
            with st.container(key="theader_log"):
                header_cols = st.columns(COL_WIDTHS)
                for col, label in zip(header_cols, ["Date", "Category", "Description", "Amount (₹)"]):
                    col.markdown(f'<span class="table-header">{label}</span>', unsafe_allow_html=True)

            for row in rows:
                is_out = row["category"].lower() in ("expense", "salary")
                color = "#E0524A" if is_out else "#22A06B"
                sign = "-" if is_out else "+"
                display_date = date.fromisoformat(row["date"]).strftime("%d/%m/%Y")

                cols = st.columns(COL_WIDTHS)
                cols[0].markdown(display_date)
                cols[1].markdown(
                    f'<span style="color:{color}; font-weight:700;">{row["category"].capitalize()}</span>',
                    unsafe_allow_html=True,
                )
                cols[2].markdown(row["description"])
                cols[3].markdown(
                    f'<span style="color:{color}; font-weight:700;">{sign}₹{row["amount"]:,}</span>',
                    unsafe_allow_html=True,
                )

    with st.container(key="pagination_log"):
        nav_cols = st.columns(3)
        with nav_cols[0]:
            if st.button("← Previous", key="log_prev", disabled=(st.session_state.log_page <= 1)):
                st.session_state.log_page -= 1
                st.rerun()
        with nav_cols[1]:
            st.markdown(
                f'<div class="pagination-label">Page {st.session_state.log_page} of {total_pages}</div>',
                unsafe_allow_html=True,
            )
        with nav_cols[2]:
            if st.button("Next →", key="log_next", disabled=(st.session_state.log_page >= total_pages)):
                st.session_state.log_page += 1
                st.rerun()