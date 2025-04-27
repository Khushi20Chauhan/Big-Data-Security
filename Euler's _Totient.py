import math

def gcd(a, b):
    """Compute GCD using Euclid's algorithm."""
    while b:
        a, b = b, a % b
    return a

def euler_totient(n):
    """Compute φ(n) using prime factorization (Fast for single numbers)."""
    if n < 1:
        return 0
    result = n
    # Check divisibility by 2
    if n % 2 == 0:
        result -= result // 2
        while n % 2 == 0:
            n //= 2
    # Check odd divisors
    p = 3
    while p * p <= n:
        if n % p == 0:
            result -= result // p
            while n % p == 0:
                n //= p
        p += 2
    # Handle remaining prime factor
    if n > 1:
        result -= result // n
    return result

def euler_totient_sieve(max_n):
    """Precompute φ(n) for all numbers from 1 to max_n using sieve."""
    phi = list(range(max_n + 1))
    for p in range(2, max_n + 1):
        if phi[p] == p:  # p is prime
            phi[p] = p - 1
            for multiple in range(2 * p, max_n + 1, p):
                phi[multiple] -= phi[multiple] // p
    return phi

def verify_totient(n):
    """Verify φ(n) by counting coprimes (Slow but accurate)."""
    count = 0
    for k in range(1, n + 1):
        if gcd(n, k) == 1:
            count += 1
    return count

def show_menu():
    """Display the menu options."""
    print("\nEuler's Totient Function Calculator")
    print("1. Calculate φ(n) for a single number ")
    print("2. Calculate φ(n) for a range of numbers ")
    print("3. Verify φ(n) by counting coprimes ")
    print("4. Exit")

def get_range_input():
    """Handle range input with proper validation."""
    while True:
        try:
            print("\nEnter the range as two numbers (start and end).")
            start = int(input("Start (≥1): "))
            end = int(input("End (≥start): "))
            if start < 1 or end < start:
                print("Error: Start must be ≥1 and end must be ≥start.")
                continue
            return start, end
        except ValueError:
            print("Invalid input. Please enter integers.")

def main():
    """Main program loop with robust input handling."""
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':  # Single number
            try:
                n = int(input("\nEnter a positive integer: "))
                if n < 1:
                    raise ValueError
                print(f"φ({n}) = {euler_totient(n)}")
            except ValueError:
                print("Invalid input. Please enter a positive integer.")
        # Range calculation
        elif choice == '2':  
            start, end = get_range_input()
            print(f"\nCalculating φ(n) from {start} to {end}...")
            phi_list = euler_totient_sieve(end)
            for i in range(start, end + 1):
                print(f"φ({i}) = {phi_list[i]}")
        # Verification option
        elif choice == '3':  
            try:
                n = int(input("\nEnter n (warning: slow for n > 10,000): "))
                if n < 1:
                    raise ValueError
                fast = euler_totient(n)
                slow = verify_totient(n)
                print(f"φ({n}) (fast method) = {fast}")
                print(f"φ({n}) (slow count)  = {slow}")
                print("✓ Match!" if fast == slow else "✗ Mismatch!")
            except ValueError:
                print("Invalid input. Please enter a positive integer.")
         # Exit option
        elif choice == '4': 
            print("\nExiting the program...")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()