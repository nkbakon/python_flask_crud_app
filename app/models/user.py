from app import mysql

class User:
    @staticmethod
    def find_by_email(email):
        cur = mysql.connection.cursor()
        cur.execute("SELECT email, password, type, id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def update_password(id, hashed_password):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_password, id))
        mysql.connection.commit()
        cur.close()

    # Add more methods as needed...
