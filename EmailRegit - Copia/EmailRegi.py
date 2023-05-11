from flask import Flask, render_template, request, session, redirect, g
import sqlite3
import os
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"

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

if __name__ == "__main__":
    app.run()
