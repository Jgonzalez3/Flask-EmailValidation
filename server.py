from flask import Flask, redirect, render_template, request, session, flash
from mysqlconnection import MySQLConnection

app = Flask(__name__)
app.secret_key = "jonny"
mysql = MySQLConnection(app, 'email_valid')
@app.route("/")
def index():
    return render_template("emailvalid.html")

@app.route("/success", methods = ["POST"])
def emailvalidation():
    query = "SELECT email FROM emails"
    data = {"user_email": request.form['email']}
    emailvalid = mysql.query_db(query)
    for i in range(0,len(emailvalid)):
        if emailvalid[i]["email"] == request.form['email']:
            session['submitted_email'] = emailvalid[i]["email"]
            return redirect("/success", submitted_email = session['submitted_email'])
        else:
            flash("Email is not valid!")
            return redirect("/")

@app.route("/success")
def success():
    flash("The email address you entered () is a VALID email address! Thank you!")
    query2 = "SELECT * FROM emails"
    user_emails = mysql.query_db(query2)
    return render_template("success.html", all_emails = user_emails)

app.run(debug=True)
