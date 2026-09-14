import streamlit as st
import calendar
from utils.auth import require_role, now_ist
from constants import ROLE_ADMIN
from utils.header import render_header
from db.payments import get_pending_fees, mark_fee_paid, get_paid_fees, get_missed_last_month

require_role([ROLE_ADMIN])

render_header("Pending")

today = now_ist()
current_month = today.month
current_year = today.year

def batch_pill(batch):
    css_class = "batch-" + batch.lower().replace(" ", "-")
    return f'<span class="batch-pill {css_class}">{batch}</span>'

tab_salary, tab_fees, tab_missed = st.tabs([
    "Coach Salary Pending",
    "Fees Pending",
    "Students Missed Last Month"
])

with tab_salary:
    from db.coaches import get_all_coaches
    from db.salary import get_salary_status, clear_coach_salary

    coaches = get_all_coaches()

    @st.dialog("Confirm Salary Payment")
    def confirm_salary_paid(coach):
        st.write(f"Mark **{coach['name']}**'s salary as paid for this month?")
        st.write(f"Amount: ₹{coach['salary']}")
        col_yes, col_no = st.columns(2)
        if col_yes.button("Yes", key=f"salary_yes_{coach['id']}", use_container_width=True):
            clear_coach_salary(
                coach_id=coach['id'],
                coach_name=coach['name'],
                salary_amount=coach['salary'],
                month=current_month,
                year=current_year
            )
            st.rerun()
        if col_no.button("Cancel", key=f"salary_no_{coach['id']}", use_container_width=True):
            st.rerun()

    with st.container(border=True, key="card_salary_pending"):

        col_widths = [0.4, 0.3, 0.3]

        if not coaches:
            st.info("No coaches added yet.")
        else:
            with st.container(key="table_salary_pending"):
                with st.container(key="theader_salary_pending"):
                    header_cols = st.columns(col_widths)
                    header_cols[0].markdown('<span class="table-header">Name</span>', unsafe_allow_html=True)
                    header_cols[1].markdown('<span class="table-header">Salary</span>', unsafe_allow_html=True)
                    header_cols[2].markdown('<span class="table-header">Status</span>', unsafe_allow_html=True)

                for coach in coaches:
                    row_cols = st.columns(col_widths)
                    row_cols[0].markdown(coach['name'])
                    row_cols[1].markdown(f"₹{coach['salary']}")

                    paid = get_salary_status(coach['id'], current_month, current_year)
                    if paid:
                        row_cols[2].markdown('<span class="status-paid">Paid</span>', unsafe_allow_html=True)
                    else:
                        if row_cols[2].button("Mark Paid", key=f"btn_markpaid_salary_{coach['id']}"):
                            confirm_salary_paid(coach)

with tab_fees:
    from datetime import date as date_cls

    pending_fees = get_pending_fees(current_month, current_year)
    paid_fees = get_paid_fees(current_month, current_year)

    # Highlight rule: final 7 days of the month (spec: today >= last_day - 6)
    last_day = calendar.monthrange(current_year, current_month)[1]
    show_highlight = today.day >= (last_day - 6)

    search_fees = st.text_input(
        "Search",
        placeholder="Search by name...",
        label_visibility="collapsed",
        key="search_fees_pending"
    )
    if search_fees:
        pending_fees = [p for p in pending_fees if search_fees.lower() in p['name'].lower()]
        paid_fees = [p for p in paid_fees if search_fees.lower() in p['name'].lower()]
        
    @st.dialog("Confirm Payment")
    def confirm_fee_paid(p):
        st.write(f"Mark **{p['name']}**'s fee as paid for {calendar.month_name[current_month]} {current_year}?")
        st.write(f"Amount: ₹{p['amount']}")
        col_yes, col_no = st.columns(2)
        if col_yes.button("Yes", key=f"fee_paid_yes_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            mark_fee_paid(
                payer_type=p['payer_type'],
                payer_id=p['payer_id'],
                amount=p['amount'],
                month=current_month,
                year=current_year,
                marked_by="admin"
            )
            st.rerun()
        if col_no.button("Cancel", key=f"fee_paid_no_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            st.rerun()

    with st.container(border=True, key="card_fees_pending"):
        col_widths = [0.35, 0.2, 0.2, 0.25]

        if not pending_fees and not paid_fees:
            st.info("No fee records for this month.")
        else:
            with st.container(key="table_fees_pending"):
                with st.container(key="theader_fees_pending"):
                    header_cols = st.columns(col_widths)
                    header_cols[0].markdown('<span class="table-header">Name</span>', unsafe_allow_html=True)
                    header_cols[1].markdown('<span class="table-header">Batch</span>', unsafe_allow_html=True)
                    header_cols[2].markdown('<span class="table-header">Amount</span>', unsafe_allow_html=True)
                    header_cols[3].markdown('<span class="table-header">Action</span>', unsafe_allow_html=True)

                # Not-paid rows first
                for p in pending_fees:
                    row_cols = st.columns(col_widths)
                    name_display = p['name']
                    if show_highlight:
                        name_display = f"🔴 {name_display}"
                    row_cols[0].markdown(name_display)
                    row_cols[1].markdown(batch_pill(p['batch']), unsafe_allow_html=True)
                    row_cols[2].markdown(f"₹{p['amount']}")

                    if row_cols[3].button("Mark Paid", key=f"btn_markpaid_fee_{p['payer_type']}_{p['payer_id']}"):
                        confirm_fee_paid(p)

                # Paid rows after, struck through
                for p in paid_fees:
                    row_cols = st.columns(col_widths)
                    row_cols[0].markdown(f"~~{p['name']}~~")
                    row_cols[1].markdown(batch_pill(p['batch']), unsafe_allow_html=True)
                    row_cols[2].markdown(f"₹{p['amount']}")

                    paid_on_display = date_cls.fromisoformat(p['paid_on']).strftime("%d/%m")
                    marked_by_display = p['marked_by'].capitalize()
                    row_cols[3].markdown(
                        f'<span class="status-paid">Paid by {marked_by_display} on {paid_on_display}</span>',
                        unsafe_allow_html=True
                    )

with tab_missed:
    from db.students import delete_student
    from db.gym_members import delete_gym_member

    missed_list, missed_month, missed_year = get_missed_last_month()

    search_missed = st.text_input(
        "Search",
        placeholder="Search by name...",
        label_visibility="collapsed",
        key="search_missed"
    )
    if search_missed:
        missed_list = [p for p in missed_list if search_missed.lower() in p['name'].lower()]

    @st.dialog("Take Action")
    def take_action_missed(p):
        st.write(f"**{p['name']}** ({p['payer_type'].capitalize()}) — missed {calendar.month_name[missed_month]} {missed_year}")
        st.write(f"Amount: ₹{p['amount']}")

        choice = st.radio(
            "Choose an action",
            options=["Mark as Late Paid", "Delete Student Record"],
            key=f"missed_choice_{p['payer_type']}_{p['payer_id']}"
        )

        if choice == "Delete Student Record":
            st.warning("This deletes their record permanently. Any past payment history is kept.")

        col_confirm, col_cancel = st.columns(2)
        if col_confirm.button("Confirm", key=f"missed_confirm_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            if choice == "Mark as Late Paid":
                mark_fee_paid(
                    payer_type=p['payer_type'],
                    payer_id=p['payer_id'],
                    amount=p['amount'],
                    month=missed_month,
                    year=missed_year,
                    marked_by="admin"
                )
            else:
                if p['payer_type'] == 'student':
                    delete_student(p['payer_id'])
                else:
                    delete_gym_member(p['payer_id'])
            st.rerun()
        if col_cancel.button("Cancel", key=f"missed_cancel_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            st.rerun()

    with st.container(border=True, key="card_missed_last_month"):
        st.markdown(f'<span class="card-subheading">{calendar.month_name[missed_month]} {missed_year}</span>', unsafe_allow_html=True)

        col_widths = [0.35, 0.2, 0.2, 0.25]

        if not missed_list:
            st.info("No one missed last month's payment.")
        else:
            with st.container(key="table_missed_last_month"):
                with st.container(key="theader_missed_last_month"):
                    header_cols = st.columns(col_widths)
                    header_cols[0].markdown('<span class="table-header">Name</span>', unsafe_allow_html=True)
                    header_cols[1].markdown('<span class="table-header">Batch</span>', unsafe_allow_html=True)
                    header_cols[2].markdown('<span class="table-header">Amount</span>', unsafe_allow_html=True)
                    header_cols[3].markdown('<span class="table-header">Action</span>', unsafe_allow_html=True)

                for p in missed_list:
                    row_cols = st.columns(col_widths)
                    row_cols[0].markdown(p['name'])
                    row_cols[1].markdown(batch_pill(p['batch']), unsafe_allow_html=True)
                    row_cols[2].markdown(f"₹{p['amount']}")

                    if row_cols[3].button("Take Action", key=f"btn_takeaction_{p['payer_type']}_{p['payer_id']}"):
                        take_action_missed(p)