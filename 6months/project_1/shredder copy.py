# shredder.py
from datetime import date
from dateutil.relativedelta import relativedelta
from db import connect_db

def check_shredding_reminders():
    today = date.today()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, first_name, last_name, last_visit, death_date FROM patients WHERE is_active = TRUE")
    patients = cursor.fetchall()

    print("🗂️ Patients eligible to move to INACTIVE (paper files can be shredded):")
    found_any = False

    for pid, fname, lname, last_visit, death_date in patients:
        shred_due = False
        reason = ""

        if death_date:
            shred_date = death_date + relativedelta(years=3, days=1)  # Adds 3 years and 1 day
            if today >= shred_date:
                shred_due = True
                reason = f"3 years + 1 day since death on {death_date}"
        elif last_visit:
            shred_date = last_visit + relativedelta(years=7, days=1)  # Adds 7 years and 1 day
            if today >= shred_date:
                shred_due = True
                reason = f"7 years + 1 day since last visit on {last_visit}"

        if shred_due:
            found_any = True
            print(f" - {fname} {lname} (ID: {pid}): {reason}")
            cursor.execute("UPDATE patients SET is_active = FALSE WHERE id = %s", (pid,))

    if not found_any:
        print(" - No patients currently eligible.")

    conn.commit()
    conn.close()