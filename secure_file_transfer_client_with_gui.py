import customtkinter as ctk
import tkinter as tk
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
    try:
        client_socket=socket.socket()
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        m="Connected to server \n"
        
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, m)
    
        client_socket.send("REQUEST_FILE".encode())
        filename=input_box.get()
        client_socket.send(filename.encode())
    
        enck= client_socket.recv(64000)
    
        tkey=bf.decrypt(enck)
    
        enckey=json.loads(tkey)
        
        result=client_socket.recv(102400).decode()
    
        if result == "Requested File Not Found":
            res="Error: Requested File Not Found"
        elif result == "Incorrect File Format":
            res="Error: Incorrect File Format"
        else:
            content=decrypt_homophonic(result,enckey)
            with open(filename, 'w') as file:
                file.write(content)
            file.close()
            res="File "+filename+" received successfully."
        
        client_socket.close()
        
        output_box.insert(tk.END, res)
    except Exception as e:
        output_box.insert(tk.END, str(e))



root = tk.Tk()
root.title("Crypto")
root.geometry("700x450")

frame = ctk.CTkFrame(root, width=800, height=600)
frame.pack(padx=40, pady=40)

input_label = ctk.CTkLabel(frame, text="Enter file name:")
input_label.pack(pady=10)

input_box = ctk.CTkEntry(frame, width=100)
input_box.pack(pady=15)

button = ctk.CTkButton(frame, text="Get File", command=request_file)
button.pack(pady=15)

output_label = ctk.CTkLabel(frame, text="Output:")
output_label.pack(pady=15)

output_box = tk.Text(frame, height=10, width=40)
output_box.pack(pady=15)

root.mainloop()

