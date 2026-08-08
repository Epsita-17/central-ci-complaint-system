import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


# ================= LOGIN PROTECTION =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()


# ================= PAGE SETTINGS =================

st.set_page_config(
    page_title="Training Modules",
    page_icon="🎓",
    layout="wide"
)

# ================= HEADER =================

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_FILE = BASE_DIR / "images" / "jsw_logo.jpeg"

# Header background and border
st.markdown(
    """
    <style>

    .training-header {
        background-color: #EAF4FF;
        border: 2px solid #B7D7F5;
        border-radius: 18px;
        padding: 30px 30px;
        margin-bottom: 15px;
        min-height: 250px;
        box-sizing: border-box;
    }

    .training-title {
        text-align: center;
        color: #0B3C6F;
        font-size: 38px;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }

    .training-subtitle {
        text-align: center;
        color: #777777;
        font-size: 14px;
        margin-top: 8px;
    }

    .training-date {
        text-align: right;
        color: #555555;
        font-size: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Header layout
header_left, header_center, header_right = st.columns([2, 6, 2])


# LEFT - LOGO
with header_left:
    st.image(
        str(LOGO_FILE),
        width=200
    )


# CENTER - TITLE
with header_center:
    st.markdown(
        '<div class="training-title">🎓 Training Modules</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="training-subtitle">JSW JFE Steel Ltd.</div>',
        unsafe_allow_html=True
    )


# RIGHT - DATE
with header_right:
    st.markdown(
        f'''
        <div class="training-date">
            📅<br>
            {datetime.now().strftime("%d-%m-%Y")}
        </div>
        ''',
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.markdown(
    "<div style='height:25px'></div>",
    unsafe_allow_html=True
)

cards = st.columns(4, gap="small")

kpi_data = [
    ("📚", "Total Modules", "6", "#1565C0"),
    ("🖥️", "DCS", "5", "#FB8C00"),
    ("⚡", "Drives", "1", "#43A047"),
    ("🎓", "Completed", "0", "#8E24AA")
]

for col, (icon, title, value, color) in zip(cards, kpi_data):

    with col:

        st.html(f"""
        <div style="
            height:115px;
            background:white;
            border-top:5px solid {color};
            border-radius:10px;
            box-shadow:0 2px 8px rgba(0,0,0,0.12);
            text-align:center;
            padding:10px;
            box-sizing:border-box;
        ">

            <div style="
                font-size:24px;
                line-height:28px;
            ">
                {icon}
            </div>

            <div style="
                font-size:13px;
                font-weight:600;
                margin-top:3px;
            ">
                {title}
            </div>

            <div style="
                font-size:27px;
                font-weight:bold;
                color:{color};
                margin-top:4px;
            ">
                {value}
            </div>

        </div>
        """)

# Small gap between KPI cards and training modules
st.markdown(
    "<div style='height:8px'></div>",
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# TRAINING MODULE LINKS
# ---------------------------------------------------------
modules = {

    "Siemens PCS7 DCS":
        "https://jsw.sharepoint.com/sites/SiemensTrainingVideos/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FSiemensTrainingVideos%2FShared%20Documents%2FSiemens%20Training%20Videos&p=true&ct=1786084504974&or=OWA%2DNT%2DMail&cid=11804597%2Da799%2D2797%2Db283%2Df599041475b7&ga=1&LOF=1",

    "ABB DCS":
        "https://jsw-my.sharepoint.com/personal/danish_kidwai_jsw_in/Lists/ABB%20Training%20Module/AllItems.aspx?ct=1786084591957&or=OWA%2DNT%2DMail&LOF=1&viewid=5e2790c3%2D2331%2D4a17%2D9ac9%2Dffcdc13fa505&playlistLayout=playback&itemId=14",

    "Yokogawa DCS":
        "https://jsw-my.sharepoint.com/personal/debasish_jena_jsw_in/Lists/YOKOGAWA%20TRAINING%20MODULE/AllItems.aspx?ct=1786084107864&or=OWA%2DNT%2DMail&LOF=1&viewid=13b37b43%2D0357%2D4716%2D818c%2Df1e972691f1e&playlistLayout=playback&itemId=12",

    "Honeywell DCS":
        "https://jsw-my.sharepoint.com/personal/debasish_jena_jsw_in/Lists/HONEYWELL%20DCS%20TRAING%20MODULE/AllItems.aspx?ct=1786084623438&or=OWA-NT-Mail&cid=4c563ef4-241e-7a20-9b2f-e1d5e08f78d1&LOF=1",

    "Schneider DCS":
        "https://jsw-my.sharepoint.com/personal/debasish_jena_jsw_in/Lists/Schneider%20Training/AllItems.aspx?ct=1786084540038&or=OWA%2DNT%2DMail&LOF=1&viewid=b723be0d%2Df540%2D4f39%2Da5f9%2Da66654cf555d&playlistLayout=playback&itemId=16",

    "ABB Drive":
        "https://jsw-my.sharepoint.com/personal/debasish_jena_jsw_in/Lists/ABB%20DRIVE%20TRAINING%20MODULE2/AllItems.aspx?ct=1786084289046&or=OWA%2DNT%2DMail&LOF=1&viewid=e8864515%2Def63%2D40aa%2D8150%2Dfa037876bd23&playlistLayout=playback&itemId=3"
}

# ---------------------------------------------------------
# IMAGE FOLDER
# ---------------------------------------------------------

IMAGE_DIR = BASE_DIR / "images"

logos = {
    "Siemens PCS7 DCS": IMAGE_DIR / "siemens.png",
    "ABB DCS": IMAGE_DIR / "abb.png",
    "Yokogawa DCS": IMAGE_DIR / "yokogawa.png",
    "Honeywell DCS": IMAGE_DIR / "honeywell.png",
    "Schneider DCS": IMAGE_DIR / "schneider.png",
    "ABB Drive": IMAGE_DIR / "abb.png"
}

# ---------------------------------------------------------
# MODULE CARDS
# ---------------------------------------------------------
module_list = list(modules.items())

for i in range(0, len(module_list), 2):

    cols = st.columns(2, gap="small")

    for col, (name, url) in zip(
        cols,
        module_list[i:i + 2]
    ):

        with col:

            with st.container(border=True, height=245):
                # Logo
                if logos[name].exists():
                    st.image(
                        str(logos[name]),
                        width=70
                    )

                # Module title
                st.markdown(
                    f"<div style='font-size:20px;font-weight:600;margin-top:-8px;'>{name}</div>",
                    unsafe_allow_html=True
                )

                st.caption(
                    "Official Training Module"
                )

                st.write("🎯 Self Learning")
                st.write("📚 Beginner → Advanced")

                # Launch button
                st.link_button(
                    "🚀 Launch Training",
                    url,
                    use_container_width=True
                )

    # Small gap between rows
    st.markdown(
        "<div style='height:4px'></div>",
        unsafe_allow_html=True
    )