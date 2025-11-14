"""
    A simple script to understand the caesar cipher and learn python.
    If desiring to decrypt a message one can comment out the encrypted
    variable and enter their own ciphertext.

    This script takes each character (e.g. uppercase, lowercase, numbers)
    and rotates them based on the key as one alphabet.
    
    There may be an issue if the encryption method of your own ciphertext utilizes
    a different method, like seperating the ASCII alphanumeric characters into multiple
    rotation alphabet tables. This is important to consider and can be seen if there
    are similar numbers and letters (uppercase and lowercase) groupings throughout the
    text. This script does not account for those variations.

    That variation can be found in my caesar-cipher.py script
"""

# Example usage:
message = 'joinUSinThEfIghTat1200'
key = 5

# Create alphabet: A–Z + a-z + 0–9
alphabet = []

for upper in range(65,91):
    alphabet.append(chr(upper))
for lower in range(97, 123):
    alphabet.append(chr(lower))
for num in range(48,58):
    alphabet.append(chr(num))


def encrypt(message, key):
    result = ''
    size = len(alphabet)
    for char in message:
        if char.isupper() or char.islower() or char.isdigit():
            # Find the character's position in the alphabet
            index = alphabet.index(char)
            # Shift forward using modulo to wrap around properly
            new_index = (index + key) % size
            result += alphabet[new_index]
        else:
            # Leave non-alphabetic characters unchanged
            result += char
    return result


def decrypt(encryption, key):
    """Decrypt by shifting backward."""
    return encrypt(encryption, -key)

"""
    H98A9W_H6UM8W_6A_9_D6C_5ZCI9C8I_D9FF6IFD (key of 5)
    C4354R_C1PH3R_15_4_817_0U7D473D_84AA1DA8 -> CAESAR_CIPHER_IS_A_BIT_OUTDATED_<HEX>
"""
# Encrypt & Decrypt with numbers enabled
encrypted = encrypt(message, key) # comment out for personal message
#encrypted = 'H98A9W_H6UM8W_6A_9_D6C_5ZCI9C8I_D9FF6IFD' # From HTB CTF box (change to personal ciphertext)
decrypted = decrypt(encrypted, key)

print("Alphabet:", alphabet) # For demonstration purposes, to show what the alphabet is being rotated off of
print("Original :", message)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
