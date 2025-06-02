"""
db.py

Handles database connection logic for the Clinic Reminder App.
Provides a resuable function to connect to the clinic.db SQLite database.
"""

import sqlite3

def connect_db():
    return sqlite3.connect("clinic.db")
    """
    Connects to the clinic.db SQLite database and returns the connection object.

    Returns:
    sqlite3.Connection: An open connection to the database.
    """

# Inserts a new patient into the database with required and optional details.
# Parameters: first_name (str), last_name (str), last_visit (date), death_date (optional date), is_active (bool)
def insert_patient(first_name, last_name, last_visit, death_date=None):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO PATIENTS (first_name, last_name, last_visit, death_date, is_active), VALUES (?, ?, ?, ?, 1)",
            (first_name, last_name, last_visit, death_date)
        )
    except Exception as e:
        print("Error inserting patient:", e)
    else:
        conn.commit()
        print("Patient inserted successfully.")
    finally:
        conn.close()

# NOTE:
# The 'active' field in the patients table uses:
#   1 = Active (patient is still being tracked)
#   0 = Inactive (patient file flagged for shredding)