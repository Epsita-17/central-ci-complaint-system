import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from audit_database import AUDIT_DATABASE
from audit_db import *
import os
import shutil

create_table()

st.set_page_config(
    page_title="Audit Report",
    page_icon="📋",
    layout="wide"
)

# Login Protection
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
AUDIT_FILE = DATA_DIR / "audit_report.xlsx"



from datetime import datetime

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

col1, col2, col3 = st.columns([2,6,2])

with col1:
    if LOGO_FILE.exists():
        st.image(str(LOGO_FILE), width=220)

with col2:
    st.markdown("""
    <h1 style="text-align:center;color:#0B3C6F;">
    📋 PLC / DCS Audit Action Tracker
    </h1>

    <p style="text-align:center;color:gray;font-size:18px;">
    JSW JFE Steel Ltd. | Central C&I Department
    </p>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="text-align:right;padding-top:20px;">
    📅 <b>Date</b><br>
    {datetime.now().strftime("%d-%m-%Y")}
    </div>
    """, unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)



st.markdown("## Audit Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    department = st.selectbox(
        "Department",
        [
            "Power Plant (3x130MW)",
            "Power Plant (116MW)",
            "Pellet Plant",
            "Beneficiation",
            "Sinter",
            "RMHS",
            "SMS-1",
            "SMS-2",
            "Coke Oven",
            "Oxygen Plant",
            "CRM",
            "WRM",
            "CSP Caster",
            "Blast Furnace",
            "LCP",
            "DRI",
            "CRM Kolkata",
            "CRM Chandigarh"
        ]
    )
audit_master = AUDIT_DATABASE.get(
    department,
    [("No Audit Checklist Available", "Please create checklist for this department")]
)

with col2:
    month = st.selectbox(
        "Month",
        [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]
    )

with col3:
    auditor = st.text_input("Audited By")

with col4:
    audit_date = st.date_input("Audit Date")

audit_df = load_audit(department)

if "status" not in audit_df.columns:
    audit_df["status"] = "Open"

if "responsible" not in audit_df.columns:
    audit_df["responsible"] = ""

if "target_date" not in audit_df.columns:
    audit_df["target_date"] = pd.Timestamp.today().date()

if audit_df.empty:

    audit_df = pd.DataFrame({
        "Sr No": range(1, len(audit_master) + 1),
        "Action Item": [x[0] for x in audit_master],
        "Detailed Scope": [x[1] for x in audit_master],
        "Responsible": [""] * len(audit_master),
        "Target Date": [pd.Timestamp.today().date()] * len(audit_master),
        "Status": ["Open"] * len(audit_master)
    })

else:

    audit_df = audit_df.rename(columns={
        "sr_no": "Sr No",
        "action_item": "Action Item",
        "detailed_scope": "Detailed Scope",
        "responsible": "Responsible",
        "target_date": "Target Date",
        "status": "Status"
    })

audit_df["Target Date"] = pd.to_datetime(
    audit_df["Target Date"],
    errors="coerce"
).dt.date

audit_df["Responsible"] = audit_df["Responsible"].astype(str)
audit_df["Status"] = audit_df["Status"].astype(str)

edited_df = st.data_editor(
    audit_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Responsible": st.column_config.TextColumn("Responsible"),
        "Target Date": st.column_config.DateColumn("Target Date"),
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=[
                "Open",
                "In Progress",
                "Completed",
                "Delayed"
            ]
        )
    },
    num_rows="fixed"
)

st.markdown("")

if st.button("💾 Save Audit Report", use_container_width=True):
    edited_df["Department"] = department
    edited_df["Month"] = month
    edited_df["Audited By"] = auditor
    edited_df["Audit Date"] = audit_date

    save_audit(
        edited_df,
        department,
        month,
        auditor,
        audit_date
    )

    st.success("✅ Audit Report Saved Successfully")
    st.rerun()
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
    📊 Audit Summary
    </h3>

    </div>
    """, unsafe_allow_html=True)


total = len(edited_df)

completed = len(edited_df[edited_df["Status"]=="Completed"])

progress = len(edited_df[edited_df["Status"]=="In Progress"])

open_count = len(edited_df[edited_df["Status"]=="Open"])

delayed = len(edited_df[edited_df["Status"]=="Delayed"])

compliance = round((completed/total)*100,1) if total>0 else 0

compliance = round(completed*100/total,1) if total>0 else 0


cards = st.columns(6)

kpis = [
    ("📋", "Total", total, "#1565C0"),
    ("🟢", "Completed", completed, "#2E7D32"),
    ("🟡", "Progress", progress, "#FB8C00"),
    ("🔴", "Open", open_count, "#E53935"),
    ("⚫", "Delayed", delayed, "#424242"),
    ("📊", "Compliance", f"{compliance}%", "#1976D2")
]

for col, (icon, title, value, color) in zip(cards, kpis):
        with col:
            st.markdown(f"""
            <div style="
            background:white;
            border-top:6px solid {color};
            border-radius:12px;
            padding:18px;
            text-align:center;
            box-shadow:0px 3px 10px rgba(0,0,0,0.15);
            ">

            <div style="font-size:30px;">{icon}</div>

            <div style="font-size:16px;font-weight:bold;">
            {title}
            </div>

            <div style="font-size:32px;color:{color};font-weight:bold;">
            {value}
            </div>

            </div>
            """, unsafe_allow_html=True)

import os
st.markdown("---")
st.subheader("📈 Department Compliance")

dept_data = []

for dept in AUDIT_DATABASE.keys():

    df = load_audit(dept)

    if len(df) == 0:
        compliance = 0

    else:
        completed = len(df[df["status"] == "Completed"])
        compliance = round(completed * 100 / len(df), 1)

    dept_data.append({
        "Department": dept,
        "Compliance": compliance
    })

graph_df = pd.DataFrame(dept_data)
fig = px.bar(
    graph_df,
    x="Department",
    y="Compliance",
    text="Compliance",
    color="Department",
    color_discrete_map={
        "Oxygen Plant": "#1f77b4",
        "Power Plant (3x130MW)": "#d62728",
        "Power Plant (116MW)": "#ff7f0e",
        "Pellet Plant": "#2ca02c",
        "Beneficiation": "#9467bd",
        "Sinter": "#8c564b",
        "RMHS": "#e377c2",
        "SMS-1": "#17becf",
        "SMS-2": "#bcbd22",
        "Coke Oven": "#7f7f7f",
        "Blast Furnace": "#8B0000",
        "CRM": "#00BFFF",
        "WRM": "#32CD32",
        "CSP Caster": "#FF1493",
        "LCP": "#FFD700",
        "DRI": "#A0522D",
        "CRM Kolkata": "#20B2AA",
        "CRM Chandigarh": "#FF8C00"
    }
)

fig.update_traces(texttemplate="%{text}%", textposition="outside")

fig.update_layout(
    xaxis_title="Department",
    yaxis_title="Compliance (%)",
    yaxis=dict(range=[0, 100]),
    height=500,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📂 Department Documents")

DOC_PATH = Path("documents") / department
DOC_PATH.mkdir(parents=True, exist_ok=True)

uploaded_files = st.file_uploader(
    "Upload Audit Documents",
    accept_multiple_files=True,
    type=["pdf", "docx", "xlsx", "pptx", "jpg", "jpeg", "png"]
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        with open(DOC_PATH / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.success("✅ Documents Uploaded Successfully")

    st.markdown("### 📁 Uploaded Documents")

    files = os.listdir(DOC_PATH)

    if files:

        for file in files:

            col1, col2, col3 = st.columns([6, 2, 2])

            with col1:
                st.write("📄", file)

            with col2:
                with open(DOC_PATH / file, "rb") as f:
                    st.download_button(
                        "⬇ Download",
                        data=f,
                        file_name=file,
                        key=f"download_{file}"
                    )

            with col3:
                if st.button("🗑 Delete", key=f"delete_{file}"):
                    os.remove(DOC_PATH / file)
                    st.success(f"{file} deleted successfully.")
                    st.rerun()

    else:
        st.info("No documents uploaded.")

st.markdown("---")
st.subheader("📥 Download Audit Report")

if os.path.exists(AUDIT_FILE):
    with open(AUDIT_FILE, "rb") as file:
        st.download_button(
            label="📥 Download Audit Report (Excel)",
            data=file,
            file_name="Audit_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
else:
    st.info("No audit report available for download.")

st.markdown("---")