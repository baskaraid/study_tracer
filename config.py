import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="baskaraid.mysql.pythonanywhere-services.com",
        user="baskaraid",
        password="1234567890",  # sesuai dashboard
        database="baskaraid$default"
    )
