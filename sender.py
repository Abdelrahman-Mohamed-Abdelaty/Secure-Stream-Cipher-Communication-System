import socket
from key_exchange import perform_key_exchange
from seed_encryption import *
from lcg_module import LCG
from stream_cipher import encrypt
import socket
import os
from dotenv import load_dotenv


class Sender:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Sender server started. Waiting for connections...")
        
    def send_seed(self, conn, seed,shared_key):
        iv = generate_iv()
        encrypted_seed = aes_encrypt(seed, shared_key, iv)
        seed_hmac = hmac_sha256(shared_key, encrypted_seed)

        conn.sendall(iv)
        conn.sendall(encrypted_seed)
        conn.sendall(seed_hmac)
    
    def send_messages(self, conn, seed):
        lcg = LCG(seed)
        with open("plaintext.txt", "rb") as file:
                while True:
                    chunk = file.read(10)
                    if not chunk:
                        break
                    print(f"current seed: {lcg.seed}")
                    ciphertext = encrypt(chunk, lcg)
                    conn.sendall(ciphertext)
                    print(f"Sender: Sent chunk: {chunk}")
                    
    def handle_connection(self, conn, addr):
        print(f"\nSender: New connection from {addr}")
        with conn:
            # Diffie-Hellman key exchange
            shared_key = perform_key_exchange(conn)
            # Generate and encrypt seed
            seed = generate_seed()    
            self.send_seed(conn, seed,shared_key)
            self.send_messages(conn, seed)
            print("Sender: Messages sent successfully.")

    def run(self):
        try:
            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    self.handle_connection(conn, addr)
                except ConnectionResetError:
                    print("Sender: Client disconnected unexpectedly")
                except ValueError as e:
                    print(f"Sender: Protocol error - {e}")
                except Exception as e:
                    print(f"Sender: Unexpected error - {e}")
                finally:
                    print("Sender: Ready for new connection...")
        except KeyboardInterrupt:
            print("\nSender: Shutting down server...")
        finally:
            self.server_socket.close()
            print("Sender: Server closed")

load_dotenv()
host = os.getenv("HOST")
port = int(os.getenv("PORT"))
print(f"Sender: Host: {host}, Port: {port}")


if __name__ == "__main__":
    sender_instance = Sender(host,port)
    sender_instance.run()
