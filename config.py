import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",                # tetap localhost karena MySQL di hosting yang sama
        user="appbaswe_studytracer",     # user database
        password="appbaswe_studytracer",# password user DB yang kamu buat di cPanel
        database="appbaswe_studytracer"  # nama database
    )
