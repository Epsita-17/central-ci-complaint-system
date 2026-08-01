import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
from datetime import datetime
import plotly.express as px

# ---------------- Page Configuration ----------------

st.set_page_config(
    page_title="Central C&I Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Project Paths ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

LOGO_FILE = BASE_DIR / "images" / "jsw_logo.jpeg"
FILE_NAME = BASE_DIR / "data" / "complaints.xlsx"

# ---------------- Header ----------------
col1, col2, col3 = st.columns([2,6,2])

with col1:
    if LOGO_FILE.exists():
        logo = Image.open(LOGO_FILE)
        st.image(logo, width=600)
    else:
        st.warning("Logo not found")

with col2:
        st.markdown("""
    <h1 style='text-align:center;color:#003366;'>
    Central C&I Complaint Management System
    </h1>
    <h4 style='text-align:center;color:gray;'>
    JSW JFE Steel Ltd. | Instrumentation Department
    </h4>
    """, unsafe_allow_html=True)

with col3:
    st.metric("Date", datetime.now().strftime("%d-%m-%Y"))

st.divider()

# ---------------- Dashboard ----------------
if FILE_NAME.exists():

    df = pd.read_excel(FILE_NAME)
    # ================= SIDEBAR FILTER =================

    st.sidebar.header("🔍 Dashboard Filters")

    department = st.sidebar.selectbox(
        "Department",
        ["All"] + sorted(df["Department"].dropna().unique().tolist())
    )

    priority = st.sidebar.selectbox(
        "Priority",
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
    )

    status = st.sidebar.selectbox(
        "Status",
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
    )

    search = st.sidebar.text_input("🔎 Search Complaint")

    filtered_df = df.copy()

    if department != "All":
        filtered_df = filtered_df[
            filtered_df["Department"] == department
            ]

    if priority != "All":
        filtered_df = filtered_df[
            filtered_df["Priority"] == priority
            ]

    if status != "All":
        filtered_df = filtered_df[
            filtered_df["Status"] == status
            ]

    if search:
        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(lambda x: x.str.contains(search, case=False))
            .any(axis=1)
        ]

    df = filtered_df
# ---------------- KPI Section ----------------

    total = len(df)

    open_count = len(df[df["Status"] == "Open"])
    assigned_count = len(df[df["Status"] == "Assigned"])
    progress_count = len(df[df["Status"] == "In Progress"])
    waiting_count = len(df[df["Status"] == "Waiting for Spare"])
    vendor_count = len(df[df["Status"] == "Vendor Support"])
    closed_count = len(df[df["Status"] == "Closed"])

    critical_count = len(df[df["Priority"] == "Critical"])

    r1 = st.columns(4)

    with r1[0]:
        st.metric("📋 Total", total)

    with r1[1]:
        st.metric("🟢 Open", open_count)

    with r1[2]:
        st.metric("🟡 Assigned", assigned_count)

    with r1[3]:
        st.metric("🛠 In Progress", progress_count)

    r2 = st.columns(3)

    with r2[0]:
        st.metric("⏳ Waiting for Spare", waiting_count)

    with r2[1]:
        st.metric("🏭 Vendor Support", vendor_count)

    with r2[2]:
        st.metric("✅ Closed", closed_count)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏭 Complaints by Department")

        dept = df["Department"].value_counts().reset_index()
        dept.columns = ["Department", "Count"]

        fig = px.bar(
            dept,
            x="Department",
            y="Count",
            text="Count",
            title="Department Wise Complaints"
        )

        fig.update_layout(
            height=400,
            xaxis_title="Department",
            yaxis_title="No. of Complaints"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("⚠️ Complaints by Priority")

        priority = df["Priority"].value_counts().reset_index()
        priority.columns = ["Priority", "Count"]

        fig = px.pie(
            priority,
            names="Priority",
            values="Count",
            hole=0.45,
            title="Priority Distribution"
        )

        fig.update_layout(height=400)

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📌 Complaint Status")
        st.bar_chart(df["Status"].value_counts())

    with col4:
        st.subheader("🔧 Breakdown Type")
        st.bar_chart(df["Breakdown Type"].value_counts())

    st.divider()

    # ================= Critical Alert =================

    critical_df = df[df["Priority"] == "Critical"]

    if len(critical_df) > 0:
        st.error(f"🚨 {len(critical_df)} Critical Complaint(s) Pending!")
    else:
        st.success("✅ No Critical Complaints Pending")

    st.subheader("📝 Latest Complaints")

    st.dataframe(
        df.sort_values("Date", ascending=False),
        use_container_width=True
    )
else:
    st.error("complaints.xlsx not found inside the data folder.")