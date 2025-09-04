import sqlite3

def connect_db():
    return sqlite3.connect("clinic.db")

def insert_patient(first_name, last_name, last_visit, death_date=None, is_active=True):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, last_visit, death_date, is_active)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, last_visit, death_date, int(is_active)))
    conn.commit()
    conn.close()
