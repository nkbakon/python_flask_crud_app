from flask import render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from app import app
from app.models.user import User
import bcrypt

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['email'] = user[0]
            session['type'] = user[2]
            session['id'] = user[3]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html', email=session['email'])
    else:
        return redirect(url_for('login'))
    

@app.route('/profile')
def profile():
    if 'email' in session:
        return render_template('profile.html', email=session['email'], id=session['id'])
    else:
        return redirect(url_for('login'))
    
@app.route('/profile/update', methods=['POST'])
def profile_update():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']

        user = User.find_by_id(id)

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):  # Corrected to user[0]
            new_password = request.form['new_password']
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            User.update_password(id, hashed_password)
            flash("Profile updated successfully!", 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid current password', 'danger')
            return redirect(url_for('profile'))
