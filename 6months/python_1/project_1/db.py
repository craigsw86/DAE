import sqlite3

def connect_db():
    return sqlite3.connect("clinic.db")

# Inserts a new patient into the database with required and optional details.
# Parameters: first_name (str), last_name (str), last_visit (date), death_date (optional date), is_active (bool)
def insert_patient(first_name, last_name, last_visit, death_date=None, is_active=True):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, last_visit, death_date, is_active)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, last_visit, death_date, int(is_active)))
    conn.commit()
    conn.close()
