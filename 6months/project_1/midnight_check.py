from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import os
from db import connect_db
from config import output_directory

# === Constants ===
DECEASED_YEARS = 3
INACTIVITY_YEARS = 7
GRACE_DAYS = 1
TIMEZONE = 'US/Eastern'

def run_nightly_reminder_check():
    """
    Runs an automated nightly reminder check:
    - Flags patients whose records meet shredding criteria
    - Updates database
    - Writes reminders to a uniquely named text file
    Returns:
        (count, filepath): tuple of number of reminders and file path
    """
    eastern = pytz.timezone(TIMEZONE)
    now = datetime.now(eastern)
    today = now.date()
    timestamp = now.strftime("%Y%m%d_%H%M")
    filename = os.path.join(output_directory, f"reminders_{timestamp}.txt")
    reminder_lines = []

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, last_visit, death_date FROM patients WHERE is_active = 1")
        patients = cursor.fetchall()

        for pid, fname, lname, last_visit, death_date in patients:
            shred_due = False
            reason = ""

            if death_date and isinstance(death_date, str) and death_date.strip():
                try:
                    parsed_death = datetime.strptime(death_date.strip(), "%Y-%m-%d").date()
                    cutoff = parsed_death + relativedelta(years=DECEASED_YEARS, days=GRACE_DAYS)
                    if today >= cutoff:
                        shred_due = True
                        reason = f"{DECEASED_YEARS} years + {GRACE_DAYS} day(s) since death on {death_date}"
                except Exception as e:
                    print(f"⚠️ Skipped patient ID {pid} due to bad death_date: {death_date} ({e})")

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
        return 0, None
    else:
        if reminder_lines:
            try:
                with open(filename, "w") as f:
                    f.write("Patient Shredding Reminders (Eastern Time)\n")
                    f.write(f"Date: {today}\n\n")
                    for line in reminder_lines:
                        f.write(f"{line}\n")

                print(f"✅ {len(reminder_lines)} reminders written to {filename}")
                return len(reminder_lines), filename
            except Exception as file_err:
                print(f"❌ File writing failed: {file_err}")
                return 0, None
        else:
            print("✅ No patients to be marked inactive today.")
            return 0, None
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_nightly_reminder_check()
