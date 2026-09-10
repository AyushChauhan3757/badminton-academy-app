import streamlit as st
import calendar
from datetime import date
from utils.auth import require_role, now_ist
from constants import ROLE_COACH
from db.payments import get_pending_fees, mark_fee_paid, get_paid_fees
from utils.header import render_header

require_role([ROLE_COACH])

render_header("Fees Pending")

today = now_ist()
current_month = today.month
current_year = today.year

# Fixed height for the scrollable row area — matches the Admin Pending page's constant
# so both roles' tables look/behave consistently.
TABLE_ROWS_HEIGHT = 380

# Highlight rule: final 7 days of the month (spec: today >= last_day - 6)
last_day = calendar.monthrange(current_year, current_month)[1]
show_highlight = today.day >= (last_day - 6)

# --- Fetch and split into Students / Gym ---
pending = get_pending_fees(current_month, current_year)
paid = get_paid_fees(current_month, current_year)

pending_students = sorted([p for p in pending if p['payer_type'] == 'student'], key=lambda p: p['name'].lower())
pending_gym = sorted([p for p in pending if p['payer_type'] == 'gym'], key=lambda p: p['name'].lower())
paid_students = sorted([p for p in paid if p['payer_type'] == 'student'], key=lambda p: p['name'].lower())
paid_gym = sorted([p for p in paid if p['payer_type'] == 'gym'], key=lambda p: p['name'].lower())

# --- Shared search bar (filters all four tables by name) ---
search_term = st.text_input("Search", placeholder="Search by name...", label_visibility="collapsed")

def filter_by_search(lst):
    if not search_term:
        return lst
    return [p for p in lst if search_term.lower() in p['name'].lower()]

pending_students = filter_by_search(pending_students)
pending_gym = filter_by_search(pending_gym)
paid_students = filter_by_search(paid_students)
paid_gym = filter_by_search(paid_gym)

st.divider()

def row_key(p):
    return f"coach_chk_{p['payer_type']}_{p['payer_id']}"

def render_not_paid_table(title, items, button_key):
    with st.container(border=True):
        st.markdown(f"**{title}**")

        selected = [p for p in items if st.session_state.get(row_key(p), False)]
        total_selected = len(selected)

        confirm_clicked = st.button(
            f"{total_selected} Mark As Paid",
            key=button_key,
            disabled=total_selected == 0
        )

        if confirm_clicked:
            for p in selected:
                mark_fee_paid(
                    payer_type=p['payer_type'],
                    payer_id=p['payer_id'],
                    amount=p['amount'],
                    month=current_month,
                    year=current_year,
                    marked_by="coach"
                )
                del st.session_state[row_key(p)]
            st.rerun()

        col_widths = [0.1, 0.6, 0.3]
        header_cols = st.columns(col_widths)
        header_cols[1].markdown("**Name**")
        header_cols[2].markdown("**Amount**")

        with st.container(height=TABLE_ROWS_HEIGHT, border=False):
            if not items:
                st.info("Nothing pending.")
            else:
                for p in items:
                    row_cols = st.columns(col_widths)
                    row_cols[0].checkbox("", key=row_key(p), label_visibility="collapsed")
                    name_display = f"**{p['name']}**"
                    if show_highlight:
                        name_display = f"🔴 {name_display}"
                    row_cols[1].markdown(name_display)
                    row_cols[2].markdown(f"₹{p['amount']}")


def render_paid_table(title, items):
    with st.container(border=True):
        st.markdown(f"**{title}**")

        # Invisible spacer matching the "Mark As Paid" button's height on the
        # Not-Paid panels, so both panel types line up in the grid.
        st.markdown(
            "<div style='height:3.5rem;'></div>",
            unsafe_allow_html=True
        )

        col_widths = [0.4, 0.3, 0.3]
        header_cols = st.columns(col_widths)
        header_cols[0].markdown("**Name**")
        header_cols[1].markdown("**Paid On**")
        header_cols[2].markdown("**Marked By**")

        with st.container(height=TABLE_ROWS_HEIGHT, border=False):
            if not items:
                st.info("No one has paid yet.")
            else:
                for p in items:
                    paid_on_display = date.fromisoformat(p['paid_on']).strftime("%d/%m/%Y")
                    marked_by_display = p['marked_by'].capitalize()

                    row_cols = st.columns(col_widths)
                    row_cols[0].markdown(f"~~{p['name']}~~")
                    row_cols[1].markdown(paid_on_display)
                    row_cols[2].markdown(marked_by_display)

# --- 2x2 grid: Students row, then Gym row ---
row1_left, row1_right = st.columns(2)
with row1_left:
    render_not_paid_table("Students — Not Paid", pending_students, button_key="coach_confirm_students")
with row1_right:
    render_paid_table("Students — Paid", paid_students)

row2_left, row2_right = st.columns(2)
with row2_left:
    render_not_paid_table("Gym Members — Not Paid", pending_gym, button_key="coach_confirm_gym")
with row2_right:
    render_paid_table("Gym Members — Paid", paid_gym)