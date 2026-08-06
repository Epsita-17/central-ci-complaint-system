import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = "centralci.support@gmail.com"
APP_PASSWORD = "kdawqpvoiithzvge"


def send_email(complaint):

    receiver = "epsita.bisoi@jsw.in"   # Change later to the required recipient

    msg = MIMEMultipart()

    msg["From"] = EMAIL
    msg["To"] = receiver
    msg["Subject"] = f"New C&I Service Request - {complaint['Complaint ID']}"

    body = f"""
JSW JFE Steel Ltd.

Central C&I Service Management System

Complaint ID : {complaint['Complaint ID']}
Date : {complaint['Date']}
Department : {complaint['Department']}
Equipment Tag : {complaint['Equipment Tag']}

Problem Description:
{complaint['Problem Description']}

Priority : {complaint['Priority']}
Category : {complaint['Category']}
Breakdown : {complaint['Breakdown Type']}

Reported By : {complaint['Reported By']}
Assigned Engineer : {complaint['Assigned To']}
Assigned Person : {complaint['Assigned Person']}

Status : Open
"""

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()