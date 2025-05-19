from db import connect_db

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    last_visit DATE,
    death_date DATE,
    is_active BOOLEAN DEFAULT TRUE
    )
    """)
