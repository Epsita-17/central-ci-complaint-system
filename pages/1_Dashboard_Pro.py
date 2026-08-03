import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
from datetime import datetime
import plotly.express as px

# Login Protection
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()

st.set_page_config(
    page_title="Dashboard Pro",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

LOGO_FILE = BASE_DIR / "images" / "jsw_logo.jpeg"
FILE_NAME = BASE_DIR / "data" / "complaints.xlsx"

df = pd.read_excel(FILE_NAME)

left, center, right = st.columns([2,6,2])

with left:
    if LOGO_FILE.exists():
        st.image(str(LOGO_FILE), width=500)

with center:
    st.markdown(
        "<h1 style='text-align:center;color:#0B3C6F;'>Central C&I Service Management System</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:gray;'>JSW JFE Steel Ltd. | Instrumentation Department</p>",
        unsafe_allow_html=True
    )

with right:
    st.metric("📅 Date", datetime.now().strftime("%d-%m-%Y"))

st.divider()

# ================= KPI CARDS =================

total = len(df)

open_count = len(df[df["Status"] == "Open"])
assigned_count = len(df[df["Status"] == "Assigned"])
progress_count = len(df[df["Status"] == "In Progress"])
vendor_count = len(df[df["Status"] == "Vendor Support"])
closed_count = len(df[df["Status"] == "Closed"])

cards = st.columns(6)

data = [
    ("📋", "Total", total, "#1565C0"),
    ("🔴", "Open", open_count, "#E53935"),
    ("🟡", "Assigned", assigned_count, "#FB8C00"),
    ("🔵", "Progress", progress_count, "#1E88E5"),
    ("🟣", "Vendor", vendor_count, "#8E24AA"),
    ("🟢", "Closed", closed_count, "#43A047")
]

for col, (icon, title, value, color) in zip(cards, data):
    with col:
        st.markdown(
            f"""
            <div style="
                background:white;
                border-top:6px solid {color};
                border-radius:12px;
                padding:18px;
                text-align:center;
                box-shadow:0 3px 10px rgba(0,0,0,0.15);
            ">
                <div style="font-size:28px;">{icon}</div>
                <div style="font-size:16px;font-weight:bold;color:#444;">
                    {title}
                </div>
                <div style="font-size:34px;font-weight:bold;color:{color};">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("""
<div style="
background:white;
padding:18px;
border-radius:12px;
box-shadow:0px 2px 8px rgba(0,0,0,0.12);
border:1px solid #E6E6E6;
margin-top:15px;
">

<h3 style="color:#0B3C6F;">
🔍 Search & Filter
</h3>

</div>
""", unsafe_allow_html=True)

st.dataframe(
    df.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True
)


f1, f2, f3 = st.columns(3)

with f1:
    department = st.selectbox(
        "Department",
        ["All"] + sorted(df["Department"].dropna().unique().tolist())
    )

with f2:
    priority = st.selectbox(
        "Priority",
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
    )

with f3:
    status = st.selectbox(
        "Status",
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
    )

if department != "All":
    df = df[df["Department"] == department]

if priority != "All":
    df = df[df["Priority"] == priority]

if status != "All":
    df = df[df["Status"] == status]

st.markdown("---")

chart1, chart2, chart3 = st.columns([1,1,1], gap="large")

with chart1:

    with st.container(border=True):

        st.markdown("### 📊 Department")

        dept = df["Department"].value_counts().reset_index()
        dept.columns = ["Department","Count"]

        fig = px.bar(
            dept,
            x="Department",
            y="Count",
            text="Count",
            color_discrete_sequence=["#1565C0"]
        )

        fig.update_layout(
            height=360,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="",
            yaxis_title="No. of Complaints",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        fig.update_traces(
            textposition="outside",
            width=0.45
        )

        st.plotly_chart(fig, use_container_width=True)

with chart2:

    with st.container(border=True):

        st.markdown("### ⚠️ Priority")

        priority_df = df["Priority"].value_counts().reset_index()
        priority_df.columns = ["Priority","Count"]

        fig = px.pie(
            priority_df,
            names="Priority",
            values="Count",
            hole=0.60,
            color="Priority",
            color_discrete_map={
                "Low": "#1976D2",
                "Medium": "#FB8C00",
                "High": "#E53935",
                "Critical": "#8E24AA"
            }
        )

        fig.update_layout(
            height=360,
            paper_bgcolor="white",
            showlegend=True,
            legend_title="",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

with chart3:

    with st.container(border=True):

        st.markdown("### 📌 Status")

        status_df = df["Status"].value_counts().reset_index()
        status_df.columns=["Status","Count"]

        fig = px.bar(
            status_df,
            x="Count",
            y="Status",
            orientation="h",
            text="Count",
            color="Status",
            color_discrete_map={
                "Open": "#E53935",
                "Assigned": "#FB8C00",
                "In Progress": "#1976D2",
                "Vendor Support": "#7B1FA2",
                "Closed": "#2E7D32"
            }
        )

        fig.update_layout(
            height=360,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="No. of Complaints",
            yaxis_title="",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        fig.update_traces(
            textposition="outside"
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="
background:white;
padding:18px;
border-radius:12px;
box-shadow:0px 2px 8px rgba(0,0,0,0.12);
border:1px solid #E6E6E6;
margin-top:15px;
">

<h3 style="color:#0B3C6F;">
📋 Latest Complaints
</h3>

</div>
""", unsafe_allow_html=True)

st.dataframe(
    df.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True
)



