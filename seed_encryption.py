import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import random
def aes_encrypt(seed, key, iv):
    aes_key = generate_ase_key(key)  
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    return cipher.encryptor().update(seed.to_bytes(4, 'big'))

def aes_decrypt(encrypted_seed, key, iv):
    aes_key = generate_ase_key(key)  
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    return int.from_bytes(cipher.decryptor().update(encrypted_seed), 'big')

# def hmac_sha256(key, message):
#     print("hello")
#     digest = hmac.n   ew(key.to_bytes(32, 'big'), message, hashlib.sha256).digest()
#     print(f"[HMAC] Generated HMAC: {digest.hex()}")
#     return digest


def hmac_sha256(key, message):
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    digest = hmac.new(key_bytes, message, hashlib.sha256).digest()
    print(f"[HMAC] Generated HMAC: {digest.hex()}")
    return digest


def verify_hmac(key, message, received_hmac):
    calculated_hmac = hmac_sha256(key, message)
    if hmac.compare_digest(calculated_hmac, received_hmac):
        print("[HMAC] HMAC verification successful.")
        return True
    else:
        print("[HMAC] HMAC verification failed.")
        return False
    

def generate_seed():
    return random.randint(0, 2**32 - 1)
def generate_iv():  
    return random.randbytes(16)

# def generate_ase_key(shared_key):
#     return shared_key.to_bytes(16, 'big')[:16]

import hashlib

def generate_ase_key(shared_key):
    # Convert the integer to bytes (large enough to hold any size)
    shared_key_bytes = shared_key.to_bytes((shared_key.bit_length() + 7) // 8, 'big')
    # Use SHA-256 and truncate to 16 bytes (128 bits)
    print(f"[AES Key] Generated AES key: {shared_key_bytes.hex()}")
    return hashlib.sha256(shared_key_bytes).digest()[:16]

