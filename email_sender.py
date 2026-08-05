try:
    import pythoncom
    import win32com.client
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False


HOD_EMAIL = "avinash.ujjwal@jsw.in"


ENGINEER_EMAILS = {
    "Unassigned": "",
    "Ashish Garnaik": "ashish.garnaik@jsw.in",
    "Saumyadip Gangopadhyay": "g.saumyadip@jsw.in",
    "Bijay Nayak": "bijay.nayak@jsw.in",
    "Krishna Tiwari": "krishna.tiwari1@jsw.in",
    "James Ekka": "james.ekka@jsw.in",
    "Gaurav Kumar": "gaurav.kumar3@jsw.in",
    "Rinku Saraf": "rinku.saraf@jsw.in",
    "Amrit Thakur": "amrit.thakur@jsw.in",
    "Jitendra Rade": "jitendra.rade@jsw.in",
    "Pawan Gupta": "pawan.gupta1@jsw.in",
    "Atul Porwal": "atul.porwal@jsw.in",
    "Akash Das": "akash.das@jsw.in",
    "Narendra Singh": "nirendra.singh@jsw.in",
    "Tanmaya Das": "tanmaya.das@jsw.in",
    "Deepak Sahani": "deepak.sahani@jsw.in",
    "Santosh Kumar": "santosh.kumar10@jsw.in",
    "Munish Kumar": "munish.kumar@jsw.in",
    "Girija Mallick": "girija.mallick@jsw.in",
    "Prakash Maheshwari": "prakash.maheshwari@jsw.in",
    "Vipin Singh": "vipin.singh@jsw.in",
    "Dinesh Mandadi": "dinesh.mandadi@jsw.in",
    "Kabir Pradhan": "kabir.pradhan@jsw.in",
    "Rahul Saxena": "rahul.saxena@jsw.in",
    "Himani Sahu": "himani.sahu@jsw.in",
    "Vicky Panwala": "vicky.panwala@jsw.in",
    "Soumya Das": "soumya.das@jsw.in",
    "Anil Yadav": "anil.yadav4@jsw.in",
    "Raju Chaubey": "raju.chaubey@jsw.in",
    "Jaiprakash Singh": "jaiprakash.singh@jsw.in",
    "R Ravikant": "r.ravikant@jsw.in",
    "Chaitanya Kanwar": "chaitanya.kanwar@jsw.in",
    "Pradeep Mohanty": "",
    "Debasish Jena": "debasish.jena@jsw.in",
    "Pritam Prusty": "pritam.prusty@jsw.in",
    "Jasvindersingh Malli": "jasvindarsingh.malli@jsw.in",
    "Epsita Bisoi": "epsita.bisoi@jsw.in"
}


def send_email(complaint):

    if not OUTLOOK_AVAILABLE:
        print("Outlook not available.")
        return

    pythoncom.CoInitialize()

    try:

        outlook = win32com.client.Dispatch("Outlook.Application")

        mail = outlook.CreateItem(0)

        mail.To = HOD_EMAIL

        mail.Subject = f"New Service Request - {complaint['Complaint ID']}"

        mail.Body = f"""
JSW JFE Steel Ltd.
Central C&I Service Management System

A new Service Request has been registered.

Complaint ID : {complaint['Complaint ID']}

Department : {complaint['Department']}

Equipment Tag : {complaint['Equipment Tag']}

Priority : {complaint['Priority']}

Category : {complaint['Category']}

Breakdown Type : {complaint['Breakdown Type']}

Reported By : {complaint['Reported By']}

Assigned Engineer : {complaint['Assigned Engineer']}

Target Date : {complaint['Target Date']}

Problem Description :

{complaint['Problem Description']}

Please login to the Central C&I Service Management System and assign the engineer.

Regards,

Central C&I Service Management System
"""

        mail.Send()

    finally:
        pythoncom.CoUninitialize()