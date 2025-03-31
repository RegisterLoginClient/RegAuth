import socket
import jsonpickle

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


while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose action: ")

    if choice == '1':
        username = input("Username: ")
        password = input("Password: ")
        response = send_request("register", username, password)
        print(response["message"])

    elif choice == '2':
        username = input("Username: ")
        password = input("Password: ")
        response = send_request("login", username, password)
        print(response["message"])

    elif choice == '3':
        print("Goodbye")
        break

    else:
        print("Error")