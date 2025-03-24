import socket
import sys
import tomllib
import base64
import json

from internet import HRequest, HResponse

user_input = sys.argv

if len(user_input) != 4:
    print("Не хватает аргументов!")
    raise Exception("ArgumentException")

sender, recipient, message = user_input[1:]

if not sender.isdigit() or not recipient.isdigit():
    print("Номер должен быть только из цифр!")
    raise Exception("ArgumentException")


with open("config.toml", 'rb') as file:
    s = socket.socket(2, 1)
    data = tomllib.load(file)
    host = data["host"]
    auth = data["auth"]

    auth64 = f"{auth['username']}:{auth['password']}"
    auth64 = base64.b64encode(auth64.encode()).decode()

    address = host["address"]
    port = host["port"]

    data = {
        "sender": sender,
        "recipient": recipient,
        "message": message
    }

    json_data = json.dumps(data)

    request = HRequest("POST", "/send_sms", "HTTP/1.1")
    request.add_header("Host", f"{address}:{port}")\
        .add_header("Content-Type", "application/json")\
        .add_header("Authorization", f"Basic {auth64}")\
        .add_header("accept", "application/json")\
        .add_header("Content-Length", str(len(json_data)))

    request.body = json_data

    s.connect((address, port))
    s.sendall(request.to_bytes())

    response = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk


    response = HResponse.from_bytes(response)

    print(response.status_code)
    print(response.body)

    s.close()






