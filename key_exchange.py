import random
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
# Load the environment variables
P = int(os.getenv("P"))
G = int(os.getenv("G"))

# P = 11470978444102577348327721122083763083795425674324648321327803015928721193331030056352559115013587470455248065285195309870167769229937277712823810231141423
# G = 2


# P=23
# G=5

def diffie_hellman_key_exchange():
    private = random.randint(1, P - 1)
    public = pow(G, private, P)
    print(f"[KeyExchange] Private: {private}, Public: {public}")
    return private, public

def generate_shared_key(private_key, other_public_key):
    shared = pow(other_public_key, private_key, P)
    print(f"[KeyExchange] Shared Key: {shared}")
    return shared

def perform_key_exchange(conn):
    # Diffie-Hellman key exchange
    private_key, public_key = diffie_hellman_key_exchange()
    conn.sendall(str(public_key).encode())
    other_public_key = int(conn.recv(1024).decode())
    shared_key = generate_shared_key(private_key, other_public_key)
    print(f"Sender: Shared key established: {shared_key}")
    return shared_key