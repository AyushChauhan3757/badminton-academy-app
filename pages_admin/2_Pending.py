import streamlit as st
import calendar
from utils.auth import require_role, now_ist
from constants import ROLE_ADMIN
from db.payments import get_pending_fees, mark_fee_paid

require_role([ROLE_ADMIN])

st.title("Fees Pending")

today = now_ist()
current_month = today.month
current_year = today.year

# Highlight rule: final 7 days of the month (spec: today >= last_day - 6)
last_day = calendar.monthrange(current_year, current_month)[1]
show_highlight = today.day >= (last_day - 6)

pending = get_pending_fees(current_month, current_year)

# Combined list, sorted by name. A person who is both a student and a gym
# member will naturally appear as two separate rows (different payer_type),
# since get_pending_fees() already returns them as distinct entries.
combined = sorted(pending, key=lambda p: p['name'].lower())

# --- Search bar + Confirm button (shared, acts on the combined list) ---
top_cols = st.columns([0.7, 0.3])

with top_cols[0]:
    search_term = st.text_input("Search", placeholder="Search by name...", label_visibility="collapsed")

if search_term:
    combined_filtered = [p for p in combined if search_term.lower() in p['name'].lower()]
else:
    combined_filtered = combined

def row_key(p):
    return f"chk_{p['payer_type']}_{p['payer_id']}"

selected = [p for p in combined_filtered if st.session_state.get(row_key(p), False)]
total_selected = len(selected)

with top_cols[1]:
    confirm_clicked = st.button(
        f"{total_selected} Mark As Paid",
        key="confirm_all",
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
            marked_by="admin"
        )
        del st.session_state[row_key(p)]
    st.rerun()

st.divider()

# --- Combined list, two-column grid, filled row by row (left, right) ---
# --- Combined list, two-column grid, filled row by row (left, right) ---
if not combined_filtered:
    st.info("No one pending for this month.")
else:
    def render_cells(cols, offset, p):
        type_label = "Student" if p['payer_type'] == 'student' else "Gym"
        cols[offset].checkbox("", key=row_key(p))
        name_display = f"**{p['name']}**"
        if show_highlight:
            name_display = f"🔴 {name_display}"
        cols[offset + 1].markdown(name_display)
        cols[offset + 2].markdown(type_label)
        cols[offset + 3].markdown(f"₹{p['amount']}")

    col_widths = [0.05, 0.17, 0.1, 0.1, 0.05, 0.17, 0.1, 0.1]

    for i in range(0, len(combined_filtered), 2):
        row_cols = st.columns(col_widths)
        render_cells(row_cols, 0, combined_filtered[i])
        if i + 1 < len(combined_filtered):
            render_cells(row_cols, 4, combined_filtered[i + 1])