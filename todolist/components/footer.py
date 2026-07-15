import streamlit as st

def render_footer():
    """Render the application footer."""
    st.markdown("""
    <div class="footer-text">
        TaskFlow Pro &copy; 2026. Made with ❤️ using Python and Streamlit.
    </div>
    """, unsafe_allow_html=True)
