from db import connect_db

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        last_visit TEXT,
        death_date TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()
    print("✅ SQLite table created.")

if __name__ == "__main__":
    create_table()


# I worked on it today.