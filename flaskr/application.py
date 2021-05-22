import os

import functools
import datetime
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, Blueprint, g, url_for
from flask_session import Session 
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

from .helpers import error_message, login_required 


# Create a blueprint to run in __init__.py
bp = Blueprint('index', __name__, url_prefix='/')
#bp_2 = Blueprint('register', __name__, url_prefix='/register')

# Create route for the app's index page
@bp.route('/')
def index():
    return render_template("index.html")

# Create page for users to login
@bp.route('/login', methods=["GET", "POST"])
def login():
    session.clear()
    db = get_db()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check that a username an password were inputted

        if not username:
            return error_message("Please provide your username!", 403)
        
        if not password:
            return error_message("Please provide your password!", 403)
        
        # Query database for all usernames
        users = db.execute("SELECT * FROM user WHERE username = ?", [username]).fetchone()
        print(users)

        # Check if username and password exist in the database

        if users is None:
            return error_message("Please provide a valid username/password!", 403)
        
        if not check_password_hash(users["password"], password):
            return error_message("Please provide a valid username/password!", 403)
        
        # Remember user who logged in

        session["user_id"] = users["id"]

        return redirect("/profile")

    return render_template("login.html")

# Create page for users to register an account
@bp.route('/register', methods=["GET", "POST"])
def register():
    session.clear()
    db = get_db()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check that user name was inputted
        if not username:
            return error_message("You must input a username!", 400)
        
        # Query database to check is username 

        users = db.execute("SELECT * FROM user WHERE username = ?", [username])
        print(users)

        if users.fetchone() is not None:
            return error_message("This username already exists!", 400)
        
        # Check that password was inputted
        if not password:
            return error_message("You must input a password!", 400)
        
        # Check that password confirmation matches password
        if not confirmation:
            return error_message("You must confirm your password!", 400)
        
        if password != confirmation:
            return error_message("Your password and confirmation do not match!", 400)
        
        # Generate password hash for user
        pass_hash = generate_password_hash(password)

        db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, pass_hash))

        db.commit()

        return redirect("/login")
        
        
    return render_template("register.html")

# Logs user out of their account
@bp.route('/logout')
def logout():

    session.clear()

    return redirect('/')

@bp.route('/preferences', methods=["GET", "POST"])
def preference():

    return render_template("preferences.html")

# Displays a users profile page
@bp.route('/profile', methods=["GET", "POST"])
@login_required
def profile():

    return render_template("profile.html")

