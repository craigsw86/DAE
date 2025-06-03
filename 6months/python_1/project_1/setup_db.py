import sqlite3

def setup_database():
    """
    Creates the patients database with required schema if it doesn't already exist.
    """
    try:
        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                last_visit TEXT,
                death_date TEXT,
                is_active INTEGER DEFAULT 1
            );
        """)

        conn.commit()

    except Exception as e:
        print(f"❌ Error creating database: {e}")

    else:
        print("✅ Database setup completed successfully.")

    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database()
