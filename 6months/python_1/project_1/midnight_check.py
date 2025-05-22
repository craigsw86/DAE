#!/usr/bin/env python3

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from db import connect_db

today = datetime(2025, 5, 23)

# Runs a nightly check of active patients to determine if physical files should be shredded.
# It checks if the patient has died (3+ years ago) or not visited in 7+ years.
# It moves qualifying patients to inactive and writes reminders to a file.
def run_nightly_reminder_check():
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern)
    today = now.date()

    reminder_lines = []
    filename = f"reminders_{today.strftime('%Y%m%d')}.txt"

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, first_name, last_name, last_visit, death_date FROM patients WHERE is_active = 1")
    patients = cursor.fetchall()

    for pid, fname, lname, last_visit, death_date in patients:
        shred_due = False
        reason = ""

        if death_date:
            cutoff = datetime.strptime(death_date, "%Y-%m-%d").date() + relativedelta(years=3, days=1)
            if today >= cutoff:
                shred_due = True
                reason = f"3 years + 1 day since death on {death_date}"
        elif last_visit:
            cutoff = datetime.strptime(last_visit, "%Y-%m-%d").date() + relativedelta(years=7, days=1)
            if today >= cutoff:
                shred_due = True
                reason = f"7 years + 1 day since last visit on {last_visit}"

        if shred_due:
            reminder_lines.append(f"{fname} {lname} (ID: {pid}) - {reason}")
            cursor.execute("UPDATE patients SET is_active = 0 WHERE id = ?", (pid,))

    conn.commit()
    conn.close()

    if reminder_lines:
        with open(filename, "w") as f:
            f.write("Patient Shredding Reminders (Eastern Time)\n")
            f.write(f"Date: {today}\n\n")
            for line in reminder_lines:
                f.write(f"{line}\n")
        print(f"✅ {len(reminder_lines)} reminders written to {filename}")
    else:
        print("✅ No patients to be marked inactive today.")

# Ensures the function runs only when this script is executed directly
if __name__ == "__main__":
    run_nightly_reminder_check()
