
import socket
from key_exchange import perform_key_exchange
from seed_encryption import *
from lcg_module import LCG
from stream_cipher import decrypt
from dotenv import load_dotenv
import os
class Receiver:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.shared_key = None
        self.lcg = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print("Receiver: Connected to sender.")

    def establish_shared_key(self):
        self.shared_key = perform_key_exchange(self.socket)
        print("Receiver: Shared key established.", self.shared_key)

    def receive_and_verify_seed(self):
        iv = self.socket.recv(16)
        encrypted_seed = self.socket.recv(4)
        received_hmac = self.socket.recv(32)

        if not verify_hmac(self.shared_key, encrypted_seed, received_hmac):
            self.socket.close()
            raise ValueError("HMAC verification failed.")

        seed = aes_decrypt(encrypted_seed, self.shared_key, iv)
        print(f"Receiver: Seed received and verified: {seed}")
        self.lcg = LCG(seed)

    def receive_message(self, output_file="output.txt"):
        with open(output_file, "ab") as f:
            while True:
                ciphertext = self.socket.recv(10)
                if not ciphertext:
                    break
                plaintext = decrypt(ciphertext, self.lcg)
                print("Receiver: Chunk received and verified:", plaintext.decode())
                f.write(plaintext)

    def close(self):
        if self.socket:
            self.socket.close()
        print("Receiver: Connection closed.")

    def run(self):
        try:
            self.connect()
            self.establish_shared_key()
            self.receive_and_verify_seed()
            self.receive_message()
        finally:
            self.close()




if __name__ == "__main__":
    load_dotenv()
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    print(f"Sender: Host: {host}, Port: {port}")
    receiver = Receiver()
    receiver.run()
    print("Receiver: Finished processing.")
