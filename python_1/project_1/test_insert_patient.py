from db import insert_patient
from datetime import date

# Add a patient who qualifies by last visit (7+ years ago)
insert_patient("Test", "OldVisit", date(2015, 5, 1))

# Add a patient who qualifies by death (3+ years ago)
insert_patient("Test", "DeadGuy", date(2012, 1, 1), death_date=date(2020, 3, 1))

print("✅ Test patients inserted.")
