import tkinter as tk

def is_prime(n):
    if n <= 1:
        return False # 0 and 1 are not prime numbers
    if n == 2:
        return True #2 is the only even prime number
    if n % 2 == 0:
        return False # Other even numbers are not prime
    
    # Only check odd divisors up to the square root of n
    for i in range (3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    
    return True

def check_prime():
    try:
        num = int(entry.get())
        if is_prime(num):
            result_label.config(text=f"{num} is a prime number.", fg="green")
        else:
            result_label.config(text=f"{num} is not a prime number.", fg="red")
    except ValueError:
            result_label.config(text="Please enter a valid integer.", fg="orange")
    
    def clear_fields():
        entry.delete(0, tk.END)  # Clear the input field
        result_label.config(text="")  # Clear the result label
    
    # Create the main window
    root = tk.Tk()
    root.title("Prime Number Checker")
    root.geometry("300x220")

    # Input label
    tk.Label(root, text="Enter a number:").pack(pady=10)

    # Entry field
    entry = tk.Entry(root)
    entry.pack()

    # Check button
    check_button = tk.Button(root, text="Check", command=check_prime)
    check_button.pack(pady=5)

    # Clear button
    clear_button = tk.Button(root, text="Clear", commmand=clear_fields)
    clear_button.pack(pady=5)

    # Result label
    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    # Run the application
    root.mainloop()
    