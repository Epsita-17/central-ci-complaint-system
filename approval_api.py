from flask import Flask

app = Flask(__name__)

@app.route("/approve/<complaint_id>")
def approve(complaint_id):
    return f"""
    <h2>Complaint Approved</h2>
    <p>Complaint ID : {complaint_id}</p>
    <a href="/assign/{complaint_id}">
        <button>Assign Engineer</button>
    </a>
    """

@app.route("/assign/<complaint_id>")
def assign(complaint_id):

    engineers = [
        "Ashish Garnaik",
        "Saumyadip Gangopadhyay",
        "Bijay Nayak",
        "Krishna Tiwari",
        "James Ekka",
        "Gaurav Kumar",
        "Epsita Bisoi"
    ]

    options = ""

    for engineer in engineers:
        options += f"<option>{engineer}</option>"

    return f"""
    <h2>Assign Engineer</h2>

    <form action="/assigned/{complaint_id}" method="get">

        <select name="engineer">
            {options}
        </select>

        <br><br>

        <input type="submit" value="Assign Engineer">

    </form>
    """

@app.route("/assigned/<complaint_id>")
def assigned(complaint_id):

    return f"""
    <h2>Engineer Assigned Successfully</h2>

    Complaint {complaint_id} assigned.

    <br><br>

    (Next step will automatically update database and send engineer email.)
    """

if __name__ == "__main__":
    app.run(port=5000)