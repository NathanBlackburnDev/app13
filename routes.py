from __main__ import app
from flask import Flask, render_template, redirect, session, url_for, request, get_flashed_messages, flash
import hashlib
from db_connector import Database
import re

db = Database()

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
        existing_account = db.queryDB('SELECT * FROM users WHERE username = ? OR email = ?', [username, email])
        username_pattern = '^[A-Za-z0-9_]+$'
        email_pattern = '^[A-Za-z0-9@.]+$'
        location_pattern = '^[A-Za-z ]+$'
        height_pattern = '^[0-9]+ cm$'
        weight_pattern = '^[0-9]+ kg$'

        # Check if user input is valid
        if existing_account:
            flash('Username or email already in use')
        elif not re.match(username_pattern, username):
            flash('Please enter valid username')
        elif not (4 < len(username) <= 14):
            flash('Username must be between 4 and 14 characters')
        elif not re.match(email_pattern, email):
            flash('Please enter a valid email')
        elif not (6 < len(email) <= 40):
            flash('Email must be between 6 and 40 characters')
        elif not re.match(location_pattern, location):
            flash('Please enter a valid location')
        elif not (4 < len(location) <= 60):
            flash('Location must be between 4 and 60 characters')
        elif not re.match(height_pattern, height):
            flash('Please enter a valid height in CM')
        elif not (4 < len(height) <= 6):
            flash('Height must be between 4 and 6 characters')
        elif not re.match(weight_pattern, weight):
            flash('Please enter a valid weight in KG')
        elif not (4 < len(weight) <= 6):
            flash('Weight must be between 4 and 6 characters')
        elif not (6 < len(password) <= 40):
            flash('Password must be between 6 and 40 characters')
        elif password != confirm_password:
            flash('Passwords must match')
        else:
            # Convert to correct measurements
            weight = weight.lower()
            height = height.lower()
            # Hash user email + password
            hashed_password = hashlib.md5(str(password).encode()).hexdigest()
            hashed_email = hashlib.md5(str(email).encode()).hexdigest()

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
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        user_account = db.queryDB('SELECT * FROM users WHERE username = ?', [username])
        stored_password = user_account[0][-1]

        if not user_account:
            flash('Account does not exist')
        elif hashed_password != stored_password:
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