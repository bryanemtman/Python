# Caesar Cipher – Python Learning Scripts

A pair of Python scripts created to explore and understand the Caesar cipher, character rotation techniques, and basic cryptographic concepts while improving Python fundamentals.

NOTE: These scripts are for educational purposes only and must not be used for real encryption.

## Project Overview

This repository contains two Caesar cipher implementations:

1. Basic Caesar Cipher

    - Rotates characters within separate character classes

    - Uppercase letters, lowercase letters, and numbers each rotate independently

2. Special Caesar Cipher

    - Rotates characters across a combined alphabet

    - Uppercase letters, lowercase letters, and digits are treated as a single rotation set

These implementations highlight how alphabet selection and rotation rules directly affect encryption and decryption behavior.

## Learning Objectives

1. Understand how Caesar ciphers work at the character level

2. Learn how different alphabets impact encryption results

3. Practice Python string handling and ASCII manipulation

4. Compare multiple cipher design approaches

5. Recognize why classical ciphers are cryptographically weak

## Security Disclaimer

### Do NOT use these scripts for protecting real data.

Caesar ciphers are:

- Trivially breakable

- Vulnerable to brute force and frequency analysis

- Insecure regardless of key size

These scripts exist strictly for learning and demonstration purposes.

## Scripts Included

1. Basic Caesar Cipher (Separated Alphabets)

<b>Concept:</b>

Each character type rotates within its own alphabet:

- Uppercase letters: A–Z

- Lowercase letters: a–z

- Numbers: 0–9 (optional)

Characters wrap within their own group and never mix with others.

<b>Key Characteristics</b>

- Alphabet groups are rotated independently

- Numbers are optional (include_numbers=True)

- Non-alphanumeric characters remain unchanged

- Compatible with many traditional Caesar cipher implementations

Example
```
Input:  hello123
Key:    58

Output: ebiil123
```

Letters rotate modulo 26, numbers rotate modulo 10.

2. Special Caesar Cipher (Combined Alphabet)

<b>Concept:</b>

All characters rotate using one combined alphabet:
```
A–Z + a–z + 0–9
```

This produces different results from the basic cipher because characters can rotate into different character types.

<b>Key Characteristics</b>

- Single rotation table for all alphanumeric characters

- Uppercase, lowercase, and digits are treated equally

- Rotation wraps around the entire combined alphabet

- Better demonstrates why alphabet design matters
```
Example Alphabet
['A'..'Z', 'a'..'z', '0'..'9']
```
Example
```
Input:  joinUSinThEfIghTat1200
Key:    5

Output: otnsZXnsYmJkNlmYfy6755
```
## Important Notes on Compatibility

If decrypting external ciphertext:

- The encryption method must match the alphabet model

- Ciphertexts generated using separated alphabets will not decrypt correctly using the combined-alphabet script

- Mixed uppercase/lowercase/numeric groupings in ciphertext can reveal which rotation method was used

This difference is intentional and serves as a learning point.

## Usage
Run the Script
```python3 caesar.py```

or

```python3 caesar-special.py```

### Encrypt a Custom Message

- Modify the message and key variables

- Comment/uncomment the provided ciphertext examples as needed

Example Output
```
Original : hello123
Encrypted: ebiil678
Decrypted: hello123
```
```
Alphabet: ['A', 'B', ..., '9']
Original : joinUSinThEfIghTat1200
Encrypted: H98A9W_H6UM8W_6A_9_D6C_5ZCI9C8I_D9FF6IFD
Decrypted: joinUSinThEfIghTat1200
```
## Key Takeaways

1. Alphabet design matters in encryption

2. Caesar ciphers are predictable and weak

3. Character classification affects cipher output

4. Classical ciphers help build intuition for modern cryptography

## Future Improvements

- Add brute-force attack demonstration

- Add frequency analysis visualization

- Add CLI argument support

- Compare Caesar vs Vigenère cipher

- Extend to Unicode handling

## License / Usage

This project is provided for educational use only.
Feel free to study, modify, and experiment—but do not rely on this code for security.
