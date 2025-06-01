def xor_operation(data, keystream):
    result = bytes([a ^ b for a, b in zip(data, keystream)])
    print(f"[StreamCipher] XOR result: {result}")
    return result

def encrypt(data, lcg):
    keystream = lcg.generate_keystream(len(data))
    return xor_operation(data, keystream)

def decrypt(ciphertext, lcg):
    return encrypt(ciphertext, lcg)  