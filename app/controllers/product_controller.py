from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.models.product import Product

@app.route('/products')
def products():
    if 'email' in session:
        data = Product.get_all()
        return render_template('products.html', products=data, email=session['email'])
    else:
        return redirect(url_for('login'))

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        flash("Product stored successfully!")
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']
        Product.insert(name, category, price, description)
        return redirect(url_for('products'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']
        Product.update(id, name, category, price, description)
        flash("Product updated successfully!")
        return redirect(url_for('products'))

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete(id):
    flash("Product deleted successfully!")
    Product.delete(id)
    return redirect(url_for('products'))
