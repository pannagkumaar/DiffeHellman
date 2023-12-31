import socket
import random

def diffie_hellman(prime,base):
    
    private_key = random.randint(2, prime - 2)
    public_key = (base ** private_key) % prime
    return prime, base, private_key, public_key

def calculate_shared_secret_key(public_key, private_key, prime):
    return (public_key ** private_key) % prime

def encrypt_string(string, key):
    encrypted_string = ""
    for char in string:
        encrypted_char = chr(ord(char) + key)
        encrypted_string += encrypted_char
    return encrypted_string

def client():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket()
    s.connect((host, port))
    s_prime = int(s.recv(1024).decode())
    s_base = int(s.recv(1024).decode())
    print("Received prime:", s_prime)
    print("Received base:", s_base)
    prime, base, private_key, public_key = diffie_hellman(s_prime,s_base)

    s.send(str(public_key).encode())
    server_public_key = int(s.recv(1024).decode())

    shared_secret_key = calculate_shared_secret_key(server_public_key, private_key, prime)
    print("Shared Secret Key:", shared_secret_key)

    # Sending encrypted string to the server
    string_to_send = "Hello, server!Hello, server!Hello, server!Hello, server!Hello, server!Hello, server!Hello, server!Hello, server!Hello, server!Hello, server!"
    encrypted_string = encrypt_string(string_to_send, shared_secret_key)
    s.send(encrypted_string.encode())

    s.close()

if __name__ == "__main__":
    client()
