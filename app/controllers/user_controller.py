from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app
from app.models.user import User
import bcrypt

@app.route('/users')
def users():
    if 'email' in session and session.get('type') == 1:
        data = User.get_all_users()
        return render_template('users.html', users=data, email=session['email'])
    else:
        return redirect(url_for('login'))

@app.route('/user/insert', methods=['POST'])
def user_insert():
    if request.method == 'POST':
        email = request.form['email']
        if not User.find_by_email(email):
            name = request.form['name']
            password = request.form['password']
            user_type = request.form['type']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            User.insert(name, email, hashed_password, user_type)
            flash("User created successfully!", 'success')
            return redirect(url_for('users'))
        else:
            flash('Already Registered User!', 'danger')
            return redirect(url_for('users'))

@app.route('/user/update', methods=['POST', 'GET'])
def user_update():
    if request.method == 'POST':
        email = request.form['email']
        id = request.form['id']
        if not User.find_by_email_exclude_id(email, id):
            name = request.form['name']
            user_type = request.form['type']
            User.update(id, name, email, user_type)
            flash('User updated successfully!', 'warning')
            return redirect(url_for('users'))
        else:
            flash('Already Registered User!', 'danger')
            return redirect(url_for('users'))

@app.route('/user_delete/<string:id>', methods=['POST', 'GET'])
def user_delete(id):
    flash('User deleted successfully!', 'danger')
    User.delete(id)
    return redirect(url_for('users'))

@app.route('/users/email/check', methods=['GET'])
def user_email_check():
    email = request.args.get('email')
    if email:
        if User.find_by_email(email):
            return jsonify(success=False)
        else:
            return jsonify(success=True)
    return jsonify(success=False)

@app.route('/users/email/update', methods=['GET'])
def user_email_update():
    email = request.args.get('email')
    id = request.args.get('id')
    if email and id:
        if User.find_by_email_exclude_id(email, id):
            return jsonify(success=False)
        else:
            return jsonify(success=True)
    return jsonify(success=False)
