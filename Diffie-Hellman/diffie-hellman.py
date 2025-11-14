"""
    This was a learning process and with many failed attempts.
    Designed to be a learning tool for the Diffie-Hellman Key Exchange (DHKE) process.
    I attempted to create a simple script to challenge my Python skills.
    While also increase my understanding of how symmetric cryptographic keys are
    securely shared/created over an insecure channel.
    Do not use to encrypt data, the original DHKE is not secure and has many holes.

    WARNING!
    Not advised to use random primes and integers.
    This is just for demonstration purposes and without 3rd party packages and modules
    Should use the Elliptic-Curve Diffie-Hellman (ECDH).
    Use of ECDH allows for a more consistant and secure key exchange process when
    combined with other key generation formulas.
    WARNING!
"""

import random
import math


min_Prime = 3000
max_Prime = 10000

min_Integer = 3000
max_Integer = 10000


# -------------------------------
# 1. Prime Number Utilities
# -------------------------------

def checkPrime(number):
    """
    Check if a number is prime.
    """
    # Checks even numbers
    # The if statements check if the number is less than 2, equal to 2 (prime), or a is even.
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    
    # Checks odd numbers
    # Check odd divisors up to sqrt(number)
    for i in range(3, int(math.sqrt(number)) + 1, 2): # loops through all odd numbers up to sqrt(number)
        if number % i == 0: # use modulus to find if divisible
            return False
    return True # Returns True if prime


def createInteger(min, max):
    """
    Return a random integer between min and max.
    """
    return random.randint(min, max)


def getPrime(min, max):
    """
    Generate a random prime number within a range.
    """
    while True:
        p = createInteger(min, max) # choose random number
        if checkPrime(p):
            return p # return first found prime


# -------------------------------
# 2. Primitive Root Finder (Generator g)
# -------------------------------

def prime_factors(n):
    """
    Return a set of prime factors of n (used for finding primitive roots).
    """
    factors = set()
    # Factor out 2s
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    # Factor out odd numbers
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.add(i)
            n //= i
    # If remaining n is prime
    if n > 2:
        factors.add(n)
    return factors


def find_primitive_root(p):
    """
    Find a primitive root (g) modulo p.
    For Diffie-Hellman, g must be a number whose powers generate all
    values from 1 to p-1 under mod p.
    """
    if p == 2:
        return 1

    phi = p - 1 # Euler's totient function for prime p
    factors = prime_factors(phi) # prime factors of phi(p)

    # Test successive integers until one satisfies primitive root conditions
    for g in range(2, p):
        if all(pow(g, phi // f, p) != 1 for f in factors):
            return g # Found a valid primitive root

    return None # Should not occur for a valid prime p


# -------------------------------
# 3. Diffie-Hellman Key Exchange Functions
# -------------------------------

def getVerification(g, p, secret):
    """
    Compute the public verification value.
    Formula: A = g^secret mod p
    This is the public key each party shares.
    """
    return pow(g, secret, p) # same as (g ** secret) % p but faster


def getKey(value, secret, p):
    """
    Compute the shared secret key.
    Formula: key = (other_public_value ^ secret) mod p
    Both parties should compute the same key.
    """
    return pow(value, secret, p)


def format_col_len(*args):
 """
 Loop in each argument and find the max length.
 Then add 2 for padding
 """
 col_len = max(len(str(x)) for x in args) + 2
 return col_len


# -------------------------------
# 4. Main Diffie-Hellman Process
# -------------------------------

def main():
    # Step 1: Publicly shared values (p and g)
    shared_Integer_P = getPrime(min_Prime, max_Prime) # large prime modulus
    shared_Integer_G = find_primitive_root(shared_Integer_P) # primitive root
    shared_P = f"Shared Prime (p): {shared_Integer_P}"
    shared_R = f"Primitive Root (g): {shared_Integer_G}"

    # Step 2: Each party (A and B) selects a private secret integer
    integerA = createInteger(min_Integer, max_Integer)
    integerB = createInteger(min_Integer, max_Integer)
    psA = f"Private Secret A: {integerA}"
    psB = f"Private Secret B: {integerB}"

    # Step 3: Each computes their public verification value
    valueA = getVerification(shared_Integer_G, shared_Integer_P, integerA) # g^a mod p
    valueB = getVerification(shared_Integer_G, shared_Integer_P, integerB) # g^b mod p
    pvA = f"Public Value A (sent to B): {valueA}"
    pvB = f"Public Value B (sent to A): {valueB}"

    # Step 4: Both compute the shared secret key using each other's public value
    keyA = getKey(valueB, integerA, shared_Integer_P) # (B^a mod p)
    keyB = getKey(valueA, integerB, shared_Integer_P) # (A^b mod p)
    sskA = f"Shared Secret Key computed by A: {keyA}"
    sskB = f"Shared Secret Key computed by B: {keyB}"
    

    # -------------------------------
    # Allows for formating of the output
    # -------------------------------
    # Send each columns data into function to find needed column width
    col_1_len = format_col_len(psA, pvA, sskA)
    col_2_len = format_col_len(psB, pvB, sskB)
    # Assigning each row and column with 
    values = [
        (shared_P, shared_R),
        (psA, psB),
        (pvA, pvB),
        (sskA, sskB)
    ]
    # Loop through each row in values, printing aligned left with padding from format_col_len()
    for left, right in values:
        print(f"{left:<{col_1_len}}{right:<{col_2_len}}\n")
    

    # Step 5: Verify both keys are identical (they should be!)
    if keyA == keyB:
        print("Key exchange successful! Both keys match.\n")
    else:
        print("Key exchange failed. Keys do not match.\n")

# Run the simulation
main()
