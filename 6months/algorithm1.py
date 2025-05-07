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
