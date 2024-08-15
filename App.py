from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = "flash message"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcrud'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT email, password, type FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['email'] = user[0] 
            session['type'] = user[2] 

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
    
@app.route('/products')
def products():
    if 'email' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from products")
        data = cur.fetchall()
        cur.close()

        return render_template('products.html', products=data, email=session['email'])
    else:
        return redirect(url_for('login'))
    
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        flash("Product stored successfully!")
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, category, price, description) VALUES (%s, %s, %s, %s)", (name, category, price, description))
        mysql.connection.commit()
        return redirect(url_for('products'))
    
@app.route('/update', methods = ['POST', 'GET'])
def update():
    if request.method == 'POST':        
        id = request.form['id']
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE products
        SET name=%s, category=%s, price=%s, description=%s
        WHERE id=%s
        """, (name, category, price, description, id))
        flash("Product updated successfully!")
        mysql.connection.commit()
        return redirect(url_for('products'))
    
@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def delete(id):
    flash("Product deleted successfully!")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (id))    
    mysql.connection.commit()
    return redirect(url_for('products'))

@app.route('/users')
def users():
    if 'email' in session:
        if session.get('type') == 1:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users")
            data = cur.fetchall()
            cur.close()

            return render_template('users.html', users=data, email=session['email'])
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    
@app.route('/user/insert', methods = ['POST'])
def user_insert():
    if request.method == 'POST':
        flash("User created successfully!")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        type = request.form['type']
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, type) VALUES (%s, %s, %s, %s)", (name, email, password, type))
        mysql.connection.commit()
        return redirect(url_for('users'))
    
@app.route('/user/update', methods = ['POST', 'GET'])
def user_update():
    if request.method == 'POST':        
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        type = request.form['type']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE users
        SET name=%s, email=%s, type=%s
        WHERE id=%s
        """, (name, email, type, id))
        flash("User updated successfully!")
        mysql.connection.commit()
        return redirect(url_for('users'))
    
@app.route('/user_delete/<string:id>', methods = ['POST', 'GET'])
def user_delete(id):
    flash("User deleted successfully!")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id))    
    mysql.connection.commit()
    return redirect(url_for('users'))

@app.route('/users/email/check', methods=['GET'])
def user_email_check():
    email = request.args.get('email')
    
    if email:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        
        if user:
            return jsonify(success=False)
        else:
            return jsonify(success=True)
    return jsonify(success=False)

if __name__ == "__main__":
    app.run(debug=True)