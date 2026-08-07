import sqlite3
import pandas as pd
import os

DB_NAME = "data/complaints.db"
FILE_NAME = "data/complaints.xlsx"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_sqlite_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        complaint_id TEXT PRIMARY KEY,
        date TEXT,
        department TEXT,
        equipment_tag TEXT,
        problem_description TEXT,
        priority TEXT,
        category TEXT,
        breakdown_type TEXT,
        reported_by TEXT,
        assigned_to TEXT,
        hod_name TEXT,
        target_date TEXT,
        hod_remark TEXT,
        closed_by TEXT,
        status TEXT,
        image_path TEXT,
        assigned_person TEXT,
        working_hours REAL,
        manpower INTEGER,
        service_remark TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_database():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=[
            "Complaint ID",
            "Date",
            "Department",
            "Equipment Tag",
            "Problem Description",
            "Priority",
            "Category",
            "Breakdown Type",
            "Reported By",
            "Assigned To",
            "HOD",
            "Target Date",
            "HOD Remark",
            "Assigned Person",
            "Working Hours",
            "Manpower",
            "Service Remark",
            "Status",
            "Image Path"
        ])

        df.to_excel(FILE_NAME, index=False)


def save_complaint(data):
    df = pd.read_excel(FILE_NAME)
    df.loc[len(df)] = data
    df.to_excel(FILE_NAME, index=False)


def get_complaints():
    if not os.path.exists(FILE_NAME):
        create_database()

    df = pd.read_excel(FILE_NAME)
    return df

def update_status(
    complaint_id,
    status,
    assigned_person,
    working_hours,
    manpower,
    service_remark
):

    df = pd.read_excel(FILE_NAME, dtype=object)

    df.loc[df["Complaint ID"] == complaint_id, "Status"] = status
    df.loc[df["Complaint ID"] == complaint_id, "Assigned Person"] = assigned_person
    df.loc[df["Complaint ID"] == complaint_id, "Working Hours"] = working_hours
    df.loc[df["Complaint ID"] == complaint_id, "Manpower"] = manpower
    df.loc[df["Complaint ID"] == complaint_id, "Service Remark"] = service_remark

    df.to_excel(FILE_NAME, index=False)
    df = pd.read_excel(FILE_NAME, dtype=object)

    df.loc[df["Complaint ID"] == complaint_id, "Status"] = str(status)
    df.loc[df["Complaint ID"] == complaint_id, "Assigned Person"] = str(assigned_person)
    df.loc[df["Complaint ID"] == complaint_id, "Working Hours"] = float(working_hours)
    df.loc[df["Complaint ID"] == complaint_id, "Manpower"] = int(manpower)
    df.loc[df["Complaint ID"] == complaint_id, "Service Remark"] = str(service_remark)

    df.to_excel(FILE_NAME, index=False)


def delete_complaint(complaint_id):
    df = pd.read_excel(FILE_NAME)

    df = df[df["Complaint ID"] != complaint_id]

    df.to_excel(FILE_NAME, index=False)


def dashboard_summary():
    df = get_complaints()

    summary = {
        "Total": len(df),
        "Open": len(df[df["Status"] == "Open"]),
        "Assigned": len(df[df["Status"] == "Assigned"]),
        "In Progress": len(df[df["Status"] == "In Progress"]),
        "Waiting for Spare": len(df[df["Status"] == "Waiting for Spare"]),
        "Vendor Support": len(df[df["Status"] == "Vendor Support"]),
        "Closed": len(df[df["Status"] == "Closed"]),
        "High": len(df[df["Priority"] == "High"]),
        "Critical": len(df[df["Priority"] == "Critical"])
    }

    return summary

def create_material_database():
    material_file = "data/material_issue.xlsx"

    if not os.path.exists(material_file):
        df = pd.DataFrame(columns=[
            "Issue ID",
            "Issue Date",
            "Department",
            "Material Name",
            "Material Code",
            "Quantity",
            "Issued To",
            "Contact Number",
            "Expected Return Date",
            "Purpose",
            "Approved By",
            "Status",
            "Actual Return Date"
        ])

        df.to_excel(material_file, index=False)


def save_material(data):
    material_file = "data/material_issue.xlsx"

    if not os.path.exists(material_file):
        create_material_database()

    df = pd.read_excel(material_file)

    df.loc[len(df)] = data

    df.to_excel(material_file, index=False)


def get_materials():
    material_file = "data/material_issue.xlsx"

    if not os.path.exists(material_file):
        create_material_database()

    return pd.read_excel(material_file)
