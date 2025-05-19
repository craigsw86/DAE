import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="clinic_db"
    )

# I worked on it today.