# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint("auth", __name__)

# In-memory user store — for simplicity, usernames and passwords are hardcoded
users = {
    "admin": "adminpass",
    "analyst": "dsat2025"
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        flash("Invalid username or password")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

