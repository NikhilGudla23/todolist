import streamlit as st

def render_styled_button(label, key, type="secondary", icon=None):
    """
    Utility wrapper to draw a standard styled Streamlit button.
    """
    button_label = f"{icon} {label}" if icon else label
    return st.button(button_label, key=key, type=type, use_container_width=True)
