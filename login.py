import streamlit as st
from pathlib import Path

USERNAME = "admin"
PASSWORD = "admin123"

BASE_DIR = Path(__file__).resolve().parent
LOGO_FILE = BASE_DIR / "images" / "jsw_logo.jpeg"

def login():

    c1, c2, c3 = st.columns([2,4,2])

    with c2:

        st.image(str(LOGO_FILE), width=180)

        st.markdown("""
        <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:1px solid #D9E2F2;
        box-shadow:0px 3px 10px rgba(0,0,0,0.15);
        ">
        <h2 style="text-align:center;color:#0B3C6F;">
        🔐 Central C&I Service Management System
        </h2>

        <p style="text-align:center;color:gray;">
        JSW JFE Steel Ltd.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        username = st.text_input(
            "👤 Username",
            placeholder="Enter Username"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter Password"
        )

        show = st.checkbox("Show Password")

        if show:
            password = st.text_input(
                "Password",
                value=password,
                key="visible_password"
            )

        st.write("")

        if st.button(
            "🔓 Login",
            use_container_width=True,
            type="primary"
        ):

            if username == USERNAME and password == PASSWORD:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("✅ Login Successful")

                st.rerun()

            else:

                st.error("❌ Invalid Username or Password")