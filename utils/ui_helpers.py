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