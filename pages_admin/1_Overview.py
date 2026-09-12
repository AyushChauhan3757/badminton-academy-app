import streamlit as st
from utils.auth import require_role
from constants import ROLE_ADMIN
from db.overview import get_totals
from db.overview import get_recent_log
from utils.header import render_header

require_role([ROLE_ADMIN])

render_header("Overview")

totals = get_totals()

def format_rupees(amount):
    if amount < 0:
        return f"-₹{abs(amount):,}"
    return f"₹{amount:,}"

st.subheader("Lifetime")
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True, key="kpi_lifetime_received"):
        st.markdown(f'''
        <div class="kpi-row">
            <div class="kpi-icon" style="background-color:#E0F2E9;"><span class="material-symbols-outlined" style="color:#22A06B;">payments</span></div>
            <div class="kpi-text">
                <div class="kpi-label">Total Received</div>
                <div class="kpi-value">{format_rupees(totals["lifetime_received"])}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

with col2:
    with st.container(border=True, key="kpi_lifetime_paid"):
        st.markdown(f'''
        <div class="kpi-row">
            <div class="kpi-icon" style="background-color:#FBE7E6;"><span class="material-symbols-outlined" style="color:#E0524A;">account_balance_wallet</span></div>
            <div class="kpi-text">
                <div class="kpi-label">Total Paid</div>
                <div class="kpi-value">{format_rupees(totals["lifetime_paid"])}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

with col3:
    with st.container(border=True, key="kpi_lifetime_profit"):
        st.markdown(f'''
        <div class="kpi-row">
            <div class="kpi-icon" style="background-color:#EAF1FB;"><span class="material-symbols-outlined" style="color:#1D4C82;">trending_up</span></div>
            <div class="kpi-text">
                <div class="kpi-label">Profit</div>
                <div class="kpi-value">{format_rupees(totals["lifetime_profit"])}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

st.subheader("This Month")
col4, col5, col6 = st.columns(3)

with col4:
    with st.container(border=True, key="kpi_month_received"):
        st.markdown(f'''
        <div class="kpi-row">
            <div class="kpi-icon" style="background-color:#E0F2E9;"><span class="material-symbols-outlined" style="color:#22A06B;">payments</span></div>
            <div class="kpi-text">
                <div class="kpi-label">Received</div>
                <div class="kpi-value">{format_rupees(totals["month_received"])}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

with col5:
    with st.container(border=True, key="kpi_month_paid"):
        st.markdown(f'''
        <div class="kpi-row">
            <div class="kpi-icon" style="background-color:#FBE7E6;"><span class="material-symbols-outlined" style="color:#E0524A;">account_balance_wallet</span></div>
            <div class="kpi-text">
                <div class="kpi-label">Paid</div>
                <div class="kpi-value">{format_rupees(totals["month_paid"])}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

with col6:
    with st.container(border=True, key="kpi_month_profit"):
        st.markdown(f'''
        <div class="kpi-row">
            <div class="kpi-icon" style="background-color:#EAF1FB;"><span class="material-symbols-outlined" style="color:#1D4C82;">trending_up</span></div>
            <div class="kpi-text">
                <div class="kpi-label">Profit</div>
                <div class="kpi-value">{format_rupees(totals["month_profit"])}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

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

with st.container(border=True, key="card_recent_activity"):
    st.subheader("Recent Activity")

    col_a, col_b = st.columns([3, 1])
    with col_a:
        if st.button("+ Add Transaction"):
            st.session_state.show_add_transaction = True
    with col_b:
        st.page_link("pages_admin/6_Log.py", label="View Full Log →")

    log_rows = get_recent_log(limit=10)

    if not log_rows:
        st.info("No activity yet.")
    else:
        header_col1, header_col2, header_col3, header_col4 = st.columns([2, 2, 3, 2])
        header_col1.markdown('<span class="table-header">Date</span>', unsafe_allow_html=True)
        header_col2.markdown('<span class="table-header">Category</span>', unsafe_allow_html=True)
        header_col3.markdown('<span class="table-header">Description</span>', unsafe_allow_html=True)
        header_col4.markdown('<span class="table-header">Amount (₹)</span>', unsafe_allow_html=True)

        st.markdown('<hr class="table-divider">', unsafe_allow_html=True)

        for row in log_rows:
            category = row['category']
            description = row['description'] or "Deleted student/member"
            is_expense = category.lower() == 'expense'
            amount_color = "#E0524A" if is_expense else "#22A06B"
            sign = "-" if is_expense else "+"

            col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
            col1.write(row['date'])
            col2.write(category.capitalize())
            col3.write(description)
            col4.markdown(f'<span style="color:{amount_color}; font-weight:600;">{sign}₹{row["amount"]:,}</span>', unsafe_allow_html=True)