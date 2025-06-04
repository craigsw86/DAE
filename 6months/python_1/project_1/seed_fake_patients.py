import csv
import os
from db import connect_db

FILENAME = "fake_patients.csv"

def seed_database_from_csv():
    if not os.path.exists(FILENAME):
        print(f"❌ CSV file '{FILENAME}' not found.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    added = 0

    with open(FILENAME, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print(f"📄 Detected columns: {reader.fieldnames}")

        for row in reader:
            try:
                fname = row.get('first_name', '').strip()
                lname = row.get('last_name', '').strip()
                visit = row.get('last_visit', '').strip()
                death = row.get('death_date', '').strip()

                if not fname or not lname:
                    print("⚠️ Skipped row with missing name fields.")
                    continue

                cursor.execute("""
                    INSERT INTO patients (first_name, last_name, last_visit, death_date, is_active)
                    VALUES (?, ?, ?, ?, 1)
                """, (fname, lname, visit, death))

                added += 1
            except Exception as e:
                print(f"⚠️ Skipped row due to error: {e}")
                continue

    conn.commit()
    conn.close()
    print(f"✅ {added} patient(s) added from '{FILENAME}'.")

if __name__ == "__main__":
    seed_database_from_csv()
