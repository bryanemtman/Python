# Diffie-Hellman Key Exchange (DHKE) – Proof of Concept

A Python-based educational simulation of the Diffie-Hellman Key Exchange (DHKE) process.
This project was built as a learning exercise to strengthen understanding of cryptographic key exchange, modular arithmetic, and Python fundamentals.

NOTE: This implementation is NOT secure and must NOT be used for real encryption.

## Purpose & Learning Goals

This script was designed to:

- Understand how symmetric keys can be securely derived over an insecure channel

- Learn the mathematics behind:

  - Prime numbers

  - Primitive roots (generators)

  - Modular exponentiation

- Practice implementing cryptographic concepts from scratch

- Improve Python problem-solving and algorithmic thinking

This project intentionally avoids third-party cryptography libraries to expose the underlying mechanics of DHKE.

## What This Script Demonstrates

- Random prime number generation

- Primitive root (generator g) discovery

- Public/private key generation

- Shared secret derivation

- Verification that both parties compute the same symmetric key

## High-Level Flow

1. Generate a shared prime p

2. Find a primitive root g modulo p

3. Each party selects a private secret

4. Public values are exchanged

5. A shared secret key is independently computed

6. Keys are verified to match

## Security Disclaimer (Important)

### DO NOT USE THIS SCRIPT FOR REAL SECURITY PURPOSES

Reasons this implementation is insecure:

- Uses small random primes

- Uses Python’s random module (not cryptographically secure)

- Implements classic Diffie-Hellman, which is vulnerable to:

  - Man-in-the-middle attacks

  - Logjam-style attacks

  - Parameter manipulation

- No authentication

- No key derivation function (KDF)

- No forward secrecy guarantees

This script exists purely for educational and demonstration purposes.

## Additional Warnings

- Random primes and integers are not safe for cryptographic use

- No protection against active attackers

- No integrity or authentication mechanisms

- No real-world cryptographic hygiene

## Requirements

- Python 3.x

- Standard library only (random, math)

No external packages required.

## Usage

Run the script directly:

```python3 diffie-hellman.py```

The script will:

1. Generate parameters

2. Simulate both parties (A and B)

3. Print values in a readable, aligned format

4. Verify that the shared secret matches

## Example Output (Simplified)
```
Shared Prime (p): 7919       Primitive Root (g): 10

Private Secret A: 4821      Private Secret B: 9012

Public Value A: 1234        Public Value B: 5678

Shared Secret Key A: 4321   Shared Secret Key B: 4321

Key exchange successful! Both keys match.
```
## Key Concepts Covered

- Modular arithmetic

- Prime checking

- Primitive roots modulo prime

- Public-key cryptography fundamentals

- Why key exchange ≠ encryption

- Why modern cryptography avoids rolling your own crypto

## Recommended Secure Alternatives

For real-world applications, use:

- Elliptic-Curve Diffie-Hellman (ECDH)

- Well-established libraries such as:

  - cryptography

  - OpenSSL-backed implementations

- Authenticated key exchange protocols

- Proper key derivation functions (HKDF)

ECDH provides:

- Smaller keys

- Better performance

- Stronger security guarantees

## Educational Takeaway

This project demonstrates how Diffie-Hellman works, not how it should be used in production.
Understanding these mechanics helps explain why modern cryptography looks the way it does and why abstraction through vetted libraries is essential.

## License / Usage

This project is provided for learning and educational purposes only.
Feel free to study, modify, and experiment—but do not deploy in any security-sensitive environment.
