import streamlit as st
from utils.auth import require_role
from constants import ROLE_ADMIN
from db.overview import get_totals
from db.overview import get_recent_log

require_role([ROLE_ADMIN])

st.title("Overview")

totals = get_totals()

st.subheader("Lifetime")
col1, col2, col3 = st.columns(3)
col1.metric("Total Received", f"₹{totals['lifetime_received']:,}")
col2.metric("Total Paid", f"₹{totals['lifetime_paid']:,}")
col3.metric("Profit", f"₹{totals['lifetime_profit']:,}")

st.subheader("This Month")
col4, col5, col6 = st.columns(3)
col4.metric("Received", f"₹{totals['month_received']:,}")
col5.metric("Paid", f"₹{totals['month_paid']:,}")
col6.metric("Profit", f"₹{totals['month_profit']:,}")

col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("+ Add Transaction"):
        st.session_state.show_add_transaction = True
with col_b:
    if st.button("View Full Log"):
        st.info("Full Log page is coming in Step 11 — not built yet.")

if st.session_state.get("show_add_transaction"):
    @st.dialog("Add Transaction")
    def add_transaction_dialog():
        title = st.text_input("Title")
        amount = st.number_input("Amount (₹)", min_value=0, step=100)

        col1, col2 = st.columns(2)
        if col1.button("Add", use_container_width=True):
            if title.strip() and amount > 0:
                from db.overview import add_transaction
                add_transaction(title.strip(), amount)
                st.session_state.show_add_transaction = False
                st.rerun()
            else:
                st.error("Please enter a title and an amount greater than 0.")
        if col2.button("Cancel", use_container_width=True):
            st.session_state.show_add_transaction = False
            st.rerun()

    add_transaction_dialog()

st.subheader("Recent Activity")

log_rows = get_recent_log(limit=10)

if not log_rows:
    st.info("No activity yet.")
else:
    for row in log_rows:
        category = row['category']
        description = row['description'] or "Deleted student/member"

        col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
        col1.write(row['date'])
        col2.write(category.capitalize())
        col3.write(description)
        col4.write(f"₹{row['amount']:,}")