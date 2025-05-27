"""
shredder.py

Contains the logic for checking which patient files should be flagged
for shredding based on legal retention rules:
- 3 years since date of death, or
- 7 years since last visit

The function returns reminder messages and updates the database.
"""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pytz
from db import connect_db

def check_shredding_reminders():
    """
    Checks all active patients to determine if their physical files should be shredded.

    A patient is eligible if:
    - They died 3+ years ago, or
    - They last visited 7+ years ago.

    Returns:
    list of str: Reminder messages for patients who now qualify for shredding.
    """
    eastern = pytz.timezone('US/Eastern')
    today = datetime.now(eastern).date()

    reminders = []

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, first_name, last_name, last_visit, death_date FROM patients WHERE is_active = 1")
    patients = cursor.fetchall()

    for patient in patients:
        patient_id, first_name, last_name, last_visit, death_date = patient
        name = f"{first_name} {last_name}"

        if death_date:
            death_date = datetime.strptime(death_date, "%Y-%m-%d").date()
            if today > death_date + relativedelta(years=3):
                reminders.append(f"Shred paper file for {name} - 3 years since death.")
                cursor.execute("UPDATE patients SET active = 0 WHERE id = ?", (patient_id,))
                continue
        
        if last_visit:
            last_visit = datetime.strptime(last_visit, "%Y-%m-%d").date()
            if today > last_visit + relativedelta(years=7):
                reminders.append(f"Shred paper file for {name} - 7 years since last visit.")
                cursor.execute("UPDATE patients SET active = 0 WHERE id = ?", (patient_id,))
    
    conn.commit()
    conn.close()

    return reminders
