from tkinter import *
from tkinter import messagebox
import jsonpickle
import socket

IP = '127.0.0.1'
PORT = 4000

def send_request(action, username, password):
    request = {
        "action": action,
        "username": username,
        "password": password
    }

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    client.send(jsonpickle.encode(request).encode('utf-8'))

    response_data = client.recv(4096).decode('utf-8')
    response = jsonpickle.decode(response_data)
    client.close()

    return response