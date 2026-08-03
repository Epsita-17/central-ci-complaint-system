import streamlit as st

# Single Admin Login
USERNAME = "admin"
PASSWORD = "admin123"

def login():

    st.markdown("<h1 style='text-align:center;'>🔐 Central C&I Service Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>JSW JFE Steel Ltd.</h4>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    show_password = st.checkbox("Show Password")

    if show_password:
        password = st.text_input("🔒 Password", value=password)

    st.write("")

    if st.button("🔓 Login", use_container_width=True):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login Successful")
            st.rerun()

        else:
            st.error("❌ Invalid Username or Password")