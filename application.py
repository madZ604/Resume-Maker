
# framework based on cs50 problem sets

from cs50 import SQL
import os
import requests
import urllib.parse
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps

# configure application
app = Flask(__name__)

# ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///resume.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code


@app.route("/login", methods=["GET", "POST"])
def login():
    # login user

    # forget any previous user
    session.clear()

    # POST
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template('error.html',err='Must provide username')
        if not request.form.get("password"):
            return render_template('error.html', err='Must provide valid password')
        username = request.form.get("username")
        hashp = generate_password_hash(request.form.get("password"))

        search = db.execute("SELECT * FROM account WHERE username=?", username)

        if not search:
            return render_template('error.html', err="Username doesn't exist")
        else:
            if check_password_hash(search[0]["password"], request.form.get("password")):
                session['user_id'] = search[0]['id']
                return redirect("/")
            else:
                return render_template('error.html', err='Incorrect passsword')
    # GET
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # POST
    if request.method== "POST":
        if not request.form.get("username"):
            return render_template('error.html',err='Must provide username')
        if not request.form.get("password"):
            return render_template('error.html', err='Must provide valid password')
        if not request.form.get("confirm"):
            return render_template('error.html', err='Confirm password')
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if not password == confirm:
            return render_template('error.html', err='Passwords should match')
        exists = db.execute("SELECT username FROM account WHERE username=?", username)
        if exists:
            return render_template('error.html', err='Username already exists')
        hashed = generate_password_hash(password)

        db.execute("INSERT INTO account (username, password) VALUES (?,?)", username, hashed)
        return redirect("/login")

    # GET
    else:
        return render_template('register.html')

@app.route("/", methods=["GET", "POST"])
@login_required
def edit():
    # page where details are entered/editted
    if request.method == 'POST':
        if not request.form.get("name"):
            return render_template('error.html', err='Name must be entered')
        if not request.form.get("email"):
            return render_template('error.html', err='Email must be entered')
        if not request.form.get("number"):
            return render_template('error.html', err='Contact number must be entered')
        if not request.form.get("skills"):
            return render_template('error.html', err='Skillset must be entered')
        if not request.form.get("exp"):
            return render_template('error.html', err='Relevant experience in said domain must be entered')
        if not request.form.get("uni"):
            return render_template('error.html', err='University must be entered')
        if not request.form.get("deg"):
            return render_template('error.html', err='Degree attained must be entered')
        if not request.form.get("major"):
            return render_template('error.html', err='Major in your field of study must be entered')
        if not request.form.get("dur"):
            return render_template('error.html', err='Duration of education must be entered')
        if not request.form.get("link"):
            return render_template('error.html', err='LinkedIn profile link must be entered')

        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        skills = request.form.get("skills")
        exp = request.form.get("exp")
        uni = request.form.get("uni")
        major = request.form.get("major")
        deg = request.form.get("deg")
        dur = request.form.get("dur")
        link = request.form.get("link")

        check = db.execute("SELECT id FROM data WHERE id=?", session['user_id'])

        if not check:
            db.execute("INSERT INTO data (id, name, number, email, link, skills, exp, uni, major, deg, dur) VALUES (?,?,?,?,?,?,?,?,?,?,?)", session['user_id'], name, number, email, link, skills, exp, uni, major, deg, dur)
        else:
            db.execute("UPDATE data SET name = ?, number=?, email=?, link=?, skills=?, exp=?, uni=?, major=?, deg=?, dur=? WHERE id = ?",name, number, email, link, skills, exp, uni, major, deg, dur, session['user_id'])
        val =  db.execute("select name, number, email, link, skills, exp, uni, major, deg, dur from data WHERE id = ?",session['user_id'])[0]
        return render_template("resume.html", val = val)

    else:
        return render_template("edit.html")

@app.route("/view")
@login_required
def view():
    # show the ultimate resume
    val = db.execute("SELECT * FROM data WHERE id=?", session['user_id'])[0]
    return render_template("resume.html", val = val)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


