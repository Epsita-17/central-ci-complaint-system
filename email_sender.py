try:
    import pythoncom
    import win32com.client
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False


def send_email(complaint):

    if not OUTLOOK_AVAILABLE:
        print("Outlook not available. Email skipped.")
        return

    pythoncom.CoInitialize()

    outlook = win32com.client.Dispatch("Outlook.Application")

    mail = outlook.CreateItem(0)

    mail.To = "epsita.bisoi@jsw.in"
    mail.Subject = f"New C&I Request - {complaint['Complaint ID']}"

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