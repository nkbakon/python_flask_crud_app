from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "flash message"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcrud'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from products")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students = data)

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
        return redirect(url_for('index'))
    
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
        return redirect(url_for('index'))
    
@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def delete(id):
    flash("Product deleted successfully!")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (id))    
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)