import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = "centralci.support@gmail.com"
APP_PASSWORD = "ouquivxfhoxtpinq"

HOD_EMAIL = "epsita.bisoi@jsw.in"

ENGINEER_EMAILS = {
    "Ashish Garnaik":"ashish.garnaik@jsw.in",
    "Saumyadip Gangopadhyay":"g.saumyadip@jsw.in",
    "Bijay Nayak":"bijay.nayak@jsw.in",
    "Krishna Tiwari":"krishna.tiwari1@jsw.in",
    "James Ekka":"james.ekka@jsw.in",
    "Gaurav Kumar":"gaurav.kumar3@jsw.in",
    "Rinku Saraf":"rinku.saraf@jsw.in",
    "Amrit Thakur":"amrit.thakur@jsw.in",
    "Jitendra Rade":"jitendra.rade@jsw.in",
    "Pawan Gupta":"pawan.gupta1@jsw.in",
    "Atul Porwal":"atul.porwal@jsw.in",
    "Akash Das":"akash.das@jsw.in",
    "Narendra Singh":"nirendra.singh@jsw.in",
    "Tanmaya Das":"tanmaya.das@jsw.in",
    "Deepak Sahani":"deepak.sahani@jsw.in",
    "Santosh Kumar":"santosh.kumar10@jsw.in",
    "Munish Kumar":"munish.kumar@jsw.in",
    "Girija Mallick":"girija.mallick@jsw.in",
    "Prakash Maheshwari":"prakash.maheshwari@jsw.in",
    "Vipin Singh":"vipin.singh@jsw.in",
    "Dinesh Mandadi":"dinesh.mandadi@jsw.in",
    "Kabir Pradhan":"kabir.pradhan@jsw.in",
    "Rahul Saxena":"rahul.saxena@jsw.in",
    "Himani Sahu":"himani.sahu@jsw.in",
    "Vicky Panwala":"vicky.panwala@jsw.in",
    "Soumya Das":"soumya.das@jsw.in",
    "Anil Yadav":"anil.yadav4@jsw.in",
    "Raju Chaubey":"raju.chaubey@jsw.in",
    "Jaiprakash Singh":"jaiprakash.singh@jsw.in",
    "R Ravikant":"r.ravikant@jsw.in",
    "Chaitanya Kanwar":"chaitanya.kanwar@jsw.in",
    "Debasish Jena":"debasish.jena@jsw.in",
    "Pritam Prusty":"pritam.prusty@jsw.in",
    "Jasvindersingh Malli":"jasvindarsingh.malli@jsw.in",
    "Epsita Bisoi":"epsita.bisoi@jsw.in"
}


def send_mail(receiver, subject, body):

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()


def send_email(complaint):

    body = f"""
New Service Request

Complaint ID : {complaint['Complaint ID']}
Department : {complaint['Department']}
Equipment : {complaint['Equipment Tag']}
Priority : {complaint['Priority']}

Problem:
{complaint['Problem Description']}
"""

    send_mail(
        HOD_EMAIL,
        f"New Service Request - {complaint['Complaint ID']}",
        body
    )


def send_engineer_email(complaint):

    receiver = ENGINEER_EMAILS.get(
        complaint["Assigned Person"],
        ""
    )

    if receiver == "":
        return

    body = f"""
    JSW JFE Steel Ltd.

    Central C&I Service Management System

    Complaint ID : {complaint['Complaint ID']}
    Department : {complaint['Department']}
    Equipment : {complaint['Equipment Tag']}

    Problem :
    {complaint['Problem Description']}

    ---------------------------------------

    Approve Complaint

    http://127.0.0.1:5000/approve/{complaint['Complaint ID']}

    ---------------------------------------

    Assign Engineer

    http://127.0.0.1:5000/assign/{complaint['Complaint ID']}

    """

    send_mail(
        receiver,
        f"Service Assigned - {complaint['Complaint ID']}",
        body
    )


def send_hod_completion_email(complaint):

    body = f"""
Engineer has completed the work.

Complaint ID : {complaint['Complaint ID']}

Engineer : {complaint['Assigned Person']}

Working Hours : {complaint['Working Hours']}

Manpower : {complaint['Manpower']}

Service Remark :

{complaint['Service Remark']}

Please verify and close the complaint.
"""

    send_mail(
        HOD_EMAIL,
        f"Completion Approval Required - {complaint['Complaint ID']}",
        body
    )