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

def register():
    username = username_entry.get()
    password = password_entry.get()
    repeat_password = repeat_password_entry.get()

    if password != repeat_password:
        messagebox.showerror("Error", "Different passwords")
        return

    if username and password:
        response = send_request("register", username, password)
        messagebox.showinfo("Response", response["message"])
    else:
        messagebox.showerror("Error", "Enter username and password")




root = Tk()
root.title("ClientGUI")

Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
username_entry = Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
password_entry = Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Repeat password:").grid(row=2, column=0, padx=10, pady=10)
repeat_password_entry = Entry(root, show="*")
repeat_password_entry.grid(row=2, column=1, padx=10, pady=10)

register_btn = Button(root, text="Register", command=register)
register_btn.grid(row=3, column=0, padx=10, pady=10)

login_btn = Button(root, text="Login", command=login)
login_btn.grid(row=3, column=1, padx=10, pady=10)


root.mainloop()