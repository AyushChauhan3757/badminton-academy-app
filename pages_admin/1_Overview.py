import streamlit as st
from utils.auth import require_role
from constants import ROLE_ADMIN
from db.overview import get_totals
from db.overview import get_recent_log
from utils.header import render_header
from datetime import date

require_role([ROLE_ADMIN])

render_header("Overview")

totals = get_totals()

def format_rupees(amount):
    if amount < 0:
        return f"-₹{abs(amount):,}"
    return f"₹{amount:,}"

with st.container(key="kpi_section_desktop"):
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


def render_mobile_kpi(key, label, value):
    with st.container(border=True, key=key):
        st.markdown(f'''
        <div class="kpi-text">
            <div class="kpi-label-mobile">{label}</div>
            <div class="kpi-value-mobile">{format_rupees(value)}</div>
        </div>
        ''', unsafe_allow_html=True)


with st.container(key="kpi_section_mobile"):
    st.subheader("Lifetime & This Month")

    hcol1, hcol2 = st.columns(2)
    hcol1.markdown('<span class="table-header">Lifetime</span>', unsafe_allow_html=True)
    hcol2.markdown('<span class="table-header">This Month</span>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        render_mobile_kpi("kpi_m_received_life", "Received", totals["lifetime_received"])
    with r1c2:
        render_mobile_kpi("kpi_m_received_month", "Received", totals["month_received"])

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        render_mobile_kpi("kpi_m_paid_life", "Paid", totals["lifetime_paid"])
    with r2c2:
        render_mobile_kpi("kpi_m_paid_month", "Paid", totals["month_paid"])

    r3c1, r3c2 = st.columns(2)
    with r3c1:
        render_mobile_kpi("kpi_m_profit_life", "Profit", totals["lifetime_profit"])
    with r3c2:
        render_mobile_kpi("kpi_m_profit_month", "Profit", totals["month_profit"])


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
        if st.button("+ Add Transaction", key="btn_add_transaction"):
            st.session_state.show_add_transaction = True
    with col_b:
        st.page_link("pages_admin/6_Log.py", label="View Full Log →", use_container_width=True)

    log_rows = get_recent_log(limit=10)

    if not log_rows:
        st.info("No activity yet.")
    else:
        with st.container(key="table_recent_activity"):
            with st.container(key="theader_recent_activity"):
                header_col1, header_col2, header_col3, header_col4 = st.columns([1.3, 1.4, 3.3, 1.5], gap="small")
                header_col1.markdown('<span class="table-header">Date</span>', unsafe_allow_html=True)
                header_col2.markdown('<span class="table-header">Category</span>', unsafe_allow_html=True)
                header_col3.markdown('<span class="table-header">Description</span>', unsafe_allow_html=True)
                header_col4.markdown('<span class="table-header">Amount (₹)</span>', unsafe_allow_html=True)

            for row in log_rows:
                category = row['category']
                description = row['description'] or "Deleted student/member"
                is_expense = category.lower() == 'expense'
                amount_color = "#E0524A" if is_expense else "#22A06B"
                sign = "-" if is_expense else "+"
                display_date = date.fromisoformat(row['date']).strftime('%d/%m/%Y')

                col1, col2, col3, col4 = st.columns([1.3, 1.4, 3.3, 1.5], gap="small")
                col1.write(display_date)
                col2.markdown(f'<span style="color:{amount_color}; font-weight:600;">{category.capitalize()}</span>', unsafe_allow_html=True)
                col3.write(description)
                col4.markdown(f'<span style="color:{amount_color}; font-weight:600;">{sign}₹{row["amount"]:,}</span>', unsafe_allow_html=True)