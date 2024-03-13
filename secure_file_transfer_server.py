import json
import random
import blowfish as bf
import socket
import os
import time

def gen_homo_key():
    letter_values={'A': 60, 'B': 11, 'C': 21, 'D': 31, 'E': 91, 'F': 17, 'G': 15, 'H': 45, 'I': 51, 'J': 1, 'K': 6, 'L': 31, 'M': 18, 'N': 50, 'O': 55, 'P': 15, 'Q': 1, 'R': 42, 'S': 45, 'T': 65, 'U': 21, 'V': 7, 'W': 18, 'X': 1, 'Y': 15, 'Z': 1, ' ': 128, '!': 2, '"': 8, '#': 1, '$': 1, '%': 1, '&': 1, "'": 10, '(': 5, ')': 5, '*': 1, '+': 1, ',': 14, '-': 15, '.': 21, '/': 1, ':': 4, ';': 4, '<': 1, '=': 1, '>': 1, '?': 2, '@': 1, '[': 1, '\\': 1, ']': 1, '^': 1, '_': 1, '`': 7, '{': 1, '|': 1, '}': 1, '~': 1,'1':2,'2':2,'3':2,'4':2,'5':2,'6':2,'7':2,'8':2,'9':2,'0':2,'\n':1}

    all_unique_numbers = [f"{i:03}" for i in range(1000)]

    encryptkey = {}

    for key, value in letter_values.items():
        if value > len(all_unique_numbers):
            raise ValueError("Not enough unique numbers available")
        random_numbers = random.sample(all_unique_numbers, value)
        encryptkey[key] = random_numbers
        for number in random_numbers:
            all_unique_numbers.remove(number)

    serialized_dict = json.dumps(encryptkey)

    enc=bf.encrypt(serialized_dict)
    
    return enc,encryptkey

def encrypt_homophonic(text,encryptkey):
    encrypted_text = ""
    for char in text.upper():
        if char in encryptkey:
            substitutions = encryptkey[char]
            random_substitution = random.choice(substitutions)
            encrypted_text += random_substitution
    return encrypted_text


def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    
    if request == 'REQUEST_FILE':
        filename = client_socket.recv(1024).decode()
        
        enc,encryptkey=gen_homo_key()

        
        client_socket.send(enc)
        
        if filename.endswith('.txt') and os.path.exists(filename):
            with open(filename, 'r') as file:
                file_data = file.read()
            
            encfile=encrypt_homophonic(file_data,encryptkey)
            client_socket.send(encfile.encode())
            
        elif not filename.endswith('.txt'):
            client_socket.send("Incorrect File Format".encode())
        else:
            client_socket.send("Requested File Not Found".encode())
            
    client_socket.close()




SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12347

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(5)
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")
    handle_client(client_socket)

