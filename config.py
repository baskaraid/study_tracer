import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # sesuaikan user mysql
        password="",         # sesuaikan password mysql
        database="study_tracer"
    )
