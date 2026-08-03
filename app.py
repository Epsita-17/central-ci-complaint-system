import streamlit as st
from login import login
from database import create_database, create_sqlite_database

st.set_page_config(
    page_title="Central C&I Service Management System",
    page_icon="🛠️",
    layout="wide"
)

create_database()
create_sqlite_database()

if "username" not in st.session_state:
    st.session_state.username = "Admin"

if "role" not in st.session_state:
    st.session_state.role = "Admin"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

st.title("🛠️ Central C&I Service Management System")
st.caption("JSW JFE Steel Ltd.")

username = st.session_state.get("username", "Admin")
role = st.session_state.get("role", "Admin")

st.success(f"Welcome, {username} 👋")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.info("""
### 👤 Logged in User

**Username:** {}

**Role:** {}

**System Status:** 🟢 Online
""".format(
        username,
        role
    ))

with col2:
    st.success("""
### 📌 Application

🏭 Central C&I Service Management System

JSW JFE Steel Ltd.

Version : 1.0
""")

st.markdown("---")

st.markdown("## 🚀 Available Modules")

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
### 📝 Complaint Management

- Register Complaint
- Update Status
- Upload Images
- Email Notification
""")

with c2:
    st.markdown("""
### 📊 Monitoring

- Dashboard
- Complaint History
- Reports
- Settings
""")

st.markdown("---")

st.info("Select any module from the left sidebar to continue.")

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()