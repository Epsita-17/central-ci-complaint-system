import streamlit as st
import pandas as pd
from database import get_complaints, update_status
from io import BytesIO
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

# Login Protection
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()


def convert_to_excel(dataframe):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Complaints"
        )

    output.seek(0)
    return output.getvalue()


def convert_to_pdf(dataframe):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4)
    )

    styles = getSampleStyleSheet()

    title = Paragraph(
        "<b><font size=16>JSW JFE Steel Ltd.</font></b>",
        styles["Title"]
    )

    subtitle = Paragraph(
        "<b>Central C&I Complaint Report</b>",
        styles["Heading2"]
    )

    pdf_df = dataframe[
        [
            "Complaint ID",
            "Date",
            "Department",
            "Equipment Tag",
            "Problem Description",
            "Priority",
            "Status"
        ]
    ]


    data = [list(pdf_df.columns)] + pdf_df.astype(str).values.tolist()

    table = Table(
        data,
        colWidths=[
            1.4 * inch,  # Complaint ID
            1.0 * inch,  # Date
            1.5 * inch,  # Department
            1.4 * inch,  # Equipment Tag
            3.2 * inch,  # Problem Description
            0.8 * inch,  # Priority
            1.0 * inch  # Status
        ]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("BOTTOMPADDING",(0,0),(-1,0),10)
    ]))

    logo = Image("images/jsw_logo.jpeg", width=70, height=35)

    doc.build([
        logo,
        title,
        subtitle,
        table
    ])

    pdf = buffer.getvalue()
    buffer.close()

    return pdf

st.set_page_config(page_title="Complaint List", layout="wide")



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
📋 Service List
</h3>

</div>
""", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)

with col1:
    search_id = st.text_input("Complaint ID")

with col2:
    search_equipment = st.text_input("Equipment Tag")

with col3:
    search_department = st.text_input("Department")

with col4:
    search_reported = st.text_input("Reported By")

df = get_complaints()
if search_id:
    df = df[df["Complaint ID"].astype(str).str.contains(search_id, case=False)]

if search_equipment:
    df = df[df["Equipment Tag"].astype(str).str.contains(search_equipment, case=False)]

if search_department:
    df = df[df["Department"].astype(str).str.contains(search_department, case=False)]

if search_reported:
    df = df[
        df["Reported By"].astype(str).str.contains(
            search_reported,
            case=False
        )
    ]

if len(df) == 0:
    st.warning("No complaints found.")
else:

    display_df = df.drop(columns=["Image Path"], errors="ignore").copy()

    display_df["Status"] = display_df["Status"].replace({
        "Open": "🔴 Open",
        "Assigned": "🟡 Assigned",
        "In Progress": "🔵 In Progress",
        "Waiting for Spare": "🟠 Waiting for Spare",
        "Vendor Support": "🟣 Vendor Support",
        "Closed": "🟢 Closed"
    })

    st.subheader("📋 Service Records")
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    st.markdown("### 📷 Complaint Image")

    selected_id = st.selectbox(
        "Select Complaint ID",
        df["Complaint ID"].tolist(),
        key="image_select"
    )

    selected_row = df[df["Complaint ID"] == selected_id].iloc[0]

    image_path = selected_row["Image Path"]

    if image_path and os.path.exists(image_path):
        st.image(image_path, caption="Uploaded Complaint Image", width=500)
    else:
        st.info("No image available for this complaint.")
    excel_file = convert_to_excel(df)

    st.download_button(
        label="📥 Download Complaints (Excel)",
        data=excel_file,
        file_name="Complaint_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    pdf_file = convert_to_pdf(df)

    st.download_button(
        label="📄 Download Complaints (PDF)",
        data=pdf_file,
        file_name="Complaint_Report.pdf",
        mime="application/pdf"
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
    📋 Update Service Status
    </h3>

    </div>
    """, unsafe_allow_html=True)

    complaint = st.selectbox(
        "Select Complaint ID",
        df["Complaint ID"].tolist(),
        key="status_select"
    )

    status = st.selectbox(
        "New Status",
        [
            "Open",
            "Assigned",
            "In Progress",
            "Waiting for Spare",
            "Vendor Support",
            "Closed"
        ]
    )

    if st.button("Update Status"):
        update_status(complaint, status)
        st.success("✅ Status Updated Successfully!")
        st.rerun()