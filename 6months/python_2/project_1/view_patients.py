from db import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("SELECT id, first_name, last_name, last_visit, death_date, is_active FROM patients")
rows = cursor.fetchall()

print("\n📋 ALL PATIENTS IN DATABASE:\n")
for row in rows:
    print(row)

conn.close()
