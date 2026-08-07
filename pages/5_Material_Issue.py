import streamlit as st
from database import create_material_database, save_material, get_materials
from datetime import date
import io

st.set_page_config(
    page_title="Material Issue Register",
    layout="wide"
)
# Login Protection
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()

create_material_database()

from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_FILE = BASE_DIR / "images" / "jsw_logo.jpeg"

col1, col2, col3 = st.columns([2,6,2])

with col1:
    st.image(str(LOGO_FILE), width=250)

with col2:
    st.markdown("""
    <h1 style="text-align:center;color:#0B3C6F;">
    Material Issue Register
    </h1>

    <p style="text-align:center;color:gray;font-size:18px;">
    JSW JFE Steel Ltd. 
    </p>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="text-align:right;padding-top:20px;">
    📅 <b>Date</b><br>
    {date.today().strftime("%d-%m-%Y")}
    </div>
    """, unsafe_allow_html=True)

import pandas as pd
from pathlib import Path

MATERIAL_FILE = BASE_DIR / "data" / "material_issue.xlsx"

if MATERIAL_FILE.exists():
    material_df = pd.read_excel(MATERIAL_FILE)
else:
    material_df = pd.DataFrame()

total = len(material_df)

issued = len(material_df[material_df["Status"] == "Issued"]) if total else 0

returned = len(material_df[material_df["Status"] == "Returned"]) if total else 0

overdue = len(
    material_df[
        (material_df["Status"] == "Issued") &
        (pd.to_datetime(material_df["Expected Return Date"]) < pd.Timestamp.today())
    ]
) if total else 0

cards = st.columns(4)

data = [
    ("📦", "Total", total, "#1565C0"),
    ("📤", "Issued", issued, "#FB8C00"),
    ("✅", "Returned", returned, "#43A047"),
    ("⏰", "Overdue", overdue, "#E53935")
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

st.markdown("<br>", unsafe_allow_html=True)

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
📦 Returnable Material Issue Form
</h3>

</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    issue_id = st.text_input(
        "Issue ID",
        value="MAT-20260807-001",
        disabled=True
    )

    issue_date = st.date_input(
        "Issue Date",
        date.today()
    )

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
            "Blast Furnace",
            "Oxygen Plant",
            "CRM",
            "WRM",
            "DRI"
        ]
    )

    material_name = st.text_input("Material Name")

    material_code = st.text_input("Material Code")

with col2:

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    issued_to = st.text_input("Issued To")

    contact = st.text_input("Contact Number")

    return_date = st.date_input("Expected Return Date")

    purpose = st.text_area("Purpose")

    hod = st.selectbox(
        "Approved By",
        [
            "Avinash Ujjwal"
        ]
    )

submit = st.button(
    "📦 Issue Material",
    use_container_width=True
)
if submit:

    data = [
        issue_id,
        issue_date,
        department,
        material_name,
        material_code,
        quantity,
        issued_to,
        contact,
        return_date,
        purpose,
        hod,
        "Issued",
        ""
    ]

    save_material(data)

    st.success("✅ Material Issued Successfully")

st.markdown("---")

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
📋 Material Issue Register
</h3>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:white;
padding:18px;
border-radius:12px;
box-shadow:0px 2px 8px rgba(0,0,0,0.12);
border:1px solid #E6E6E6;
margin-top:15px;
margin-bottom:20px;
">

<h3 style="color:#0B3C6F;">
🔍 Search & Filter
</h3>

</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    search_material = st.text_input(
        "Material Name",
        key="search_material"
    )

with c2:
    search_department = st.text_input(
        "Department",
        key="search_department"
    )

with c3:
    search_person = st.text_input(
        "Issued To",
        key="search_person"
    )

try:
    material_df = get_materials()

    if search_material:
        material_df = material_df[
            material_df["Material Name"].astype(str).str.contains(
                search_material, case=False
            )
        ]

    if search_department:
        material_df = material_df[
            material_df["Department"].astype(str).str.contains(
                search_department, case=False
            )
        ]

    if search_person:
        material_df = material_df[
            material_df["Issued To"].astype(str).str.contains(
                search_person, case=False
            )
        ]

    st.dataframe(
        material_df,
        use_container_width=True,
        hide_index=True
    )

    excel_buffer = io.BytesIO()

    material_df.to_excel(
        excel_buffer,
        index=False,
        engine="openpyxl"
    )

    excel_buffer.seek(0)

    st.download_button(
        "📥 Export Material Register (Excel)",
        data=excel_buffer,
        file_name="Material_Issue_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


except Exception as e:
    st.error(f"Error: {e}")