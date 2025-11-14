"""
    A simple script to understand the caesar cipher and learn python.
    If desiring to decrypt a message one can comment out the encrypted
    variable and enter their own ciphertext.

    This script takes each character and rotates them based on the key for
    their own character type (e.g. uppercase, lowercase, numbers).
    
    There may be an issue if the encryption method of your own ciphertext utilizes
    a different method, like stacking the ASCII alphanumeric characters into one
    rotation table. This is important to consider and can be seen if there are a mixture
    of numbers and letters (uppercase and lowercase) throughout the text. This script
    does not account for those variations.

    That variation can be found in my caesar-special.py script
"""

# Example usage:
message = 'hello123'
key = 58
# If message includes numbers
numbers = True

def encrypt(message, key, include_numbers=False):
    result = ''

    for char in message:
        if char.isupper():
            # Encrypt uppercase letters (A–Z)
            result += chr((ord(char) - 65 + key) % 26 + 65)
        elif char.islower():
            # Encrypt lowercase letters (a–z)
            result += chr((ord(char) - 97 + key) % 26 + 97)
        elif include_numbers and char.isdigit():
            # Encrypt numbers (0–9)
            result += chr((ord(char) - 48 + key) % 10 + 48)
        else:
            # Leave non-alphabetic (and non-numeric if disabled) characters as-is
            result += char
    return result

def decrypt(encryption, key, include_numbers=False):
    """Decrypt by reversing the Caesar shift."""
    # To decrypt, shift by (alphabet_size - key)
    return encrypt(encryption, -key, include_numbers)

# Encrypt & Decrypt with numbers enabled
encrypted = encrypt(message, key, include_numbers=numbers) # comment out if wanting to decrypt personal ciphertext
#encrypted = 'uryyb678' # key of 65 to decrypt
decrypted = decrypt(encrypted, key, include_numbers=numbers)

print("Original :", message)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
