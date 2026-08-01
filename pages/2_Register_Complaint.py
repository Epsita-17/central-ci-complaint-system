import streamlit as st
from datetime import date
from database import create_database, save_complaint
from email_sender import send_email
create_database()
import pandas as pd
import os

# Login Protection
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 Please login first.")
    st.switch_page("app.py")
    st.stop()

st.set_page_config(page_title="Register Complaint", layout="wide")

create_database()

FILE_NAME = "data/complaints.xlsx"

if os.path.exists(FILE_NAME):
    df = pd.read_excel(FILE_NAME)
    complaint_id = f"CI-{date.today().strftime('%Y%m%d')}-{len(df)+1:03d}"
else:
    complaint_id = f"CI-{date.today().strftime('%Y%m%d')}-001"


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
📝 Register New Complaint
</h3>

</div>
""", unsafe_allow_html=True)

with st.form("complaint_form"):

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Complaint ID", value=complaint_id, disabled=True)
        complaint_date = st.date_input("Date", date.today())
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
        equipment = st.text_input("Equipment Tag*")

    with col2:
        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Critical"]
        )
        breakdown = st.selectbox(
            "Breakdown Type",
            ["Electrical", "Instrumentation", "Mechanical", "Process"]
        )
        reported_by = st.text_input("Reported By*")
        assigned_to = st.selectbox(
            "Assign To",
            [
                "Unassigned",
                "Instrumentation Team",
                "Electrical Team",
                "Automation Team",
                "Mechanical Team",
                "Vendor",
                "Contractor"
            ]
        )

    problem = st.text_area("Problem Description*")
    uploaded_image = st.file_uploader(
        "Upload Problem Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Image Preview", width=300)

    submit = st.form_submit_button(
        "🚀 Register Complaint",
        use_container_width=True,
        type="primary"
    )

if submit:
    import os

    os.makedirs("complaints_images", exist_ok=True)

    image_path = ""

    if uploaded_image is not None:
        image_path = f"complaints_images/{complaint_id}_{uploaded_image.name}"

        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

    data = [
        complaint_id,
        complaint_date,
        department,
        equipment,
        problem,
        priority,
        breakdown,
        reported_by,
        assigned_to,
        "Open",
        image_path
    ]

    with st.spinner("Registering complaint..."):
        if equipment.strip() == "":
            st.error("Equipment Tag is required.")
            st.stop()

        if reported_by.strip() == "":
            st.error("Reported By is required.")
            st.stop()

        if problem.strip() == "":
            st.error("Problem Description is required.")
            st.stop()
        save_complaint(data)

    complaint = {
        "Complaint ID": complaint_id,
        "Date": complaint_date,
        "Department": department,
        "Equipment Tag": equipment,
        "Problem Description": problem,
        "Priority": priority,
        "Breakdown Type": breakdown,
        "Reported By": reported_by,
        "Assigned To": assigned_to,
        "Status": "Open"
    }

    try:
        send_email(complaint)
        st.balloons()

        st.success(
            f"""
        ### ✅ Complaint Registered Successfully

        Complaint ID : **{complaint_id}**

        The complaint has been saved successfully.
        """
        )
        st.info("📧 Email notification sent successfully.")
    except Exception as e:
        st.success(f"✅ Complaint {complaint_id} Registered Successfully!")
        st.warning(f"Complaint saved, but email could not be sent.\n\n{e}")