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
from pathlib import Path

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

    logo = Image(str(LOGO_FILE), width=70, height=35)

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

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_FILE = BASE_DIR / "images" / "jsw_logo.jpeg"

col1, col2, col3 = st.columns([2,6,2])

with col1:
    st.image(str(LOGO_FILE), width=250)

with col2:
    st.markdown("""
    <h1 style="text-align:center;color:#0B3C6F;">
    Central C&I Service Management System
    </h1>

    <p style="text-align:center;color:gray;font-size:18px;">
    JSW JFE Steel Ltd. 
    </p>
    """, unsafe_allow_html=True)

with col3:
    from datetime import date
    st.markdown(f"""
    <div style="text-align:right;padding-top:20px;">
    📅 <b>Date</b><br>
    {date.today().strftime("%d-%m-%Y")}
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
    styled_df = display_df.style.set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#0B3C6F"),
                ("color", "white"),
                ("font-weight", "bold"),
                ("text-align", "center")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("background-color", "white"),
                ("color", "black")
            ]
        }
    ])

    st.data_editor(
        display_df,
        width="stretch",
        hide_index=True,
        disabled=True
    )
    st.markdown("### 📷 Complaint Image")

    selected_id = st.selectbox(
        "Select Complaint ID",
        df["Complaint ID"].tolist(),
        key="image_select"
    )

    selected_row = df[df["Complaint ID"] == selected_id].iloc[0]

    image_path = str(selected_row["Image Path"])

    if image_path != "nan" and os.path.exists(image_path):
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

    assigned_person = st.selectbox(
        "Assigned Person",
        [
            "Unassigned",
            "Ashish Garnaik",
            "Saumyadip Gangopadhyay",
            "Bijay Nayak",
            "Krishna Tiwari",
            "James Ekka",
            "Gaurav Kumar",
            "Rinku Saraf",
            "Amrit Thakur",
            "Jitendra Rade",
            "Pawan Gupta",
            "Atul Porwal",
            "Akash Das",
            "Nirendra Singh",
            "Tanmaya Das",
            "Deepak Sahani",
            "Santosh Kumar",
            "Munish Kumar",
            "Girija Mallick",
            "Prakash Maheshwari",
            "Vipin Singh",
            "Dinesh Mandadi",
            "Kabir Pradhan",
            "Rahul Saxena",
            "Himani Sahu",
            "Vicky Panwala",
            "Soumya Das",
            "Anil Yadav",
            "Raju Chaubey",
            "Jaiprakash Singh",
            "R Ravikant",
            "Chaitanya Kanwar",
            "Pradeep Mohanty",
            "Debasish Jena",
            "Pritam Prusty",
            "Jasvindersingh Malili",
            "Epsita Bisoi"
        ]
    )

    working_hours = st.number_input(
        "Working Hours",
        min_value=0.0,
        step=0.5
    )

    manpower = st.number_input(
        "No. of Manpower",
        min_value=1,
        step=1
    )

    service_remark = st.text_area("Service Remark")

    from email_sender import send_engineer_email, send_hod_completion_email

    from email_sender import send_engineer_email, send_hod_completion_email

    if st.button("Update Status"):

        update_status(
            complaint,
            status,
            assigned_person,
            working_hours,
            manpower,
            service_remark
        )

        row = df[df["Complaint ID"] == complaint].iloc[0]

        complaint_data = {
            "Complaint ID": complaint,
            "Department": row["Department"],
            "Equipment Tag": row["Equipment Tag"],
            "Problem Description": row["Problem Description"],
            "Priority": row["Priority"],
            "Reported By": row["Reported By"],
            "Assigned Person": assigned_person,
            "Working Hours": working_hours,
            "Manpower": manpower,
            "Service Remark": service_remark
        }

        if status == "Assigned":
            send_engineer_email(complaint_data)

        elif status == "Closed":
            send_hod_completion_email(complaint_data)

        st.success("✅ Status Updated Successfully!")
        st.rerun()

        row = df[df["Complaint ID"] == complaint].iloc[0]

        complaint_data = {
            "Complaint ID": complaint,
            "Department": row["Department"],
            "Equipment Tag": row["Equipment Tag"],
            "Problem Description": row["Problem Description"],
            "Priority": row["Priority"],
            "Reported By": row["Reported By"],
            "Assigned Person": assigned_person,
            "Working Hours": working_hours,
            "Manpower": manpower,
            "Service Remark": service_remark
        }

        if status == "Assigned":
            send_engineer_email(complaint_data)

        elif status == "Completed":
            send_hod_completion_email(complaint_data)

        st.success("✅ Status Updated Successfully!")
        st.rerun()