from db import insert_patient
from datetime import date

fake_patients = [
    ("Alice", "Johnson", date(2015, 6, 10), None, True),
    ("Bob", "Smith", date(2014, 9, 23), date(2019, 3, 1), True),
    ("Carla", "Lopez", date(2022, 1, 15), None, True),
    ("David", "Kim", date(2010, 7, 30), date(2012, 5, 10), True),
    ("Ella", "Patel", date(2017, 10, 4), None, True),
    ("Frank", "Nguyen", date(2013, 12, 19), None, True),
    ("Grace", "White", date(2020, 11, 22), date(2021, 8, 5), True),
    ("Henry", "Lee", date(2016, 4, 5), None, True),
    ("Ivy", "Brown", date(2018, 3, 14), None, True),
    ("Jack", "Garcia", date(2019, 6, 29), date(2022, 6, 30), True),
    ("Kara", "Wright", date(2011, 8, 9), None, True),
    ("Liam", "Martinez", date(2015, 5, 17), date(2016, 9, 21), True),
]

for first, last, last_visit, death_date, active in fake_patients:
    insert_patient(first, last, last_visit, death_date, active)
    print(f" Added {first} {last}")

