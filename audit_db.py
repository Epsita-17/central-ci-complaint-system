import sqlite3
import pandas as pd

DB_NAME = "data/audit.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_table():

    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS audit(
        department TEXT,
        sr_no INTEGER,
        action_item TEXT,
        detailed_scope TEXT,
        responsible TEXT,
        target_date TEXT,
        status TEXT,
        month TEXT,
        audited_by TEXT,
        audit_date TEXT,
        PRIMARY KEY(department, sr_no)
    )
    """)

    conn.commit()
    conn.close()


def load_audit(department):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM audit WHERE department=? ORDER BY sr_no",
        conn,
        params=(department,)
    )

    conn.close()

    return df

def save_audit(df, department, month, auditor, audit_date):

    conn = get_connection()

    conn.execute(
        "DELETE FROM audit WHERE department=?",
        (department,)
    )

    for _, row in df.iterrows():

        conn.execute("""
        INSERT INTO audit
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            department,
            int(row["Sr No"]),
            row["Action Item"],
            row["Detailed Scope"],
            row["Responsible"],
            str(row["Target Date"]),
            row["Status"],
            month,
            auditor,
            str(audit_date)
        ))

    conn.commit()
    conn.close()