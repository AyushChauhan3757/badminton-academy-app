import streamlit as st

def batch_pill(batch):
    css_class = "batch-" + batch.lower().replace(" ", "-")
    return f'<span class="batch-pill {css_class}">{batch}</span>'

def timing_pill(timing):
    css_class = "timing-" + timing.replace(":", "-")
    return f'<span class="batch-pill {css_class}">{timing}</span>'

def render_dialog_icon(icon, variant="info"):
    st.markdown(f'''
    <div class="dialog-icon-wrap">
        <div class="dialog-icon-circle dialog-icon-{variant}">
            <span class="material-symbols-outlined">{icon}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_dialog_message(title, subtext=None):
    st.markdown(f'<div class="dialog-title">{title}</div>', unsafe_allow_html=True)
    if subtext:
        st.markdown(f'<div class="dialog-subtext">{subtext}</div>', unsafe_allow_html=True)

TOAST_ICONS = {
    "success": ":material/check_circle:",
    "danger": ":material/delete:",
    "info": ":material/info:",
}

def queue_toast(title: str, detail: str = None, kind: str = "success"):
    """Call right before st.rerun(). The toast shows after the rerun."""
    st.session_state["pending_toast"] = {"title": title, "detail": detail, "kind": kind}

def show_pending_toast():
    """Call once per rerun. Shows a queued toast, then clears it."""
    toast = st.session_state.pop("pending_toast", None)
    if toast:
        body = f"**{toast['title']}**"
        if toast["detail"]:
            body += f"\n\n{toast['detail']}"
        st.toast(body, icon=TOAST_ICONS.get(toast["kind"], TOAST_ICONS["success"]))


BATCH_COLORS = {
    "Beginner": ("#EAF1FB", "#1D4C82"),
    "Advanced 1": ("#FBF0DC", "#A9711B"),
    "Advanced 2": ("#F3E8FB", "#7B3FA0"),
}
TIMING_COLORS = {
    "4-5": ("#E9F7F6", "#0E7C86"),
    "5-6": ("#FDEEDC", "#B4530A"),
    "6-7": ("#F3E8FB", "#7B3FA0"),
    "4-6": ("#EAF1FB", "#1D4C82"),
}

def tint_dialog_selects(batch, timing, suffix):
    """Tint the closed Batch/Timing selectboxes to match the table pills."""
    rules = ""
    for key, value, palette in (
        (f"dlg_batch_{suffix}", batch, BATCH_COLORS),
        (f"dlg_timing_{suffix}", timing, TIMING_COLORS),
    ):
        bg, fg = palette.get(value, ("#FFFFFF", "#14304F"))
        rules += f"""
        .st-key-{key} [role="group"] {{ background-color: {bg} !important; }}
        .st-key-{key} [role="group"],
        .st-key-{key} [role="group"] * {{
            color: {fg} !important;
            -webkit-text-fill-color: {fg} !important;
            font-weight: 700 !important;
        }}"""
    st.markdown(f"<style>{rules}</style>", unsafe_allow_html=True)