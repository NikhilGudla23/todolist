import streamlit as st
import utils.session as sess
import utils.auth as auth

def render_register():
    """Render the Registration Page inline."""
    # Header branding
    st.markdown("""
    <div class="anim-fade-in" style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 700; background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">⚡ TaskFlow Pro</h1>
        <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.5rem;">Join us and start organizing your tasks</p>
    </div>
    """, unsafe_allow_html=True)

    # Register Form Container
    st.markdown("<div class='glass-card anim-card-pop'>", unsafe_allow_html=True)
    st.write("### 📝 Create Account")

    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        username = st.text_input("Username *", placeholder="Choose a username")
        email = st.text_input("Email *", placeholder="name@domain.com")
        password = st.text_input("Password *", type="password", placeholder="Minimum 4 characters")
        confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Repeat password")
        
        submit = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
        
        if submit:
            with st.spinner("Creating account..."):
                success, msg = auth.register_user(name, username, email, password, confirm_password)
                if success:
                    st.success(msg)
                    st.markdown("""
                    <div style="background-color: rgba(16, 185, 129, 0.1); color: #10b981; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;">
                        Registration completed! You can now log in using the button below.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

    # Redirect to Login
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.write("Already have an account?")
    with col2:
        if st.button("Sign In", use_container_width=True):
            st.session_state.auth_page = "Login"
            sess.rerun()
