import streamlit as st
from datetime import date, timedelta
from utils.auth import require_role, now_ist
from constants import ROLE_ADMIN
from db.log import get_log_page, get_log_total_count, PAGE_SIZE

require_role([ROLE_ADMIN])

st.title("Activity Log")

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

today = now_ist().date()


def _reset_to_page_1():
    st.session_state.log_page = 1


def _first_day_of_month(d):
    return d.replace(day=1)


def _last_day_of_prev_month(d):
    return _first_day_of_month(d) - timedelta(days=1)


def _btn_type(preset_name):
    return "primary" if st.session_state.log_active_preset == preset_name else "secondary"


# --- Category filter ---
filter_options = {
    "All": None,
    "Fees only": "fee",
    "Bills/Salary only": "bill",
}
selected_label = st.selectbox(
    "Category",
    options=list(filter_options.keys()),
    index=list(filter_options.keys()).index(st.session_state.log_category_filter),
)
if selected_label != st.session_state.log_category_filter:
    st.session_state.log_category_filter = selected_label
    _reset_to_page_1()

category_filter = filter_options[st.session_state.log_category_filter]

# --- Date range presets ---
st.markdown("**Date range**")
preset_cols = st.columns(4)

with preset_cols[0]:
    if st.button("This month", type=_btn_type("this_month")):
        st.session_state.log_start_date = _first_day_of_month(today)
        st.session_state.log_end_date = today
        st.session_state.log_active_preset = "this_month"
        _reset_to_page_1()
        st.rerun()

with preset_cols[1]:
    if st.button("Last month", type=_btn_type("last_month")):
        last_month_end = _last_day_of_prev_month(today)
        last_month_start = _first_day_of_month(last_month_end)
        st.session_state.log_start_date = last_month_start
        st.session_state.log_end_date = last_month_end
        st.session_state.log_active_preset = "last_month"
        _reset_to_page_1()
        st.rerun()

with preset_cols[2]:
    if st.button("Last year", type=_btn_type("last_year")):
        prev_year = today.year - 1
        st.session_state.log_start_date = date(prev_year, 1, 1)
        st.session_state.log_end_date = date(prev_year, 12, 31)
        st.session_state.log_active_preset = "last_year"
        _reset_to_page_1()
        st.rerun()

with preset_cols[3]:
    if st.button("Clear filter", type=_btn_type("cleared_unused")):
        st.session_state.log_start_date = None
        st.session_state.log_end_date = None
        st.session_state.log_active_preset = None
        _reset_to_page_1()
        st.rerun()

# --- Custom range picker ---
range_cols = st.columns(2)
with range_cols[0]:
    custom_start = st.date_input(
        "From", value=st.session_state.log_start_date, format="DD/MM/YYYY", key="log_from_input"
    )
with range_cols[1]:
    custom_end = st.date_input(
        "To", value=st.session_state.log_end_date, format="DD/MM/YYYY", key="log_to_input"
    )

if custom_start != st.session_state.log_start_date or custom_end != st.session_state.log_end_date:
    st.session_state.log_start_date = custom_start
    st.session_state.log_end_date = custom_end
    st.session_state.log_active_preset = "custom"
    _reset_to_page_1()

start_date_str = st.session_state.log_start_date.isoformat() if st.session_state.log_start_date else None
end_date_str = st.session_state.log_end_date.isoformat() if st.session_state.log_end_date else None

st.divider()

# --- Log display ---
total_count = get_log_total_count(category_filter=category_filter, start_date=start_date_str, end_date=end_date_str)
total_pages = max(1, (total_count + PAGE_SIZE - 1) // PAGE_SIZE)

if st.session_state.log_page > total_pages:
    st.session_state.log_page = total_pages

rows = get_log_page(
    page=st.session_state.log_page,
    category_filter=category_filter,
    start_date=start_date_str,
    end_date=end_date_str,
)

if not rows:
    st.info("No activity found for this filter.")
else:
    header_cols = st.columns([0.2, 0.2, 0.4, 0.2])
    header_cols[0].markdown("**Date**")
    header_cols[1].markdown("**Category**")
    header_cols[2].markdown("**Description**")
    header_cols[3].markdown("**Amount**")

    for row in rows:
        cols = st.columns([0.2, 0.2, 0.4, 0.2])
        cols[0].write(row["date"])
        cols[1].write(row["category"].capitalize())
        cols[2].write(row["description"])
        cols[3].write(f"₹{row['amount']:,}")

st.divider()

nav_cols = st.columns([0.15, 0.7, 0.15])
with nav_cols[0]:
    if st.button("← Previous", disabled=(st.session_state.log_page <= 1)):
        st.session_state.log_page -= 1
        st.rerun()
with nav_cols[1]:
    st.markdown(
        f"<div style='text-align:center;'>Page {st.session_state.log_page} of {total_pages}</div>",
        unsafe_allow_html=True,
    )
with nav_cols[2]:
    if st.button("Next →", disabled=(st.session_state.log_page >= total_pages)):
        st.session_state.log_page += 1
        st.rerun()