from app import mysql

class Product:
    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products")
        data = cur.fetchall()
        cur.close()
        return data

    @staticmethod
    def insert(name, category, price, description):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, category, price, description) VALUES (%s, %s, %s, %s)", 
                    (name, category, price, description))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update(id, name, category, price, description):
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE products
        SET name=%s, category=%s, price=%s, description=%s
        WHERE id=%s
        """, (name, category, price, description, id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM products WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

    # Add more methods as needed...
