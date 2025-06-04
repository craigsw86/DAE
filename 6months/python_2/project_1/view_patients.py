from db import connect_db

def view_patients(status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, last_name, last_visit, death_date FROM patients WHERE is_active = ?", (status,))
    rows = cursor.fetchall()

    if status == 1:
        print("\n🟢 ACTIVE PATIENTS:\n")
    else:
        print("\n🔴 INACTIVE PATIENTS:\n")

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    while True:
        choice = input("View (A)ctive or (I)nactive patients? (Q to quit): ").strip().upper()
        if choice == "A":
            view_patients(1)
        elif choice == "I":
            view_patients(0)
        elif choice == "Q":
            break
        else:
            print("Invalid option. Please try again.")
