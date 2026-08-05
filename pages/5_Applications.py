import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Applications",
    page_icon="🌐",
    layout="wide"
)

# ---------------- Login ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()

# ---------------- Logo ----------------

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_FILE = BASE_DIR / "images" / "jsw_logo.jpeg"

st.markdown("""
<div style="
background:#EAF4FF;
border:2px solid #BFD8FF;
border-radius:18px;
padding:20px;
margin-bottom:25px;
">
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2,6,2])

with c1:
    if LOGO_FILE.exists():
        st.image(str(LOGO_FILE), width=220)

with c2:
    st.markdown("""
    <h1 style="text-align:center;color:#0B3C6F;">
    🌐 Central C&I Applications
    </h1>

    <p style="text-align:center;color:gray;font-size:18px;">
    JSW JFE Steel Ltd. | Central C&I Department
    </p>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="text-align:right;padding-top:20px;">
    📅 <b>Date</b><br>
    {datetime.now().strftime("%d-%m-%Y")}
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Applications ----------------

col1, col2 = st.columns(2)

with col1:

    st.info("🤖 Central Automation Dashboard")

    st.markdown("""
Monitor Automation Dashboard, Digital Projects,
Reports and Analytics.
""")

    st.markdown("""
<a href="https://centralautomationdeptv3.streamlit.app/"
target="_blank">
<button style="
width:100%;
padding:12px;
background:#1565C0;
color:white;
border:none;
border-radius:8px;
font-size:16px;
cursor:pointer;">
🚀 Open Automation Dashboard
</button>
</a>
""", unsafe_allow_html=True)

with col2:

    st.info("🔧 Central Repair Lab")

    st.markdown("""
Repair History, Vendor Repair,
Equipment Tracking and Reports.
""")

    st.markdown("""
<a href="https://central-repair-lab.web.app/"
target="_blank">
<button style="
width:100%;
padding:12px;
background:#2E7D32;
color:white;
border:none;
border-radius:8px;
font-size:16px;
cursor:pointer;">
🚀 Open Repair Lab
</button>
</a>
""", unsafe_allow_html=True)

st.markdown("---")

st.success("✅ More Central C&I Applications will be added here.")