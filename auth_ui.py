import streamlit as st
from auth import signup_user, login_user
from datetime import date

def show_logged_in_user():
    if "user" in st.session_state and st.session_state.user:
        user = st.session_state.user
        user_info_html = f"""
        <div class="sidebar-user">
            <h4>👤 Logged In User</h4>
            <p><strong>Name:</strong> {user.get('displayName', 'N/A')}</p>
            <p><strong>Email:</strong> {user.get('email', 'N/A')}</p>
            <p><strong>UID:</strong> <span class="uid">{user.get('localId', 'N/A')}</span></p>
        </div>
        """
        st.sidebar.markdown(user_info_html, unsafe_allow_html=True)
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout", key="logout_btn"):
            st.session_state.user = None
            st.success("You've been logged out.")
            st.rerun()

def login_signup_ui():
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Signup"])

    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_btn"):
            if not (email and password):
                st.warning("Enter your email and password.")
            else:
                result = login_user(email, password)
                if result.get("success"):
                    st.session_state.user = result["data"]
                    name = result["data"].get("displayName", "there")
                    st.success(f"👋 Hey {name.capitalize()}, welcome, the stars are shining just for you!!")
                    st.rerun()
                else:
                    st.error(result.get("message", "Login failed."))

    with tab2:
        st.subheader("Create a New Account")
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        birthdate = st.date_input(
            "Birthdate",
            value=date(2000, 1, 1),
            min_value=date(1950, 1, 1),
            max_value=date.today(),
            key="signup_birthdate"
        )

        if st.button("Sign Up", key="signup_btn"):
            if not (name and email and password and birthdate):
                st.warning("Please fill all fields.")
            else:
                result = signup_user(name, email, password, birthdate.strftime("%Y-%m-%d"))
                if result.get("success"):
                    login_result = login_user(email, password)
                    if login_result.get("success"):
                        user_data = login_result["data"]
                        user_data["displayName"] = name
                        st.session_state.user = user_data
                        zodiac = result.get("zodiac", "unknown")
                        st.success(f"🎉 Account created for {name}!\nZodiac: {zodiac.capitalize()}")
                        st.rerun()
                    else:
                        st.error("Account created, but auto-login failed.")
                else:
                    st.error(result.get("message", "Signup failed."))
