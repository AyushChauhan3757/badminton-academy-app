import streamlit as st
import calendar
from datetime import date as date_cls
from utils.auth import require_role, now_ist
from constants import ROLE_COACH
from utils.header import render_header
from db.payments import get_pending_fees, mark_fee_paid, get_paid_fees, get_missed_last_month
from utils.ui_helpers import batch_pill, queue_toast

require_role([ROLE_COACH])

render_header("Pending")

today = now_ist()
current_month = today.month
current_year = today.year

# No salary tab for coaches (spec: coaches never see salary figures).
tab_fees, tab_missed = st.tabs([
    "Fees Pending",
    "Students Missed Last Month"
])

with tab_fees:
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
                marked_by="coach"
            )
            queue_toast("Payment Recorded", f"{p['name']} · ₹{p['amount']}")
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
    missed_list, missed_month, missed_year = get_missed_last_month()

    search_missed = st.text_input(
        "Search",
        placeholder="Search by name...",
        label_visibility="collapsed",
        key="search_missed"
    )
    if search_missed:
        missed_list = [p for p in missed_list if search_missed.lower() in p['name'].lower()]

    # Coach can only record a late payment. Deleting a student/gym record stays
    # Admin-only (spec Permission Model), so there is no delete option here.
    @st.dialog("Mark as Late Paid")
    def confirm_missed_paid(p):
        st.write(f"Mark **{p['name']}** ({p['payer_type'].capitalize()}) as paid for {calendar.month_name[missed_month]} {missed_year}?")
        st.write(f"Amount: ₹{p['amount']}")
        col_yes, col_no = st.columns(2)
        if col_yes.button("Yes", key=f"missed_yes_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            mark_fee_paid(
                payer_type=p['payer_type'],
                payer_id=p['payer_id'],
                amount=p['amount'],
                month=missed_month,
                year=missed_year,
                marked_by="coach"
            )
            queue_toast("Late Payment Recorded", f"{p['name']} · ₹{p['amount']}")
            st.rerun()
        if col_no.button("Cancel", key=f"missed_no_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
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

                    if row_cols[3].button("Mark Paid", key=f"btn_markpaid_missed_{p['payer_type']}_{p['payer_id']}"):
                        confirm_missed_paid(p)