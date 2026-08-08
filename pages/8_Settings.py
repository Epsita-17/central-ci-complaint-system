import streamlit as st

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.markdown("""
<style>

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 3px 10px rgba(0,0,0,0.12);
    border:1px solid #EAEAEA;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)



st.markdown("""
<div style="
background:white;
padding:18px;
border-radius:12px;
box-shadow:0px 2px 8px rgba(0,0,0,0.12);
border:1px solid #E6E6E6;
margin-top:15px;
margin-bottom:25px;
">

<h3 style="color:#0B3C6F;">
⚙️ Settings
</h3>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🏭 Application Information")

    st.text_input(
        "Application",
        value="Central C&I Service Management System",
        disabled=True
    )

    st.text_input(
        "Company",
        value="JSW JFE Steel Ltd.",
        disabled=True
    )

    st.text_input(
        "Version",
        value="Version 1.0",
        disabled=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col2:

    st.subheader("👤 User Information")

    st.text_input(
        "Logged In User",
        value=st.session_state.get("username", "Admin"),
        disabled=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.button("🔑 Change Password")

    st.button("🚪 Logout")

st.divider()

st.subheader("📧 Email Settings")

st.info("Email notification is enabled.")

st.divider()

st.subheader("💾 Backup")

st.button("📥 Download Complaint Database")

st.divider()

st.subheader("ℹ️ About")

st.success("""
Central C&I Service Management System

Developed for

JSW JFE Steel Ltd.

Instrumentation & Automation Department
""")