import socket
import random
from prime import primitive_root, getLowLevelPrime, isMillerRabinPassed

def get_prime_and_base():
    while True:
        n = 20
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            base = primitive_root(prime_candidate)
            return prime_candidate, base
def diffie_hellman():
    prime, base = get_prime_and_base()
    private_key = random.randint(2, prime - 2)
    public_key = (base ** private_key) % prime
    return prime, base, private_key, public_key

def calculate_shared_secret_key(public_key, private_key, prime):
    return (public_key ** private_key) % prime

def server():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket()
    s.bind((host, port))
    s.listen(1)

    print("Waiting for incoming connection...")
    conn, addr = s.accept()
    print("Connection from: " + str(addr))

    prime, base, private_key, public_key = diffie_hellman()
    conn.send(str(prime).encode())
    print("Sent prime:", prime)
    conn.send(str(base).encode())
    print("Sent base:", base)
    conn.send(str(public_key).encode())
    client_public_key = int(conn.recv(1024).decode())

    shared_secret_key = calculate_shared_secret_key(client_public_key, private_key, prime)
    print("Shared Secret Key:", shared_secret_key)

    # Receiving encrypted string from the client
    encrypted_string = conn.recv(1024).decode()

    # Decrypt the string using the shared secret key
    decrypted_string = decrypt_string(encrypted_string, shared_secret_key)
    print("Received String:", decrypted_string)

    conn.close()

def decrypt_string(encrypted_string, key):
    decrypted_string = ""
    for char in encrypted_string:
        decrypted_char = chr(ord(char) - key)
        decrypted_string += decrypted_char
    return decrypted_string

if __name__ == "__main__":
    server()
