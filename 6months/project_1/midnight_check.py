#!/usr/bin/env python3

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from db import connect_db

# === Constants ===
DECEASED_YEARS = 3
INACTIVITY_YEARS = 7
GRACE_DAYS = 1  # extra day added after threshold
TIMEZONE = 'US/Eastern'

# === Main Function ===
def run_nightly_reminder_check():
    """
    Runs an automated nightly reminder check:
    - Flags patients whose records meet shredding criteria
    - Updates database
    - Writes reminders to a text file
    """
    eastern = pytz.timezone(TIMEZONE)
    now = datetime.now(eastern)
    today = now.date()
    reminder_lines = []
    filename = f"reminders_{today.strftime('%Y%m%d')}.txt"

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, last_visit, death_date FROM patients WHERE is_active = 1")
        patients = cursor.fetchall()

        for pid, fname, lname, last_visit, death_date in patients:
            shred_due = False
            reason = ""

            if death_date:
                cutoff = datetime.strptime(death_date, "%Y-%m-%d").date() + relativedelta(years=DECEASED_YEARS, days=GRACE_DAYS)
                if today >= cutoff:
                    shred_due = True
                    reason = f"{DECEASED_YEARS} years + {GRACE_DAYS} day(s) since death on {death_date}"
            elif last_visit:
                cutoff = datetime.strptime(last_visit, "%Y-%m-%d").date() + relativedelta(years=INACTIVITY_YEARS, days=GRACE_DAYS)
                if today >= cutoff:
                    shred_due = True
                    reason = f"{INACTIVITY_YEARS} years + {GRACE_DAYS} day(s) since last visit on {last_visit}"

            if shred_due:
                reminder_lines.append(f"{fname} {lname} (ID: {pid}) - {reason}")
                cursor.execute("UPDATE patients SET is_active = 0 WHERE id = ?", (pid,))

        conn.commit()

    except Exception as e:
        print(f"❌ Database error occurred: {e}")
    else:
        if reminder_lines:
            try:
                with open(filename, "w") as f:
                    f.write("Patient Shredding Reminders (Eastern Time)\n")
                    f.write(f"Date: {today}\n\n")
                    for line in reminder_lines:
                        f.write(f"{line}\n")
                print(f"✅ {len(reminder_lines)} reminders written to {filename}")
            except Exception as file_err:
                print(f"❌ File writing failed: {file_err}")
        else:
            print("✅ No patients to be marked inactive today.")
    finally:
        if 'conn' in locals():
            conn.close()

# Run if executed directly
if __name__ == "__main__":
    run_nightly_reminder_check()
