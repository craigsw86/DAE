from db import connect_db

while True:
    choice = input("View (A)ctive or (I)nactive pateints? (Q to quit): ")
    if choice == "A":
        view_patients(1)
    elif choice == "I":
        view_patients(0)
    elif choice == "Q":
        break
    else:
        print("Invalid option. Please try again.")
        continue

conn = connect_db()
cursor = conn.cursor()

cursor.execute("SELECT id, first_name, last_name, last_visit, death_date, is_active FROM patients")
rows = cursor.fetchall()

print("\n📋 ALL PATIENTS IN DATABASE:\n")
for row in rows:
    print(row)

conn.close()
