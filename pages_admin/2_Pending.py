import streamlit as st
import calendar
from utils.auth import require_role, now_ist
from constants import ROLE_ADMIN
from utils.header import render_header
from db.payments import get_pending_fees, mark_fee_paid, get_paid_fees, get_missed_last_month
from utils.ui_helpers import batch_pill, render_dialog_icon, render_dialog_message, queue_toast

require_role([ROLE_ADMIN])

render_header("Pending")

today = now_ist()
current_month = today.month
current_year = today.year


def _set_missed_choice(key, value):
    """on_click callback for the Missed Last Month 'Take Action' dialog's
    two option-card buttons — updates session_state BEFORE Streamlit
    reruns/repaints, so the newly-selected card shows correctly on the
    very next render (a plain 'if st.button(...):' would lag one click
    behind, since it only updates state after the button has already
    been drawn with the old style for this render)."""
    st.session_state[key] = value


tab_salary, tab_fees, tab_missed = st.tabs([
    "Coach Salary Pending",
    "Fees Pending",
    "Students Missed Last Month"
])

with tab_salary:
    from db.coaches import get_all_coaches
    from db.salary import get_salary_status, clear_coach_salary

    coaches = get_all_coaches()

    # -------------------------------------------------------------------
    # Confirm Salary Payment - same icon-circle + message + button-variant
    # pattern as Mark Fee Paid, kept navy/primary rather than gold per
    # explicit decision (simpler, one less variant to maintain).
    # -------------------------------------------------------------------
    @st.dialog("Confirm Salary Payment")
    def confirm_salary_paid(coach):
        render_dialog_icon("check_circle", "success")
        render_dialog_message(
            "Mark Salary as Paid?",
            f"Are you sure you want to mark this month's salary as paid for<br><b>{coach['name']}</b>?<br>"
            f"Amount: ₹{coach['salary']} ({calendar.month_name[current_month]} {current_year})"
        )
        col_no, col_yes = st.columns(2)
        if col_no.button("Cancel", key=f"dlg_secondary_salary_no_{coach['id']}", use_container_width=True):
            st.rerun()
        if col_yes.button("Yes, Mark Paid", key=f"dlg_primary_salary_yes_{coach['id']}", use_container_width=True):
            clear_coach_salary(
                coach_id=coach['id'],
                coach_name=coach['name'],
                salary_amount=coach['salary'],
                month=current_month,
                year=current_year
            )
            queue_toast("Salary Paid", f"{coach['name']} · ₹{coach['salary']}")
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

    # -------------------------------------------------------------------
    # Mark Fee Paid - icon-circle + centered message + button-variant
    # pattern (see utils/styling.py's apply_dialog_styles() and
    # utils/ui_helpers.py's render_dialog_icon()/render_dialog_message()).
    # Cancel renders left, the colored confirm action renders right,
    # matching the reference mockup.
    # -------------------------------------------------------------------
    @st.dialog("Confirm Payment")
    def confirm_fee_paid(p):
        render_dialog_icon("check_circle", "success")
        render_dialog_message(
            "Mark Fee as Paid?",
            f"Are you sure you want to mark the fee as paid for<br><b>{p['name']}</b>?<br>"
            f"Amount: ₹{p['amount']} ({calendar.month_name[current_month]} {current_year})"
        )
        col_no, col_yes = st.columns(2)
        if col_no.button("Cancel", key=f"dlg_secondary_feepaid_no_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            st.rerun()
        if col_yes.button("Yes, Mark Paid", key=f"dlg_primary_feepaid_yes_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            mark_fee_paid(
                payer_type=p['payer_type'],
                payer_id=p['payer_id'],
                amount=p['amount'],
                month=current_month,
                year=current_year,
                marked_by="admin"
            )
            queue_toast("Payment Recorded", f"{p['name']} · ₹{p['amount']}")
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

    # -------------------------------------------------------------------
    # Take Action - warning icon-circle + centered "Choose Action"
    # message, radio choice kept as-is (the radio-then-Confirm sequence
    # itself is the safeguard, per spec), with a st.warning shown when
    # "Delete Student Record" is selected. The Confirm button switches
    # from navy (dlg_primary_) to red (dlg_danger_) depending on which
    # radio option is currently selected, since Streamlit reruns this
    # dialog function on every radio interaction - a small extra
    # warning cue before an irreversible delete, beyond what the
    # reference mockup itself shows.
    # -------------------------------------------------------------------
    @st.dialog("Take Action")
    def take_action_missed(p):
        render_dialog_icon("warning", "warning")
        render_dialog_message(
            "Choose Action",
            f"<b>{p['name']}</b> ({p['payer_type'].capitalize()}) — missed "
            f"{calendar.month_name[missed_month]} {missed_year}<br>Amount: ₹{p['amount']}"
        )

        # -----------------------------------------------------------
        # Choice, as two selectable "cards" instead of st.radio.
        # Selection lives in session_state, keyed per payer so it
        # persists across reruns within this one dialog instance.
        # Each button's key PREFIX (dlg_option_selected_ vs.
        # dlg_option_unselected_) is what the CSS matches on, so the
        # selected one always renders filled/bold and the other
        # stays plain-outlined.
        # -----------------------------------------------------------
        choice_key = f"missed_choice_{p['payer_type']}_{p['payer_id']}"
        if choice_key not in st.session_state:
            st.session_state[choice_key] = "Mark as Late Paid"

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            prefix = "dlg_option_selected" if st.session_state[choice_key] == "Mark as Late Paid" else "dlg_option_unselected"
            # on_click (not "if st.button(...):") is what makes the new
            # selection show up on the FIRST click instead of the second.
            # With "if st.button(...):", the button is drawn with the
            # OLD prefix/style before we ever get a chance to update
            # session_state inside the if-block — the visible change
            # only appears a click later, once the *next* rerun computes
            # prefix from the now-updated state. on_click runs BEFORE
            # Streamlit repaints, so the state is already correct by the
            # time this widget is drawn on the very next rerun.
            st.button(
                "Mark as Late Paid",
                key=f"{prefix}_latepaid_{p['payer_type']}_{p['payer_id']}",
                use_container_width=True,
                on_click=_set_missed_choice,
                args=(choice_key, "Mark as Late Paid"),
            )
        with col_opt2:
            prefix = "dlg_option_selected" if st.session_state[choice_key] == "Delete Student Record" else "dlg_option_unselected"
            st.button(
                "Delete Student Record",
                key=f"{prefix}_delete_{p['payer_type']}_{p['payer_id']}",
                use_container_width=True,
                on_click=_set_missed_choice,
                args=(choice_key, "Delete Student Record"),
            )

        choice = st.session_state[choice_key]

        if choice == "Delete Student Record":
            st.warning("This deletes their record permanently. Any past payment history is kept.")

        confirm_variant = "dlg_danger" if choice == "Delete Student Record" else "dlg_primary"
        confirm_label = "Delete" if choice == "Delete Student Record" else "Confirm"

        col_cancel, col_confirm = st.columns(2)
        if col_cancel.button("Cancel", key=f"dlg_secondary_missed_cancel_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            del st.session_state[choice_key]
            st.rerun()
        if col_confirm.button(confirm_label, key=f"{confirm_variant}_missed_confirm_{p['payer_type']}_{p['payer_id']}", use_container_width=True):
            if choice == "Mark as Late Paid":
                mark_fee_paid(
                    payer_type=p['payer_type'],
                    payer_id=p['payer_id'],
                    amount=p['amount'],
                    month=missed_month,
                    year=missed_year,
                    marked_by="admin"
                )
                queue_toast("Late Payment Recorded", f"{p['name']} · ₹{p['amount']}")
            else:
                if p['payer_type'] == 'student':
                    delete_student(p['payer_id'])
                else:
                    delete_gym_member(p['payer_id'])
                queue_toast("Record Deleted", p['name'], kind="danger")
            del st.session_state[choice_key]
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