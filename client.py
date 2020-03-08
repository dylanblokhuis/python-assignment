import socket
import pickle
import utils

user_name = input("Whats your username? \n> ")


def get_chatrooms():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.connect(('127.0.0.1', 1234))
    while True:
        msg = server.recv(4096)
        try:
            return pickle.loads(msg)
        except EOFError:
            pass


chatrooms = get_chatrooms()
answer = utils.prompt("Which chatroom would you like to join?", list(map(lambda question: question.name, chatrooms)))

selected_chatroom = object
for chatroom in chatrooms:
    if chatroom.name == answer:
        selected_chatroom = chatroom


print(f'Joining: {selected_chatroom.name}')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
server.connect(('127.0.0.1', selected_chatroom.port))
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
