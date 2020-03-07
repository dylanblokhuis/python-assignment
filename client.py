import socket

user_name = input("Whats your username? \n> ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
server.connect(('127.0.0.1', 1235))
payload = ""

while True:
    msg = server.recv(1024)
    print(msg.decode("utf-8"))

    while True:
        payload = input("> ")

        if payload == 'quit':
            server.close()
            break
        server.send(payload.encode("utf-8"))
