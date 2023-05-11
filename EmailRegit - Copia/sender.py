from flask import Flask, render_template, request, session, redirect, g
import sqlite3
import os
import threading
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "your_secret_key"

# SMTP email configuration
#SMTP_SERVER = "smtp.gmail.com"
#SMTP_PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT= 587
SMTP_USERNAME = "kebab2803"
SMTP_PASSWORD = "mzvhirdrugvzzyqt"
SENDER_EMAIL = "kebab2803@gmail.com"

# SQLite database setup
DATABASE = "users.db"

def get_database_connection():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)")
    return db

@app.teardown_appcontext
def close_database_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if "email" in session:
        return redirect("/dashboard")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if login_user(email, password):
            session["email"] = email
            return redirect("/dashboard")
        else:
            return render_template("index.html", error="Invalid email or password.")
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "email" in session:
        return redirect("/dashboard")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if register_user(email, password):
            session["email"] = email
            send_registration_email(email)
            return redirect("/dashboard")
        else:
            return render_template("register.html", error="Email already registered.")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "email" in session:
        return render_template("dashboard.html", username=session["email"])
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/")

# Helper functions
def register_user(email, password):
    db = get_database_connection()
    cursor = db.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone() is not None:
        return False
    db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    db.commit()
    return True

def login_user(email, password):
    db = get_database_connection()
    cursor = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return cursor.fetchone() is not None

def send_registration_email(email):
    msg = MIMEText("Thank you for registering!")
    msg["Subject"] = "Registration Confirmation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        print("mando la mail")
        server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("son loggedin")
        server.sendmail(SENDER_EMAIL, [email], msg.as_string())
        print("mando la mail")
        server.quit()
    except smtplib.SMTPException as e:
        print("Error sending email:", str(e))
        print("SMTP debug response:", server.get_debuglevel())

if __name__ == "__main__":
    app.run(debug=True)
