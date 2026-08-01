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
        breakdown_type TEXT,
        reported_by TEXT,
        assigned_to TEXT,
        status TEXT,
        image_path TEXT
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
            "Breakdown Type",
            "Reported By",
            "Assigned To",
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


def update_status(complaint_id, status):
    df = pd.read_excel(FILE_NAME)

    df.loc[
        df["Complaint ID"] == complaint_id,
        "Status"
    ] = status

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

