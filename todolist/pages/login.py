import streamlit as st
import utils.session as sess
import utils.auth as auth

def render_login():
    """Render the Login Page inline."""
    # Header branding
    st.markdown("""
    <div class="anim-fade-in" style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 700; background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">⚡ TaskFlow Pro</h1>
        <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.5rem;">Sleek, Secure & Professional Task Board</p>
    </div>
    """, unsafe_allow_html=True)

    # Login Form Container
    st.markdown("<div class='glass-card anim-card-pop'>", unsafe_allow_html=True)
    st.write("### 🔑 Sign In")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember Me", value=False) # Visual placeholder
        
        submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Verifying credentials..."):
                    if auth.login_user(username, password):
                        st.success("Successfully logged in! Redirecting...")
                        sess.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Register Switch Redirect
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.write("Don't have an account yet?")
    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.auth_page = "Register"
            sess.rerun()
