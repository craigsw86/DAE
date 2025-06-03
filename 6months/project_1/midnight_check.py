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

            # === Deceased Case ===
            if death_date and isinstance(death_date, str) and death_date.strip():
                try:
                    parsed_death = datetime.strptime(death_date.strip(), "%Y-%m-%d").date()
                    cutoff = parsed_death + relativedelta(years=DECEASED_YEARS, days=GRACE_DAYS)
                    if today >= cutoff:
                        shred_due = True
                        reason = f"{DECEASED_YEARS} years + {GRACE_DAYS} day(s) since death on {death_date}"
                except Exception as e:
                    print(f"⚠️ Skipped patient ID {pid} due to bad death_date: {death_date} ({e})")

            # === Inactivity Case ===
            elif last_visit and isinstance(last_visit, str) and last_visit.strip():
                try:
                    parsed_visit = datetime.strptime(last_visit.strip(), "%Y-%m-%d").date()
                    cutoff = parsed_visit + relativedelta(years=INACTIVITY_YEARS, days=GRACE_DAYS)
                    if today >= cutoff:
                        shred_due = True
                        reason = f"{INACTIVITY_YEARS} years + {GRACE_DAYS} day(s) since last visit on {last_visit}"
                except Exception as e:
                    print(f"⚠️ Skipped patient ID {pid} due to bad last_visit: {last_visit} ({e})")

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
                return len(reminder_lines)
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
