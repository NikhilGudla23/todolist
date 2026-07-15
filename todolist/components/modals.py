import streamlit as st
import utils.session as sess

def render_confirm_dialog(message, key_prefix, on_confirm):
    """
    Render a clean warning block with Confirm and Cancel buttons.
    """
    st.markdown("<div style='background-color: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; padding: 1rem; border-radius: 8px; margin: 1rem 0;'>", unsafe_allow_html=True)
    st.write(f"⚠️ **{message}**")
    
    col_yes, col_no = st.columns([0.5, 0.5])
    confirmed = False
    
    with col_yes:
        if st.button("Yes, Permanent Delete", key=f"{key_prefix}_yes", type="primary", use_container_width=True):
            confirmed = True
            on_confirm()
            
    with col_no:
        if st.button("Cancel", key=f"{key_prefix}_no", use_container_width=True):
            # Clearing states is handled by caller rerunning
            sess.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
    return confirmed
