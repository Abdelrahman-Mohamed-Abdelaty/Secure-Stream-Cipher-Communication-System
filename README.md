# Secure Stream Cipher Communication System

This project implements a **secure communication system** using a **stream cipher** based on a **Linear Congruential Generator (LCG)**. It includes cryptographic mechanisms such as **AES encryption**, **HMAC verification**, and **Diffie-Hellman key exchange** to ensure confidentiality and integrity of messages exchanged over TCP.

---

## Features

* Reliable data transmission over TCP sockets
* Secure key exchange using Diffie-Hellman
* AES-encrypted seed sharing with CBC mode
* Seed integrity validation using HMAC-SHA256
* Lightweight stream cipher using XOR + LCG

---

## Design Overview

### 1. Communication Protocol

* **Protocol**: TCP/IP
* **Reason**: Ensures reliable, ordered, and error-checked delivery—critical for cryptographic communication.

### 2. Key Exchange

* **Algorithm**: Diffie-Hellman (DH)
* **Purpose**: Establishes a shared secret key over an insecure channel without transmitting the key itself.

### 3. Seed Encryption

* **Algorithm**: AES (CBC mode)
* **IV**: Random 16-byte initialization vector generated with `os.urandom`

### 4. Seed Integrity

* **Verification**: HMAC-SHA256
* **Purpose**: Confirms that the encrypted seed has not been modified in transit.

### 5. Stream Cipher

* **Method**: Linear Congruential Generator (LCG)
* **Usage**: Produces a pseudorandom keystream used for XOR-based encryption and decryption.

---

## Module Details

### Sender Class

* Listens on a TCP socket for incoming connections
* Performs Diffie-Hellman key exchange
* Generates, encrypts, and signs a seed
* Sends encrypted seed, IV, and HMAC to receiver
* Uses LCG to generate a keystream and encrypts data from `plaintext.txt`

### Receiver Class

* Connects to the sender over TCP
* Completes Diffie-Hellman key exchange
* Verifies and decrypts the received seed
* Initializes LCG and decrypts message chunks into `output.txt`

### LCG Class

* Implements:

  ```
  next = (a * seed + c) % m
  ```

  * `a = 1664525`
  * `c = 1013904223`
  * `m = 2^32`
* Converts output to bytes using modulo 256 for keystream generation

### Key Exchange Module

* Performs private/public key generation
* Exchanging public keys
* Computes the shared secret key using DH algorithm

### Seed Encryption Module

* **AES Encryption/Decryption**: Uses CFB mode
* **HMAC-SHA256**: Ensures seed integrity
* **Key Generation**: Shared key is hashed and truncated to 128 bits for AES
* **IV Generation**: Random 16-byte IV for AES

### Stream Cipher Module

* **XOR Operation**: XORs keystream with data
* **Encrypt/Decrypt**: Uses symmetric XOR operation for both encryption and decryption

---

## Security Features

| Feature                     | Purpose                                  |
| --------------------------- | ---------------------------------------- |
| Diffie-Hellman Key Exchange | Securely establish a shared secret       |
| AES Encryption (CBC)        | Encrypt the seed for secure transmission |
| HMAC-SHA256                 | Validate the integrity of the seed       |
| LCG Stream Cipher           | Lightweight encryption of data chunks    |

---

## Conclusion

This system demonstrates a secure and modular approach to encrypting streaming data between two endpoints. By combining a lightweight stream cipher (LCG) with robust cryptographic primitives for key exchange and seed security, the project achieves a balance between performance and security suitable for academic or instructional use.

---
