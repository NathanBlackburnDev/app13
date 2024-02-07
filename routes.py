from __main__ import app
from flask import Flask, render_template, redirect, session, url_for, request, get_flashed_messages, flash
from flask_bcrypt import Bcrypt
from db_connector import Database
import re

db = Database()
bcrypt = Bcrypt(app)

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        location = request.form['location']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        height = request.form['height']
        weight = request.form['weight']

        # Valid patterns for user input
        height = height.lower()
        weight = weight.lower()
        existing_account = db.queryDB('SELECT * FROM users WHERE username = ? OR email = ?', [username, email])
        username_pattern = '^[A-Za-z0-9_]$'
        email_pattern = '^[A-Za-z0-9@. ]$'
        location_pattern = '^[A-Za-z ]$'
        height_pattern = '^[0-9]+ kg$'
        weight_pattern = '^[0-9]+ cm$'
        password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        # Convert to correct measurements
        weight = weight.lower()
        height = height.lower()
        # Hash user email + password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        hashed_email = bcrypt.generate_password_hash(email).decode('utf-8')

        # Create user account
        db.updateDB('INSERT INTO users (username, email, location, height, weight, password) VALUES (?, ?, ?, ?, ?, ?)', [username, hashed_email, location, height, weight, hashed_password])
        return redirect(url_for('index'))

    # Return inital register page
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Get the password from database
        user_account = db.queryDB('SELECT * FROM users WHERE username = ?', [username])
        stored_password = user_account[0][-1]

        if not user_account:
            flash('Account does not exist')
        elif not bcrypt.check_password_hash(stored_password, password):
            flash('Incorrect password')
        # If the users password is correct
        else:
            # Log the user in
            session['user'] = username
            return redirect(url_for('index'))
    
    # If the user is already logged in
    if 'user' in session:
        return redirect(url_for('index'))

    # Return initial login page
    return render_template('login.html')

# Log user out
@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)

    return redirect(url_for('index'))