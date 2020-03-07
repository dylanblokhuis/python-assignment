import socket
import inquirer
import pickle

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

answers = inquirer.prompt([
    inquirer.List(
        'chatroom',
        message="What chatroom would you like to join?",
        choices=list(map(lambda chatroom: chatroom.name, get_chatrooms()))
    )
])

print(answers)

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# server.connect(('127.0.0.1', 1234))
# payload = ""
#
# while True:
#     msg = server.recv(1024)
#     print(msg.decode("utf-8"))
#
#     while True:
#         payload = input("> ")
#
#         if payload == 'quit':
#             server.close()
#             break
#         server.send(payload.encode("utf-8"))
