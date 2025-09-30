from config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    @staticmethod
    def create_user(nama, email, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (nama, email, password) VALUES (%s, %s, %s)",
                       (nama, email, hashed_pw))
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def check_password(stored_password, input_password):
        return check_password_hash(stored_password, input_password)
