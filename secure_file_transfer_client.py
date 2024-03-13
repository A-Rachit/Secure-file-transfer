import json
import random
import blowfish as bf
import socket
import os
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12347

def decrypt_homophonic(text,encryptkey):
    decryptkey = {number: letter for letter, numbers in encryptkey.items() for number in numbers}
    decrypted_text = ""
    for i in range(0,len(text),3):
        if text[i]+text[i+1]+text[i+2] in decryptkey:
            decrypted_text += decryptkey[text[i]+text[i+1]+text[i+2]]
    return decrypted_text

def request_file():
    client_socket=socket.socket()
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server")
    
    client_socket.send("REQUEST_FILE".encode())
    filename=str(input("input file name: "))
    client_socket.send(filename.encode())
    
    #enck= client_socket.recv(1048576)
    enck= client_socket.recv(64000)
    
    tkey=bf.decrypt(enck)
    
    enckey=json.loads(bf.decrypt(enck))
    
    #result=client_socket.recv(1048576).decode()
    result=client_socket.recv(512).decode()
    
    if result == "Requested File Not Found":
        print("Error: Requested File Not Found")
    elif result == "Incorrect File Format":
        print("Error: Incorrect File Format")
    else:
        content=decrypt_homophonic(result,enckey)
        with open(filename, 'w') as file:
            file.write(content)
        file.close()
        print(f"File '{filename}' received successfully.")
    
    client_socket.close()

if __name__ == '__main__':
    request_file()



