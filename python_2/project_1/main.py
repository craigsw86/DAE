from view_patients import view_patients
from midnight_check import run_nightly_reminder_check
from send_reminder_alert import send_reminder_alert

def main_menu():
    """
    Interactive CLI menu for running patient system operations.
    """
    while True:
        print("\n==== Patient File Manager ====")
        print("1. View Active Patients")
        print("2. Run Midnight Reminder Check")
        print("3. Send Reminder Alert")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            view_patients()
        elif choice == "2":
            run_nightly_reminder_check()
        elif choice == "3":
            send_reminder_alert()
        elif choice == "4":
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
