import pythoncom
import win32com.client

def send_email(complaint):
    pythoncom.CoInitialize()

    outlook = win32com.client.Dispatch("Outlook.Application")

    mail = outlook.CreateItem(0)

    mail.To = "epsita.bisoi@jsw.in"
    mail.Subject = f"New C&I Complaint - {complaint['Complaint ID']}"

    mail.Body = f"""
JSW JFE Steel Ltd.

Complaint ID : {complaint['Complaint ID']}
Department : {complaint['Department']}
Equipment : {complaint['Equipment Tag']}
Priority : {complaint['Priority']}

Problem:
{complaint['Problem Description']}
"""

    mail.Send()

    pythoncom.CoUninitialize()